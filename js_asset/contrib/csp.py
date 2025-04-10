from django.forms import Media
from django.utils.functional import LazyObject

from ..js import CSS, JS, JSON, ImportMap


def apply_nonce_to_js(js_list, nonce):
    """Apply nonce to a list of JS assets."""
    result = []
    for js in js_list:
        if isinstance(js, JS) and nonce and "nonce" not in js.attrs:
            # Create copy with updated attrs
            js_copy = JS(js.src, js.attrs.copy())
            js_copy.attrs["nonce"] = nonce
            result.append(js_copy)
        elif isinstance(js, JSON) and nonce and "nonce" not in js.attrs:
            # Create copy with updated attrs
            js_copy = JSON(js.data.copy(), id=js.id, attrs=js.attrs.copy())
            js_copy.attrs["nonce"] = nonce
            result.append(js_copy)
        elif isinstance(js, ImportMap) and nonce and not js._attrs.get("nonce"):
            # Create copy with updated attrs
            js_copy = ImportMap(
                js._importmap.copy(), attrs=js._attrs.copy() if js._attrs else {}
            )
            js_copy._attrs["nonce"] = nonce
            result.append(js_copy)
        elif isinstance(js, str) and nonce:
            # Wrap string paths in JS objects with nonce
            result.append(JS(js, {"nonce": nonce}))
        else:
            result.append(js)
    return result


def apply_nonce_to_css(css_dict, nonce):
    """Apply nonce to a dict of CSS assets."""
    result = {}
    for medium, sublist in css_dict.items():
        new_sublist = []
        for css in sublist:
            if isinstance(css, CSS) and nonce and "nonce" not in css.attrs:
                # Create copy with updated attrs
                css_copy = CSS(
                    css.src, inline=css.inline, media=css.media, attrs=css.attrs.copy()
                )
                css_copy.attrs["nonce"] = nonce
                new_sublist.append(css_copy)
            elif isinstance(css, str) and nonce:
                # Wrap string paths in CSS objects with nonce
                new_sublist.append(CSS(css, attrs={"nonce": nonce}))
            else:
                new_sublist.append(css)
        result[medium] = new_sublist
    return result


def apply_csp_nonce(media, nonce):
    """Apply CSP nonce to all media elements in a Media object."""
    if not media or not nonce:
        return media

    # Create new media with nonce applied to all elements
    js_with_nonce = apply_nonce_to_js(media._js, nonce) if hasattr(media, "_js") else []
    css_with_nonce = (
        apply_nonce_to_css(media._css, nonce) if hasattr(media, "_css") else {}
    )

    # Create new Media object with the modified js and css
    return Media(js=js_with_nonce, css=css_with_nonce)


class CSPNonce(LazyObject):
    """
    A lazy object to hold the CSP nonce from the request.
    Used by the context processor and CSPMediaMixin.
    """

    def _setup(self):
        self._wrapped = None

    def __bool__(self):
        return self._wrapped is not None


csp_nonce = CSPNonce()


def get_csp_media(media=None, css=None, js=None):
    """
    Helper function to create a Media object with CSP nonces applied.

    Usage:
        # In your form/widget:
        def media(self):
            return get_csp_media(css={'all': ['style.css']}, js=['script.js'])

        # Or with an existing Media instance:
        def media(self):
            base_media = super().media
            return get_csp_media(media=base_media)
    """
    # Create the base media object
    if media is not None:
        base_media = media
    else:
        base_media = Media(css=css, js=js)

    # Apply CSP nonce if available
    if csp_nonce:
        return apply_csp_nonce(base_media, csp_nonce._wrapped)

    return base_media


class CSPMediaMixin:
    """
    A mixin to automatically apply CSP nonces to media.

    Usage:
        class MyWidget(CSPMediaMixin, Widget):
            class Media:
                js = ['script.js']
                css = {'all': ['style.css']}
    """

    @property
    def media(self):
        # Get the base media from the parent class
        if hasattr(super(), "media"):
            base_media = super().media
        else:
            # Fall back to Media class definition if available
            base_media = Media()
            if hasattr(self, "Media"):
                if hasattr(self.Media, "js"):
                    base_media = Media(js=self.Media.js)
                if hasattr(self.Media, "css"):
                    if base_media._js:
                        base_media = base_media + Media(css=self.Media.css)
                    else:
                        base_media = Media(css=self.Media.css)

        # Apply CSP nonce if available
        if csp_nonce:
            return apply_csp_nonce(base_media, csp_nonce._wrapped)

        return base_media


def csp_context_processor(request):
    """
    Context processor to add the CSP nonce to the template context and set the global csp_nonce.

    Add to TEMPLATES settings:
        'OPTIONS': {
            'context_processors': [
                'js_asset.contrib.csp.csp_context_processor',
            ],
        },
    """
    # If the request has a CSP nonce attribute, set it in the global csp_nonce
    if hasattr(request, "csp_nonce"):
        csp_nonce._wrapped = request.csp_nonce
        return {"csp_nonce": request.csp_nonce}
    return {}


import base64
import secrets


class CSPNonceMiddleware:
    """
    Middleware that generates a CSP nonce for each request.

    Add to MIDDLEWARE settings:
        'js_asset.contrib.csp.CSPNonceMiddleware',

    Optionally, configure in settings:
        CSP_NONCE_LENGTH = 16  # Default
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Generate nonce
        from django.conf import settings

        nonce_length = getattr(settings, "CSP_NONCE_LENGTH", 16)
        nonce = base64.b64encode(secrets.token_bytes(nonce_length)).decode("ascii")

        # Add to request
        request.csp_nonce = nonce

        # Set global nonce for widgets and forms rendered outside views
        csp_nonce._wrapped = nonce

        # Get response
        response = self.get_response(request)

        # Add CSP header if not already present
        if hasattr(settings, "CSP_ENABLED") and settings.CSP_ENABLED:
            if not response.has_header("Content-Security-Policy"):
                # Build a basic CSP policy if CSP_DEFAULT_SRC is defined
                if hasattr(settings, "CSP_DEFAULT_SRC"):
                    default_src = " ".join(settings.CSP_DEFAULT_SRC)
                    script_src = f"'nonce-{nonce}'"
                    if hasattr(settings, "CSP_SCRIPT_SRC"):
                        script_src = f"{script_src} {' '.join(settings.CSP_SCRIPT_SRC)}"
                    style_src = f"'nonce-{nonce}'"
                    if hasattr(settings, "CSP_STYLE_SRC"):
                        style_src = f"{style_src} {' '.join(settings.CSP_STYLE_SRC)}"

                    csp = f"default-src {default_src}; script-src {script_src}; style-src {style_src}"

                    # Add additional directives
                    for directive in [
                        "IMG_SRC",
                        "FONT_SRC",
                        "CONNECT_SRC",
                        "FRAME_SRC",
                        "OBJECT_SRC",
                        "MEDIA_SRC",
                        "CHILD_SRC",
                        "FORM_ACTION",
                        "FRAME_ANCESTORS",
                        "WORKER_SRC",
                        "MANIFEST_SRC",
                    ]:
                        if hasattr(settings, f"CSP_{directive}"):
                            value = " ".join(getattr(settings, f"CSP_{directive}"))
                            csp += f"; {directive.lower().replace('_', '-')} {value}"

                    response["Content-Security-Policy"] = csp

        return response

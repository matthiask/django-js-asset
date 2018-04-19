from __future__ import unicode_literals

from django.apps import apps
from django.forms.utils import flatatt
from django.utils.html import format_html, mark_safe


__all__ = ('JS', 'static')


def static(path):
    # Django >= 1.10 does this automatically. We can revert to simply using
    # static(path) then.
    if apps.is_installed('django.contrib.staticfiles'):
        from django.contrib.staticfiles.storage import staticfiles_storage

        return staticfiles_storage.url(path)
    else:
        from django.templatetags.static import static

        return static(path)


class JS(object):
    """
    Use this to insert a script tag via ``forms.Media`` containing additional
    attributes (such as ``id`` and ``data-*`` for CSP-compatible data
    injection.)::

        forms.Media(js=[
            JS('asset.js', {
                'id': 'asset-script',
                'data-answer': '"42"',
            }),
        ])

    The rendered media tag (via ``{{ media.js }}`` or ``{{ media }}`` will
    now contain a script tag as follows, without line breaks::

        <script type="text/javascript" src="/static/asset.js"
            data-answer="&quot;42&quot;" id="asset-script"></script>

    The attributes are automatically escaped. The data attributes may now be
    accessed inside ``asset.js``::

        var answer = document.querySelector('#asset-script').dataset.answer;
    """
    def __init__(self, js, attrs=None, static=True):
        self.js = js
        self.attrs = attrs or {}
        self.static = static

    def startswith(self, _):
        # Masquerade as absolute path so that we are returned as-is.
        return True

    def __html__(self):
        js = static(self.js) if self.static else self.js
        return format_html(
            '{}"{}',
            js,
            mark_safe(flatatt(self.attrs)),
        )[:-1] if self.attrs else js

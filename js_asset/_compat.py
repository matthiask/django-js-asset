import django
from django.forms.utils import flatatt
from django.templatetags.static import static
from django.utils.html import format_html, html_safe


if django.VERSION >= (5, 2):
    from django.forms.widgets import MediaAsset, Script

else:

    @html_safe
    class MediaAsset:
        element_template = "{path}"

        def __init__(self, path, **attributes):
            self._path = path
            self.attributes = attributes

        def __eq__(self, other):
            # Compare the path only, to ensure performant comparison in Media.merge.
            return (self.__class__ is other.__class__ and self.path == other.path) or (
                isinstance(other, str) and self._path == other
            )

        def __hash__(self):
            # Hash the path only, to ensure performant comparison in Media.merge.
            return hash(self._path)

        def __str__(self):
            return format_html(
                self.element_template,
                path=self.path,
                attributes=flatatt(self.attributes),
            )

        def __repr__(self):
            return f"{type(self).__qualname__}({self._path!r})"

        @property
        def path(self):
            """
            Ensure an absolute path.
            Relative paths are resolved via the {% static %} template tag.
            """
            if self._path.startswith(("http://", "https://", "/")):
                return self._path
            return static(self._path)

    class Script(MediaAsset):
        element_template = '<script src="{path}"{attributes}></script>'

        def __init__(self, src, **attributes):
            # Alter the signature to allow src to be passed as a keyword argument.
            super().__init__(src, **attributes)

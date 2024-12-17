from dataclasses import dataclass, field
from typing import Any

from django.forms.utils import flatatt
from django.templatetags.static import static
from django.utils.html import format_html, html_safe, json_script, mark_safe


__all__ = ["CSS", "JS", "JSON", "static"]


def static_if_relative(path):
    return path if path.startswith(("http://", "https://", "/")) else static(path)


@html_safe
@dataclass(eq=True)
class CSS:
    src: str
    inline: bool = field(default=False, kw_only=True)

    def __hash__(self):
        return hash(self.__str__())

    def __str__(self):
        if self.inline:
            return format_html("<style>{}</style>", self.src)
        return format_html(
            '<link rel="stylesheet" href="{}">', static_if_relative(self.src)
        )


@html_safe
@dataclass(eq=True)
class JS:
    src: str
    attrs: dict[str, Any] = field(default_factory=dict)

    def __hash__(self):
        return hash(self.__str__())

    def __str__(self):
        return format_html(
            '<script src="{}"{}></script>',
            static_if_relative(self.src),
            mark_safe(flatatt(self.attrs)),
        )


@html_safe
@dataclass(eq=True)
class JSON:
    data: dict[str, Any]
    id: str | None = field(default="", kw_only=True)

    def __hash__(self):
        return hash(self.__str__())

    def __str__(self):
        return json_script(self.data, self.id)

import json
from dataclasses import dataclass
from typing import Any

from django import forms
from django.utils.html import html_safe, json_script, mark_safe


def _forms_media_add(self, other):
    # forms.Media etc. do not implement __radd__
    if type(other) is not forms.Media and hasattr(other, "__radd__"):
        return other.__radd__(self)
    return orig_forms_media_add(self, other)


# See https://code.djangoproject.com/ticket/36104
orig_forms_media_add = forms.Media.__add__
forms.Media.__add__ = _forms_media_add


@html_safe
@dataclass(eq=True)
class ImportMap:
    map: dict[str, Any]

    def __hash__(self):
        return hash(json.dumps(self.map, sort_keys=True))

    def __str__(self):
        return ""


class ExtendedMedia(forms.Media):
    def render_js(self):
        importmap = self.render_importmap(
            asset for asset in self._js if isinstance(asset, ImportMap)
        )
        return [importmap, *filter(None, super().render_js())]

    def render_importmap(self, maps):
        if not maps:
            return ""
        result = {}
        for map in maps:
            if imports := map.map.get("imports"):
                result.setdefault("imports", {}).update(imports)
            if integrity := map.map.get("integrity"):
                result.setdefault("integrity", {}).update(integrity)
            if scopes := map.map.get("scopes"):
                for scope, imports in scopes.items():
                    result.setdefault("scopes", {}).setdefault(scope, {}).update(
                        imports
                    )
        html = json_script(result).removeprefix('<script type="application/json">')
        return mark_safe(f'<script type="importmap">{html}')

    def _add_media(self, other, *, reverse):
        if reverse:
            a = other
            b = self
        else:
            a = self
            b = other

        combined = self.__class__()  # That's the difference
        combined._css_lists = a._css_lists[:]
        combined._js_lists = a._js_lists[:]
        for item in b._css_lists:
            if item and item not in a._css_lists:
                combined._css_lists.append(item)
        for item in b._js_lists:
            if item and item not in a._js_lists:
                combined._js_lists.append(item)
        return combined

    def __add__(self, other):
        return self._add_media(other, reverse=False)

    def __radd__(self, other):
        return self._add_media(other, reverse=True)

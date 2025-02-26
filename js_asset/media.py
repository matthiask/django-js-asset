import json
from dataclasses import dataclass
from itertools import chain
from typing import Any

from django import forms
from django.utils.html import html_safe, json_script, mark_safe

from js_asset import CSS, JS


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
    def __init__(self, assets=None, *, css=None, js=None):
        self._asset_lists = []
        if assets:
            self._asset_lists.append(assets)

        if css:
            self._asset_lists.append(self._convert_css(css))
        if js:
            self._asset_lists.append(self._convert_js(js))

    def _convert_css(self, medium_css_list):
        assets = []
        for medium, css_list in sorted(medium_css_list.items()):
            assets.extend(
                CSS(css, media=medium) if isinstance(css, str) else css
                for css in css_list
            )
        return assets

    def _convert_js(self, js_list):
        return [JS(js) if isinstance(js, str) else js for js in js_list]

    def render(self):
        assets = self.merge(*self._asset_lists)

        importmap = self.render_importmap(
            asset for asset in assets if isinstance(asset, ImportMap)
        )

        return mark_safe(
            "\n".join(
                filter(None, chain([importmap], (asset.__html__() for asset in assets)))
            )
        )

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
        combined = self.__class__()

        if type(other) is forms.Media:
            combined._asset_lists = []
            if not reverse:
                combined._asset_lists.extend(self._asset_lists)
            for medium_css_list in other._css_lists:
                combined._asset_lists.append(self._convert_css(medium_css_list))
            for js_list in other._js_lists:
                combined._asset_lists.append(self._convert_js(js_list))
            if reverse:
                combined._asset_lists.extend(self._asset_lists)
            return combined

        if type(other) is ExtendedMedia:
            combined = self.__class__()

            if reverse:
                combined._asset_lists = [*other._asset_lists, *self._asset_lists]
            else:
                combined._asset_lists = [*self._asset_lists, *other._asset_lists]

            return combined

        return NotImplemented

    def __add__(self, other):
        return self._add_media(other, reverse=False)

    def __radd__(self, other):
        return self._add_media(other, reverse=True)

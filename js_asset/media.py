from django import forms
from django.utils.html import format_html, html_safe, json_script, mark_safe


@html_safe
class ImportMap:
    def __init__(self, importmap):
        self._importmap = importmap

    def __str__(self):
        html = json_script(self._importmap).removeprefix(
            '<script type="application/json">'
        )
        return mark_safe(f'<script type="importmap">{html}')

    def __eq__(self, other):
        return isinstance(other, ImportMap) and self._importmap == other._importmap

    def __hash__(self):
        return hash(self.__str__())

    def __add__(self, other):
        if not isinstance(other, ImportMap):
            return NotImplemented
        combined = {}
        for map in [self, other]:
            if imports := map._importmap.get("imports"):
                combined.setdefault("imports", {}).update(imports)
            if integrity := map._importmap.get("integrity"):
                combined.setdefault("integrity", {}).update(integrity)
            if scopes := map._importmap.get("scopes"):
                for scope, imports in scopes.items():
                    combined.setdefault("scopes", {}).setdefault(scope, {}).update(
                        imports
                    )
        return self.__class__(combined)


def _render_js(self):
    importmap = None
    js = []
    for asset in self._js:
        if isinstance(asset, ImportMap):
            if importmap is None:
                importmap = asset
            else:
                importmap += asset
        else:
            js.append(
                asset.__html__()
                if hasattr(asset, "__html__")
                else format_html(
                    '<script src="{}"></script>', self.absolute_path(asset)
                )
            )

    if importmap is not None:
        js.insert(0, importmap.__html__())
    return js


forms.Media.render_js = _render_js

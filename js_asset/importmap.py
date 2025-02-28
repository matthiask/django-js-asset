from django.utils.html import html_safe, json_script, mark_safe


__all__ = ["importmap"]


@html_safe
class ImportMap:
    def __init__(self, importmap):
        self._importmap = importmap

    def __str__(self):
        if self._importmap:
            html = json_script(self._importmap).removeprefix(
                '<script type="application/json">'
            )
            return mark_safe(f'<script type="importmap">{html}')
        return ""

    def update(self, other):
        if isinstance(other, ImportMap):
            other = other._importmap

        if imports := other.get("imports"):
            self._importmap.setdefault("imports", {}).update(imports)
        if integrity := other.get("integrity"):
            self._importmap.setdefault("integrity", {}).update(integrity)
        if scopes := other.get("scopes"):
            for scope, imports in scopes.items():
                self._importmap.setdefault("scopes", {}).setdefault(scope, {}).update(
                    imports
                )

    def __or__(self, other):
        if isinstance(other, ImportMap):
            combined = self.__class__({})
            combined.update(self)
            combined.update(other)
            return combined
        return NotImplemented


importmap = ImportMap({})


def context_processor(request):
    return {"importmap": importmap}

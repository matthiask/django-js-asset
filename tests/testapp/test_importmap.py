from django.test import TestCase

from js_asset.js import ImportMap


class MediaTest(TestCase):
    def test_merging(self):
        a = ImportMap(
            {
                "imports": {"a": "/static/a.js"},
                "integrity": {"/static/a.js": "sha384-blub-a"},
                "_unknown_": "Automatically dropped when merging.",
            }
        )
        b = ImportMap(
            {
                "imports": {"b": "/static/b.js"},
                "integrity": {"/static/b.js": "sha384-blub-b"},
            }
        )

        self.assertEqual(
            str(a | b),
            """\
<script type="importmap">{"imports": {"a": "/static/a.js", "b": "/static/b.js"}, "integrity": {"/static/a.js": "sha384-blub-a", "/static/b.js": "sha384-blub-b"}}</script>""",
        )

        c = ImportMap(
            {
                "imports": {
                    "/app/": "./original-app/",
                    "/app/helper": "./helper/index.mjs",
                },
                "scopes": {"/js": {"/app/": "./js-app/"}},
            }
        )

        self.assertEqual(
            str(a | b | c),
            """\
<script type="importmap">{"imports": {"a": "/static/a.js", "b": "/static/b.js", "/app/": "./original-app/", "/app/helper": "./helper/index.mjs"}, "integrity": {"/static/a.js": "sha384-blub-a", "/static/b.js": "sha384-blub-b"}, "scopes": {"/js": {"/app/": "./js-app/"}}}</script>""",
        )

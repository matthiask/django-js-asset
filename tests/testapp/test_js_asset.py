from django.forms import Media
from django.test import TestCase

from js_asset.js import CSS, JS, JSON


class AssetTest(TestCase):
    def test_asset(self):
        media = Media(
            css={"print": ["app/print.css"]},
            js=[
                "app/test.js",
                JS("app/asset.js", {"id": "asset-script", "data-the-answer": 42}),
                JS("app/asset-without.js", {}),
            ],
        )
        html = str(media)

        # print(html)

        self.assertInHTML(
            '<link href="/static/app/print.css" media="print" rel="stylesheet" />',
            html,
        )
        self.assertInHTML(
            '<script src="/static/app/test.js"></script>',
            html,
        )
        self.assertInHTML(
            '<script src="/static/app/asset.js" data-the-answer="42" id="asset-script"></script>',
            html,
        )
        self.assertInHTML(
            '<script src="/static/app/asset-without.js"></script>',
            html,
        )

    def test_absolute(self):
        media = Media(js=[JS("https://cdn.example.org/script.js")])
        html = str(media)

        self.assertInHTML(
            '<script src="https://cdn.example.org/script.js"></script>',
            html,
        )

    def test_asset_merging(self):
        media1 = Media(js=["thing.js", JS("other.js"), "some.js"])
        media2 = Media(js=["thing.js", JS("other.js"), "some.js"])
        media = media1 + media2
        self.assertEqual(len(media._js), 3)
        self.assertEqual(media._js[0], "thing.js")
        self.assertEqual(media._js[2], "some.js")

    def test_set(self):
        media = [
            JS("app/asset.js", {"id": "asset-script", "data-the-answer": 42}),
            JS("app/asset.js", {"id": "asset-script", "data-the-answer": 42}),
            JS("app/asset.js", {"id": "asset-script", "data-the-answer": 43}),
        ]

        self.assertEqual(len(set(media)), 2)

    def test_boolean_attributes(self):
        self.assertEqual(
            str(JS("app/asset.js", {"bool": True, "cool": False})),
            '<script src="/static/app/asset.js" bool></script>',
        )

    def test_css(self):
        self.assertEqual(
            str(CSS("app/style.css")),
            '<link href="/static/app/style.css" media="all" rel="stylesheet">',
        )

        self.assertEqual(
            str(CSS("app/style.css", media="screen")),
            '<link href="/static/app/style.css" media="screen" rel="stylesheet">',
        )

        self.assertEqual(
            str(CSS("p{color:red}", inline=True)),
            '<style media="all">p{color:red}</style>',
        )

    def test_json(self):
        self.assertEqual(
            str(JSON({"hello": "world"}, id="hello")),
            '<script id="hello" type="application/json">{"hello": "world"}</script>',
        )

        self.assertEqual(
            str(JSON({"hello": "world"})),
            '<script type="application/json">{"hello": "world"}</script>',
        )

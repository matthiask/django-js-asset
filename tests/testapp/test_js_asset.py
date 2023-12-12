from unittest import skipIf

import django
from django.forms import Media
from django.test import TestCase

from js_asset.js import JS


CSS_TYPE = ' type="text/css"' if django.VERSION < (4, 1) else ""
JS_TYPE = ' type="text/javascript"' if django.VERSION < (3, 1) else ""


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
        html = "%s" % media

        # print(html)

        self.assertInHTML(
            f'<link href="/static/app/print.css"{CSS_TYPE} media="print" rel="stylesheet" />',
            html,
        )
        self.assertInHTML(
            f'<script{JS_TYPE} src="/static/app/test.js"></script>',
            html,
        )
        self.assertInHTML(
            f'<script{JS_TYPE} src="/static/app/asset.js" data-the-answer="42" id="asset-script"></script>',
            html,
        )
        self.assertInHTML(
            f'<script{JS_TYPE} src="/static/app/asset-without.js"></script>',
            html,
        )

    def test_absolute(self):
        media = Media(js=[JS("https://cdn.example.org/script.js", static=False)])
        html = "%s" % media

        self.assertInHTML(
            f'<script{JS_TYPE} src="https://cdn.example.org/script.js"></script>',
            html,
        )

    def test_asset_merging(self):
        media1 = Media(js=["thing.js", JS("other.js"), "some.js"])
        media2 = Media(js=["thing.js", JS("other.js"), "some.js"])
        media = media1 + media2
        self.assertEqual(len(media._js), 3)
        self.assertEqual(media._js[0], "thing.js")
        self.assertEqual(media._js[2], "some.js")

    def test_repr(self):
        self.assertEqual(
            repr(
                JS("app/asset.js", {"id": "asset-script", "data-the-answer": 42})
            ).lstrip("u"),
            'JS(app/asset.js, {"data-the-answer": 42, "id": "asset-script"})',
        )

    def test_set(self):
        media = [
            JS("app/asset.js", {"id": "asset-script", "data-the-answer": 42}),
            JS("app/asset.js", {"id": "asset-script", "data-the-answer": 42}),
            JS("app/asset.js", {"id": "asset-script", "data-the-answer": 43}),
        ]

        self.assertEqual(len(set(media)), 2)

    @skipIf(
        django.VERSION < (4, 1),
        "django-js-asset doesn't support boolean attributes yet",
    )
    def test_boolean_attributes(self):
        self.assertEqual(
            str(JS("app/asset.js", {"bool": True, "cool": False})),
            '<script src="/static/app/asset.js" bool></script>',
        )

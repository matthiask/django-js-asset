from __future__ import unicode_literals

from django.forms import Media
from django.test import TestCase

from js_asset.js import JS


class AssetTest(TestCase):
    def test_asset(self):
        media = Media(
            css={
                'print': ['app/print.css'],
            },
            js=[
                'app/test.js',
                JS('app/asset.js', {
                    'id': 'asset-script',
                    'data-the-answer': 42,
                }),
                JS('app/asset-without.js', {}),
            ],
        )
        html = '%s' % media

        # print(html)

        self.assertInHTML(
            '<link href="/static/app/print.css" type="text/css" media="print" rel="stylesheet" />',  # noqa
            html,
        )
        self.assertInHTML(
            '<script type="text/javascript" src="/static/app/test.js"></script>',  # noqa
            html,
        )
        self.assertInHTML(
            '<script type="text/javascript" src="/static/app/asset.js" data-the-answer="42" id="asset-script"></script>',  # noqa
            html,
        )
        self.assertInHTML(
            '<script type="text/javascript" src="/static/app/asset-without.js"></script>',  # noqa
            html,
        )

    def test_absolute(self):
        media = Media(
            js=[
                JS(
                    'https://cdn.example.org/script.js',
                    static=False,
                ),
            ],
        )
        html = '%s' % media

        self.assertInHTML(
            '<script type="text/javascript" src="https://cdn.example.org/script.js"></script>',  # noqa
            html,
        )

from __future__ import unicode_literals

from js_asset.js import JS

from django.forms import Media
from django.test import TestCase


class AssetTest(TestCase):
    def test_asset(self):
        media = Media()
        media.add_css({
            'print': ('app/print.css',),
        })
        media.add_js(('app/test.js',))
        media.add_js((
            JS('app/asset.js', {
                'id': 'asset-script',
                'data-the-answer': 42,
            }),
        ))
        html = '%s' % media

        print(html)

        self.assertInHTML(
            '<link href="/static/app/print.css" type="text/css" media="print" rel="stylesheet" />',
            html,
        )
        self.assertInHTML(
            '<script type="text/javascript" src="/static/app/test.js"></script>',
            html,
        )
        self.assertInHTML(
            '<script type="text/javascript" src="/static/app/asset.js" data-the-answer="42" id="asset-script"></script>',
            html,
        )
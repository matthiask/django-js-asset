from django.forms import Media
from django.test import TestCase

from js_asset.js import JS
from js_asset.media import ExtendedMedia, ImportMapImport


class MediaTest(TestCase):
    def test_importmap(self):
        media_ab = Media(js=["a.js", "b.js"])
        media_bc = Media(js=["b.js", "c.js"])
        media_ac = Media(js=["a.js", "c.js"])

        extended_a = ExtendedMedia(
            [JS("a.js"), ImportMapImport("library-a", "/static/library-a.abcdef.js")]
        )
        extended_b = ExtendedMedia(
            [ImportMapImport("htmx.org", "/static/htmx.org.012345.js"), JS("b.js")]
        )

        merged = media_ab + media_bc + media_ac + extended_a + extended_b

        self.assertEqual(
            str(merged),
            """\
<script type="importmap">{"imports": {"htmx.org": "/static/htmx.org.012345.js", "library-a": "/static/library-a.abcdef.js"}}</script>
<script src="/static/a.js"></script>
<script src="/static/b.js"></script>
<script src="/static/c.js"></script>""",
        )

        self.assertEqual(
            str(merged),
            str(extended_a + media_ab + media_ac + extended_b + media_bc),
        )

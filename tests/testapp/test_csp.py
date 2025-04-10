from django.forms.widgets import Media
from django.test import RequestFactory, TestCase

from js_asset.contrib.csp import (
    CSPMediaMixin,
    CSPNonceMiddleware,
    apply_csp_nonce,
    csp_context_processor,
    csp_nonce,
    get_csp_media,
)
from js_asset.js import JS


class DummyView:
    def __call__(self, request):
        return None


class DummyWidget:
    class Media:
        js = ["script.js", JS("module.js", {"type": "module"})]
        css = {"all": ["style.css"]}


class CSPWidget(CSPMediaMixin, DummyWidget):
    pass


class CSPTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = CSPNonceMiddleware(DummyView())

    def test_csp_media(self):
        """Test applying CSP nonce to media"""
        # Create regular media
        base_media = Media(
            js=["script.js", JS("module.js", {"type": "module"})],
            css={"all": ["style.css"]},
        )

        # Apply CSP nonce
        media = apply_csp_nonce(base_media, "test-nonce")

        # Test rendering with nonce
        html = str(media)
        self.assertIn('nonce="test-nonce"', html)
        self.assertIn(
            '<script src="/static/script.js" nonce="test-nonce"></script>', html
        )
        # Note: attribute order may vary but as long as both attributes are present
        self.assertIn('src="/static/module.js"', html)
        self.assertIn('type="module"', html)
        self.assertIn('nonce="test-nonce"', html)
        self.assertIn(
            '<link href="/static/style.css" media="all" rel="stylesheet" nonce="test-nonce">',
            html,
        )

        # Test get_csp_media helper
        media2 = get_csp_media(
            js=["script.js", JS("module.js", {"type": "module"})],
            css={"all": ["style.css"]},
        )
        # Set nonce manually since there's no global nonce in the test
        media2 = apply_csp_nonce(media2, "test-nonce")
        html2 = str(media2)
        self.assertIn('nonce="test-nonce"', html2)

    def test_middleware(self):
        """Test CSPNonceMiddleware adds nonce to request"""
        request = self.factory.get("/")
        self.middleware(request)

        # Check if nonce is added to request
        self.assertTrue(hasattr(request, "csp_nonce"))
        self.assertIsInstance(request.csp_nonce, str)
        self.assertGreater(len(request.csp_nonce), 10)  # Reasonable nonce length

        # Check if global nonce is set
        self.assertTrue(bool(csp_nonce))
        self.assertEqual(csp_nonce._wrapped, request.csp_nonce)

    def test_context_processor(self):
        """Test context processor adds nonce to context"""
        request = self.factory.get("/")
        request.csp_nonce = "test-nonce"

        context = csp_context_processor(request)
        self.assertEqual(context["csp_nonce"], "test-nonce")
        self.assertEqual(csp_nonce._wrapped, "test-nonce")

    def test_csp_media_mixin(self):
        """Test CSPMediaMixin automatically applies nonce"""
        request = self.factory.get("/")
        request.csp_nonce = "test-nonce"

        # Update global nonce
        csp_nonce._wrapped = request.csp_nonce

        # Create widget with mixin
        widget = CSPWidget()
        media = widget.media

        # Test rendering
        html = str(media)
        self.assertIn('nonce="test-nonce"', html)
        self.assertIn(
            '<script src="/static/script.js" nonce="test-nonce"></script>', html
        )
        # Note: attribute order may vary but as long as both attributes are present
        self.assertIn('src="/static/module.js"', html)
        self.assertIn('type="module"', html)
        self.assertIn('nonce="test-nonce"', html)
        self.assertIn(
            '<link href="/static/style.css" media="all" rel="stylesheet" nonce="test-nonce">',
            html,
        )

__version__ = "3.1.2"

import contextlib


with contextlib.suppress(ImportError):
    from js_asset.js import *  # noqa: F403

# Optional CSP support
try:
    from js_asset.contrib.csp import (  # noqa: F401
        CSPMediaMixin,
        CSPNonceMiddleware,
        apply_csp_nonce,
        csp_context_processor,
        csp_nonce,
        get_csp_media,
    )
except ImportError:
    pass

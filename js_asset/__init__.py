__version__ = "2.0.0"

import contextlib


with contextlib.suppress(ImportError):
    from js_asset.js import *  # noqa: F403

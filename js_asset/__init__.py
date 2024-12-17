__version__ = "3.0.0"

import contextlib


with contextlib.suppress(ImportError):
    from js_asset.js import *  # noqa: F403

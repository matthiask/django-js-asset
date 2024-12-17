__version__ = "3.0.1"

import contextlib


with contextlib.suppress(ImportError):
    from js_asset.js import *  # noqa: F403

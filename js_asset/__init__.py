__version__ = "3.1.0"

import contextlib


with contextlib.suppress(ImportError):
    from js_asset.importmap import *  # noqa: F403
    from js_asset.js import *  # noqa: F403

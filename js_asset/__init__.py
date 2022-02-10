VERSION = (2, 0, 0)
__version__ = ".".join(map(str, VERSION))


try:
    from js_asset.js import *  # noqa
except ImportError:  # pragma: no cover
    pass

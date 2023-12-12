
.. _changelog:

Change log
==========

Next version
~~~~~~~~~~~~


2.2 (2023-12-12)
~~~~~~~~~~~~~~~~

- Started running the tests periodically to detect breakages early.
- Added Django 5.0, Python 3.12.
- Fixed building with hatchling 1.19. Thanks Michał Górny!


2.1 (2023-06-28)
~~~~~~~~~~~~~~~~

- Added Django 4.1, 4.2 and Python 3.11 to the CI.
- Removed the pytz dependency from the tests.
- Dropped Python < 3.8, Django < 3.2 from the CI.
- Switched to hatchling and ruff.


`2.0`_ (2022-02-10)
~~~~~~~~~~~~~~~~~~~

.. _2.0: https://github.com/matthiask/django-js-asset/compare/1.2...2.0

- Raised the minimum supported versions of Python to 3.6, Django to 2.2.
- Added pre-commit.
- Replaced the explicit configuration of whether ``static()`` should be used or
  not with automatic configuration. The ``static`` argument is still accepted
  but ignored and will be removed at a later time.
- Added support for boolean attributes when using Django 4.1 or better.


Released as 1.2.1 and 1.2.2:
----------------------------

- Made ``JS()`` objects hashable so that they can be put into sets in
  preparation for a possible fix for media ordering in Django #30179.
- Confirmed support for Django 3.0 and 3.1a1.
- Django dropped ``type="text/javascript"`` in 3.1, changed our tests to
  pass again.
- Switched from Travis CI to GitHub actions.
- Dropped Django 1.7 from the CI jobs list because it somehow didn't
  discover our tests.
- Renamed the main branch to ``main``.
- Added CI testing for Django 3.2.


`1.2`_ (2019-02-08)
~~~~~~~~~~~~~~~~~~~

- Reformatted the code using Black.
- Added equality of ``JS()`` objects to avoid adding the same script
  more than once in the same configuration.
- Determine the ``static`` callable at module import time, not each time
  a static path is generated.
- Customized the ``repr()`` of ``JS()`` objects.
- Added Python 3.7 and Django 2.2 to the test matrix.


`1.1`_ (2018-04-19)
~~~~~~~~~~~~~~~~~~~

- Added support for skipping ``static()``, mostly useful when adding
  external scripts via ``JS()`` (e.g for adding ``defer="defer"``).
- Made the attributes dictionary optional.


`1.0`_ (2018-01-16)
~~~~~~~~~~~~~~~~~~~

- Added an export of the ``js_asset.static()`` helper (which does the
  right thing regarding ``django.contrib.staticfiles``)
- Fixed the documentation to not mention internal (and removed) API of
  Django's ``Media()`` class.
- Switched to using tox_ for running tests and style checks locally.
- Added more versions of Python and Django to the CI matrix.


`0.1`_ (2017-04-19)
~~~~~~~~~~~~~~~~~~~

- Initial public release extracted from django-content-editor_.


.. _Django: https://www.djangoproject.com/
.. _django-content-editor: https://django-content-editor.readthedocs.io/
.. _tox: https://tox.readthedocs.io/

.. _0.1: https://github.com/matthiask/django-js-asset/commit/e335c79a87
.. _1.0: https://github.com/matthiask/django-js-asset/compare/0.1...1.0
.. _1.1: https://github.com/matthiask/django-js-asset/compare/1.0...1.1
.. _1.2: https://github.com/matthiask/django-js-asset/compare/1.1...1.2

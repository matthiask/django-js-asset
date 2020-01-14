
.. _changelog:

Change log
==========

`Next version`_
~~~~~~~~~~~~~~~

- Made ``JS()`` objects hashable so that they can be put into sets in
  preparation for a possible fix for media ordering in Django #30179.
- Run tests with Django 3.0 too.


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
.. _Next version: https://github.com/matthiask/django-js-asset/compare/1.2...master

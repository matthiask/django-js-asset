
.. _changelog:

Change log
==========

`Next version`_
~~~~~~~~~~~~~~~


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
.. _1.0: https://github.com/matthiask/django-js-asset/compare/0.1...1.0.0
.. _Next version: https://github.com/matthiask/django-js-asset/compare/1.0.0...master

===============================================================================
django-js-asset -- script tag with additional attributes for django.forms.Media
===============================================================================

.. image:: https://github.com/matthiask/django-js-asset/workflows/Tests/badge.svg
    :target: https://github.com/matthiask/django-js-asset

Usage
=====

Use this to insert a script tag via ``forms.Media`` containing additional
attributes (such as ``id`` and ``data-*`` for CSP-compatible data
injection.):

.. code-block:: python

    from js_asset import JS

    forms.Media(js=[
        JS("asset.js", {
            "id": "asset-script",
            "data-answer": "42",
        }),
    ])

The rendered media tag (via ``{{ media.js }}`` or ``{{ media }}`` will
now contain a script tag as follows, without line breaks:

.. code-block:: html

    <script type="text/javascript" src="/static/asset.js"
        data-answer="42" id="asset-script"></script>

The attributes are automatically escaped. The data attributes may now be
accessed inside ``asset.js``:

.. code-block:: javascript

    var answer = document.querySelector("#asset-script").dataset.answer;

Also, because the implementation of ``static`` differs between supported
Django versions (older do not take the presence of
``django.contrib.staticfiles`` in ``INSTALLED_APPS`` into account), a
``js_asset.static`` function is provided which does the right thing
automatically.


Compatibility
=============

At the time of writing this app is compatible with Django 4.2 and better
(up to and including the Django main branch), but have a look at the
`tox configuration
<https://github.com/matthiask/django-js-asset/blob/main/tox.ini>`_ for
definitive answers.

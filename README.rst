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


CSS and JSON support
====================

Since 3.0 django-js-asset also ships a ``CSS`` and ``JSON`` media object which
can be used to ship stylesheets, inline styles and JSON blobs to the frontend.
It's recommended to pass those through ``forms.Media(js=[])`` as well since
``js`` is a simple list while ``css`` uses a dictionary keyed with the media to
use for the stylesheet.

So, you can add everything at once:

.. code-block:: python

    from js_asset import CSS, JS, JSON

    forms.Media(js=[
        JSON({"configuration": 42}, id="widget-configuration"),
        CSS("widget/style.css"),
        CSS("p{color:red;}", inline=True),
        JS("widget/script.js", {"type": "module"}),
    ])

This produces:

.. code-block:: html

    <script id="widget-configuration" type="application/json">{"configuration": 42}</script>
    <link rel="stylesheet" href="/static/widget/style.css">
    <style>p{color:red;}</style>
    <script src="/static/widget/script.js" type="module"></script>



Compatibility
=============

At the time of writing this app is compatible with Django 4.2 and better
(up to and including the Django main branch), but have a look at the
`tox configuration
<https://github.com/matthiask/django-js-asset/blob/main/tox.ini>`_ for
definitive answers.

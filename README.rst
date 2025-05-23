==================================================================
django-js-asset -- JS, CSS and JSON support for django.forms.Media
==================================================================

.. image:: https://github.com/matthiask/django-js-asset/workflows/Tests/badge.svg
    :target: https://github.com/matthiask/django-js-asset

**Note!** `Django 5.2 adds its own support for JavaScript objects
<https://docs.djangoproject.com/en/dev/topics/forms/media/#script-objects>`__.
This library has a slightly different API and also supports much older versions
of Django, *and* it also supports CSS and JSON tags.

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
    <link href="/static/widget/style.css" media="all" rel="stylesheet">
    <style media="all">p{color:red;}</style>
    <script src="/static/widget/script.js" type="module"></script>



Compatibility
=============

At the time of writing this app is compatible with Django 4.2 and better
(up to and including the Django main branch), but have a look at the
`tox configuration
<https://github.com/matthiask/django-js-asset/blob/main/tox.ini>`_ for
definitive answers.


Extremely experimental importmap support
========================================

django-js-asset ships an extremely experimental implementation adding support
for using `importmaps
<https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script/type/importmap>`_.

One of the reasons why importmaps are useful when used with Django is that this
easily allows us to use the file name mangling offered for example by Django
``ManifestStaticFilesStorage`` without having to rewrite import statements in
scripts themselves.

Browser support for multiple importmaps is not generally available; at the time
of writing (February 2025) it's not even clear if Mozilla wants to support them
ever, so merging importmaps is -- for now -- the only viable way to use them in
production. Because of this the implementation uses a global importmap variable
where new entries can be added to and a context processor to make the importmap
available to templates.

The ``importmap`` object can be imported from ``js_asset``. Usage is as follows:

.. code-block:: python

    # static is a lazy version of Django's static() function used in the
    # {% static %} template tag.
    from js_asset import JS, static_lazy, importmap

    # Run this during project initialization, e.g. in App.ready or whereever.
    importmap.update({
        "imports": {
            "my-library": static_lazy("my-library.js"),
        },
    })

The importmap should be initialized on server startup, not later.

You have to add ``js_asset.context_processors.importmap`` to the list of
context processors in your settings (or choose some other way of making the
``importmap`` object available in templates) and add ``{{ importmap }}``
somewhere in your base template, preferrably at the top before including any
scripts. This is especially important if you're using some way of replacing
parts of the website after the initial load with parts also containing scripts,
such as `htmx <https://htmx.org/>`__.

When you've done that you can start profiting from the importmap by adding
JavaScript modules. When using media objects in the Django admin you also have
to add the importmap to the list of JavaScript assets via
``forms.Media(js=[...])`` if you do not want to add the ``{{ importmap }}`` tag
to your admin base templates. You have to ensure that the importmap is included
before any other JavaScript modules.

If you're using the same widget for the admin interface as for the rest of your
site, adding the importmap to the ``js`` list will mean that your HTML contains
the importmap twice. This doesn't hurt a lot since the contents should be
identical. Ways to work around it include either only ever using ``{{ importmap
}}`` or ``{{ form.media }}`` on a given page (if possible) or using different
widget classes for the admin than for the rest of your site.

.. code-block:: python

    # Example for adding a code.js JavaScript *module*
    forms.Media(js=[
        importmap,  # See paragraph above!
        JS("code.js", {"type": "module"}),
    ])

The code in ``code.js`` can now use a JavaScript import to import assets from
the library, even though the library's filename may contain hashes not known at
programming time:

.. code-block:: javascript

    import { Stuff } from "my-library"

One-off modifications to importmaps, for example in views
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to add to the base importmap in a view, you can do it as follows:

.. code-block:: python

    # Again, static is the same as Django's static() helper
    from js_asset import importmap, static

    def view(request):
        # ...

        specific_importmap = {
            "imports": {
                "stuff": static("stuff.js"),
            },
        }

        return render(
            request,
            "...",
            {"importmap": importmap | specific_importmap},
        )

Of course this only works if the importmap is rendered in the template and not
passed through ``forms.Media``. This isn't perfect of course, so I'm still
looking into ways to improve the behavior.

When using ``importmap.update(...)`` you are updating the global importmap
object. When you are OR-ing importmap objects together you get a new importmap
object which is unrelated to the global importmap.

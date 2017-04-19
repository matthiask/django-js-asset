#!/bin/sh
venv/bin/coverage run --branch --include="*js_asset/*" --omit="*tests*" ./manage.py test testapp
venv/bin/coverage html

#!/usr/bin/env bash

cd /s104_juk/ || exit 1
python manage.py migrate
python manage.py collectstatic --noinput
daphne -b 0.0.0.0 -p 8087 --access-log /var/log/s104_juk/daphne_access.log juk.asgi:application

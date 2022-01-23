#!/usr/bin/env bash

FILE=/db/db.sqlite3

if [[ -f "$FILE" ]]; then
    echo "$FILE exists."
else
    echo "$FILE does not exist."
    python3 manage.py migrate
    python3 manage.py migrate AdNotifyManager
    DJANGO_SUPERUSER_PASSWORD=admin python3 manage.py createsuperuser \
    --no-input \
    --username=admin \
    --email=admin@domain.com
fi

python3 manage.py migrate
python3 manage.py migrate AdNotifyManager
# python3 manage.py runserver 0.0.0.0:8000

python manage.py collectstatic --no-input

# run qcluster
python manage.py qcluster &
exec "$@"
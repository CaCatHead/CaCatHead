#!/bin/bash

if [ `id -u` -ne 0 ]; then
  echo "Please re-run ${this_file} as root."
  exit 1
fi

export DB_PASS=$(cat $DB_PASS_FILE)

if [ "$1" = "server" ] ; then
  # wait mysql bootstrap
  sleep 10
  /usr/src/.venv/bin/python ./manage.py migrate
  /usr/src/.venv/bin/python ./manage.py collectstatic --no-input
  /usr/src/.venv/bin/uvicorn CaCatHead.asgi:application --workers 4 --host 0.0.0.0 --port 8000
elif [ "$1" = "judge" ] ; then
  /usr/src/.venv/bin/python ./judge.py
fi

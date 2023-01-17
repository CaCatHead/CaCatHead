#!/bin/bash

if [ `id -u` -ne 0 ]; then
  echo "Please re-run ${this_file} as root."
  exit 1
fi

export DB_PASS=$(cat $DB_PASS_FILE)

export REDIS_PASS=$(cat $REDIS_PASS_FILE)

export MINIO_PASS=$(cat $MINIO_PASS_FILE)

export RMQ_PASS=$(cat $RMQ_PASS_FILE)

if [ "$1" = "server" ] ; then
  # wait postgresql bootstrap
  ./wait
  /usr/src/.venv/bin/python ./manage.py migrate
  /usr/src/.venv/bin/python ./manage.py collectstatic --no-input
  
  # start cron jobs
  cron

  # start standing worker
  /usr/src/.venv/bin/celery -A CaCatHead.core multi start worker \
    -l INFO -Q "$CONTEST_WORKER_QUEUE" \
    --pidfile="/root/celery/run/%n.pid" \
    --logfile="/root/celery/log/%n%I.log"
  
  # start server
  /usr/src/.venv/bin/uvicorn CaCatHead.asgi:application --workers 4 --host 0.0.0.0 --port 8000
elif [ "$1" = "judge" ] ; then
  # ensure catj exists
  if [ ! -f "/usr/bin/catj" ]; then
    echo "catj does not exist"
    exit 1
  else
    catj -v
  fi
  # ensure checkers exist
  if [ ! -f "/root/checkers/lcmp" ]; then
    echo "lcmp does not exist"
    exit 1
  fi

  # wait rabbitmq bootstrap
  ./wait

  # start celery worker
  export C_FORCE_ROOT=true
  /usr/src/.venv/bin/celery -A CaCatHead.core worker -X "$CONTEST_WORKER_QUEUE" -l INFO
fi

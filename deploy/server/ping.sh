#!/bin/bash

if [ `id -u` -ne 0 ]; then
  echo "Please re-run ${this_file} as root."
  exit 1
fi

export DEBUG=false

export DB_PASS=$(cat /run/secrets/db_pass)

export REDIS_PASS=$(cat /run/secrets/redis_pass)

export MINIO_PASS=$(cat /run/secrets/minio_pass)

export RMQ_PASS=$(cat /run/secrets/rmq_pass)

/usr/src/.venv/bin/python /root/CaCatHead/manage.py runcrons


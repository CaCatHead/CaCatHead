#!/bin/bash

DB_PASS=$(cat $DB_PASS_FILE)

# See https://gobackup.github.io/   
BACKUP="models:
  cacathead:
    compress_with:
      type: tgz
    schedule:
      cron: '0 0 * * *'  # At 0:00 AM every day
    storages:
      local:
        type: local
        path: /root/backup
    databases:
      postgresql:
        type: postgresql
        host: postgresql
        port: 5432
        database: cacathead
        username: root
        password: $DB_PASS
        args: --if-exists --no-owner"

echo "$BACKUP" > ~/.gobackup/gobackup.yml

./wait
./gobackup perform
./gobackup run

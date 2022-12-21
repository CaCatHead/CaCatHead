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
      mysql:
        type: mysql
        host: mysql
        port: 3306
        database: cacathead
        username: root
        password: $DB_PASS
        additional_options: --single-transaction --quick"

echo "$BACKUP" > ~/.gobackup/gobackup.yml

./wait
./gobackup perform
./gobackup run

#!/bin/bash

case "$1" in
  "up")
    docker compose up --build -d
    ;;
  "logs")
    if [ -z "$2" ] ; then
      docker compose logs -f
    else
      docker logs "cacathead_$2" -f
    fi
    ;;
  "exec")
    docker exec -it "cacathead_$2" /bin/bash 
    ;;
  *)
    echo "Usage: ./manage.sh [up|logs|exec]"
    exit 1
    ;;
esac

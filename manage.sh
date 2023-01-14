#!/bin/bash

case "$1" in
  "up")
    docker compose up --build -d
    ;;
  "judge")
    docker compose -f docker-compose.judge.yml --profile catjudge up --build -d
    ;;
  "ps")
    docker compose ps
    ;;
  "stop")
    if [ -z "$2" ] ; then
      docker compose stop
    else
      docker compose stop "$2"
    fi
    ;;
  "restart")
    if [ -z "$2" ] ; then
      docker compose restart
    else
      docker compose restart "$2"
    fi
    ;;
  "logs")
    if [ -z "$2" ] ; then
      docker compose logs -f
    elif [ "$2" = "node" ] ; then 
      docker logs "catjudge_node" -f
    else
      docker logs "cacathead_$2" -f
    fi
    ;;
  "exec")
    docker exec -it "cacathead_$2" /bin/bash 
    ;;
  *)
    echo "Usage: ./manage.sh [up|judge|ps|stop|restart|logs|exec]"
    ;;
esac

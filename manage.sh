#!/bin/bash

case "$1" in
  "up")
    if [ -z "$2" ] ; then
      docker compose up --build -d
    else
      docker compose up "$2" --build -d
    fi
    ;;
  "judge")
    if [ -z "$2" ] ; then
      docker compose -f docker-compose.judge.yml --profile catjudge up --build -d
    elif [ "$2" = "stop" ] ; then
      docker stop "catjudge_node"
    elif [ "$2" = "restart" ] ; then
      docker restart "catjudge_node"
    elif [ "$2" = "logs" ] ; then
      docker logs "catjudge_node" -f
    elif [ "$2" = "exec" ] ; then
      docker exec -it "catjudge_node" /bin/bash 
    fi
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

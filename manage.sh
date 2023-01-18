#!/bin/bash

function prompt_password() {
  pass=$(gum input --password --header="CaCatHead $1 Password:" --placeholder="...")
  if [ $? -eq 0 ] ; then
    cat "$pass" "./deploy/password/$2_pass.txt"
  else
    exit $?
  fi
}

function prompt_config() {
  if ! [ -x "$(command -v gum)" ]; then
    echo 'Error: gum is not installed, see https://github.com/charmbracelet/gum' >&2
    exit 1
  fi

  prompt_password Postgresql db
  prompt_password Redis redis
  prompt_password MinIO minio
  prompt_password RabbitMQ rmq

  echo "default_user = root" > ./deploy/rabbitmq.conf
  echo "default_pass = $(cat ./deploy/password/rmq_pass.txt)" >> ./deploy/rabbitmq.conf
}

ALL_SERVICE=("nginx" "app" "server" "judge" "backup" "postgresql" "minio" "redis" "rabbitmq")

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
  "rm")
    if [ -z "$2" ] ; then
      docker compose rm
    else
      docker compose rm "$2"
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
    if [ -z "$2" ] ; then
      service=$(gum choose ${ALL_SERVICE[@]})
      docker exec -it "cacathead_$service" /bin/bash 
    else
      docker exec -it "cacathead_$2" /bin/bash 
    fi
    ;;
  "config")
    prompt_config
    ;;
  *)
    echo "Usage: ./manage.sh <command>"
    echo ""
    echo "CaCatHead deploy management script."
    echo ""
    echo "Commands":
    echo "  up [service]       Create and start CaCatHead containers"
    echo "  stop [service]     Stop CaCatHead containers"
    echo "  restart [service]  Restart CaCatHead service containers"
    echo "  rm [service]       Remove CaCatHead stopped service containers"
    echo "  logs [service]     View output from CaCatHead containers"
    echo "  exec [service]     Go to the CaCatHead containers"
    echo "  ps                 List CaCatHead containers"
    echo "  config             Config CaCatHead serivce passwords"
    echo "  judge              Create and start CaCatHead judge containers"
    echo "  judge stop         Stop CaCatHead judge containers"
    echo "  judge restart      Restart CaCatHead judge containers"
    echo "  judge logs         View output from CaCatHead judge containers"
    echo "  judge exec         Go to the CaCatHead judge containers"
    echo ""
    ;;
esac

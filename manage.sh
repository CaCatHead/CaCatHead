#!/bin/bash

function prompt_password() {
  pass=$(gum input --password --header="CaCatHead $1 Password:" --placeholder="...")
  if [ $? -eq 0 ] ; then
    echo "$pass" > "./deploy/password/$2_pass.txt"
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

export COMMIT_SHA="$(git rev-parse HEAD)"

case "$1" in
  "up")
    if [ -z "$2" ] ; then
      docker compose up --build -d
    else
      docker compose up "$2" --build -d
    fi
    ;;
  "sync")
    git pull
    if [ $? -ne 0 ] ; then
      exit $?
    fi
    docker compose up --build -d
    ;;
  "judge")
    case "$2" in
      "" | "up")
        docker compose -f docker-compose.judge.yml --profile catjudge up --build -d
        ;;
      "sync")
        git pull
        if [ $? -ne 0 ] ; then
          exit $?
        fi
        docker compose -f docker-compose.judge.yml --profile catjudge up --build -d
        ;;
      "stop")
        docker compose stop
        ;;
      "restart")
        docker compose restart
        ;;
      "logs")
        docker logs "catjudge_node" -f
        ;;
      "exec")
        docker exec -it "catjudge_node" /bin/bash 
        ;;
      *)
        echo "Usage: ./manage.sh judge <sub command>"
        ;;
    esac
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
    echo "  sync               Sync code and start CaCatHead containers"
    echo "  ps                 List CaCatHead containers"
    echo "  config             Config CaCatHead serivce passwords"
    echo "  judge              Create and start CaCatHead judge containers"
    echo "  judge sync         Sync code and start CaCatHead judge containers"
    echo "  judge stop         Stop CaCatHead judge containers"
    echo "  judge restart      Restart CaCatHead judge containers"
    echo "  judge logs         View output from CaCatHead judge containers"
    echo "  judge exec         Go to the CaCatHead judge containers"
    echo ""
    ;;
esac

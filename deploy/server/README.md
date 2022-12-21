# Deploy Server using Docker

## Content

This directory contains files:

+ `Dockerfile`: Build server docker image
+ `.env`: Environment variables that will be mapped in the container and something in it is related to the `docker-compose.yml`
+ `cacathead.yml`: Server configuration file that will be mapped in the container
+ `docker-entrypoint.sh`: Container bootstrap shell script, and it supports two different mode:
  + `./docker-entrypoint.sh server`: Start web server
  + `./docker-entrypoint.sh judge`: Start judge node
+ `wait`:  wait for database docker images to be started, and this is the binary downloaded from [docker-compose-wait](https://github.com/ufoscout/docker-compose-wait)

## Container Directory Structure

The server code is located at `/root/CaCatHead`.

The testcase root is located at `/root/testcases`.

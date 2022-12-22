# Contributing

Thank you for your support and interest to [CaCatHead](https://github.com/XLoJ/CaCatHead).

## Prepare Environment

Your environment should have the following tools installed globally:

### [Node.js](https://nodejs.org/)

Node.js® is an open-source, cross-platform JavaScript runtime environment.

You can download [Node.js](https://nodejs.org/) at the official site.

Or you can use any node version manager ([nvm](https://github.com/nvm-sh/nvm), [volta](https://github.com/nvm-sh/nvm), [fnm](https://github.com/Schniz/fnm), ...). You can see detailed guide in their website.

Then, make sure you have installed it globally. (Your version should be greater than mine)

```bash
$ node --version
v16.9.0

$ npm --version
8.19.3
```

### [pnpm](https://pnpm.io/)

Fast, disk space efficient package manager.

You can see installation guide [here](https://pnpm.io/installation).

Or you can install it with [npm].

```bash
$ npm i -g pnpm
# ...

$ pnpm --version
7.19.0
```

### [python](https://www.python.org/)

Python is a programming language that lets you work quickly and integrate systems more effectively.

**Your python version is at least 3.10.**

If you are using **Windows**, you can download it [here](https://www.python.org/downloads/). When installation, make sure you add python to your `PATH` environment variable. Or you can use some Windows package managers like [chocolatey](https://chocolatey.org/) or [Scoop](https://scoop.sh/), and you can see some guide in their websites.

If you are using **Mac OS**, you can use [Homebrew](https://brew.sh/) to download python.

If you are using **Linux**, I have no idea, and you should make sure your python version is **at least 3.10** for yourself.

```bash
$ python --version
Python 3.10.8
```

### [pipenv](https://pipenv.pypa.io/)

Pipenv is a tool that aims to bring the best of all packaging worlds (bundler, composer, npm, cargo, yarn, etc.) to the Python world.

You can see installation guide [here](https://pipenv.pypa.io/en/latest/#install-pipenv-today). Or just install it with pip (Make sure you use the **pip from your python 3.10**).

```bash
$ pip install --user pipenv
# ...

$ pipenv --version
pipenv, version 2022.10.12
```

### [Docker](https://www.docker.com/)

Docker is a platform designed to help developers build, share, and run modern applications. We handle the tedious setup, so you can focus on the code.

If you are using Windows or Mac OS, you can download Docker Desktop [here](https://www.docker.com/get-started/). If you are using Linux, you can follow official guide [here](https://docs.docker.com/engine/install/).

```bash
$ docker --version
Docker version 20.10.8, build 3967b7d
```

If you are tired of setting up the following environment, you can use this `docker-compose.yml` to start up all the required dev service.

First, make a temp directory. Then copy the following config to `docker-compose.yml` and create a text file `pass.txt` with your database password.

```yml
version: '3.9'

services:
  postgresql:
    image: postgres:15.1
    container_name: cacathead_dev_postgres
    restart: always
    networks:
      - cat_net
    ports:
      - '5432:5432'
    secrets:
      - db_pass
    environment:
      TZ: Asia/Shanghai
      PGTZ: Asia/Shanghai
      POSTGRES_DB: cacathead
      POSTGRES_USER: root
      POSTGRES_PASSWORD_FILE: /run/secrets/db_pass

  minio:
    image: minio/minio:RELEASE.2022-12-12T19-27-27Z
    container_name: cacathead_dev_minio
    command: server --console-address ":9090" /data
    restart: always
    networks:
      - cat_net
    ports:
      - '9000:9000'
      - '9090:9090'
    secrets:
      - minio_pass
    environment:
      TZ: Asia/Shanghai
      MINIO_ROOT_USER: root
      MINIO_ROOT_PASSWORD_FILE: /run/secrets/minio_pass

  redis:
    image: redis:7.0.5-alpine
    container_name: cacathead_dev_redis
    restart: always
    networks:
      - cat_net
    ports:
      - '6379:6379'

  rabbitmq:
    image: rabbitmq:management
    container_name: cacathead_dev_rabbitmq
    restart: always
    ports:
      - '5672:5672'
      - '15672:15672'
    networks:
      - cat_net

networks:
  cat_net:

secrets:
  db_pass:
    file: ./pass.txt
  minio_pass:
    file: ./pass.txt
  rmq_pass:
    file: ./pass.txt
```

Finally, start up docker compose service in this temp directory.

```bash
$ docker compose up
```

### [MinIO](https://min.io/)

> Life is short, we use docker.

```bash
$ docker run -d --name cacathead_dev_minio \
  -p 9000:9000 -p 9090:9090 \
  minio server --console-address ":9090"
```

### [RabbitMQ](https://www.rabbitmq.com/)

This is *optional*. If you want to develop something related to the judge queue, you should install it.

> Life is short, we use docker.

```bash
$ docker run -d --name cacathead_dev_rabbitmq \
  -p 15672:15672 -p 5672:5672 \
  rabbitmq:management
```

### [PostgreSQL](https://www.postgresql.org/)

This is *optional*. If you want to develop something related to the judge queue, you should install it.

> Life is short, we use docker.

```bash
$ docker run -d --name cacathead_dev_postgresql \
  -e TZ=Asia/Shanghai \
  -e PGTZ=Asia/Shanghai \
  -e POSTGRES_DB=cacathead \
  -e POSTGRES_USER=root \
  -e POSTGRES_PASSWORD=123456 \
  -p 5432:5432 \
  postgres
```

## Start CaCatHead Dev Server

After cloning the project, you should first update the submodules.

```bash
# Clone this project
$ git clone https://github.com/XLoJ/CaCatHead.git

# Go to the root directory
$ cd CaCatHead

# Clone submodules
$ git submodule update --init --recursive
```

If it is your first time to run dev server or the dependencies were changed, you should install dependencies. If the database models were changed, you should run django migrate command.

```bash
# You are at the root directory of this project

# Install frontend dependencies
$ pnpm i

$ cd server

# Install backend dependencies
$ pipenv install

# Migrate database
$ pipenv run python ./manage.py migrate
```

Start Django backend dev server:

```bash
# You are at the root directory of this project
$ cd server

$ pipenv run python ./manage.py runserver
```

Start Nuxt3 frontend dev server:

```bash
# You are at the root directory of this project
$ pnpm dev:app
```

## Start CaCatHead Judge Node

Make sure you have RabbitMQ and PostgreSQL on your local machine or you can connect to them on a remote dev server.

**The judge node should run in the Linux**. If you are using OS other than Linux, you can use docker, WSL, or any virtual machine.

First, if you are running the judge node somewhere different, do not forget following the previous guide to clone this project and its submodules, setup [pipenv](https://pipenv.pypa.io/), install dependencies, migrate your database.

Second, prepare the sandbox program. You should have [cmake](https://cmake.org/) installed.

```bash
# You are at the root directory of this project
$ cd CatJudge

# Copy the testlib to the include path
$ cp ./testlib/testlib.h /usr/local/include/testlib.h

# Setup CatJ log path
$ export LOG_PATH="/root/catj/logs"
$ mkdir -p "$LOG_PATH"

# Setup default checker
$ export DEFAULT_CHECKER="/usr/bin/lcmp"

# Build the program
$ cmake -DCMAKE_BUILD_TYPE:STRING=Release -B ./build -G "Unix Makefiles"
$ cmake --build ./build --config Release --target all

# Test whether CatJ works fine
$ cd ./build
$ ctest --verbose

# Copy the program to PATH
$ cp ./main /usr/bin/catj
$ cp ./fcmp /usr/bin/fcmp
$ cp ./hcmp /usr/bin/hcmp
$ cp ./lcmp /usr/bin/lcmp
$ cp ./ncmp /usr/bin/ncmp
$ cp ./nyesno /usr/bin/nyesno
$ cp ./rcmp4 /usr/bin/rcmp4
$ cp ./rcmp6 /usr/bin/rcmp6
$ cp ./rcmp9 /usr/bin/rcmp9
$ cp ./wcmp /usr/bin/wcmp
$ cp ./yesno /usr/bin/yesno

# Test CatJ
$ catj -h
catjudge/0.1.1

Options:
  -d <dir>       Run directory
  -l <language>  Code Language
  -t <time>      Time limit
  -m <memory>    Memory limit
  -s <checker>   Checker path
```

Third, copy [./server/cacathead.example.yml](./server/cacathead.example.yml) to `./server/cacathead.yml`. Then modify the config of your database and RabbitMQ connection like the following.

**Notice that your judge queue and django server should share the same database and rabbitmq config.**

```yml
# ...

database:
  engine: postgresql
  name: cacathead
  host: <your database host>
  port: '5432'
  username: root
  password: '123456'

rabbitmq:
  host: <your rmq host>
  port: '5672'
  username: guest
  password: guest
  judge_queue: local_judge_test

# ...
```

Finally, start the judge node and django server

```bash
$ pipenv run python ./judge.py
```

<p align="center">
  <img src="https://user-images.githubusercontent.com/30072175/199655609-e58c7e16-1cad-491e-be98-4033dba188f9.png" alt="CaCatHead" height="150">
</p>

# CaCatHead

[![CI](https://github.com/XLoJ/CaCatHead/actions/workflows/ci.yml/badge.svg)](https://github.com/XLoJ/CaCatHead/actions/workflows/ci.yml) [![Demo](https://img.shields.io/badge/CaCatHead-Demo-brightgreen)](https://oj.xlorpaste.cn/)

CaCatHead is the fully rewritten open-source successor of Cat (used internally by NJUST).

+ 📺 [Online Demo | 在线 Demo](https://oj.xlorpaste.cn/)
+ 📖 [Chinese Document | 中文文档](https://oj-docs.onekuma.cn/)

## Deploy

> **Prerequisite**
>
> Install latest [docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/).

First, clone this repo and its submodules.

```bash
# Clone this repo
$ git clone https://github.com/XLoJ/CaCatHead.git --depth 1

# Go to the root directory of this repo
$ cd CaCatHead

# Clone submodules
$ git submodule update --init --recursive
```

Then, create password files at [./deploy/pass/](./deploy/pass/). You should create 4 password files:

+ `./deploy/pass/db_pass.txt`: Postgresql database root user password
+ `./deploy/pass/redis_pass.txt`: Redis password
+ `./deploy/pass/minio_pass.txt`: MinIO password
+ `./deploy/pass/rmq_pass.txt`: RabbitMQ password

For example (If you are using Windows and Powershell, note that the stdout of `echo` command may be encoded by UTF-16):

```bash
$ echo "12345678" > ./deploy/password/db_pass.txt
$ echo "12345678" > ./deploy/password/redis_pass.txt
$ echo "12345678" > ./deploy/password/minio_pass.txt
$ echo "12345678" > ./deploy/password/rmq_pass.txt
```

Then, create RabbitMQ config file at `./deploy/rabbitmq.conf` to specify the default user is `root` and the default password is the same as the `./deploy/pass/rmq_pass.txt`. For example:

```bash
$ echo "default_user = root" >> ./deploy/rabbitmq.conf
$ echo "default_pass = $(cat ./deploy/password/rmq_pass.txt)" >> ./deploy/rabbitmq.conf
```

### Deploy locally

```bash
# Deploy docker
$ docker compose up -d
# or
$ ./manage.sh up

# See container logs
$ docker compose logs -f
# or
$ ./manage.sh logs

# Rebuild and Restart service
$ docker compose up --build -d
# or
$ ./manage.sh up
```

### Deploy on your server

Modify the nginx config at [./deploy/nginx/sites-enabled/cacathead.conf](./deploy/nginx/sites-enabled/cacathead.conf).

```nginx
server {
    listen              80;
    listen              [::]:80;
    server_name         <server domain>;
    # listen              443 ssl http2;
    # listen              [::]:443 ssl http2;
    # server_name         <server domain>;
}
```

You should change the `<server domain>` to the domain of your website.

If you want to enable HTTPS, you should add the following config (they are commented in the config file), and create the SSL key at the `./deploy/nginx/cert/ssl.pem` and `./deploy/nginx/cert/ssl.key`.

```nginx
    # SSL
    ssl_certificate     /root/cert/ssl.pem;
    ssl_certificate_key /root/cert/ssl.key;
```

Then, modify the server config at [./deploy/server/cacathead.yml](./deploy/server/cacathead.yml). Add your site domain to the `server.allowed_host` and your site url to the `server.trusted_origin`, like this:

```yaml
server:
  allowed_host:
    - '127.0.0.1'
    - server  # This is docker-compose service name, and is used for nginx
    - oj.xlorpaste.cn  # Config your domain here
  trusted_origin:
    - http://127.0.0.1
    - https://oj.xlorpaste.cn  # Config your domain here
  # ...
```

Finally, docker compose up.

```bash
$ docker compose up --build -d
# or
$ ./manage.sh up
```

## License

AGPL-3.0 License © 2022 [XLor](https://github.com/yjl9903)

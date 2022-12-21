<p align="center">
  <img src="https://user-images.githubusercontent.com/30072175/199655609-e58c7e16-1cad-491e-be98-4033dba188f9.png" alt="CaCatHead" height="150">
</p>

# CaCatHead

[![CI](https://github.com/XLoJ/CaCatHead/actions/workflows/ci.yml/badge.svg)](https://github.com/XLoJ/CaCatHead/actions/workflows/ci.yml)

CaCatHead is the fully rewritten open-source successor of Cat (used internally by NJUST).

+ 📺 [Online Demo | 在线 Demo](https://oj.xlorpaste.cn/)
+ 📖 [Document | 文档](https://oj.docs.onekuma.cn/)

## Deploy

> **Prerequisite**
>
> Install latest [docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/).

Create `pass.txt` to set the password of the database root user. (If you are using Windows and Powershell, note that the stdout of `echo` command may be encoded by UTF-16)

```bash
$ echo 'xxxyyy' > pass.txt
```

### Deploy locally

```bash
# Clone submodule CatJudge
$ git submodule update --init --recursive

# Deploy docker
$ docker compose up -d

# See container logs
$ docker compose logs -f

# Rebuild and Restart service
$ docker compose up --build -d
```

### Deploy on your server

First modify the nginx config at [./deploy/nginx/sites-enabled/cacathead.conf](./deploy/nginx/sites-enabled/cacathead.conf).

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

If you want to enable HTTPS, you should use the following config, and create the SSL key at `./.cert/ssl.pem` and `./.cert/ssl.key` (at the root directory of this project in your host machine).

```nginx
    # SSL
    ssl_certificate     /root/cert/ssl.pem;
    ssl_certificate_key /root/cert/ssl.key;
```

Then, modify the server config at [./deploy/server/cacathead.yml](./deploy/server/cacathead.yml). Add your site domain to the `server.allowed_host` and your site url to the `server.trusted_origin`, like this.

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

## License

AGPL-3.0 License © 2022 [XLor](https://github.com/yjl9903)

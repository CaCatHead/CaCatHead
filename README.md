# CaCatHead

[![CI](https://github.com/XLoJ/CaCatHead/actions/workflows/ci.yml/badge.svg)](https://github.com/XLoJ/CaCatHead/actions/workflows/ci.yml)

CaCatHead is the fully rewritten open-source successor of Cat (used internally by NJUST).

## Deploy

> **Prerequisite**
>
> Install latest [docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/).

Create `pass.txt` to set the password of the database root user. (If you are using Windows and Powershell, note that the stdout of `echo` command may be encoded by UTF-16)

```bash
$ echo 'xxxyyy' > pass.txt
```

Locally deploy:

```bash
# Clone submodule CatJudge
$ git submodule update --init --recursive
# Deploy docker
$ docker compose up
```

If you want to deploy it to a server, you should first modify the nginx config at [./deploy/nginx/sites-enabled/cacathead.conf](./deploy/nginx/sites-enabled/cacathead.conf).

```nginx
server {
    listen              80;
    listen              [::]:80;
    server_name         127.0.0.1;
    # listen              443 ssl http2;
    # listen              [::]:443 ssl http2;
    # server_name         <server address>;
}
```

You should change the `server_name` to the address of your website. If you want to enable HTTPS, you should use the following config, and create the SSL key at `./.cert/ssl.pem` and `./.cert/ssl.key` (in the host machine).

## License

AGPL-3.0 License © 2022 [XLor](https://github.com/yjl9903)

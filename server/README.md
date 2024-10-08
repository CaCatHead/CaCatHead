# CaCatHead - Server

[![CI](https://github.com/CaCatHead/CaCatHead/actions/workflows/ci.yml/badge.svg)](https://github.com/CaCatHead/CaCatHead/actions/workflows/ci.yml) [![codecov](https://codecov.io/gh/CaCatHead/CaCatHead/branch/main/graph/badge.svg?token=PEALBR8V0B)](https://codecov.io/gh/CaCatHead/CaCatHead)

CaCatHead server subproject is based on [Django](https://www.djangoproject.com/) web framework.

## Usage

### API Server

Start the api web server.

```bash
$ pipenv install                         # install deps
$ pipenv run python manage.py migrate    # migrate database
$ pipenv run python manage.py runserver  # start dev server
```

Open `Client/user.http` to try the api endpoints.

> We recommend you use
> the [IntelliJ HTTP Client](https://www.jetbrains.com/help/idea/http-client-in-product-code-editor.html) to test the api.

### Contest and Judge Worker

```bash
$ export C_FORCE_ROOT=true
$ export NODE_NAME=local_dev
$ pipenv run celery -A CaCatHead.core worker -l INFO
```

## Config

See [.env.example](./.env.example) and [cacathead.example.yml](./cacathead.example.yml).

## License

AGPL-3.0 License © 2022 [XLor](https://github.com/yjl9903)

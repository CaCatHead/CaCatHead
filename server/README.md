# CaCatHead - Server

[![CI](https://github.com/XLoJ/CaCatHead/actions/workflows/ci.yml/badge.svg)](https://github.com/XLoJ/CaCatHead/actions/workflows/ci.yml) [![codecov](https://codecov.io/gh/XLoJ/CaCatHead/branch/main/graph/badge.svg?token=PEALBR8V0B)](https://codecov.io/gh/XLoJ/CaCatHead)

CaCatHead server subproject is based on [Django](https://www.djangoproject.com/) web framework.

## Usage

Start the api web server.

```bash
$ pipenv install                         # install deps
$ pipenv run python manage.py migrate    # migrate database
$ pipenv run python manage.py runserver  # start dev server
```

Open `Client/user.http` to try the api endpoints.

> We recommend you use
> the [IntelliJ HTTP Client](https://www.jetbrains.com/help/idea/http-client-in-product-code-editor.html) to test the api.

## Config

See [.env.example](./.env.example).

# CaCatHead - Server

CaCatHead server sub-project is based on [Django](https://www.djangoproject.com/) web framework.

## Usage

Start the api web server.

```bash
$ pipenv install                         # install deps
$ export DEBUG='true'                    # enable debug mode
$ pipenv run python manage.py runserver  # start dev server
```

Open `client/user.http` to try the api endpoints.

> We recommend you use the Visual Studio Code extension [REST Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client).

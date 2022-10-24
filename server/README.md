# CaCatHead - Server

CaCatHead server sub-project is based on [Django](https://www.djangoproject.com/) web framework.

## Usage

Start the api web server.

```bash
$ pipenv install                                # install deps
$ export DEBUG='true'                           # enable debug mode
$ pipenv run python manage.py migrate           # migrate database
$ pipenv run python manage.py createsuper user  # create super user
$ pipenv run python manage.py runserver         # start dev server
```

Open `client/user.http` to try the api endpoints.

> We recommend you use the [IntelliJ HTTP Client](https://www.jetbrains.com/help/idea/http-client-in-product-code-editor.html) to test the api.

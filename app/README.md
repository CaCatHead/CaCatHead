# CaCatHead - Nuxt APP

[![CI](https://github.com/XLoJ/CaCatHead/actions/workflows/ci.yml/badge.svg)](https://github.com/XLoJ/CaCatHead/actions/workflows/ci.yml)

CaCatHead app subproject is based on [Nuxt](https://nuxt.com/) intuitive web framework.

## Usage

You should start django server first.

Start the app web server.

```bash
# At the root directory, not this sub directory
$ pnpm install

$ pnpm dev:app
```

## Config

The app will read the following environment variables.

+ `API_BASE`: The API endpoint of the web server
+ `ENABLE_CACHE`: You can set it `"false"` to disable cache
+ `SHIKI_CDN`: shiki cdn prefix

## License

AGPL-3.0 License © 2022 [XLor](https://github.com/yjl9903)

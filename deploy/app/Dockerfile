# This should be run at the project top level

FROM node:18 AS builder

ADD . /root/CaCatHead

WORKDIR /root/CaCatHead

RUN npm i --registry https://registry.npm.taobao.org -g pnpm

RUN pnpm install --registry https://registry.npm.taobao.org

ENV API_BASE http://server:8000

ENV NUXT_PROXY_OPTIONS_TARGET http://server:8000

RUN pnpm build:app

FROM node:18 AS runtime

COPY --from=builder /root/CaCatHead/app/.output /root/CaCatHead/app/.output

WORKDIR /root/CaCatHead

ENV NITRO_PORT 3333

EXPOSE 3333

CMD ["node", "app/.output/server/index.mjs"]

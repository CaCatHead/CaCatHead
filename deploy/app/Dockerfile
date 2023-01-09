# This should be run at the project top level

FROM node:18 AS builder

RUN npm i --registry https://registry.npm.taobao.org -g pnpm

ADD . /root/CaCatHead

WORKDIR /root/CaCatHead

# @nuxt/image-edge 依赖的 sharp 镜像
ENV npm_config_sharp_binary_host=https://cdn.npmmirror.com/binaries/sharp \
    npm_config_sharp_libvips_binary_host=https://cdn.npmmirror.com/binaries/sharp-libvips \
    API_BASE=http://server:8000 \
    NUXT_PROXY_OPTIONS_TARGET=http://server:8000

RUN pnpm install --registry https://registry.npm.taobao.org

RUN pnpm build:app

FROM node:18 AS runtime

COPY --from=builder /root/CaCatHead/app/.output /root/CaCatHead/app/.output

WORKDIR /root/CaCatHead

ENV NITRO_PORT 3333

EXPOSE 3333

CMD ["node", "app/.output/server/index.mjs"]

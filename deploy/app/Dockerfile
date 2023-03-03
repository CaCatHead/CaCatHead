# This should be run at the project top level

FROM node:18 AS builder

RUN npm i --registry https://registry.npmmirror.com/ -g pnpm

ADD ./package.json ./.npmrc ./pnpm-lock.yaml ./pnpm-workspace.yaml /root/CaCatHead/

ADD ./app/package.json /root/CaCatHead/app/

ADD ./app/patches /root/CaCatHead/app/patches/

ADD ./server/package.json /root/CaCatHead/server/

WORKDIR /root/CaCatHead

# @nuxt/image-edge 依赖的 sharp 镜像
ENV npm_config_sharp_binary_host=https://cdn.npmmirror.com/binaries/sharp \
    npm_config_sharp_libvips_binary_host=https://cdn.npmmirror.com/binaries/sharp-libvips \
    API_BASE=http://server:8000 \
    NUXT_PROXY_OPTIONS_TARGET=http://server:8000

RUN pnpm install --registry https://registry.npmmirror.com/

ADD ./app /root/CaCatHead/app/

ADD ./deploy/app/cacathead.json /root/CaCatHead/app/

ADD ./deploy/app/public /root/CaCatHead/app/public/

ARG SHIKI_CDN

ARG COMMIT_SHA

ENV SHIKI_CDN=${SHIKI_CDN} COMMIT_SHA=${COMMIT_SHA}

RUN pnpm build:app

FROM node:18 AS runtime

ENV TZ=Asia/Shanghai TimeZone=Asia/Shanghai

RUN echo "${TimeZone}" > /etc/timezone \
   && dpkg-reconfigure -f noninteractive tzdata

COPY --from=builder /root/CaCatHead/app/.output /root/CaCatHead/app/.output

WORKDIR /root/CaCatHead

ENV NITRO_PORT 3333

EXPOSE 3333

CMD ["node", "app/.output/server/index.mjs"]

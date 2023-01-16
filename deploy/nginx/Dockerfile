FROM nginx:latest

# TimeZone
ENV TimeZone Asia/Shanghai

RUN echo "${TimeZone}" > /etc/timezone \
   && dpkg-reconfigure -f noninteractive tzdata

ARG SHIKI_VERSION=0.12.1

# Download shiki
RUN curl https://cdn.npmmirror.com/packages/shiki/${SHIKI_VERSION}/shiki-${SHIKI_VERSION}.tgz --output shiki.tgz \
   && tar -xvzf shiki.tgz \
   && mkdir -p /var/www/cacathead/public \
   && cp -R package/ /var/www/cacathead/shiki

ADD ./deploy/nginx /etc/nginx/

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]

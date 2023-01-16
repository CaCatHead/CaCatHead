FROM nginx:latest

COPY . /etc/nginx/

# TimeZone
ENV TimeZone Asia/Shanghai

RUN echo "${TimeZone}" > /etc/timezone \
   && dpkg-reconfigure -f noninteractive tzdata

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]

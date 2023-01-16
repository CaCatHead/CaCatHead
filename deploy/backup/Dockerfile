FROM postgres:15.1

ENV TZ=Asia/Shanghai TimeZone=Asia/Shanghai

RUN echo "${TimeZone}" > /etc/timezone \
   && dpkg-reconfigure -f noninteractive tzdata

# See https://github.com/ufoscout/docker-compose-wait
ADD ./deploy/server/wait ./

# See https://gobackup.github.io/
ADD ./deploy/backup/gobackup ./

ADD ./deploy/backup/docker-entrypoint.sh ./

RUN mkdir -p ~/.gobackup/ \
  && chmod +x ./wait \
  && chmod +x ./gobackup \
  && chmod +x ./docker-entrypoint.sh

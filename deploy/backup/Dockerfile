FROM mysql:8.0.30

# See https://github.com/ufoscout/docker-compose-wait
ADD ./deploy/server/wait ./

# See https://gobackup.github.io/
ADD ./deploy/backup/gobackup ./

ADD ./deploy/backup/docker-entrypoint.sh ./

RUN mkdir -p ~/.gobackup/ \
  && chmod +x ./wait \
  && chmod +x ./gobackup \
  && chmod +x ./docker-entrypoint.sh

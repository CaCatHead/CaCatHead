# This should be run at the project top level

FROM python:3.10 AS builder

# 换成阿里源
RUN sed -i "s@http://deb.debian.org@http://mirrors.aliyun.com@g" /etc/apt/sources.list \
  && rm -rf /var/lib/apt/lists/*

RUN apt-get update \
  && apt-get install -y gcc g++ cmake default-jdk default-jre

# 换成清华源
RUN pip install --user pipenv -i https://pypi.tuna.tsinghua.edu.cn/simple/ --trusted-host pypi.tuna.tsinghua.edu.cnpypi.tuna.tsinghua.edu.cn 

ENV PIPENV_VENV_IN_PROJECT=1

ADD ./server/Pipfile.lock ./server/Pipfile /usr/src/

WORKDIR /usr/src

RUN /root/.local/bin/pipenv sync \
  && /usr/src/.venv/bin/python -c "import django; print(django.__version__)"

ADD ./CatJudge /usr/src/CatJudge/

RUN cd /usr/src/CatJudge \
  && cp ./testlib/testlib.h /usr/local/include/testlib.h \
  && mkdir -p /root/catj/logs \
  && export LOG_PATH="/root/catj/logs" \
  && export DEFAULT_CHECKER="/usr/bin/lcmp" \
  && cmake -DCMAKE_BUILD_TYPE:STRING=Release -B ./build -G "Unix Makefiles" \
  && cmake --build ./build --config Release --target all \
  && cd ./build \
  && ctest --verbose \
  && cp ./main /usr/bin/catj \
  && cp ./fcmp /usr/bin/fcmp \
  && cp ./hcmp /usr/bin/hcmp \
  && cp ./lcmp /usr/bin/lcmp \
  && cp ./ncmp /usr/bin/ncmp \
  && cp ./nyesno /usr/bin/nyesno \
  && cp ./rcmp4 /usr/bin/rcmp4 \
  && cp ./rcmp6 /usr/bin/rcmp6 \
  && cp ./rcmp9 /usr/bin/rcmp9 \
  && cp ./wcmp /usr/bin/wcmp \
  && cp ./yesno /usr/bin/yesno

FROM python:3.10 AS runtime

# 换成阿里源
RUN sed -i "s@http://deb.debian.org@http://mirrors.aliyun.com@g" /etc/apt/sources.list \
  && rm -rf /var/lib/apt/lists/*

RUN apt-get update \
  && apt-get install -y cron gcc g++ default-jdk default-jre

RUN mkdir -v /usr/src/.venv \
  && mkdir -p /root/catj/logs

COPY --from=builder /usr/src/.venv/ /usr/src/.venv/

COPY --from=builder /usr/local/include/testlib.h /usr/local/include/testlib.h

COPY --from=builder /usr/bin/catj \
    /usr/bin/fcmp /usr/bin/hcmp /usr/bin/lcmp /usr/bin/ncmp /usr/bin/nyesno \
    /usr/bin/rcmp4 /usr/bin/rcmp6 /usr/bin/rcmp9 /usr/bin/wcmp /usr/bin/yesno \
    /usr/bin/

ADD ./server /root/CaCatHead

ADD ./deploy/server/docker-entrypoint.sh /root/CaCatHead

ADD ./deploy/server/ping.cron /root/CaCatHead

ADD ./deploy/server/ping.sh /root/CaCatHead

# See https://github.com/ufoscout/docker-compose-wait
ADD ./deploy/server/wait /root/CaCatHead

WORKDIR /root/CaCatHead

RUN /usr/src/.venv/bin/python -c "import django; print(django.__version__)" \
  && /usr/src/.venv/bin/python ./manage.py collectstatic --no-input \
  && chmod +x ./docker-entrypoint.sh \
  && chmod +x ./ping.sh \
  && chmod +x ./wait \
  && chmod 0644 ./ping.cron \
  && crontab ./ping.cron \
  && touch /var/log/cron.log

EXPOSE 80

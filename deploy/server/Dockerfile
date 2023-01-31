# This should be run at the project top level

FROM yjl9903/sandbox:latest AS builder

# 换成阿里源
RUN sed -i "s@http://archive.ubuntu.com@http://mirrors.aliyun.com@g" /etc/apt/sources.list \
  && sed -i "s@http://security.ubuntu.com@http://mirrors.aliyun.com@g" /etc/apt/sources.list \
  && rm -rf /var/lib/apt/lists/* \
  && apt-get update \
  && apt-get install -y cmake python3-pip

# 换成清华源
RUN pip3 install --user pipenv -i https://pypi.tuna.tsinghua.edu.cn/simple/ --trusted-host pypi.tuna.tsinghua.edu.cnpypi.tuna.tsinghua.edu.cn 

ENV PIPENV_VENV_IN_PROJECT=1

ADD ./server/Pipfile.lock ./server/Pipfile /usr/src/

WORKDIR /usr/src

RUN /root/.local/bin/pipenv sync \
  && /usr/src/.venv/bin/python -c "import django; print(django.__version__)"

ADD ./CatJudge /usr/src/CatJudge/

RUN cd /usr/src/CatJudge \
  && mkdir -p /root/catj/logs \
  && mkdir -p /root/checkers \
  && export LOG_PATH="/root/catj/logs" \
  && export CHECKER_ROOT="/root/checkers" \
  && export DEFAULT_CHECKER="lcmp" \
  && cmake -DCMAKE_BUILD_TYPE:STRING=Release -B ./build -G "Unix Makefiles" \
  && cmake --build ./build --config Release --target all \
  && cd ./build \
  && cp ./main /usr/bin/catj \
  && cp ./fcmp /root/checkers/fcmp \
  && cp ./hcmp /root/checkers/hcmp \
  && cp ./lcmp /root/checkers/lcmp \
  && cp ./ncmp /root/checkers/ncmp \
  && cp ./nyesno /root/checkers/nyesno \
  && cp ./rcmp4 /root/checkers/rcmp4 \
  && cp ./rcmp6 /root/checkers/rcmp6 \
  && cp ./rcmp9 /root/checkers/rcmp9 \
  && cp ./wcmp /root/checkers/wcmp \
  && cp ./yesno /root/checkers/yesno \
  && ln -s /usr/bin/python3 /usr/local/bin/python \
  && ctest --verbose

FROM yjl9903/sandbox:latest AS runtime

# 换成阿里源
RUN sed -i "s@http://archive.ubuntu.com@http://mirrors.aliyun.com@g" /etc/apt/sources.list \
  && sed -i "s@http://security.ubuntu.com@http://mirrors.aliyun.com@g" /etc/apt/sources.list \
  && rm -rf /var/lib/apt/lists/* \
  && apt-get update \
  && apt-get install -y cron \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir -v /usr/src/.venv \
  && mkdir -p /root/catj/logs \
  && mkdir -p /root/checkers

COPY --from=builder /usr/src/.venv/ /usr/src/.venv/

COPY --from=builder /usr/bin/catj /usr/bin/catj

COPY --from=builder /root/checkers/* /root/checkers/

ADD ./server ./deploy/server/docker-entrypoint.sh \
    ./deploy/server/ping.cron ./deploy/server/ping.sh ./deploy/server/wait \
    /root/CaCatHead/

WORKDIR /root/CaCatHead

RUN /usr/src/.venv/bin/python -c "import django; print(django.__version__)" \
  && /usr/src/.venv/bin/python ./manage.py collectstatic --no-input \
  && chmod +x ./docker-entrypoint.sh \
  && chmod +x ./ping.sh \
  && chmod +x ./wait \
  && chmod 0644 ./ping.cron \
  && mkdir -p /root/cron/log/ \
  && touch /root/cron/log/cron.log \
  && crontab ./ping.cron

ARG COMMIT_SHA

ENV COMMIT_SHA=${COMMIT_SHA}

EXPOSE 80

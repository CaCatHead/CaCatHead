FROM python:3.10 AS builder

RUN apt-get update \
  && apt-get install -y gcc g++ cmake default-jdk default-jre

RUN pip install --user pipenv

# Tell pipenv to create venv in the current directory
ENV PIPENV_VENV_IN_PROJECT=1

# Pipfile contains requests
ADD Pipfile.lock Pipfile /usr/src/

WORKDIR /usr/src

# NOTE: If you install binary packages required for a python module, you need
# to install them again in the runtime. For example, if you need to install pycurl
# you need to have pycurl build dependencies libcurl4-gnutls-dev and libcurl3-gnutls
# In the runtime container you need only libcurl3-gnutls

# RUN apt install -y libcurl3-gnutls libcurl4-gnutls-dev

RUN /root/.local/bin/pipenv sync

RUN /usr/src/.venv/bin/python -c "import django; print(django.__version__)"

ADD CatJudge /usr/src/CatJudge/

RUN cd /usr/src/CatJudge \
  && cp ./testlib/testlib.h /usr/local/include/testlib.h \
  && mkdir -p /root/catj/logs \
  && export LOG_PATH="/root/catj/logs" \
  && export DEFAULT_CHECKER="/usr/bin/lcmp" \
  && cmake -DCMAKE_BUILD_TYPE:STRING=Release -B ./build -G "Unix Makefiles" \
  && cmake --build ./build --config Release --target all -j 18 \
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

RUN apt-get update \
  && apt-get install -y gcc g++ default-jdk default-jre

RUN mkdir -v /usr/src/.venv \
  && mkdir -p /root/catj/logs

COPY --from=builder /usr/src/.venv/ /usr/src/.venv/

COPY --from=builder /usr/local/include/testlib.h /usr/local/include/testlib.h

COPY --from=builder /usr/bin/catj \
    /usr/bin/fcmp /usr/bin/hcmp /usr/bin/lcmp /usr/bin/ncmp /usr/bin/nyesno \
    /usr/bin/rcmp4 /usr/bin/rcmp6 /usr/bin/rcmp9 /usr/bin/wcmp /usr/bin/yesno \
    /usr/bin/

ADD ./ /root/CaCatHead

WORKDIR /root/CaCatHead

RUN /usr/src/.venv/bin/python -c "import django; print(django.__version__)" \
  && /usr/src/.venv/bin/python ./manage.py collectstatic --no-input \
  && chmod +x ./docker-entrypoint.sh

# HERE GOES ANY CODE YOU NEED TO ADD TO CREATE YOUR APPLICATION'S IMAGE
# For example
# RUN apt install -y libcurl3-gnutls
# RUN adduser --uid 123123 coolio
# ADD run.py /usr/src/

EXPOSE 80

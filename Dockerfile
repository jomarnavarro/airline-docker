FROM ubuntu:latest

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y \
  && apt-get install -y python3-pip python3-dev postgresql postgresql-contrib libpq-dev \
  && apt-get install -y python-psycopg2 \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

COPY . /usr/src/app
WORKDIR /usr/src/app
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
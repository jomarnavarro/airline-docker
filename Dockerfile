FROM python:3.8.11-alpine3.14

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

COPY . /usr/src/app
WORKDIR /usr/src/app
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
FROM python:3.8-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN apt-get update \
  && apt-get install -y netcat

RUN pip install --upgrade pip \
  && pip install pipenv

COPY Pipfile Pipfile.lock /code/

RUN pipenv install --system

COPY . /code/

ENTRYPOINT ["./entrypoint.sh"] 

FROM python:3.8.1-alpine

# set work directory
WORKDIR /code

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy requirements file
COPY ./requirements.txt /code/requirements.txt

# install dependencies
RUN set -eux \
    && apk add --no-cache --virtual .build-deps build-base \
        libressl-dev libffi-dev gcc musl-dev python3-dev \
        mariadb-dev mysql-client\
    && pip install --upgrade pip setuptools wheel \
    && pip install -r /code/requirements.txt \
    && rm -rf /root/.cache/pip

# copy project
COPY . /code
RUN chmod +x ./scripts/wait-for-db.sh
EXPOSE 8080
CMD ["./scripts/wait-for-db.sh","--","uvicorn","src.main:app","--reload","--workers 1","--host 0.0.0.0","--port 8080"]

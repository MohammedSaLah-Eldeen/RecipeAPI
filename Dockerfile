FROM python:3.9-alpine3.13
LABEL maintainer="supermaker"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false
RUN python -m venv /.api && \
    /.api/bin/pip install --upgrade pip && \
    /.api/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
       then /.api/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        apiuser

ENV PATH="/.api/bin:$PATH"
USER apiuser

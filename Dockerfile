FROM python:3.10.9-slim-buster

RUN apt-get update && \
    apt-get install -y gcc libpq-dev git && \
    apt clean && \
    rm -rf /var/cache/apt/* && \
    git config --global --add safe.directory /src

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8

COPY requirements/ /tmp/requirements

RUN pip install -U pip && \
    pip install --no-cache-dir -r /tmp/requirements/dev.txt

COPY . /src
ENV PATH "$PATH:/src/scripts"


WORKDIR /src
RUN useradd -m -d /src -s /bin/bash app

CMD ["./scripts/start-dev.sh"]
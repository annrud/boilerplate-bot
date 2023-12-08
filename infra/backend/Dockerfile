FROM python:3.9-slim

WORKDIR /code

COPY requirements.txt .
COPY boilerplate_bot .
COPY infra/backend/entrypoint.sh /entrypoint.sh


RUN set -ex \
    && python3 -m pip install --upgrade pip \
    && pip3 install -r requirements.txt \
    && chmod +x /entrypoint.sh


ENTRYPOINT ["/entrypoint.sh"]

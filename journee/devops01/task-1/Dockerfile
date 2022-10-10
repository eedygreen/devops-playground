# syntax=docker/dockerfile:1

FROM python:3.9.5

WORKDIR /journee

COPY ./requirements.txt /journee/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /journee/requirements.txt


COPY ./app /journee/app

RUN --mount=type=secret,id=mysecret cat /run/secrets/mysecret


HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8000/secret || exit 1


CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]
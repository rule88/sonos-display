ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-alpine as builder

RUN apk add libxml2-dev libxslt-dev cargo

WORKDIR /app
COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

FROM python:${PYTHON_VERSION}-alpine

RUN apk add libxslt-dev

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

WORKDIR /app
COPY ./app ./

ENV TZ=Europe/Amsterdam
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["python","./index.py"]

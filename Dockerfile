ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-alpine

RUN apk add libxml2-dev libxslt-dev cargo

WORKDIR /app
COPY ./requirements.txt /tmp/
COPY ./app ./

RUN pip install -r /tmp/requirements.txt

ENV TZ=Europe/Amsterdam
ENV PYTHONUNBUFFERED=1

CMD ["python","./index.py"]

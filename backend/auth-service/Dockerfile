FROM python:3.8-slim

WORKDIR /

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

RUN apt-get update \
    && apt-get install -y --no-install-recommends apt-utils gcc python-dev  \
    && rm -rf /var/lib/apt/lists/* \
    && pip install pipenv \
    && pipenv lock  \
    && pipenv install --ignore-pipfile --system\
    && apt-get purge -y --auto-remove gcc python-dev

EXPOSE 8001
CMD python src/main.py

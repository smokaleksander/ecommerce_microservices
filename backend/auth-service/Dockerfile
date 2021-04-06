FROM python:slim

WORKDIR /app
COPY requirements.txt .
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc python-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install -r requirements.txt \
    && apt-get purge -y --auto-remove gcc python-dev

COPY . .
EXPOSE 8001
CMD python app/main.py

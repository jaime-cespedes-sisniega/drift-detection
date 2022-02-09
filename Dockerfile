FROM python:3.8.11-slim

RUN apt-get -y update &&\
    apt-get -y install python3-opencv

EXPOSE 5001

RUN adduser --disabled-password --gecos '' api-user

WORKDIR /src

COPY requirements/requirements.txt .

RUN pip install --upgrade -r requirements.txt --no-cache-dir && \
    rm requirements.txt && \
    mkdir .multiproc && \
    chown api-user: .multiproc

COPY ./app app/
COPY ./gunicorn_conf.py .

USER api-user

# Default env variables
ENV NUM_WORKERS 1
ENV TIMEOUT 120
ENV PROMETHEUS_MULTIPROC_DIR ".multiproc"

CMD ["sh", "-c", "gunicorn -b 0.0.0.0:5001 -w ${NUM_WORKERS} -t ${TIMEOUT} -c gunicorn_conf.py -k uvicorn.workers.UvicornWorker app.main:app"]
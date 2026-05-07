FROM python:3.10.4-bullseye

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r ./requirements.txt

COPY ./app /usr/src/app
WORKDIR /usr/src/app

RUN chmod -R g+w /usr/src/app/instance

CMD gunicorn --bind 0.0.0.0:5000 app4:app
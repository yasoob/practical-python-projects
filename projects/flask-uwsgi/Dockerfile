FROM python:3.7-slim

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install nginx \
    && apt-get -y install python3-dev \
    && apt-get -y install build-essential

COPY . /flask_app
WORKDIR /flask_app

RUN pip install -r requirements.txt --src /usr/local/src
COPY nginx.conf /etc/nginx
RUN chmod +x ./start-script.sh
CMD ["./start-script.sh"]
FROM python:3.7

RUN mkdir /usr/app

COPY ./requirements.txt /usr/app
COPY ./uwsgi.ini /usr/app

WORKDIR /usr/app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install uwsgi

# Update and allow for apt over HTTPS
RUN apt-get update && \
  apt-get install -y apt-utils

RUN apt-get install -y apt-transport-https

EXPOSE 5000

#RUN pip3 install flask

#CMD ["python", "app.py"]

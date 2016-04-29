FROM python:3

RUN apt-get update && apt-get install -y \
        wget curl git vim tig screen tree

RUN useradd --uid 1000 -d /opt/bitwrap bitwrap

ENV PROJECT_VERSION=0.0.3

RUN mkdir /opt/app

COPY requirements.txt /opt/app/

COPY . /opt/app/
WORKDIR /opt/app

RUN pip install -r requirements.txt 
RUN chown bitwrap:bitwrap /opt/app

USER bitwrap

EXPOSE 8080
VOLUME ["/home/bitwrap", "/opt/bitwrap"]

CMD python -m bitwrap.io

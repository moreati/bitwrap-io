FROM python

RUN \
      apt-get update &&\
      apt-get install -y \
        sudo wget curl git vim tig screen tree

RUN useradd --uid 1000 -d /opt/bitwrap bitwrap && \
 echo "bitwrap ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

ENV PROJECT_VERSION=0.0.2

RUN pip install virtualenv

RUN mkdir /opt/app && chown bitwrap:bitwrap /opt/app

COPY . /opt/app/
WORKDIR /opt/app

RUN virtualenv -p python3 /opt/app/.env
RUN . /opt/app/.env/bin/activate && pip install -r requirements.txt 

USER bitwrap

EXPOSE 8080
VOLUME ["/home/bitwrap", "/opt/bitwrap"]

CMD . /opt/app/.env/bin/activate && python -m bitwrap.io

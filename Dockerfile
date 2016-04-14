FROM python

RUN \
      apt-get update &&\
      apt-get install -y \
        sudo wget curl git vim tig screen tree

RUN useradd --uid 1000 -d /opt/bitwrap bitwrap && \
 echo "bitwrap ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

ENV PROJECT_VERSION=0.0.1

RUN mkdir /opt/app && chown bitwrap:bitwrap /opt/app

COPY . /opt/app/
WORKDIR /opt/app

#RUN pip install -r requirements.txt 

USER bitwrap

EXPOSE 5000
VOLUME ["/home/bitwrap", "/opt/bitwrap"]

CMD ["bash", "--login"]

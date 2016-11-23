FROM python:2.7.11

RUN apt-get update && apt-get install -y \
        wget curl git vim tig tree cmake

RUN mkdir /opt/bitwrap /repo

ENV PROJECT_VERSION=0.0.4

COPY requirements.txt /opt/bitwrap/
RUN pip install -r /opt/bitwrap/requirements.txt 

COPY bitwrap_io /opt/bitwrap/bitwrap_io
COPY entry.sh /opt/bitwrap/
COPY service.tac /opt/bitwrap/

WORKDIR /opt/bitwrap

EXPOSE 80
VOLUME ["/repo"]

ENV BITWRAP_REPO_PATH=/repo/
ENV BITWRAP_PORT=80

ENTRYPOINT ["/opt/bitwrap/entry.sh"]

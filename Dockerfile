FROM python:2.7.11

RUN apt-get update && \
    apt-get install -y \
        sudo wget curl git vim tig screen tree

RUN useradd --uid 1000 -d /opt/bitwrap bitwrap && \
 echo "bitwrap ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

ENV PROJECT_VERSION=0.0.1

RUN mkdir /opt/bitwrap-pnml

COPY requirements.txt /opt/bitwrap-pnml/
WORKDIR /opt/bitwrap-pnml

RUN pip install -r requirements.txt 

COPY app.tac /opt/bitwrap-pnml/ 
COPY entry.sh /opt/bitwrap-pnml/
COPY examples/ /opt/bitwrap-pnml/examples
COPY bitwrap_pnml/ /opt/bitwrap-pnml/bitwrap_pnml

RUN chown -R bitwrap:bitwrap /opt/bitwrap-pnml
USER bitwrap

EXPOSE 80

VOLUME ["/opt/bitwrap", "/repo"]

ENV BITWRAP_REPO_PATH=/repo/
ENV BITWRAP_PORT=80

ENTRYPOINT ["/opt/bitwrap-pnml/entry.sh"]

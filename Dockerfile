FROM python:2.7.12

ENV PROJECT_VERSION=0.1.0

WORKDIR /opt/bitwrap
COPY . /opt/bitwrap/ 
RUN pip install -r requirements.txt 

EXPOSE 8080

VOLUME ["/opt/bitwrap", "/repo"]

ENV LMDB_PATH=/repo/
ENV SCHEMA_PATH=/opt/bitwrap/schemata
ENV BITWRAP_PORT=8080

ENTRYPOINT ["/opt/bitwrap/entry.sh"]

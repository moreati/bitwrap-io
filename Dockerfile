FROM python:2.7.12

ENV PROJECT_VERSION=0.1.0

WORKDIR /opt/bitwrap-io
COPY . /opt/bitwrap-io/ 
RUN pip install -r requirements.txt 

VOLUME ["/opt/bitwrap", "/repo"]

ENV BITWRAP_DATASTORE=lmdb
ENV LMDB_PATH=/repo/
ENV SCHEMA_PATH=/opt/bitwrap-io/bitwrap_io/schemata
ENV BITWRAP_PORT=8080

EXPOSE 8080

ENTRYPOINT ["/opt/bitwrap-io/entry.sh"]


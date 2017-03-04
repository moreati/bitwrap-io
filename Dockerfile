FROM python:2.7.13

ENV PROJECT_VERSION=0.1.4

WORKDIR /opt/bitwrap-io
COPY . /opt/bitwrap-io/ 
RUN pip install -r requirements.txt 

VOLUME ["/opt/bitwrap", "/repo"]

ENV BITWRAP_DATASTORE=lmdb
ENV SCHEMA_PATH=/opt/bitwrap-io/bitwrap_io/schemata
ENV LMDB_PATH=/repo/

EXPOSE 8080

ENTRYPOINT ["/opt/bitwrap-io/entry.sh"]


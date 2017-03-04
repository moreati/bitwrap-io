FROM python:2.7.13

WORKDIR /opt/bitwrap-io
COPY . .
RUN pip install .

VOLUME ["/opt/bitwrap", "/repo"]

ENV BITWRAP_DATASTORE=lmdb
ENV SCHEMA_PATH=/opt/bitwrap-io/bitwrap_io/schemata
ENV LMDB_PATH=/repo/

EXPOSE 8080

ENTRYPOINT ["/opt/bitwrap-io/entry.sh"]


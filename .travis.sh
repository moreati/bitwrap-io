#!/usr/bin/env bash

function write() {
  echo $1 >> rds_config.py
}

> rds_config.py

write 'db_username = "travis"'
write 'db_password = ""'
write 'db_name = "bitwrap"'
write 'rds_host = "127.0.0.1"'

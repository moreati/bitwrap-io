#!/usr/bin/env bash
PYTHONPATH=./
twistd -n bitwrap --listen-address 0.0.0.0 --listen-port 8080

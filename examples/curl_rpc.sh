#!/usr/bin/env bash

if [[ "${BITWRAP_ENDPOINT}x" == "x" ]] ; then
    BITWRAP_ENDPOINT='http://127.0.0.1:8080'
fi

printf "\n\n$(date)\ntesting: ${BITWRAP_ENDPOINT}"

ID=`date +%s`
METHOD='transform'
SCHEMA='counter'
ACTION='INC'

#OID="OID${ID}"
OID="000000000"

REQ=`echo {\"id\":${ID}, \"method\":\"${METHOD}\", \"params\":[{\"oid\": \"${OID}\", \"schema\": \"${SCHEMA}\", \"action\": \"${ACTION}\" }]}`

function title() {
  printf "\n\n$1 =>  "   
}

function post_rpc() {
  title '<= RPC'
  title 'POST'
  echo "${REQ}" | python -m json.tool
  
  title ${BITWRAP_ENDPOINT}/api
  curl ${BITWRAP_ENDPOINT}/api --data "${REQ}" 2>/dev/null | python -m json.tool
}

function get_state() {
  title '<= STATE'
  URL="${BITWRAP_ENDPOINT}/${SCHEMA}/${OID}.json"
  title $URL
  curl $URL 2>/dev/null | python -m json.tool
}

function get_machine() {
  title '<= MACHINE'
  URL="${BITWRAP_ENDPOINT}/machine/${SCHEMA}.json"
  title $URL
  curl $URL 2>/dev/null | python -m json.tool
}

function get_event() {
  title '<= EVENT'
  URL="${BITWRAP_ENDPOINT}/head/${SCHEMA}/${OID}.json"
  title $URL
  curl $URL 2>/dev/null | python -m json.tool
}

post_rpc && \
get_state && \
get_machine && \
get_event

if [[ $? -ne 0 ]] ; then
  echo "FAIL"
  exit 1
else
  echo "PASS"
fi

#!/usr/bin/env bash

if [[ "${BITWRAP_ENDPOINT}x" == "x" ]] ; then
    BITWRAP_ENDPOINT='http://127.0.0.1:8080/api'
fi

printf "\n\n$(date)\ntesting: ${BITWRAP_ENDPOINT}"

ID=`date +%s`
METHOD='transform'
SCHEMA='counter'
ACTION='INC'

#OID="OID${ID}"
OID="000000000"

REQ=`echo {\"id\":${ID}, \"method\":\"${METHOD}\", \"params\":[{\"oid\": \"${OID}\", \"schema\": \"${SCHEMA}\", \"action\": \"${ACTION}\" }]}`

function post_rpc() {
  printf "\n\nrequest => "
  echo "${REQ}" | python -m json.tool
  
  printf "\n\nresponse => "
  curl ${BITWRAP_ENDPOINT} --data "${REQ}" 2>/dev/null | python -m json.tool
}

post_rpc #&>/dev/null

if [[ $? -ne 0 ]] ; then
  echo "FAIL"
else
  echo "PASS"
fi

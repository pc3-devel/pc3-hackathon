#!/bin/bash

if [ $# -ne 5 ]; then
	echo "Usage: $0 <server> <teamName> <problemName> <language> <submit>"
	exit 1
fi

echo "Input your team password: "
#read $PASSWORD

PASSWORD="password"

curl -c /tmp/cookie.txt -d "username=$2&password="$PASSWORD $1:5000/authenticate
echo
curl -b /tmp/cookie.txt -F teamCode=@$5 $1:5000/compete/$3/$4
echo
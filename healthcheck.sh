#!/bin/sh

pg_uri="postgres://root:test1234@postgres-flask/flights"
# make sure pg is ready to accept connections
# command = "pg_isready -h localhost -p 5432 -U root"
until pg_isready -h postgres-flask -p 5432 -U root
do
    echo "Waiting for postgres at: $pg_uri"
    sleep 2
done
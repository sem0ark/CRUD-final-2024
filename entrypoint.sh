#!/bin/bash

echo "Waiting for postgres..."

while ! nc -z db $POSTGRES_PORT; do
  sleep 0.1
done
echo "PostgreSQL started"

echo "add command for your migrations here"
exec "$@"

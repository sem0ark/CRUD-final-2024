#!/bin/bash

echo "Waiting for postgres..."

while ! nc -z db $POSTGRES_PORT; do
  sleep 0.1
done
echo "PostgreSQL started"

echo "Running migrations"
alembic upgrade head

echo "Running server"

if [ "$DEV" = "1" ]
then
echo "Running in DEV mode"
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
else
uvicorn src.main:app --host 0.0.0.0 --port 8000
fi

echo "Running exec command"
exec "$@"

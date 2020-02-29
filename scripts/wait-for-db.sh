#!/bin/sh


cmd="$@"

echo "Waiting for MariaDB Server..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done

echo "Connected to MariaDB Server"
exec $cmd

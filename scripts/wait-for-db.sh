#!/bin/sh


cmd="$@"

echo "Waiting for MariaDB Server..."
while ! nc -z $DB_HOST 3306; do
  sleep 0.1
done

echo "Connected to MariaDB Server"
exec $cmd

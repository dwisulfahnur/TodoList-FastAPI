#!/bin/sh

cmd="$@"


echo "Waiting for MariaDB Server..."
until mysql -u "root" -proot -h "$DB_HOST" -e "\q"; do
  sleep 2
done

echo "Connected to MariaDB Server"
exec $cmd

#!/bin/sh

cmd="$@"


echo "Waiting for MariaDB Server..."
until mysql -p"$MYSQL_ROOT_PASSWORD" -h "$DB_HOST" -u "root" -e "\q"; do
  sleep 2
done

echo "Connected to MariaDB Server"
exec $cmd

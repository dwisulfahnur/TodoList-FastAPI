#!/bin/sh

cmd="$@"


until mysql -u "root" -p"$MYSQL_ROOT_PASSWORD" -h "$DB_HOST"; do
  sleep 2
done

>&2 echo "MariaDB is up - executing command"
exec $cmd
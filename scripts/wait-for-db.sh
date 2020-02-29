#!/bin/sh


cmd="$@"

echo "Waiting for MariaDB Server..."
sleep 30

echo "Connected to MariaDB Server"
exec $cmd

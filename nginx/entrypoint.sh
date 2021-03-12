#!/bin/bash

echo "------ STARTING WITH CONFIG ------"
echo "APP_NAME=lift-pass"
echo "STAGE=${STAGE}"
echo "PORT=${PORT}"
echo "AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}"
echo "AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}"
echo "AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION}"

echo
echo

touch /app/logs/gunicorn.log
touch /app/logs/access.log
tail -n 0 -f /app/logs/*.log &

cd /app

exec gunicorn app:app \
    --name flaskapp \
    --bind 0.0.0.0:5000 \
    --worker-class gevent \
    --workers 5 \
    --timeout 90 \
    --log-level=info \
    --log-file=/app/logs/gunicorn.log \
    --access-logfile=/app/logs/access.log &

exec /usr/bin/supervisord
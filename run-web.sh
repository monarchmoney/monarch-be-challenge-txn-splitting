#!/bin/bash
DEVELOP=${DEVELOP:-1}
AUTORELOAD=${AUTORELOAD:-1}
PORT=${PORT:-8000}

if [ -f /.dockerenv ]; then
  # only do this stuff if running in Docker
  until psql -c "select 1" > /dev/null 2>&1; do
    echo "Waiting for Postgres server to start up..."
    sleep 1
  done

  if [ "$( psql -tAc "SELECT 1 FROM pg_database WHERE datname='monarch'" )" != '1' ];
  then
    echo "Database does not exist, creating 'monarch'"
    createdb monarch
    ./manage.py migrate
  fi
fi

while true; do
  echo "Starting development server (autoreload=$AUTORELOAD)"
  if [[ $AUTORELOAD == "1" ]]; then
    # echo "Running Django with watchdog"
    watchmedo auto-restart -d . -p'*.py' --recursive -- ./manage.py runserver 0.0.0.0:${PORT} --noreload
    # ./manage.py runserver 0.0.0.0:${PORT}
  else
    ./manage.py runserver 0.0.0.0:${PORT} --noreload
  fi
  echo "Server exited with code $?.. restarting in a few seconds..."
  sleep 2
done

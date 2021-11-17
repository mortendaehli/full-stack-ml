#!/usr/bin/env sh

# Wait until the service is ready before continuing.
# This is to ensure that the service is initialized before the API tries to connect.
service_is_ready() {
    NAME=$1
    HOST=$2
    DB_PORT=$3
    # echo "Using service $NAME: $HOST:$PORT"
    i=1
    while ! nc -z $HOST $DB_PORT; do
        sleep 1
        i=$((i+1));
        if [ $i -eq 600 ]; then
            echo "Service $NAME '$HOST:$DB_PORT' not responding. Exiting..."
            exit 1
        fi;
    done
}

if [ -n "$DB_HOST" ]; then
  service_is_ready "DATABASE" ${DB_HOST} ${DB_PORT}
fi


if [ "$1" = 'api' ]; then
  OLD_PYTHONPATH=$PYTHONPATH
  export PYTHONPATH=$PYTHONPATH:/code
  alembic upgrade head
  alembic_exit=$?
  if [ $alembic_exit -ne 0 ]; then
      echo "Alembic migrations failed"
      exit $alembic_exit
  fi
  export PYTHONPATH=$OLD_PYTHONPATH

  if [ ENVIRONMENT != "development" ]; then
    python scripts/pre_start.py
    python scripts/initial_data.py
    python scripts/export_openapi.py
    uvicorn app.main:app --reload --host 0.0.0.0 --port ${PORT:-8888} --log-level debug
    exit $?
  fi

  python app/main.py
  exit $?
fi

if [ "$1" = 'alembic' ]; then
  export PYTHONPATH=$PYTHONPATH:/code
fi

if [ "$1" = 'poetry' ]; then
  export PYTHONPATH=$PYTHONPATH:/code
fi

if [ "$1" = 'python' ]; then
  export PYTHONPATH=$PYTHONPATH:/code
fi

if [ "$1" = 'celery' ]; then
  export PYTHONPATH=$PYTHONPATH:/code
  celery --app=app.worker worker -l INFO -Q main-queue -c 1
fi

exec "$@"

#!/bin/bash -e

CMD=$1
shift 1
ARGS=$@

case $CMD in
    '' | sh | bash) exec bash;;
    msgrepo-api) exec gunicorn -b :80 -w 4 -t 300 msgrepo.wsgi:app;;
    msgrepo-beat) exec python -m msgrepo.beat;;
    msgrepo-worker) exec python -m msgrepo.worker;;
    web-api) exec uvicorn webapi.main:app --host 0.0.0.0 --port 49960 --workers 4 --reload;;
    login-api) exec uvicorn loginApi.main:app --host 0.0.0.0 --port 54393 --workers 4 --reload;;
    params-api) exec uvicorn paramsApi.main:app --host 0.0.0.0 --port 49964 --workers 4 --reload;;
    listenning-api) exec uvicorn listenningApi.main:app --host 0.0.0.0 --port 49966 --workers 4 --reload;;
    lepus-beat) exec python -m lepus.beat;;
    lepus-worker) exec python -m lepus.worker;;
    console-api) exec gunicorn -b :80 -w 4 -t 60 console.wsgi:app;;
    *) echo "unknown command: $CMD";;
esac
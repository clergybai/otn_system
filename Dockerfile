FROM python:3.11

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY deploy/image/entrypoint.sh /app/entrypoint.sh
# Fix for dos '\r\n' -> '\n'
RUN ["sed", "-i", "s/\r$//g", "/app/entrypoint.sh"]
ENTRYPOINT ["/app/entrypoint.sh"]
CMD bash

COPY common /app/common
COPY listenningApi /app/listenningApi
COPY loginApi /app/loginApi
COPY paramsApi /app/paramsApi
COPY webapi /app/webapi
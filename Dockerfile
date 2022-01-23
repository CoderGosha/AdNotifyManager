FROM python:3 AS runtime
WORKDIR /app
COPY . .
RUN dir /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt clean && apt update --allow-insecure-repositories && apt install -y netcat
RUN apt install python3-psycopg2
RUN pip3 install -r requirements.txt
RUN chmod +x /app/docker-entrypoint.sh


ENTRYPOINT ["/app/docker-entrypoint.sh"]

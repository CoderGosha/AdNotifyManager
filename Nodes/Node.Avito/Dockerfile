FROM python:3 AS runtime
WORKDIR /app
COPY Node/Node.Avito /app
RUN dir /app

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "app.py"]

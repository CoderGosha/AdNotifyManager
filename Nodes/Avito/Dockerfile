FROM ubuntu AS runtime
WORKDIR /app
COPY . .

RUN apt update
RUN apt install -y firefox
RUN apt install -y python3 python3-pip libcurl4-openssl-dev libssl-dev
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "app.py"]

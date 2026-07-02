FROM python:3.8-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc default-libmysqlclient-dev pkg-config

COPY . .

RUN pip install flask mysqlclient

EXPOSE 5002

CMD ["python", "app.py"]

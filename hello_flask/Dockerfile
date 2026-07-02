FROM python:3.8-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc default-libmysqlclient-dev pkg-config

COPY . .

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libmariadb-dev \
    pkg-config

RUN pip install flask mysqlclient

EXPOSE 5002

CMD ["python", "app.py"]
RUN pip install flask mysqlclient

EXPOSE 5002

CMD ["python", "app.py"]

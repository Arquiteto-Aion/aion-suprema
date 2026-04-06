FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl wget git \
    && rm -rf /var/lib/apt/lists/*

RUN pip install flask geocoder requests

COPY . .

EXPOSE 5000

CMD ["python", "aion_completo.py"]

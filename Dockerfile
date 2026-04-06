FROM python:3.10-slim
WORKDIR /app
RUN pip install flask geocoder requests
COPY . .
EXPOSE 5000
CMD ["python", "aion_server_completo.py"

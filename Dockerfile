FROM python:3.10-slim
WORKDIR /app
RUN pip install flask
COPY aion_server_completo.py .
EXPOSE 5000
CMD ["python", "aion_server_completo.py"]

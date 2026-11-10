FROM python:3.12-slim
WORKDIR /app
COPY puente.py .
ENV PYTHONUNBUFFERED=1
VOLUME ["/data"]
EXPOSE 8080
CMD ["python", "puente.py"]

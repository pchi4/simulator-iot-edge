FROM python:3.11-slim
WORKDIR /app
COPY result_logger.py /app/
RUN pip install --no-cache-dir paho-mqtt
ENV MQTT_BROKER=mosquitto
ENV MQTT_PORT=1883
CMD ["python", "result_logger.py"]

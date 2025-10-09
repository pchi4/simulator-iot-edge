FROM python:3.11-slim
WORKDIR /app
COPY edge_processor.py /app/
COPY model /app/model
RUN pip install --no-cache-dir paho-mqtt numpy
ENV MQTT_BROKER=mosquitto
ENV MQTT_PORT=1883
CMD ["python", "edge_processor.py"]

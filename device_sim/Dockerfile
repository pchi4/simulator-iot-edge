FROM python:3.11-slim
WORKDIR /app
COPY device_simulator.py /app/
RUN pip install --no-cache-dir paho-mqtt numpy
ENV MQTT_BROKER=mosquitto
ENV MQTT_PORT=1883
CMD ["python", "device_simulator.py"]

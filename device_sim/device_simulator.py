import os
import time
import json
import uuid
import random
import socket
import paho.mqtt.client as mqtt


# BROKER = os.getenv("MQTT_BROKER", "mosquitto")
# PORT = int(os.getenv("MQTT_PORT", "1883"))

# # Each container instance will have a unique ID.
# # When using docker-compose scaling, you can also set DEVICE_ID via env.
DEVICE_ID = os.getenv("DEVICE_ID", f"device-{uuid.uuid4().hex[:8]}")
# CLIENT_ID = f"sim-{DEVICE_ID}"


BROKER = "mosquitto"
PORT = 1883
CLIENT_ID = "device-simulator"

topic = f"devices/{DEVICE_ID}/telemetry"



def connect_mqtt():
    try:
        client = mqtt.Client(
            client_id=CLIENT_ID,
            protocol=mqtt.MQTTv311,
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2
        )

        def on_connect(client, userdata, flags, rc, properties=None):
            if rc == 0:
                print(f"[simulator] ✅ Conectado ao broker como {CLIENT_ID}")
            else:
                print(f"[simulator] ❌ Falha na conexão. Código: {rc}")

        client.on_connect = on_connect
        client.connect(BROKER, PORT)
        return client  # 👈 ESSENCIAL!
    except Exception as e:
        print(f"[simulator] ❌ Erro ao conectar MQTT: {e}")
        return None


def generate_payload():
    ts = int(time.time())
    temperature = 20 + random.gauss(0, 2) + (random.random() * 5)
    humidity = 50 + random.gauss(0, 5)
    vibration = abs(random.gauss(0, 0.5))
    if random.random() < 0.02:
        temperature += random.uniform(15, 30)
        vibration += random.uniform(2, 5)
    payload = {
        "device_id": DEVICE_ID,
        "timestamp": ts,
        "sensors": {
            "temperature": round(temperature, 3),
            "humidity": round(humidity, 3),
            "vibration": round(vibration, 3)
        }
    }
    return payload

def main():
    client = connect_mqtt()
    client.loop_start()
    print(f"[simulator] starting {DEVICE_ID} -> {topic} @ {BROKER}:{PORT}")
    try:
        while True:
            payload = generate_payload()
            client.publish(topic, json.dumps(payload), qos=0)
            time.sleep(random.uniform(0.5, 2.0))
    except KeyboardInterrupt:
        pass
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()

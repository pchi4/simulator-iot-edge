import os
import json
import time
from math import exp
import numpy as np
from paho.mqtt import client as mqtt

BROKER = os.getenv("MQTT_BROKER", "mosquitto")
PORT = int(os.getenv("MQTT_PORT", "1883"))
MODEL_PATH = os.getenv("MODEL_PATH", "/app/model/model.json")

def load_model(path):
    with open(path, 'r') as f:
        return json.load(f)

model = load_model(MODEL_PATH)
weights = model['weights']
bias = model['bias']
threshold = model.get('threshold', 0.5)

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

def inference(sensors):
    # linear score
    score = sensors['temperature']*weights['temperature'] + \
            sensors['humidity']*weights['humidity'] + \
            sensors['vibration']*weights['vibration'] + bias
    prob = sigmoid(score)
    is_anomaly = prob >= threshold
    return {"prob": float(prob), "anomaly": bool(is_anomaly), "score": float(score)}

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload)
        sensors = payload.get('sensors', {})
        result = inference(sensors)
        output = {
            "device_id": payload.get("device_id"),
            "timestamp": int(time.time()),
            "inference": result,
            "raw": payload
        }
        # publish results to a topic for loggers / actuators
        client.publish(f"edge/results/{payload.get('device_id')}", json.dumps(output))
        print("[edge] inferenced:", output)
    except Exception as e:
        print("Error processing message:", e)

def main():
    client = mqtt.Client(client_id="edge-processor", callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    client.connect(BROKER, PORT)
    client.on_message = on_message
    client.loop_start()
    # subscribe to all devices
    client.subscribe("devices/+/telemetry")
    print("[edge] subscribed to devices/+/telemetry")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()

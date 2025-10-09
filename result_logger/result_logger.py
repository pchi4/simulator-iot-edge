import os
import json
import time
import paho.mqtt.client as mqtt

BROKER = os.getenv("MQTT_BROKER", "mosquitto")
PORT = int(os.getenv("MQTT_PORT", "1883"))

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload)
        # Aqui apenas registramos no console, mas poderia salvar em DB, enviar HTTP, etc.
        print("[logger] received result:", json.dumps(payload))
    except Exception as e:
        print("[logger] error:", e)

def main():
    # ✅ versão atualizada para MQTT 2.0+
    client = mqtt.Client(
    client_id="result-logger",
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2
    )

    # Opcional: logging de conexão
    def on_connect(client, userdata, flags, rc, properties=None):
        if rc == 0:
            print(f"[logger] Connected to {BROKER}:{PORT} ✅")
        else:
            print(f"[logger] Connection failed with code {rc}")

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER, PORT)
    client.loop_start()
    client.subscribe("edge/results/+")
    print("[logger] subscribed to edge/results/+")

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

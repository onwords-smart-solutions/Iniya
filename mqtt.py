
import paho.mqtt.client as mqtt
def publish(topic, msg):
        BROKER = "mqtt.onwords.in"
        PORT = 1883
        USERNAME = 'Navin'
        PASSWORD = 'Navi@1405'
        client = mqtt.Client()
        client.username_pw_set(USERNAME, PASSWORD)
        client.connect(BROKER, PORT, keepalive=60)
        client.publish(topic, msg)
        client.disconnect()

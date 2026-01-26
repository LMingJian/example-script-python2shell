import time
from paho.mqtt import client as mqtt_client

broker = '192.168.1.230'
port = 1883
topic = "python/mqtt"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-publish'
username = 'python'
password = None


def on_connect(client, userdata, flags, rc):  # noqa
    if rc == 0:
        print(f"Connected to {broker} MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)


def connect_mqtt():
    client = mqtt_client.Client(client_id=client_id)
    # client.tls_set(ca_certs='./server-ca.crt')
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 0
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    temp = input('请输入 MQTT 服务器地址：')
    if temp:
        broker = temp
    run()

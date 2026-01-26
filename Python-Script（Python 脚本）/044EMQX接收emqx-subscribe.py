from paho.mqtt import client as mqtt_client

broker = '192.168.1.230'
port = 1883
topic = [
    "python/mqtt",
]
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-subscribe'
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


def on_message(client, userdata, msg):  # noqa
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")


def subscribe(client):
    for each in topic:
        client.subscribe(each)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    temp = input('请输入 MQTT 服务器地址：')
    if temp:
        broker = temp
    run()

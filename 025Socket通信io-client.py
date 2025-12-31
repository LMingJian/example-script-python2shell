import time

import socketio

sio = socketio.Client()


@sio.event
def connect():
    print('connection established')


@sio.event
def disconnect():
    print('disconnected from server')


@sio.event
def message(data):
    # 由 send 发出的默认事件
    print('message received with ', data)


def message_handler(msg):
    print('Received message: ', msg)
    sio.send('OK')


sio.on('user', message_handler)
"""
使用 on 绑定事件，相当于下面这个
@sio.on('my_event')
def my_event(data):
    print('Received data: ', data)
"""
sio.connect('http://localhost:5000')
time.sleep(5)
sio.send('Hello')
# send 默认为 message 事件
time.sleep(2)
sio.send('Welcome')
time.sleep(2)
sio.emit("user", {"user": "admin"})
# 若使用 emit 则需填写事件名称
sio.wait()
# sio.disconnect()

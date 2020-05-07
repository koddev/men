import socketio



try:

    sio = socketio.Client()
    sio.connect('http://62.244.197.146:5551')
    

    sio.emit('frreq', {'img': 'bar'})
    # sio.disconnect()
except Exception as e:
    print(e)



@sio.event
def message(data):
    print('I received a message!')

@sio.on('frres')
def on_message(data):
    print(data)
    
@sio.event
def connect():
    print("I'm connected!")

@sio.event
def connect_error():
    print("The connection failed!")

@sio.event
def disconnect():
    print("I'm disconnected!")
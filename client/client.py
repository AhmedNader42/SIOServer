import socketio
import numpy as np
import cv2
import base64
import random
import time


sio = socketio.Client()
@sio.event
def connect():
    print("I'm connected!")

@sio.event
def connect_error():
    print("The connection failed!")

@sio.event
def disconnect():
    print("I'm disconnected!")

@sio.on('movement')
def movement(data):
    if data == "F":
        print("Move Forward")
    elif data == "B":
        print("Move Backward")
    elif data == "L":
        print("Move Left")
    elif data == "R":
        print("Move Right")
    else:
        print("Unknown Movement")

sio.connect('http://192.168.1.16:4200')


# State of the robot at the current time (Should be kept updated to be sent to the client)
errorMode = False

sio.emit('state', { "error_mode" : errorMode})

def sendError():
    sio.emit('error', errorMode)

# sendError()
# while True:
#     time.sleep(2.0)
#     errorMode =  not errorMode
#     sendError()



def sendLocation_Speed(lat, lon, speed):
    sio.emit('location', {"lat": lat, "lon": lon})
    sio.emit('speed', speed)
# sendLocation()    

def sendCamera():
    cap = cv2.VideoCapture(0)
    cap.set(3,300)
    cap.set(4,300)
    lat = 30.0444
    lon = 31.2357
    speed = 10


    while(True) :
        lat += 0.000001
        lon += 0.000001
        speed += 0.001

        ret, frame = cap.read()
        # cv2.imshow('frame', frame)
        state, image = cv2.imencode('.png', frame)
        encondedImage = base64.b64encode(image)
        # print(encondedImage)
        sio.emit('video', {'image': encondedImage})
        sendLocation_Speed(lat, lon, speed)
        # print("Sent")
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

sendCamera()





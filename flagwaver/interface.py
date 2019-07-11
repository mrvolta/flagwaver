from flask import Flask, jsonify, render_template, request
import time
import serial
import sys
import glob
import json
from decimal import Decimal
from threading import Lock
from flask import Flask, render_template, session, request, \
    copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
import math
import random
import requests
from flagwaver.arduino import *
from flagwaver.vector_math import *

async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()
# import logging
# log = logging.getLogger('werkzeug')
# log.disabled = True
# app.logger.disabled = True



class interface:

    def __init__(self):
        thread = None
        thread_lock = Lock()

    @classmethod
    def initiate(self):
        socketio.run(app, port=5000, debug=True, host='0.0.0.0')

    #ser = serial.Serial()
    #ser.baudrate = 115200
    #ser.port = '\\\\.\\COM11' #'\\\\.\\' + 
    #ser.timeout = 3
    #print(ser.port)

    def send_to_interface(msg, type):
        if type == "ports":
            socketio.emit('my_ports',
                          {'data': msg, 'count': 1},
                          namespace='/test')
            print("done1")
            print(msg)
            socketio.sleep(0.1)
        else:
            if type == "serials":
                socketio.emit('my_response',
                          {'data': msg, 'count': 1},
                          namespace='/test')
                socketio.sleep(10)

        print("done")

    def background_thread():
        """Example of how to send server generated events to clients."""
        #ser.open()
        s = []
        while True:
            socketio.sleep(0.1)
            #arduino.check_serial_connection()
            #arduino.connect_to_serial(arduino.serial_ports()[0],115200)
            #send_to_interface(arduino.serial_ports(),"ports")
            #MainLoop()
            try:
                if arduino.check_serial_connection() != True:
                    try:
                        serials = arduino.serial_ports()
                        #arduino.connect_to_serial(serials[0],115200)
                        if s != serials:
                            interface.send_to_interface(serials,"ports")
                            s = serials
                    except:
                        print('error gamed')
                        continue
                    
                    #arduino.open_serial()
                #print(ser.timeout)
                #out = ser.readline(100)
                #print(out)
                count = arduino.read_serial_data()
                if count != '':
                    c = 0
                    socketio.emit('my_response',
                          {'data': count, 'count': 1},
                          namespace='/test')

                    #Resultant Calculations
                    readings = eval(count[1:])
                    direction = count[0:1]
                    S1 = readings[0]
                    S2 = readings[1]
                    S3 = readings[2]
                    S4 = readings[3]
                    print(readings)
                    V = np.array([[-90,0],[S1,S1],[S2,-S2],[-S3,-S3], [-S4,S4]])

                    V_u = unit_vector(V)

                    v12 = V_u[1] + V_u[2] + V_u[3] + V_u[4]
                    flag_angle = math.degrees(angle_between(v12,V[0]))
                    if (v12[0] < 0) and (v12[1] < 0):
                        flag_angle = 360 - flag_angle
                    if (v12[0] > 0) and (v12[1] < 0):
                        flag_angle = 360 - flag_angle
                    speed = length(v12) * 130

                    speed = round(speed, 2)
                    flag_angle = round(flag_angle, 2)
                    print("Speed: " + str(speed))
                    print("Angle: " + str(flag_angle))
                    print("-------------------")

                    ko = str("Speed: " + str(speed) + ", Angle: " + str(flag_angle) + "---------------------")
                    socketio.emit('my_response',
                          {'data': ko, 'count': 1},
                          namespace='/test')
                    socketio.emit('my_angle',
                          {'data': flag_angle, 'count': 1},
                          namespace='/test')
                    socketio.emit('my_speed',
                          {'data': speed, 'count': 1},
                          namespace='/test')
                else:
                    c += 1
                    if c == 2:
                        arduino.close_serial()
                        print('disconnected')
                        socketio.emit('my_angle',
                                {'data': 0, 'count': 1},
                          namespace='/test')
                        socketio.emit('my_speed',
                                {'data': 0, 'count': 1},
                          namespace='/test')
                        socketio.emit('my_disconnect',
                                {'data': 1, 'count': 1},
                          namespace='/test')
            except serial.serialutil.SerialException:
                print('error')
                # interface.socketio.emit('my_response',
                #           {'data': 'No Serial Available', 'count': 1},
                #           namespace='/test')
                interface.send_to_interface('No Connection Established',"serials")
                socketio.emit('my_angle',
                        {'data': 0, 'count': 1},
                  namespace='/test')
                socketio.emit('my_speed',
                        {'data': 0, 'count': 1},
                  namespace='/test')
        #print('koko')
        #ser.close()



    def check_internet():
        url='http://www.google.com/'
        timeout=5
        try:
            _ = requests.get(url, timeout=timeout)
            return True
        except requests.ConnectionError:
            print("No Internet")
        return False

    serials = []


    #if __name__ == '__main__':
       #app.run(port=5000, debug=True, host='0.0.0.0')
    #   socketio.run(app, port=5000, debug=True, host='0.0.0.0')

@app.route("/")
def main():
    a = bytearray.fromhex("427920536865726966205261736877616e").decode()
    return render_template('main.html', n=a, reload = time.time(), async_mode=socketio.async_mode)

@app.route("/api/info")
def api_info():
    info = {
       "ip" : "127.0.0.1",
       "hostname" : "everest",
       "description" : "Main server",
       "load" : [ 3.21, 7, 14 ]
    }
    return jsonify(info)


@app.route("/api/calc")
def add():
    #if ser.isOpen() != True :
    #  ser.open()
    #out = ser.read()
    # let's wait one second before reading output (let's give device time to answer)
    #out = ''
    #ser.isOpen()
    #ser.open()
    #ser.flushInput()
    #ser_bytes = ser.readline()
    
    #decoded_bytes = ser_bytes[0:len(ser_bytes)-2].decode("utf-8")
    #out = out + "," + decoded_bytes
    #ser.close()
    out = b''
    #time.sleep(1)
    #out = ser.readline()
    # let's wait one second before reading output (let's give device time to answer)
    
    #while ser.inWaiting() > 0:
    #  out += ser.read(1)
    #p = out.decode()  
    #if p != '':
        #s = p
    serials = arduino.serial_ports()
    p = ''
    a = request.args.get('a', 0)
    print("Connecting to " + a)
    arduino.connect_to_serial(a,115200)
    b = serials#json.dumps(serials, ensure_ascii=False)
    #s = out
    div = 'na'
    # if b != 0:
    #     div = a/b
    return jsonify({
        "a"        :  a,
        "b"        :  b,
        "add"      :  a,
        "multiply" :  a,
        "subtract" :  a,
        "divide"   :  a,
        "Serial"   :  p,
    })

@app.route("/api/disconnect")
def disconnect_serial():
    #if ser.isOpen() != True :
    #  ser.open()
    #out = ser.read()
    # let's wait one second before reading output (let's give device time to answer)
    #out = ''
    #ser.isOpen()
    #ser.open()
    #ser.flushInput()
    #ser_bytes = ser.readline()
    
    #decoded_bytes = ser_bytes[0:len(ser_bytes)-2].decode("utf-8")
    #out = out + "," + decoded_bytes
    #ser.close()
    out = b''
    #time.sleep(1)
    #out = ser.readline()
    # let's wait one second before reading output (let's give device time to answer)
    
    #while ser.inWaiting() > 0:
    #  out += ser.read(1)
    #p = out.decode()  
    #if p != '':
        #s = p
    #serials = arduino.serial_ports()
    p = ''
    a = '' #request.args.get('a', 0)
    print("Disconnecting.....")
    if arduino.close_serial() == True:
        b = 'diconnected'#json.dumps(serials, ensure_ascii=False)
    else:
        b = 'connected'
    #s = out
    div = 'na'
    # if b != 0:
    #     div = a/b
    return jsonify({
        "a"        :  a,
        "b"        :  b,
        "add"      :  a,
        "multiply" :  a,
        "subtract" :  a,
        "divide"   :  a,
        "Serial"   :  p,
    })

@socketio.on('my_event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})


@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()

    session['receive_count'] = session.get('receive_count', 0) + 1
    # for this emit we use a callback function
    # when the callback function is invoked we know that the message has been
    # received and it is safe to disconnect
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']},
         callback=can_disconnect)


@socketio.on('my_ping', namespace='/test')
def ping_pong():
    emit('my_pong')


@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(interface.background_thread)
    emit('my_response', {'data': 'Initiating WebSocket', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)

#if __name__ == '__main__':
   #app.run(port=5000, debug=True, host='0.0.0.0')
#   socketio.run(app, port=5000, debug=True, host='0.0.0.0')

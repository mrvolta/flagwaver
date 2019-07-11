from flagwaver.vector_math import *
from flagwaver.arduino import *
from flagwaver.interface import *

count = 0
c = 0

def run():
    serials = arduino.serial_ports()
    #print(serials)
    if len(serials) > 0:
        interface.initiate()
        send_to_interface(serials,"ports")
    else:
        print("Please connect your arduino and try again")

if __name__ == '__main__':
    #interface = interface()
    #arduino = arduino()
    run()
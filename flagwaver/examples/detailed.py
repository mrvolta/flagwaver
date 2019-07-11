from flagwaver import flagwaver
import time

def run():
	while True:
	    serials = flagwaver.arduino.serial_ports()
	    #print(serials)
	    if len(serials) > 0:
	        #flagwaver.interface.send_to_interface(serials,"ports")
	        flagwaver.interface.initiate()
	    else:
	        print("Please connect your arduino and try again")
	        time.sleep(2)


if __name__ == '__main__':
    run()
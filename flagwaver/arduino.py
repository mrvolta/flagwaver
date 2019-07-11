import serial
import sys

class arduino:
	#Get available serial ports and return an array "result"
	@classmethod
	def serial_ports(self):
	    if sys.platform.startswith('win'):
	        ports = ['COM%s' % (i + 1) for i in range(256)]
	    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
	        # this excludes your current terminal "/dev/tty"
	        ports = glob.glob('/dev/tty[A-Za-z]*')
	    elif sys.platform.startswith('darwin'):
	        ports = glob.glob('/dev/tty.*')
	    else:
	        raise EnvironmentError('Unsupported platform')

	    result = []
	    for port in ports:
	        try:
	            s = serial.Serial(port)
	            s.close()
	            result.append(port)
	        except (OSError, serial.SerialException):
	            pass
	    return result

	#Initialize serial object globally
	global ser
	ser = serial.Serial()

	#Function to initialize serial object
	#def initialize_serial():
	#	ser = serial.Serial()
	@classmethod
	def open_serial(self):
		ser.open()
	#Check if the serial connection is open or closed, return true if open , False if closed
	def check_serial_connection():
		if ser.isOpen() == True:
			return True
		else:
			return False

	#
	def connect_to_serial(port, speed):

	    #ser = serial.Serial()
	    ser.baudrate = 115200
	    ser.port = '\\\\.\\' + port#arduino.serial_ports()[0]#'\\\\.\\' + 
	    ser.timeout = 3
	    arduino.open_serial()
	    print(ser.port)
	    return True

	def connect_to_arduino(port, speed):
	    if arduino.connect_to_serial(port,speed) == True:
	        return True
	    else:
	        return False

	def read_serial_data():
	    output_bytes = ser.readline(100)
	    print(output_bytes)
	    decoded_output = output_bytes.decode()
	    return decoded_output

	def close_serial():
		ser.close()
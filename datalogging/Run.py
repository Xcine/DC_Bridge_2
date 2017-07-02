import sys
sys.path.insert(0, '/Users/Georg/micropython/tools')
sys.path.insert(0, '/Users/Georg/micropython')
import pyboard
import serial

def main():
	#pyb1 = pyboard.Pyboard('/dev/tty.usbmodem1412')
	#pyb1.enter_raw_repl()
	#pyb1.exec('print("Hallo")')
	#pyb1.follow()
	#pyb1.exec('printsome()')
	#pyb1.exec("import pyb")
	#pyb1.exec("pyb.LED(3).toggle()")
	#pyb1.exec("pyb.delay(1000)")
	#pyb1.exec("pyb.LED(3).toggle()")
	#pyb1.exit_raw_repl()
	#pyb1.close()

	#pyboard.execfile("test.py", device = "/dev/tty.usbmodem1412")

	#port = '/dev/tty.usbmodem1412'
	#print('Opening serial port {}'.format(port))
	#serial_port = serial.Serial(port=port)
	#line = pyb1.serial.readline().strip()
	#print(line)
	#print(int(line)+1)
	#pyb1.close()

	pyb1 = pyboard.Pyboard(device = "/dev/tty.usbmodem1412")
	pyb1.enter_raw_repl()
	output = pyb1.execfile("test.py")
	pyboard.stdout_write_bytes(output)
	pyb1.exit_raw_repl()
	pyb1.close()

	print("_______________")
	sys.stdout.buffer.write(output)

if __name__ == '__main__':
    main()
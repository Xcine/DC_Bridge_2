import sys
sys.path.insert(0, '/Users/Georg/micropython/tools')
sys.path.insert(0, '/Users/Georg/micropython')
import pyboard
import serial

def main():
	#pyboard.execfile("test.py", device = "/dev/tty.usbmodem1412")
	port = '/dev/tty.usbmodem1412'

	print('Opening serial port {}'.format(port))
	serial_port = serial.Serial(port=port)

	line = serial_port.readline().strip()
	print(line)
	print(int(line)+1)

	"""
    pyb = pyboard.Pyboard('/dev/tty.usbmodem1412')
    pyb.enter_raw_repl()
    pyb.exec('import pyb')
    pyb.exec('sw = pyb.Switch()')
    pyb.exec('sw.callback(lambda:print('press!'))')
    pyb.exec("sw()")
    pyb.exec('pyb.LED(1).on()')
    pyb.exec('print("Hallo")')
    pyb.exit_raw_repl()
	"""

if __name__ == '__main__':
    main()
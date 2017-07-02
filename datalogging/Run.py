import sys
sys.path.insert(0, '/Users/Georg/micropython/tools')
sys.path.insert(0, '/Users/Georg/micropython')
import pyboard
import serial

def main():
	pyb1 = pyboard.Pyboard(device = "/dev/tty.usbmodem1412")
	pyb1.enter_raw_repl()
	#output = pyb1.execfile("test.py")
	output = pyb1.exec_('print(1+1)')
	pyb1.exit_raw_repl()
	pyb1.close()
	print("_______________")
	print(output.decode("utf-8"))
	zahl = int(output.decode("utf-8"))
	print(zahl+51)

if __name__ == '__main__':
    main()
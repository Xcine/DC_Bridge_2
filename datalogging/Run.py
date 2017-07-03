import sys
sys.path.insert(0, '/Users/Georg/micropython/tools')
sys.path.insert(0, '/Users/Georg/micropython')
import pyboard
import serial
import numpy as np
import re

def string_to_array(input):
	all_ns = [m.start() for m in re.finditer('\n', input)]
	string_array = ["" for x in range(len(all_ns))]
	i = 0
	for x in range(len(all_ns)):
		string_array[x] = input[i:all_ns[x]]
		i = all_ns[x] + 1

	return string_array

def main():
	pyb1 = pyboard.Pyboard(device = "/dev/tty.usbmodem1412")
	pyb1.enter_raw_repl()
	#output = pyb1.execfile("test.py")
	output = pyb1.exec_('printres()')
	pyb1.exit_raw_repl()
	pyb1.close()
	print("_______________")
	output.decode("utf-8")
	#output_arr = string_to_array(output)
	res_values = re.findall(r"[-+]?\d*\.\d+|\d+", output)
	res_values = [float(x) for x in res_values]
	print(res_values)
	#zahl = int(output.decode("utf-8"))
	#print(zahl+51)

if __name__ == '__main__':
    main()
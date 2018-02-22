import sys
sys.path.insert(0, '/home/georg/Dokumente/Arbeit/micropython-master/tools')
sys.path.insert(0, '/home/georg/Dokumente/Arbeit/micropython-master')
import pyboard
#from serial import serial 
import numpy as np
import re
import matplotlib.pyplot as plt

def string_to_array(input):
	all_ns = [m.start() for m in re.finditer('\n', input)]
	string_array = ["" for x in range(len(all_ns))]
	i = 0
	for x in range(len(all_ns)):
		string_array[x] = input[i:all_ns[x]]
		i = all_ns[x] + 1

	return string_array

def main():
	#pyb1 = pyboard.Pyboard(device = "/dev/tty.usbmodem1412")
	pyb1 = pyboard.Pyboard(device = "/dev/ttyACM0")
	pyb1.enter_raw_repl()
	pyb1.exec_('from resistor import Resistor')
	pyb1.exec_('res = Resistor()')
	pyb1.exec_('res.set_resistor(3400)')
	value = float(pyb1.exec_('res.get_resistor_string()'))
	print(value)
	#pyb1.exec_('res.set_resistor(1500)')
	#pyb1.exit_raw_repl()
	#pyb1.close()
	#print("_______________")
	#output.decode("utf-8")
	#print(output)
	"""
	#output_arr = string_to_array(output)
	res_values = re.findall(r"[-+]?\d*\.\d+|\d+", output)
	res_values = [float(x) for x in res_values]
	print(res_values)
	vol_values = [x*1.5 for x in res_values]
	print(vol_values)
	plt.plot(res_values, vol_values)
	plt.show()
	#zahl = int(output.decode("utf-8"))
	#print(zahl+51)
	"""

if __name__ == '__main__':
	main()

#pyb1 = pyboard.Pyboard(device = "/dev/tty.usbmodem1412")
#pyb1.enter_raw_repl()
#pyb1.exec_('from resistor import Resistor')
#pyb1.exec_('res = Resistor()')
#pyb1.exec_('res.set_resistor(2000)')
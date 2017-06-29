from pyb import I2C

class Resistor(object):
	"""Class for editing the variable resistor.

	The Resistor class can find or set the next valid resistor on the chip.

	Attributes:
		all_resistors: list of all resistor packs

	"""

	def __init__(self, all_resistors=[1600, 800, 400, 200, 100, 50, 25, 12.5, 6.25, 3.125]):
		self.all_resistors = all_resistors
		self.current_resistor_binary = [1,1,1,1,1,1,1,1,1,1]
		self.i2c = I2C(2)
		self.i2c = I2C(2, I2C.MASTER)
		self.i2c.init(I2C.MASTER, baudrate=20000)
		info = self.i2c.scan()
		#print("scan ",info)

	def find_binary_resistor(self, input=1000.0):
		input -= 1000.0
		resistor_bin = [1,1,1,1,1,1,1,1,1,1]

		for x in range(10):
			if input >= self.all_resistors[x]:
				resistor_bin[x] = 0
				input -= self.all_resistors[x]
			else:
				pass

		return resistor_bin

	def set_resistor(self, input = 1000.0):

		if (type(input) == int) or (type(input) == float): 
			resistor_bin = self.find_binary_resistor(input)
			self.current_resistor_binary = resistor_bin
			binary2 = resistor_bin[2:]
			binary3 = resistor_bin[:2]
		elif (type(input) == list) and len(input) == 10:
			self.current_resistor_binary = input
			binary2 = input[2:]
			binary3 = input[:2]
		else:
			print("ERROR: wrong type oder length of array")

		data = bytearray([0x02,0x46,0xFF,0x03])
		data[2] = self.get_binary_of_list(binary2)
		data[3] = self.get_binary_of_list(binary3)

		print("setting resistor to", self.get_resistor(), "Ohm")
		self.i2c.send(data,96)

	def get_resistor(self):
		return (self.dot_prod(self.negate_binary_list(self.current_resistor_binary), self.all_resistors) + 1000.0)

	def find_resistor(self, input):
		return (self.dot_prod(self.negate_binary_list(self.find_binary_resistor(input)), self.all_resistors) + 1000.0)

	def get_binary_of_list(self, input):
		out = 0
		for bit in input:
			out = (out << 1) | bit

		return out

	def dot_prod(self, list1, list2):
		sum = 0
		for x in range(10):
			sum += (list1[x]*list2[x])

		return sum

	def negate_binary_list(self, input):
		dummy_list = [1,1,1,1,1,1,1,1,1,1]
		for x in range(10):
			dummy_list[x] = not input[x]

		return dummy_list





			
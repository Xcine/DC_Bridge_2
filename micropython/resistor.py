from pyb import I2C
import time
import lcd160cr

class Resistor(object):
	"""Class for editing the variable resistor.

	The Resistor class can find or set the next valid resistor on the chip.

	Attributes:
		all_resistors: list of all resistor packs
		current_resistor_binary: list of bits of the current set resistor
		i2c: i2c object
	"""

	def __init__(self, all_resistors=[1600, 800, 400, 200, 100, 50, 25, 12.5, 6.25, 3.125]):
		"""Inits Resistor class."""
		self.all_resistors = all_resistors
		self.current_resistor_binary = [1,1,1,1,1,1,1,1,1,1]
		self.current_resistor = (self.dot_prod(self.negate_binary_list(self.current_resistor_binary), self.all_resistors) + 1000.0)
		self.i2c = I2C(2)
		self.i2c = I2C(2, I2C.MASTER)
		self.i2c.init(I2C.MASTER, baudrate=20000)
		info = self.i2c.scan()
		#print("scan ",info)

		#LCD
		self.lcd = lcd160cr.LCD160CR('YX')
		self.lcd.set_orient(lcd160cr.LANDSCAPE)
		self.lcd.set_pos(30, 20)
		self.lcd.set_text_color(self.lcd.rgb(255, 255, 255), self.lcd.rgb(0, 0, 0))
		self.lcd.set_font(1,1,0,0,0)

		self.lcd.erase()
		self.lcd.set_pos(25, 60)
		self.lcd.write("0000.000Ω")

	def find_binary_resistor(self, input=1000.0):
		"""Finds the next valid resistor and returns the resistor as a list of bits."""
		input -= 1000.0
		resistor_bin = [1,1,1,1,1,1,1,1,1,1]

		for x in range(10):
			if input >= self.all_resistors[x]:
				resistor_bin[x] = 0
				input -= self.all_resistors[x]
			else:
				pass

		return resistor_bin

	def max_test(self, a):
		return a*a

	def set_resistor(self, input = 1000.0):
		"""Sets the next valid resistor in accordance to the input."""
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
			raise TypeError("ERROR: wrong type oder length of array")

		data = bytearray([0x02,0x46,0xFF,0x03])
		data[2] = self.get_binary_of_list(binary2)
		data[3] = self.get_binary_of_list(binary3)

		print("Setting resistor to", self.get_resistor(), "Ohm.")
		self.i2c.send(data,96)

		string = "%.3f" % self.get_resistor()
		self.lcd.set_pos(25, 60)
		self.lcd.write(string)

	def get_resistor(self):
		"""Returns the current set resistor(float)."""
		return self.current_resistor

	def get_resistor_string(self):
		"""Returns the current set resistor(float)."""
		#print(self.dot_prod(self.negate_binary_list(self.current_resistor_binary), self.all_resistors) + 1000.0)
		print(self.current_resistor)

	def find_resistor(self, input):
		"""Finds the next valid resistor(float)."""
		return (self.dot_prod(self.negate_binary_list(self.find_binary_resistor(input)), self.all_resistors) + 1000.0)

	def set_resistor_list(self, input, sleeptime=0.5):
		"""Runs through a list of resistor values in a specified sleeptime."""
		for x in input:
			self.set_resistor(x)
			time.sleep(sleeptime)

	def set_resistor_step(self, res1, res2, resistor_step=100.0, sleeptime=0.5):
		"""Starts with a resistor value and increases the resistor in a specified step
		till the second resistor value."""
		if res1 <= res2:
			if res1 < 1000.0:
				res1 = 1000.0
			if res2 > 4196.875:
				res2 = 4196.875
			while res1 <= res2:
				self.set_resistor(res1)
				res1 += resistor_step
				time.sleep(sleeptime)
		else:
			if res1 > 4196.875:
				res1 = 4196.875
			if res2 < 1000.0:
				res2 = 1000.0
			while res2 <= res1:
				self.set_resistor(res1)
				res1 -= resistor_step
				time.sleep(sleeptime)

	def get_binary_of_list(self, input):
		"""Returns the binary from of a list of bits."""
		out = 0
		for bit in input:
			out = (out << 1) | bit

		return out

	def dot_prod(self, list1, list2):
		"""Returns the dot product of two vectors."""
		sum = 0
		for x in range(10):
			sum += (list1[x]*list2[x])

		return sum

	def negate_binary_list(self, input):
		"""Negates a binary list."""
		dummy_list = [1,1,1,1,1,1,1,1,1,1]
		for x in range(10):
			dummy_list[x] = not input[x]

		return dummy_list
			
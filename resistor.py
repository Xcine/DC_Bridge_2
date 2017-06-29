#from numpy import dot
from pyb import I2C

class Resistor(object):

	def __init__(self, allResistors = [1600, 800, 400, 200, 100, 50, 25, 12.5, 6.25, 3.125]):
		self.allResistors = allResistors
		self.currenResistorBinary = [0,0,0,0,0,0,0,0,0,0]
		self.i2c = I2C(2)
		self.i2c = I2C(2, I2C.MASTER)
		self.i2c.init(I2C.MASTER, baudrate=20000)
		info = self.i2c.scan()
		print("scan ",info)

	def FindBinaryResistor(self, input = 1000.0):
		input -= 1000.0
		resistorBin = [0,0,0,0,0,0,0,0,0,0]

		for x in range(10):
			if input >= self.allResistors[x]:
				resistorBin[x] = 1
				input -= self.allResistors[x]
			else:
				pass

		return resistorBin

	def SetResistor(self, input = 1000.0):
		resistorBin = self.FindBinaryResistor(input)
		self.currenResistorBinary = resistorBin
		Bin1 = resistorBin[:2]
		Bin2 = resistorBin[2:]

		data = bytearray([0x02,0x46,0xFF,0x03])
		data[2] = self.GetBinaryOfList(Bin2)
		data[3] = self.GetBinaryOfList(Bin1)

		print("setting resistor to", self.GetResistor(), "Ohm")
		self.i2c.send(data,96)

	def GetResistor(self):
		return (self.dotProd(self.currenResistorBinary, self.allResistors) + 1000.0)

	def FindResistor(self, input):
		return (self.dotProd(self.FindBinaryResistor(input), self.allResistors) + 1000.0)

	def GetBinaryOfList(self, input):
		out = 0
		for bit in input:
			out = (out << 1) | bit

		return out

	def dotProd(self, list1, list2):
		sum = 0
		for x in range(10):
			sum += (list1[x]*list2[x])

		return sum






			
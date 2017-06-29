#from numpy import dot

class Resistor(object):

	def __init__(self, allResistors = [1600, 800, 400, 200, 100, 50, 25, 12.5, 6.25, 3.125]):
		self.allResistors = allResistors

	def GetResistor(self, input = 1000.0):
		input -= 1000.0
		resistorBin = [0,0,0,0,0,0,0,0,0,0]

		for x in range(10):
			if input >= self.allResistors[x]:
				resistorBin[x] = 1
				input -= self.allResistors[x]
			else:
				pass

		#print dot(resistorBin, self.allResistors) + 1000.0
		print resistorBin
		return resistorBin

	def SetResistor(self, input):
		resistorBin = self.GetResistor(input)
		Bin1 = resistorBin[:2]
		Bin2 = resistorBin[2:]

		data = bytearray([0x02,0x46,0xFF,0x03])
		data[2] = self.GetBinaryOfList(Bin2)
		data[3] = self.GetBinaryOfList(Bin1)

		#i2c.send(data,96)
		print data[2]
		print data[3]


	def GetBinaryOfList(self, input):
		out = 0
		for bit in input:
			out = (out << 1) | bit

		return out





			
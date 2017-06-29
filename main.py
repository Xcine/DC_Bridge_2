#from pyb import I2C
from resistor import Resistor
"""
i2c = I2C(2)
i2c = I2C(2, I2C.MASTER)
i2c.init(I2C.MASTER, baudrate=20000)
info = i2c.scan()
print("scan ",info)

import time
data = bytearray([0x02,0x46,0xFF,0x03])
w = 1
for i in range(10):
    w = w << 1
    data[2] = w & 0x0FF
    data[3] = (w & 0x300) >> 8
    i2c.send(data,96)
    time.sleep(1)


i2c.send(b'\x02F\x07\x02',96)
"""
res = Resistor()
#res.GetResistor(3000)
res.SetResistor(3000)

#from pyb import I2C
#ANSCHLUS LINKS (Seite des micro usbs), LCD Rechts
import pyb
import lcd160cr

from resistor import Resistor

res = Resistor()
res.set_resistor(3000.0)

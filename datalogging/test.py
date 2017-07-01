import pyb
import time

sw = pyb.Switch()
i = 0

while not sw():
	print(i)
	time.sleep(1)
	i += 1


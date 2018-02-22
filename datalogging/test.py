# coding: utf8
import matplotlib
matplotlib.use('TkAgg')

from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler


from matplotlib.figure import Figure

import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

import sys
sys.path.insert(0, '/home/georg/Dokumente/Arbeit/micropython-master/tools')
sys.path.insert(0, '/home/georg/Dokumente/Arbeit/micropython-master')
import pyboard
#from serial import serial
import numpy as np
import re
import matplotlib.pyplot as plt

root = Tk.Tk()
root.wm_title("Gleichstrombrücke")


f = Figure(figsize=(5, 4), dpi=100)
a = f.add_subplot(111)
t = arange(0.0, 20.0, 1.0)
s = []
a.set_ylim([0,4200])
a.set_xlim([0,100])
line1, = a.plot([],[],'r.')


#pyb1 = pyboard.Pyboard(device = "/dev/tty.usbmodem1412")
pyb1 = pyboard.Pyboard(device = "/dev/ttyACM0")
pyb1.enter_raw_repl()
#output = pyb1.execfile("test.py")
pyb1.exec_('import time')
pyb1.exec_('from resistor import Resistor')
pyb1.exec_('res = Resistor()')
value = 1000

def set_resistor_step(res1, res2, resistor_step=100.0, sleeptime=0.5):
    """Starts with a resistor value and increases the resistor in a specified step
    till the second resistor value."""
    if res1 <= res2:
        if res1 < 1000.0:
            res1 = 1000.0
        if res2 > 4196.875:
            res2 = 4196.875
        while res1 <= res2:
            pyb1.exec_('res.set_resistor(' + str(res1) + ')')
            res1 += resistor_step
            val = pyb1.exec_('res.get_resistor_string()')
            s.append(val)
            t = arange(0, len(s), 1.0)
            line1.set_ydata(s)
            line1.set_xdata(t)
            f.canvas.draw()
            pyb1.exec_('time.sleep(' + str(sleeptime) + ')')
    else:
        if res1 > 4196.875:
            res1 = 4196.875
        if res2 < 1000.0:
            res2 = 1000.0
        while res2 <= res1:
            pyb1.exec_('res.set_resistor(' + str(res1) + ')')
            res1 -= resistor_step
            time.sleep(sleeptime)



# a tk.DrawingArea
canvas = FigureCanvasTkAgg(f, master=root)
canvas.show()
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

toolbar = NavigationToolbar2TkAgg(canvas, root)
toolbar.update()
canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)


def on_key_event(event):
    print('you pressed %s' % event.key)
    key_press_handler(event, canvas, toolbar)

canvas.mpl_connect('key_press_event', on_key_event)


def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate


def change_res(value):
    pyb1.exec_('res.set_resistor(' + str(value) + ')')
    s.append(value)
    t = arange(0, len(s), 1.0)
    line1.set_ydata(s)
    line1.set_xdata(t)
    f.canvas.draw()

#buttonframe = Tk.Frame(root)
#buttonframe.grid(row=0, column=2, columnspan=2)    
button1 = Tk.Button(master=root, text='Change Res1', command=lambda: change_res(1000))
#button1.grid(row=0,column=0)
button1.pack(side=Tk.LEFT)
button2 = Tk.Button(master=root, text='Change Res2', command=lambda: change_res(2000))
#button2.grid(row=0,column=1)
button2.pack(side=Tk.LEFT)
button4 = Tk.Button(master=root, text='Change Resss', command=lambda: set_resistor_step(1000,4000))
#button2.grid(row=0,column=1)
button4.pack(side=Tk.LEFT)

button3 = Tk.Button(master=root, text='Quit', command=_quit)
#button3.grid(row=0,column=2)
button3.pack(side=Tk.LEFT)

Tk.mainloop()
# If you put root.destroy() here, it will cause an error if
# the window is closed with the window manager.
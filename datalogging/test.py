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
sys.path.insert(0, '/Users/Georg/micropython/tools')
sys.path.insert(0, '/Users/Georg/micropython')
import pyboard
import serial
import numpy as np
import re
import matplotlib.pyplot as plt

root = Tk.Tk()
root.wm_title("Gleichstrombrücke")


f = Figure(figsize=(5, 4), dpi=100)
a = f.add_subplot(111)
t = arange(0.0, 3.0, 0.01)
s = sin(2*pi*t)

a.plot(t, s)

pyb1 = pyboard.Pyboard(device = "/dev/tty.usbmodem1412")
pyb1.enter_raw_repl()
#output = pyb1.execfile("test.py")
pyb1.exec_('from resistor import Resistor')
pyb1.exec_('res = Resistor()')
value = 1000

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
    print(value)

button = Tk.Button(master=root, text='Change Res1', command=change_res(1000))
button.pack(side=Tk.BOTTOM)
button = Tk.Button(master=root, text='Change Res2', command=change_res(2000))
button.pack(side=Tk.BOTTOM)

button = Tk.Button(master=root, text='Quit', command=_quit)
button.pack(side=Tk.BOTTOM)

Tk.mainloop()
# If you put root.destroy() here, it will cause an error if
# the window is closed with the window manager.
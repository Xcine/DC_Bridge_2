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
#sys.path.insert(0, '/home/georg/Dokumente/Arbeit/micropython-master/tools')
#sys.path.insert(0, '/home/georg/Dokumente/Arbeit/micropython-master')
#import pyboard
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

"""
#pyb1 = pyboard.Pyboard(device = "/dev/tty.usbmodem1412")
pyb1 = pyboard.Pyboard(device = "/dev/ttyACM0")
pyb1.enter_raw_repl()
#output = pyb1.execfile("test.py")
pyb1.exec_('import time')
pyb1.exec_('from resistor import Resistor')
pyb1.exec_('res = Resistor()')
value = 1000

def set_resistor_step(res1, res2, resistor_step=100.0, sleeptime=0.5):
    #Starts with a resistor value and increases the resistor in a specified step
    #till the second resistor value.
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
"""


# a tk.DrawingArea
#draw_frame = Tk.Frame(root)
#draw_frame.grid(row=0,column=0)
canvas = FigureCanvasTkAgg(f, master=root)
canvas.show()
#canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
canvas.get_tk_widget().grid(row=0, column=0)

toolbar_frame = Tk.Frame(root)
toolbar_frame.grid(row=1,column=0)
toolbar = NavigationToolbar2TkAgg(canvas, toolbar_frame)
toolbar.update()
#canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
canvas._tkcanvas.grid(row=0, column=0)

def on_key_event(event):
    print('you pressed %s' % event.key)
    key_press_handler(event, canvas, toolbar)

canvas.mpl_connect('key_press_event', on_key_event)


def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate


def change_res(value):
    #pyb1.exec_('res.set_resistor(' + str(value) + ')')
    s.append(value)
    t = arange(0, len(s), 1.0)
    line1.set_ydata(s)
    line1.set_xdata(t)
    f.canvas.draw()

ia_frame = Tk.Frame(root)
ia_frame.grid(row=0, column=1, sticky=Tk.N)

info_frame = Tk.Frame(ia_frame, highlightthickness=10)
info_frame.grid(row=0, column=0, columnspan=4, sticky=Tk.N)
info_title = Tk.Label(master=info_frame, text="Momentane Messwerte:")
info_title.grid(row=0, column=0, columnspan=4, sticky=Tk.N)

info_res_label = Tk.Label(master=info_frame, text="R = ")
info_res_label.grid(row=1, column=0, sticky=Tk.N)
info_res_value = Tk.Label(master=info_frame, text="1000 Ohm")
info_res_value.grid(row=1, column=1, sticky=Tk.N)

info_u_label = Tk.Label(master=info_frame, text="U = ")
info_u_label.grid(row=1, column=2, sticky=Tk.N)
info_u_value = Tk.Label(master=info_frame, text="3.3 Volt")
info_u_value.grid(row=1, column=3, sticky=Tk.N)

graph_settings_frame = Tk.Frame(ia_frame, highlightthickness=10)
graph_settings_frame.grid(row=1, column=0, columnspan=4, sticky=Tk.N)
graph_settings_title = Tk.Label(master=graph_settings_frame, text="Graph Einstellungen:")
graph_settings_title.grid(row=0, column=0, columnspan=4, sticky=Tk.N)

button_graph_reset = Tk.Button(master=graph_settings_frame, text="Graph zurücksetzen", command=lambda: change_res(1000))
button_graph_reset.grid(row=1, column=0, columnspan=4, sticky=Tk.N)

button_graph_toggle = Tk.Button(master=graph_settings_frame, text="Starte Messung", command=lambda: change_res(1000))
button_graph_toggle.grid(row=2, column=0, columnspan=4, sticky=Tk.N)

button_graph_over_again = Tk.Button(master=graph_settings_frame, text="Starte Messung bei Null", command=lambda: change_res(1000))
button_graph_over_again.grid(row=3, column=0, columnspan=4, sticky=Tk.N)

graph_colors= Tk.Label(master=graph_settings_frame, text="Farbauswahl:")
graph_colors.grid(row=4, column=0, columnspan=4, sticky=Tk.N)
button_black = Tk.Button(master=graph_settings_frame, text="Schwarz", fg="black", command=lambda: change_res(1000))
button_black.grid(row=5, column=0, sticky=Tk.N)
button_blue = Tk.Button(master=graph_settings_frame, text="Blau", fg="blue", command=lambda: change_res(1000))
button_blue.grid(row=5, column=1, sticky=Tk.N)
button_red = Tk.Button(master=graph_settings_frame, text="Rot", fg="red", command=lambda: change_res(1000))
button_red.grid(row=5, column=2, sticky=Tk.N)
button_green = Tk.Button(master=graph_settings_frame, text="Grün", fg="green", command=lambda: change_res(1000))
button_green.grid(row=5, column=3, sticky=Tk.N)

res_settings_frame = Tk.Frame(ia_frame, highlightthickness=10)
res_settings_frame.grid(row=2, column=0, columnspan=4, sticky=Tk.N)
res_settings_title = Tk.Label(master=res_settings_frame, text="Widerstands Einstellungen:")
res_settings_title.grid(row=0, column=0, columnspan=4, sticky=Tk.N)

set_res_entry = Tk.Entry(master=res_settings_frame, text="z.B. 3000.25")
set_res_entry.grid(row=1, column=0, sticky=Tk.N)
set_res_entry_label = Tk.Label(master=res_settings_frame, text=" Ohm")
set_res_entry_label.grid(row=1, column=1, sticky=Tk.N)
set_res_send = Tk.Button(master=res_settings_frame, text="senden", command=lambda: change_res())
set_res_send.grid(row=1, column=2, sticky=Tk.N)



"""
button1 = Tk.Button(master=ia_frame, text='Change Res1', command=lambda: change_res(1000))
button1.grid(row=0,column=1, sticky=Tk.N)
#button1.pack(side=Tk.LEFT)
button2 = Tk.Button(master=ia_frame, text='Change Res2', command=lambda: change_res(2000))
button2.grid(row=0,column=2, sticky=Tk.N)
#button2.pack(side=Tk.LEFT)
button4 = Tk.Button(master=ia_frame, text='Change Resss', command=lambda: set_resistor_step(1000,4000))
button4.grid(row=1,column=1, columnspan=2, sticky=Tk.N)
#button4.pack(side=Tk.LEFT)
"""
button3 = Tk.Button(master=ia_frame, text='Quit', command=_quit)
button3.grid(row=5,column=0, columnspan=4,sticky=Tk.N)
#button3.pack(side=Tk.LEFT)

Tk.mainloop()
# If you put root.destroy() here, it will cause an error if
# the window is closed with the window manager.
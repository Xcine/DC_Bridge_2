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

f = Figure(figsize=(10, 5.8), dpi=100)
f.suptitle("Widerstands-Spannungskurve", fontsize=14)
a = f.add_subplot(111)
res = []
vol = []
a.set_ylabel("Brueckenspannung in Volt")
a.set_ylim([0,5])
a.set_xlabel("Widerstand R in Ohm")
a.set_xlim([0,4200])
line1, = a.plot([],[],'r.')
graph_color = "black"

#pyb1 = pyboard.Pyboard(device = "/dev/tty.usbmodem1412")
pyb1 = pyboard.Pyboard(device = "/dev/ttyACM0")
pyb1.enter_raw_repl()
#output = pyb1.execfile("test.py")
pyb1.exec_('import time')
pyb1.exec_('from resistor import Resistor')
pyb1.exec_('res = Resistor()')

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
            value_board = pyb1.exec_('res.get_resistor_string()')
            if value_board != res1:
                raise ValueError("Resistor was not set.")
            vol_val = float(pyb1.exec_('res.get_adc_string()'))
            res1 += resistor_step
            res.append(value_board)
            vol.append(vol_val)
            line1.set_ydata(res)
            line1.set_xdata(vol)
            f.canvas.draw()
            pyb1.exec_('time.sleep(' + str(sleeptime) + ')')
    else:
        if res1 > 4196.875:
            res1 = 4196.875
        if res2 < 1000.0:
            res2 = 1000.0
        while res2 <= res1:
            pyb1.exec_('res.set_resistor(' + str(res1) + ')')
            value_board = pyb1.exec_('res.get_resistor_string()')
            if value_board != res1:
                raise ValueError("Resistor was not set.")
            vol_val = float(pyb1.exec_('res.get_adc_string()'))
            res1 += resistor_step
            res.append(value_board)
            vol.append(vol_val)
            line1.set_ydata(res)
            line1.set_xdata(vol)
            f.canvas.draw()
            pyb1.exec_('time.sleep(' + str(sleeptime) + ')')

def set_resistors():
    num=0
    try:
        start_r = float(res_start_entry.get())
        res_start_entry.config({"background": "white"})
        num += 1
    except:
        res_start_entry.config({"background": "red"})

    try:
        end_r = float(res_end_entry.get())
        res_end_entry.config({"background": "white"})
        num += 1
    except:
        res_end_entry.config({"background": "red"})

    try:
        step_r = float(res_step_entry.get())
        res_step_entry.config({"background": "white"})
        num += 1
    except:
        res_step_entry.config({"background": "red"})

    try:
        time_r = float(res_time_entry.get())
        res_time_entry.config({"background": "white"})
        num += 1
    except:
        res_time_entry.config({"background": "red"})

    if num == 4:
        set_resistor_step(start_r, end_r, step_r, time_r)


def set_resistor():
    try:
        value = float(set_res_entry.get())
        set_res_entry.config({"background": "white"})

        pyb1.exec_('res.set_resistor(' + str(value) + ')')
        value_board = float(pyb1.exec_('res.get_resistor_string()'))
        if value_board != value:
            raise ValueError("Resistor was not set.")
        vol_val = float(pyb1.exec_('res.get_adc_string()'))
        res.append(value)
        vol.append(vol_val)
        line1.set_ydata(res)
        line1.set_xdata(vol)
        f.canvas.draw()
    except:
        set_res_entry.config({"background": "red"})

def reset_graph():
    line1.set_ydata([])
    line1.set_xdata([])

def set_graph_color(string):
    if string == "black":
        line1.set_color('#000000')
        graph_color = "black"
        graph_pen.config(text='Stift ist bei: (0,0), ' + graph_color)
    elif string == "blue":
        line1.set_color('#0000FF')
        graph_color = "blue"
        graph_pen.config(text='Stift ist bei: (0,0), ' + graph_color)
    elif string == "red":
        line1.set_color('#FF0000')
        graph_color = "red"
        graph_pen.config(text='Stift ist bei: (0,0), ' + graph_color)
    elif string == "green":
        line1.set_color('#00FF00')
        graph_color = "green"
        graph_pen.config(text='Stift ist bei: (0,0), ' + graph_color)
    else:
        raise ValueError("No such color.")

def showit():
    num=0
    try:
        start_r = float(res_start_entry.get())
        res_start_entry.config({"background": "white"})
        num += 1
    except:
        res_start_entry.config({"background": "red"})

    try:
        end_r = float(res_end_entry.get())
        res_end_entry.config({"background": "white"})
        num += 1
    except:
        res_end_entry.config({"background": "red"})

    try:
        step_r = float(res_step_entry.get())
        res_step_entry.config({"background": "white"})
        num += 1
    except:
        res_step_entry.config({"background": "red"})

    try:
        time_r = float(res_time_entry.get())
        res_time_entry.config({"background": "white"})
        num += 1
    except:
        res_time_entry.config({"background": "red"})

    if num == 4:
        set_resistor_step(start_r, end_r, step_r, time_r)

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

ia_frame = Tk.Frame(root, highlightthickness=0, highlightcolor="black", highlightbackground="black")
ia_frame.grid(row=0, column=1, sticky=Tk.N+Tk.S+Tk.W+Tk.E)

info_frame = Tk.Frame(ia_frame, highlightthickness=1, bd=10, highlightcolor="black", highlightbackground="black")
info_frame.grid(row=0, column=0, columnspan=4, sticky=Tk.N+Tk.S+Tk.W+Tk.E)
info_frame.columnconfigure(0, weight=1)
info_frame.columnconfigure(1, weight=1)
info_frame.columnconfigure(2, weight=1)
info_frame.columnconfigure(3, weight=1)

info_title = Tk.Label(master=info_frame, text="Momentane Messwerte:")
info_title.grid(row=0, column=0, columnspan=4, sticky=Tk.N+Tk.S+Tk.W+Tk.E)

info_res_label = Tk.Label(master=info_frame, text="R = ")
info_res_label.grid(row=1, column=0, sticky=Tk.N+Tk.W)
info_res_value = Tk.Label(master=info_frame, text="1000 Ohm")
info_res_value.grid(row=1, column=1, sticky=Tk.N+Tk.W)

info_u_label = Tk.Label(master=info_frame, text="U = ")
info_u_label.grid(row=1, column=2, sticky=Tk.N+Tk.E)
info_u_value = Tk.Label(master=info_frame, text="3.3 Volt")
info_u_value.grid(row=1, column=3, sticky=Tk.N+Tk.E)

graph_settings_frame = Tk.Frame(ia_frame, bd=10, highlightthickness=1, highlightcolor="black", highlightbackground="black")
graph_settings_frame.grid(row=1, column=0, columnspan=4, sticky=Tk.N+Tk.S+Tk.W+Tk.E)
graph_settings_frame.columnconfigure(0, weight=1)
graph_settings_frame.columnconfigure(1, weight=1)
graph_settings_frame.columnconfigure(2, weight=1)
graph_settings_frame.columnconfigure(3, weight=1)
graph_settings_title = Tk.Label(master=graph_settings_frame, text="Graph Einstellungen:")
graph_settings_title.grid(row=0, column=0, columnspan=4, sticky=Tk.N)

button_graph_reset = Tk.Button(master=graph_settings_frame, text="Graph zurücksetzen", command=lambda: reset_graph())
button_graph_reset.grid(row=1, column=0, columnspan=4, sticky=Tk.N+Tk.S+Tk.W+Tk.E)

button_graph_toggle = Tk.Button(master=graph_settings_frame, text="Starte Messung", command=lambda: change_res(1000))
button_graph_toggle.grid(row=2, column=0, columnspan=4, sticky=Tk.N+Tk.S+Tk.W+Tk.E)

button_graph_over_again = Tk.Button(master=graph_settings_frame, text="Setze Stift auf (0,0)", command=lambda: change_res(1000))
button_graph_over_again.grid(row=3, column=0, columnspan=4, sticky=Tk.N+Tk.S+Tk.W+Tk.E)

graph_colors= Tk.Label(master=graph_settings_frame, text="Farbauswahl:")
graph_colors.grid(row=4, column=0, columnspan=4, sticky=Tk.N)
button_black = Tk.Button(master=graph_settings_frame, text="Schwarz", fg="black", command=lambda: set_graph_color("black"))
button_black.grid(row=5, column=0, sticky=Tk.N+Tk.S+Tk.W+Tk.E)
button_blue = Tk.Button(master=graph_settings_frame, text="Blau", fg="blue", command=lambda: set_graph_color("blue"))
button_blue.grid(row=5, column=1, sticky=Tk.N+Tk.S+Tk.W+Tk.E)
button_red = Tk.Button(master=graph_settings_frame, text="Rot", fg="red", command=lambda: set_graph_color("red"))
button_red.grid(row=5, column=2, sticky=Tk.N+Tk.S+Tk.W+Tk.E)
button_green = Tk.Button(master=graph_settings_frame, text="Grün", fg="green", command=lambda: set_graph_color("green"))
button_green.grid(row=5, column=3, sticky=Tk.N+Tk.S+Tk.W+Tk.E)
graph_pen= Tk.Label(master=graph_settings_frame, text="Stift ist bei: (0,0), blau")
graph_pen.grid(row=6, column=0, columnspan=4, sticky=Tk.N+Tk.S+Tk.W+Tk.E)


res_settings_frame = Tk.Frame(ia_frame, bd=10, highlightthickness=1, highlightcolor="black", highlightbackground="black")
res_settings_frame.grid(row=2, column=0, columnspan=4, sticky=Tk.N+Tk.S+Tk.W+Tk.E)
res_settings_frame.columnconfigure(0, weight=1)
res_settings_frame.columnconfigure(1, weight=1)
res_settings_frame.columnconfigure(2, weight=1)
res_settings_frame.columnconfigure(3, weight=1)

res_settings_title = Tk.Label(master=res_settings_frame, text="Widerstands Einstellungen:")
res_settings_title.grid(row=0, column=0, columnspan=4, sticky=Tk.N)

set_res_label = Tk.Label(master=res_settings_frame, text="R = ")
set_res_label.grid(row=1, column=0, sticky=Tk.N, pady=5, padx=5)
set_res_entry = Tk.Entry(master=res_settings_frame, justify=Tk.RIGHT, width=9)
set_res_entry.insert(0, "3000.25")
set_res_entry.grid(row=1, column=1, sticky=Tk.N, pady=5)
set_res_entry_label = Tk.Label(master=res_settings_frame, text=" Ohm")
set_res_entry_label.grid(row=1, column=2, sticky=Tk.N, pady=5, padx=5)
set_res_send = Tk.Button(master=res_settings_frame, text="senden", command=lambda: set_resistor())
set_res_send.grid(row=1, column=3, sticky=Tk.N)

res_row_frame = Tk.Frame(ia_frame, bd=10, highlightthickness=1, highlightcolor="black", highlightbackground="black")
res_row_frame.grid(row=3, column=0, columnspan=2, sticky=Tk.N+Tk.S+Tk.W+Tk.E)
res_row_frame.columnconfigure(0, weight=1)
res_row_frame.columnconfigure(1, weight=1)
res_row_frame.columnconfigure(2, weight=1)
res_row_frame.columnconfigure(3, weight=1)

res_row_title = Tk.Label(master=res_row_frame, text="Widerstandreihen Einstellungen:")
res_row_title.grid(row=0, column=0, columnspan=4, sticky=Tk.N)

res_start_label = Tk.Label(master=res_row_frame, text="Startwiderstand (in Ohm): ")
res_start_label.grid(row=1, column=0, sticky=Tk.N)
res_start_entry = Tk.Entry(master=res_row_frame, width=9)
res_start_entry.insert(0, "1000.0")
res_start_entry.grid(row=1, column=1, sticky=Tk.N)

res_end_label = Tk.Label(master=res_row_frame, text="Endwiderstand (in Ohm): ")
res_end_label.grid(row=2, column=0, sticky=Tk.N)
res_end_entry = Tk.Entry(master=res_row_frame, width=9)
res_end_entry.insert(0, "4000.0")
res_end_entry.grid(row=2, column=1, sticky=Tk.N)

res_step_label = Tk.Label(master=res_row_frame, text="Widerstandsschritt (in Ohm): ")
res_step_label.grid(row=3, column=0, sticky=Tk.N)
res_step_entry = Tk.Entry(master=res_row_frame, width=9)
res_step_entry.insert(0, "100.0")
res_step_entry.grid(row=3, column=1, sticky=Tk.N)

res_time_label = Tk.Label(master=res_row_frame, text="Zeitschritt (in Sekunden): ")
res_time_label.grid(row=4, column=0, sticky=Tk.N)
res_time_entry = Tk.Entry(master=res_row_frame, width=9)
res_time_entry.insert(0, "0.5")
res_time_entry.grid(row=4, column=1, sticky=Tk.N)

res_row_send = Tk.Button(master=res_row_frame, text="Starte Messreihe", command=lambda: set_resistors())
res_row_send.grid(row=5, column=0, columnspan=2, sticky=Tk.N+Tk.S+Tk.W+Tk.E)
res_row_stop = Tk.Button(master=res_row_frame, text="Stope Messreihe", command=lambda: change_res(1000))
res_row_stop.grid(row=6, column=0, columnspan=2, sticky=Tk.N+Tk.S+Tk.W+Tk.E)

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

end_frame = Tk.Frame(ia_frame, bd=10, highlightthickness=1, highlightcolor="black", highlightbackground="black")
end_frame.grid(row=4, column=0, columnspan=2, sticky=Tk.N+Tk.S+Tk.W+Tk.E)
end_frame.columnconfigure(0, weight=1)
end_frame.columnconfigure(1, weight=1)

status_label = Tk.Label(master=end_frame, text="Verbindungsstatus pyboard: ")
status_label.grid(row=6, column=0, sticky=Tk.S)
status_label_val = Tk.Label(master=end_frame, text="Ok.", fg="green")
status_label_val.grid(row=6, column=1, sticky=Tk.S)

button3 = Tk.Button(master=end_frame, text='Programm schließen', command=_quit)
button3.grid(row=7,column=0, columnspan=2, sticky=Tk.S+Tk.W+Tk.E)
#button3.pack(side=Tk.LEFT)

Tk.mainloop()
# If you put root.destroy() here, it will cause an error if
# the window is closed with the window manager.
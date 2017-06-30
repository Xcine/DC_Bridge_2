import sys
sys.path.insert(0, '/Users/Georg/micropython/tools')
sys.path.insert(0, '/Users/Georg/micropython')
import pyboard

def main():
    pyb = pyboard.Pyboard('/dev/tty.usbmodem1412')
    pyb.enter_raw_repl()
    pyb.exec('import pyb')
    pyb.exec('sw = pyb.Switch()')
    pyb.exec('sw.value()')
    pyb.exec('pyb.LED(1).on()')
    pyb.exec('print("Hallo")')
    pyb.exit_raw_repl()

if __name__ == '__main__':
    main()
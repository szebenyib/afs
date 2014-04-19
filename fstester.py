import pyuipc
import serial
from time import sleep

#Init arduino
arduinoSerial = serial.Serial("COM1", 9600)
sleep(1.5)

#Open Fs2004
pyuipc.open(7)

def convertBCD(data, length):
    """BCD to string"""
    bcd = ""
    for i in range(0, length):
        digit = chr(ord('0') + (data&0x0f))
        data >>= 4
        bcd = digit + bcd
    return bcd

batteryToRead = pyuipc.prepare_data([(0x028c, "d")])

batteryState = pyuipc.read(batteryToRead)
#batteryStateConverted = convertBCD(batteryState[0], len(batteryState))
#print batteryStateConverted
print batteryState[0]
print chr(batteryState[0]+48)
print str(chr(batteryState[0]+48))

#arduinoSerial.write(str(0))
arduinoSerial.write(str(batteryState[0]))
#arduinoSerial.write(str(chr(batteryState[0]+48)))
print arduinoSerial.readline()

#batteryToSet = pyuipc.prepare_data([(0x281C, "d", 1),], False)
#batteryToSet = pyuipc.prepare_data([(0x281c, "d")], False)
#pyuipc.write(batteryToSet, [1])
if batteryState[0] == 1:
    newState = 0
else:
    newState = 1

pyuipc.write([(0x028c, "h", newState)])

batteryState = pyuipc.read(batteryToRead)
print batteryState

while True:
    batteryState = pyuipc.read(batteryToRead)
    if batteryState[0] == 1:
        newState = 0
    else:
        newState = 1
    pyuipc.write([(0x028c, "h", newState)])
    batteryState = pyuipc.read(batteryToRead)
    arduinoSerial.write(str(batteryState[0]))
    sleep(1)
    print arduinoSerial.readline()

pyuipc.close()



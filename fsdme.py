import pyuipc
import serial
from time import sleep
from Readings import Readings


def create_fs_connection(fs_version=7):
    """Creates the connection with the flight simulator.

    Returns: the connection to the Flight Sim"""
    return pyuipc.open(fs_version)


def create_arduino_connection():
    """Creates the connection with the Arduino using the given COM port.
    Baud rate is set automatically. If no COM port is given it will try
    to connect on COM1-COM4. There is a 1.5 sec delay built in to handle
    connection setup time.

    Returns: a serial.Serial object (pyserial library)"""

    # Try all ports if none specified.
    not_found_port = True
    i = 1
    while not_found_port and i <= 4:
        try:
            print "Trying arduino on: COM" + str(i)
            arduino_serial = serial.Serial("COM" + str(i))
            arduino_serial.setBaudrate(57600)
            arduino_serial.setTimeout(2)
            sleep(1.5)
            arduino_serial.write('T')  # T for test
            sleep(.1)
            arduino_serial.write('T')  # T for test
            x = arduino_serial.readline()
            if x == 'T':
                not_found_port = False
                print "Found arduino on " + arduino_serial.name
                return arduino_serial
            else:
                print arduino_serial.name
            i += 1
        except Exception, e:
            print e.message
            # This is the last try and no valid com port has been found.
            if i == 4:
                print "Arduino not detected."
            i += 1

#Init arduino
arduinoSerial = create_arduino_connection()

#Init Fs2004
create_fs_connection()

readings = Readings(pyuipc)

readings.create_prepared_data()
readings.read_and_convert()

# valuesToRead = readings.get_values_to_read()
#
# dmeToRead = pyuipc.prepare_data([(0x0300, "H")])
# dmeValue = pyuipc.read(dmeToRead)
#
# data = pyuipc.read(create_prepared_data(valuesToRead))
#
# data2 = convert_read_data_from_fs(data, valuesToRead)
#
# print data
# print convert_bcd(data[0], 4)
#
#
while True:
    arduinoSerial.write(readings.get_value("Dme1"))
    sleep(0.5)

# def readDme(dmeToRead, s):
#     while True:
#         dmeValue = pyuipc.read(dmeToRead)
#         arduinoSerial.write(str(dmeValue[0]))
#         time.sleep(s)
#
# t = Thread(target=readDme, args=(dmeToRead,2))
# t.start()

pyuipc.close()
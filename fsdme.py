import pyuipc
import serial
from time import sleep
#  from threading import Thread
import time


def create_fs_connection(fs_version=7):
    """Creates the connection with the flight simulator."""
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


def create_prepared_data(values_to_read):
    """Creates the prepared data for the tuples or list it receives. Expected
    is a list of offsets like 0x0300 without apostrophes and another list
    with types as found in the fsuipc documentation (Offset status pdf),
    and pyuipc documentation like "H" (0x0300 stands for VOR1 DME distance,
    16-bit integer -> 2 byte unsigned value will do, so use H)
    Example = [(0x0300, "H"),] """

    """A corrected list is needed to remove the extra parameters of the values
    to read list."""
    corrected_list = []
    for item in values_to_read:
        corrected_list.append((item[0], item[1]))

    prepared_data = pyuipc.prepare_data(corrected_list)
    return prepared_data


def convertBCD(data, length):
        """Convert a data item encoded as BCD into a string of the given number
        of digits."""
        bcd = ""
        for i in range(0, length):
            digit = chr(ord('0') + (data & 0x0f))
            data >>= 4
            bcd = digit + bcd
        return bcd


def convert_read_data_from_fs(read_data):
    """Converts data from the list that has been returned from reading from
    fsuipc. It is necessary to do as some of the returned values are so
    called BCD values and transformation is needed to send the appropriate
    number to arduino. Additionally leading '1's are needed in front of the
    frequencies."""
    n = len(read_data)
    i
        #valuesToRead list contains the info about BCD conversion necessity.
        if valuesToRead

#Init arduino
arduinoSerial = create_arduino_connection()

#Init Fs2004
create_fs_connection()

"""Values to read, a list of tuples, the third item tells if BCD conversion is
#needed or not"""
valuesToRead = [
    (0x0350, "H", 1),  # Nav1active
    (0x311e, "H", 1),  # Nav1sby
    (0x0352, "H", 1),  # Nav2active
    (0x3120, "H", 1),  # Nav2sby
    (0x034e, "H", 1),  # Com1active
    (0x311a, "H", 1),  # Com1sby
    (0x3118, "H", 1),  # Com2active
    (0x311c, "H", 1),  # Com2sby
    (0x034c, "H", 1),  # Adf1
    (0x0300, "H", 0),  # Dme1
    (0x0306, "H", 0), ]  # Dme2


dmeToRead = pyuipc.prepare_data([(0x0300, "H")])
dmeValue = pyuipc.read(dmeToRead)

data = pyuipc.read(create_prepared_data(valuesToRead))

print data
print convertBCD(data[0], 4)


while True:
    dmeValue = pyuipc.read(dmeToRead)
    arduinoSerial.write(str(dmeValue[0]) + '\n')
    print str(dmeValue[0])
    time.sleep(0.5)

# def readDme(dmeToRead, s):
#     while True:
#         dmeValue = pyuipc.read(dmeToRead)
#         arduinoSerial.write(str(dmeValue[0]))
#         time.sleep(s)
#
# t = Thread(target=readDme, args=(dmeToRead,2))
# t.start()

print dmeValue[0]
#arduinoSerial.write(str(dmeValue[0]))

pyuipc.close()
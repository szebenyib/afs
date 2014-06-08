from collections import OrderedDict

__author__ = 'Balint Szebenyi'


class Readings():
    """Holds the values that are to be read, reads, converts and retrieves
    values using pyuipc"""

    #pyuipc
    _pyuipc = None

    #Default values to read.
    #First: fsuipc offset
    #Second: type of reading, see pyuipc sdk
    #Third: bcd conversion is needed or not
    _valuesToRead = OrderedDict()

    #The keys ot the dictionary
    _availableValues = None

    #Stores the data that is used directly by fsuipc. Converting the data
    #once from valuesToRead and storing it to avoid convertion costs.
    _preparedData = None

    #Stores the data that is read by fsuipc. It needs conversion, addition
    #of preceeding '1's so it cannot be directly used.
    _readData = None

    #Stores the converted data that has been prepared to send to arduino.
    _convertedData = OrderedDict()

    def __init__(self, pyuipc):
        self._pyuipc = pyuipc
        self._valuesToRead['Nav1Active'] = (0x0350, "H", True)
        self._valuesToRead['Nav1Standby'] = (0x311e, "H", True)
        self._valuesToRead['Nav2Active'] = (0x0352, "H", True)
        self._valuesToRead['Nav2Standby'] = (0x3120, "H", True)
        self._valuesToRead['Com1Active'] = (0x034e, "H", True)
        self._valuesToRead['Com1Standby'] = (0x311a, "H", True)
        self._valuesToRead['Com2Active'] = (0x3118, "H", True)
        self._valuesToRead['Com2Standby'] = (0x311c, "H", True)
        self._valuesToRead['Adf1'] = (0x034c, "H", False)
        self._valuesToRead['Dme1'] = (0x0300, "H", False)
        self._valuesToRead['Dme2'] = (0x0306, "H", False)
        self._availableValues = self._valuesToRead.keys()

    def get_value(self, key):
        """Gets the arduino ready value for the given item"""

        return self._convertedData[key]

    def create_prepared_data(self):
        """Creates the prepared data for the tuples or list it receives.
            Expected is a list of offsets like 0x0300 without apostrophes and
            another list with types as found in the fsuipc documentation
            (Offset status pdf), and pyuipc documentation like "H"
            (0x0300 stands for VOR1 DME distance,
            16-bit integer -> 2 byte unsigned value will do, so use H)
            Example = [(0x0300, "H"),]

            Returns: a list of tuples of prepared data"""

        #A corrected list is needed to remove the extra parameters of the values
        #to read list.
        corrected_list = []
        for i in range(0, len(self._valuesToRead)):
            corrected_list.append((self._valuesToRead.get(
                self._availableValues[i])[0],
                self._valuesToRead.get(self._availableValues[i])[1]))
        # for item in self._valuesToRead:
        #     corrected_list.append((item[0], item[1]))

        self._preparedData = self._pyuipc.prepare_data(corrected_list)

    def _read_prepared_data(self):
        """Reads the data from flight sim using pyuipc after the data has
            been prepared."""
        self._readData = self._pyuipc.read(self._preparedData)

    @staticmethod
    def _convert_bcd(data, length):
        """Convert a data item encoded as BCD into a string of the given number
            of digits.

            Returns: the decoded value"""

        bcd = ""
        for i in range(0, length):
            digit = chr(ord('0') + (data & 0x0f))
            data >>= 4
            bcd = digit + bcd
        return bcd

    def _convert_read_data_from_fs(self):
        """Converts data from the list that has been returned from reading from
            fsuipc. It is necessary to do as some of the returned values are so
            called BCD values and transformation is needed to send the
            appropriate number to arduino.
            Additionally leading '1's are needed in front of the
            frequencies."""

        for i in range(0, len(self._readData)):
            #if conversion is necessary
            if self._valuesToRead.get(self._availableValues[i])[2]:
                self._convertedData[self._availableValues[i]] = "1" + self \
                    ._convert_bcd(self._readData[i], len(str(self
                    ._readData[i]))) + "\n"
            else:
                self._convertedData[self._availableValues[i]] = str(self \
                    ._readData[i]) + "\n"

    def read_and_convert(self):
        """Combines read_prepared_data, and convert_read_data_from_fs as a
        shortcut."""

        self._read_prepared_data()
        self._convert_read_data_from_fs()

    def print_all_values(self):
        """Prints all the keys and values for quick debugging."""
        print self._convertedData
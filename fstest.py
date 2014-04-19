import pyuipc

pyuipc.open(7) #fs2004

def convertBCD(data, length):
	"""BCD to string"""
	bcd = ""
	for i in range (0, length):
		digit = chr(ord('0') + (data&0x0f))
		data >>= 4
		bcd = digit + bcd
	return bcd

nav1 = pyuipc.read([(0x0350, "H"),]) #Nav1

print nav1
print convertBCD(nav1, 4)

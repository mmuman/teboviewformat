#!/usr/bin/env python3

import sys
import struct



# Read a pascal string from d
def getPString(data):
	l = data.pop(0)
	s = data[0:l]
	del data[0:l]
	return s.decode('utf-8')

# Read an LE uint32 from d
def getUInt32(data):
	(i,) = struct.unpack("<I",data[0:4])
	del data[0:4]
	return i

# Read an LE int32 from d
def getInt32(data):
	(i,) = struct.unpack("<i",data[0:4])
	del data[0:4]
	return i

def dumpLayer(data, i):
	print("== Layer %d:" % i)
	print("LayerName	%s" % getPString(data))
	print("InitialName	%s" % getPString(data))
	print("Path	%s" % getPString(data))
	# Layer number??? no, not unique.
	# Some bitmask flags?
	layerTypes = ['Document', 'Top', 'Bottom', 'Signal', 'Power ground', 'Solder Mask [Top]', 'Solder Mask [Bottom]', 'Silkscreen [Top]', 'Silkscreen [Bottom]', 'Paste [Top]', 'Paste [Bottom]', 'Drill', 'Roul']
	print("Type	%s" % layerTypes[getUInt32(data)])
	print("PadColor	0x%x" % getUInt32(data))
	print("LineColor	0x%x" % getUInt32(data))
	# Whatever ?
	for n in range(0, 80):
		#print("?	0x%x" % getUInt32(data))
		x, y = getInt32(data), getInt32(data)
		print("?	0x%x %i , 0x%x %i" % (x, x, y, y))
		x, y = getInt32(data), getInt32(data)
		print("?		0x%x %i , 0x%x %i" % (x, x, y, y))
		x, y = getInt32(data), getInt32(data)
		print("?		0x%x %i , 0x%x %i" % (x, x, y, y))

if len(sys.argv) < 2:
	raise SystemExit("usage: %s file.tvw" % sys.argv[0])

with open(sys.argv[1], "rb") as f:
	data = f.read(-1)
	# get a mutable bytes array so we can pop() from it
	data = bytearray(data)

	print("== Header:")
	print("?	%s" % getPString(data))
	print("?	0x%x" % getUInt32(data))
	print("?	%s" % getPString(data))
	# unknown null byte, could be an empty string?
	print("?	%s" % getPString(data))
	#print("?	%x" % data.pop(0))
	# some per layer flags in ASCII maybe? Length doesn't match layer count though
	print("?	%s" % getPString(data))
	# 3 unknown null bytes, could be empty strings?
	print("?	%s" % getPString(data))
	print("?	%s" % getPString(data))
	print("?	%s" % getPString(data))

	print("?	0x%x" % getUInt32(data))
	print("?	0x%x" % getUInt32(data))
	print("?	0x%x" % getUInt32(data))
	nrLayers = getUInt32(data)
	print("nrLayers	%i" % nrLayers)

	# could this actually be part of the first layer?
	print("?	0x%x" % getUInt32(data))
	print("?	0x%x" % getUInt32(data))
	print("?	0x%x" % getUInt32(data))
	print("?	0x%x" % getUInt32(data))
	print()

	for i in range(0, nrLayers):
		dumpLayer(data, i)

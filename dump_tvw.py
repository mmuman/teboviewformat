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
	shapes = []
	# maybe rather the start id for shapes
	nItems = getUInt32(data)
	for n in range(0, nItems):
		#nShapes = getUInt32(data)
		#for m in range(0, nShapes):
		# is it some item type or count ?
		itemType = getUInt32(data)
		if itemType == 1:
			# bounds ?
			bounds = getInt32(data), getInt32(data)
			print(bounds)
			if bounds != (0, 1):
				shapeType = getUInt32(data)
				shapeTypes = ['rounded??', 'rect', 'empty??', 'rounded', 'circle', 'FAIL to open', '??', '??', '???', '???']
				print("shapeType: 0x%x" % shapeType)
				print("Shape: %s (0x%x) %i x %i (0x%x x 0x%x)" % (shapeTypes[shapeType], shapeType, bounds[0], bounds[1], bounds[0], bounds[1]))
				unknown = getInt32(data)
				print("?	0x%x" % (unknown))
				# curvature radius?
				radius = getInt32(data)
				print("radius?	0x%x %i" % (radius, radius))
				shapes.append({'type': shapeType, 'bounds': bounds, 'args': [unknown, radius]})
			else:
				nPads = getInt32(data)
				print("nPads?	0x%x" % (nPads))
				unknown1 = getInt32(data)
				print("?	0x%x" % (unknown1))
				unknown2 = getInt32(data)
				print("?	0x%x" % (unknown2))
				for m in range(0, nPads):
					idx = getInt32(data)
					print("shapeIndex	0x%x %i" % (idx, idx))
					pos = getInt32(data), getInt32(data)
					print("shape[%i] at %i x %i (0x%x x 0x%x)" % (idx, pos[0], pos[1], pos[0], pos[1]))
					unknownP = getInt32(data)
					print("?	0x%x" % (unknownP))
					# 3 unknown null bytes, could be empty strings?
					print("?	%s" % getPString(data))
					print("?	%s" % getPString(data))
					print("?	%s" % getPString(data))
		elif itemType == 8:
			unknown = getInt32(data)
			print("?	0x%x %i" % (unknown, unknown))
			print("?	0x%x %i" % (unknown, unknown))
			
			
		else:
			raise SystemExit("Unknown itemType %s" % itemType)

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




# hints: strings from:

# DCodeManagerModule.dll
#donut%sx%s
#rect%sx%sxr%s
#rect%sx%sxr%sxa%d
#oval%sx%s
#oval%sx%sxa%d
#rect%sx%s
#rect%sx%sxa%d
#
#triangle
#diamond
#hexagon
#Octagon
#Thermal
#Target

# IctGraphicFunction.dll
#?AddPad_Circle@CPhysicLayerEditor@@QAEPAVIPad@@PAUtagPOINT@@J@Z
#?AddPad_Rect@CPhysicLayerEditor@@QAEPAVIPad@@PAUtagPOINT@@JJN@Z
#?AddPad_Oblong@CPhysicLayerEditor@@QAEPAVIPad@@PAUtagPOINT@@JJN@Z
#?AddPad_Donut@CPhysicLayerEditor@@QAEPAVIPad@@PAUtagPOINT@@JJ@Z
#?AddPad_Thermal@CPhysicLayerEditor@@QAEPAVIPad@@PAUtagPOINT@@JJJN@Z
#?AddPad_DCode@CPhysicLayerEditor@@QAEPAVIPad@@PAUtagPOINT@@PAVIDCodeManager@@H@Z

# OutputPcbFunction.dll
#Pads
#TestPoints
#Fonts
#LayerSets
#LayerNames
#Layers
#Padstacks
#Parts
#Packages
#Padsymbols
#Nets
#Fab

# IctData.dll
#TestPad
#DrlLayer
#MillLayer
#PanelLayer
#Line
#Surface
#Text
#ColorLine
#DrlHole
#DrlCircle
#DrlSlot
#DrlArc
#MillPoly
#MillZBrushRemark
#Panel
#TestPad HoleSize
#TestPad Mask
#TestPad DCode
#%s(%d)
#TestPad Net
#TestPad CenterPoint Y Coordinate
#TestPad CenterPoint X Coordinate
#TestPad Name
#TestPad Is TP
#Unknown(%d)
#TestPad Type
#TestPad No
#Layer Type
#Layer Pad Color
#Layer Line Color
#Layer Name
#Layer Init Name
#Layer Line/Pad Visible
#Layer Init Path
#Drl From Layer
#Drl To Layer
#.aft
#complex
#italic
#romans
#\Setting\
#Auto-ICT Font 1.0
#Pad CenterPoint X Coordinate
#Pad CenterPoint Y Coordinate
#UnTest Reason
#Pad Hole CenterPoint Coordinate
#Pad Hole Size cy
#Pad Hole Size cx
#Pad Mask
#DCode Height
#DCode Width
#DCode Shape
#DCode No.
#Net No.
#EndPoint Y Coordinate
#EndPoint X Coordinate
#BeginPoint Y Coordinate
#BeginPoint X Coordinate
#StartPoint Y Coordinate
#StartPoint X Coordinate
#CenterPoint Y Coordinate
#CenterPoint X Coordinate
#StartAngle
#%.2f
#SweepAngle
#Clockwise
#Surface edge num
#Line Width
#%d(I%d)
#Surface void num
#False
#True
#Text mirror
#Text angle
#Text Location
#Text Content
#Font Weight
#Font Height
#Text Font
#Text Color
#Line Color
#Hole CenterPoint X Coordinate
#Hole CenterPoint Y Coordinate
#Tool No.
#Tool Size
#Circle CenterPoint X Coordinate
#Circle CenterPoint Y Coordinate
#Circle Diameter
#Z Value
#Accurate Tool Size
#Accurate Tool No.
#Inch
#[%d]%s
#Angle
#NC_%d
#IctData.dll
#Arial
#BOTTOM
#%%2.%df

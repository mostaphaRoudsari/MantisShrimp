#Copyright(c) 2014, Konrad Sobon
# @arch_laboratory, http://archi-lab.net

import clr
import sys
clr.AddReference('ProtoGeometry')

pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

import os
appDataPath = os.getenv('APPDATA')
msPath = appDataPath + r"\Dynamo\0.7\packages\Mantis Shrimp\extra"
if msPath not in sys.path:
	sys.path.Add(msPath)

possibleRhPaths = []
possibleRhPaths.append(r"C:\Program Files\Rhinoceros 5 (64-bit)\System\RhinoCommon.dll")
possibleRhPaths.append(r"C:\Program Files\Rhinoceros 5.0 (64-bit)\System\RhinoCommon.dll")
possibleRhPaths.append(r"C:\Program Files\McNeel\Rhinoceros 5.0\System\RhinoCommon.dll")
possibleRhPaths.append(msPath)
checkPaths = map(lambda x: os.path.exists(x), possibleRhPaths)
for i, j in zip(possibleRhPaths, checkPaths):
	if j and i not in sys.path:
		sys.path.Add(i)
		clr.AddReferenceToFileAndPath(i)

from Autodesk.DesignScript.Geometry import *
import Rhino as rc

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN
rhObjects = IN[0]
_units = IN[1]

#unit conversion function from Rhino to DS
def toDSUnits(_units):
	if _units == rc.UnitSystem.Millimeters:
		return 0.001
	elif _units == rc.UnitSystem.Centimeters:
		return 0.01
	elif _units == rc.UnitSystem.Decimeters:
		return 0.1
	elif _units == rc.UnitSystem.Meters:
		return 1
	elif _units == rc.UnitSystem.Inches:
		return 0.0254
	elif _units == rc.UnitSystem.Feet:
		return 0.3048
	elif _units == rc.UnitSystem.Yards:
		return 0.9144

#Vector3d conversion function
def rhVector3dToVector(rhVector):
	VectorX = rhVector.X * toDSUnits(_units)
	VectorY = rhVector.Y * toDSUnits(_units)
	VectorZ = rhVector.Z * toDSUnits(_units)
	dsVector = Vector.ByCoordinates(VectorX, VectorY, VectorZ)
	return dsVector

#3dPoint Conversion function
def rhPoint3dToPoint(rhPoint):
	rhPointX = rhPoint.X * toDSUnits(_units)
	rhPointY = rhPoint.Y * toDSUnits(_units)
	rhPointZ = rhPoint.Z * toDSUnits(_units)
	dsPoint = Point.ByCoordinates(rhPointX, rhPointY, rhPointZ)
	return dsPoint
	
#Plane conversion function
def rhPlaneToPlane(rhPlane):
	normal = rhVector3dToVector(rhPlane.Normal)
	origin = rhPoint3dToPoint(rhPlane.Origin)
	dsPlane = Plane.ByOriginNormal(origin, normal)
	return dsPlane

#circle conversion function
def rhCircleToCircle(rhCurve):
	rhCircle = rhCurve.TryGetCircle()[1]
	radius = rhCircle.Radius * toDSUnits(_units)
	plane = rhPlaneToPlane(rhCircle.Plane)
	dsCircle = Circle.ByPlaneRadius(plane, radius)
	return dsCircle

#convert rhino/gh geometry to ds geometry
dsCircles = []
for i in rhObjects:
	try:
		i = i.Geometry
	except:
		pass
	if i.ToString() == "Rhino.Geometry.ArcCurve" and i.IsCircle():
		dsCircles.append(rhCircleToCircle(i))

#Assign your output to the OUT variable
OUT = dsCircles

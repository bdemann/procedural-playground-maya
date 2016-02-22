import maya.cmds as mc
import random

class Model:
	'Class for modeling things by itself before incorporating it into the model.'
		
	def __init__(self, dHeight):
		self.dHeight = dHeight
		
	def buildModel(self):
		line = mc.polyCube(d = 10, h = 1, w = 1, sx = 3)[0]
		
		pEx = mc.polyExtrudeFacet(line + ".f[6:8]", keepFacesTogether=1, pvx=0, pvy=0, pvz=-5, divisions=1)[0]
		mc.setAttr(pEx + ".localTranslate", 0, 0, 1, type="double3")
		
		pEx = mc.polyExtrudeFacet(line + ".f[0:2]", keepFacesTogether=1, pvx=0, pvy=0, pvz=-5, divisions=1)[0]
		mc.setAttr(pEx + ".localTranslate", 0, 0, 1, type="double3")
		
		mc.select(line + ".f[16]")
		mc.select(line + ".f[20]", tgl = True)
		mc.select(line + ".f[24]", tgl = True)
		mc.select(line + ".f[28]", tgl = True)
		pEx = mc.polyExtrudeFacet()[0]
		mc.setAttr(pEx + ".localTranslate", 0, 0, 5, type="double3")
		
		exFace = mc.polyExtrudeFacet(line + ".f[4]")
		mc.setAttr(exFace[0] + ".localTranslate", 0, 0, -0.5, type="double3")
		
		dbHeight = 3
		dropBar = mc.polyCylinder(r = 0.15, height = dbHeight, sx = 20, sy = 1, sz = 1, ax = [0, 1, 0])[0]
		mc.move(0, dbHeight/2, 0, dropBar)
		hHeight = 3
		handle = mc.polyCylinder(r = 0.15, height = hHeight, sx = 20, sy = 1, sz = 1, ax = [1, 0, 0])[0]
		mc.move(0, dbHeight, 0, handle)
		
		self.name = mc.group(line, name = "zipline")
		return self.name
		
	def temp(self):
		print ""

model = Model(-3)
model.buildModel()

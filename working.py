import maya.cmds as mc
import random

class Model:
	'Class for modeling things by itself before incorporating it into the model.'
		
	def __init__(self, dHeight):
		self.dHeight = dHeight
		
	def buildModel(self):
		steps = range(0)
		numOfSteps = 7;
		stepDepth = 1;
		for i in range(numOfSteps):
			steps.append(mc.polyCube(w = 8, h = .5, d = 1)[0])
			y = i * (8.0 / numOfSteps)
			z = (i * (10.0 / numOfSteps)) + (stepDepth/2.0) -5
			mc.move(0, y, z)
		self.name = mc.group(steps, name = "stairs")
		return self.name
		
	def buildModel2(self):
		height = abs(self.dHeight)
		bars = range(0)
		numOfBars = height * 5
		width = 3.0
		for i in range(1, numOfBars + 1):
			bars.append(mc.polyCylinder(r = 0.1, height = width, sx = 20, sy = 1, sz = 1, ax = [1, 0, 0])[0])
			y = ((height * 8.0)/numOfBars) * i
			mc.move(0, y, 0)
		
		rails = range(0)
		for i in range(2):
			rails.append(mc.polyCylinder(r = 0.2, h = 8*height, sx = 20, sy = 1, sz = 1, ax = [0, 1, 0])[0])
			mc.move(pow(-1, i) * (width/2), height * 4.0, 0)
			
		supports = range(0)
		for i in range(2):
			supports.append(mc.polyCylinder(r = 0.2, h = 10, sx = 20, sy = 1, sz = 1, ax = [1, 0, 0])[0])
			mc.move(0, i * height * 8.0, 0)
		
		ladder = mc.group(bars, rails, supports)
		mc.move(0, 0, -5, ladder)
		mc.move(0, 0, 0, ladder + ".scalePivot", ladder + ".rotatePivot", absolute=True)
		
		path = mc.polyCube( w = 8, h = 1 , d = 10)[0]
		path = mc.group(path)
		
		self.name = mc.group(ladder, path, name = "ladder")
		
		if( self.dHeight < 0 ):
			mc.move(0, height * -8.0, 0, self.name, r = True)
			mc.rotate(0, 180, 0, self.name)
			#mc.polyCylinder()
			print "The dHeight is negative"
		else:
			mc.move(0, 0, 0, self.name, r = True)
			#mc.polyCube()
			print "The dHeight is positive"
		return self.name
		
model = Model(-3)
model.buildModel()
model.buildModel2()

mc.polyCube()
mc.rotate( 30, 45, 0 )
mc.move( 2, 0, 2, r=True )
mc.scale( 2, 1, 2, r=True )
mc.makeIdentity( apply=True, t=1, r=1, s=1, n=2 )

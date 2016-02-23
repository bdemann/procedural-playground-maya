import maya.cmds as mc
import random

		
def setShader(shaderName):
	mc.sets(e = True, forceElement = shaderName)

def createShader(type, name, r, g, b):
	shaderNode = mc.shadingNode(type, asShader = True, name = (name + "Shader"))
	shaderSet = mc.sets(renderable = True, noSurfaceShader = True, empty = True, name = name)
	mc.setAttr((shaderNode + ".color"), r, g, b, type = "double3")
	mc.defaultNavigation(connectToExisting = True, source = shaderNode, destination = shaderSet)
	return shaderSet
	
board = createShader("lambert", "boardColor", 0.871, 0.722, 0.529)
metal = createShader("phong", "metalColor", 0.827, 0.827, 0.827)
shape = createShader("lambert", "shapeColor", 0.5, 0.5, 0.5)

class Model:
	'Class for modeling things by itself before incorporating it into the model.'
	headSpace = 10
	
	def __init__(self, dHeight):
		self.dHeight = dHeight
		
	def buildModel(self):
		planks = range(0)
		numOfPlanks = 10;
		roofHeight = 8.0
		platformWidth = 10.0
		for i in range(0, numOfPlanks):
			planks.append(mc.polyCube(w = 8, h = .5, d = 1)[0])
			y = roofHeight - ((i/2) * (roofHeight / numOfPlanks))
			z = pow(-1, i) * (i * ((platformWidth/2.0) / numOfPlanks))
			mc.move(0, y, z)
			rotateX = pow(-1, i) * 45
			mc.rotate(rotateX, 0, 0)
			mc.move(0, (i/2) * -.15, 0, r = True, os = True)
			setShader(board)
		roof = mc.group(planks, name = "bridge")
		return roof
		
	def temp(self):
		plat = Platform()

model = Model(-3)
model.buildModel()

import maya.cmds as mc
import random
		
class Platform:
	'Playground platform'
	shapeCount = 0
	
	def __init__(self, up = False, down = False, left = False, right = False, height = 1):
		self.height = height
		self.up = up;
		self.down = down;
		self.left = left;
		self.right = right;
		self.visted = False;
		Platform.shapeCount += 1
		self.draw()
		
	def displayCount(self):
		print "Total Shapes %d" % Shape.shapeCount
		
	def displayShape(self):
		print self.sType
		
	def draw(self):
		self.name = mc.polyCube(w = 10, h = 1, d = 10, sx = 3, sz = 3)[0]
		
		if(self.up or self.down or self.right or self.left):
			mc.select(cl = True)
			if(self.up):
				mc.select(self.name + ".f[25]", tgl = True)
			if(self.left):
				mc.select(self.name + ".f[13]", tgl = True)
			if(self.down):
				mc.select(self.name + ".f[28]", tgl = True)
			if(self.right):
				mc.select(self.name + ".f[1]", tgl = True)
			exFace = mc.polyExtrudeFacet()
			mc.setAttr(exFace[0] + ".localTranslate", 0, 0, 3, type="double3")
		
	def getName(self):
		return self.name

shapes = range(3)

for i in range(3):
	shapes[i] = Platform()
	mc.move(i, i, i, shapes[i].getName())
	print shapes[i].getName()
	
colCount = 5;
rowCount = 6;
platform = [[0 for x in range(colCount)] for x in range(rowCount)]
for i in range(rowCount):
	row = "";
	for j in range(colCount):
		platform[i][j] = Platform(up = True, down = True, left = True, right = True);
		mc.move(i*16, 0, j*16, platform[i][j].getName())
		row = row + str(platform[i][j].getName())
	print row

def generateMaze(platforms):
	generateNeighbors(platforms, 0, 0)
	
def generateNeighbors(platforms, row, col):
	#Figure out up
	if(row == 0):
		up = False
	
	#Figure out right
	if(col + 1 >= len(platforms[0])):
		right = False
	
	#Figure out left
	
	#Figure out down
	platforms[row][col] = Platform(up = True, right = True)
	if(platform.hasUp()):
		generateNeighbors
	
	

def makeGear(radius, height, thickness, sections):
    inner = mc.polyPipe(r = 3.5, h = height, t = 1)
    gear = mc.polyPipe(r = radius, h = height, t = thickness)
    mc.setAttr(gear[1] + ".subdivisionsAxis", sections)
    for i in range(sections):
        if(i % 2 == 0):
            mc.select( gear[0] + ".f[" + str(i) + "]" )
            exFace = mc.polyExtrudeFacet(gear[0] + ".f[" + str(i + sections * 2) + "]")
            mc.setAttr(exFace[0] + ".localTranslate", 0, 0, 3, type="double3")
            mc.setAttr(exFace[0] + ".localScale", .75, 1, 1)
        if(i % 4 == 0):
            mc.select( gear[0] + ".f[" + str(i) + "]" )
            exFace = mc.polyExtrudeFacet(gear[0] + ".f[" + str(i) + "]")
            mc.setAttr(exFace[0] + ".localTranslate", 0, 0, radius - thickness - 3, type="double3")
            mc.setAttr(exFace[0] + ".localScale", .8, 1, 1)


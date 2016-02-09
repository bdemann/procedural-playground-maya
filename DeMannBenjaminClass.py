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
		
	def hasUp(self):
		return self.up
		
	def hasDown(self):
		return self.down
		
	def hasRight(self):
		return self.right
		
	def hasLeft(self):
		return self.left

# shapes = range(3)

# for i in range(3):
	# shapes[i] = Platform()
	# mc.move(i, i, i, shapes[i].getName())
	# print shapes[i].getName()
	
colCount = 5
rowCount = 5
# platform = [[0 for x in range(colCount)] for x in range(rowCount)]
# for i in range(rowCount):
	# row = "";
	# for j in range(colCount):
		# platform[i][j] = Platform(up = True, down = True, left = True, right = True);
		# mc.move(i*16, 0, j*16, platform[i][j].getName())
		# row = row + str(platform[i][j].getName())
	# print row

def generateMaze(platforms):
	generateNeighbors(platforms, 0, 0)
	for i in range(rowCount):
	row = "";
	for j in range(colCount):
		platform[i][j] = Platform(up = True, down = True, left = True, right = True);
		mc.move(i*16, 0, j*16, platform[i][j].getName())
		row = row + str(platform[i][j].getName())
	print row
	
def generateNeighbors(platforms, row, col):
	if(row > 5 or col > 5 or row < 0 or col < 0):
		return
	if(platforms[row][col] != 0):
		return
	
	#Figure out up
	if(row <= 0):
		up = False
	else:
		up = True
	
	#Figure out right
	if(col >= 5 - 1):
		right = False
	else:
		right = True
	
	#Figure out left
	if(col <= 0):
		left = False
	else:
		left = True
	
	#Figure out down
	if(row >= 5 -1):
		down = False
	else:
		down = True
		
	print "Row is " + str(row) + " Col is " + str(col)
		
	platforms[row][col] = Platform(up = up, right = right, left = left, down = down)
	platform = platforms[row][col]
	if(platform.hasRight()):
		generateNeighbors(platforms, row, col + 1)
	if(platform.hasDown()):
		generateNeighbors(platforms, row + 1, col)
	if(platform.hasLeft()):
		generateNeighbors(platforms, row, col - 1)
	if(platform.hasUp()):
		generateNeighbors(platforms, row - 1, col)
	

platform = [[0 for x in range(colCount)] for x in range(rowCount)]
generateMaze(platform)

# def makeGear(radius, height, thickness, sections):
    # inner = mc.polyPipe(r = 3.5, h = height, t = 1)
    # gear = mc.polyPipe(r = radius, h = height, t = thickness)
    # mc.setAttr(gear[1] + ".subdivisionsAxis", sections)
    # for i in range(sections):
        # if(i % 2 == 0):
            # mc.select( gear[0] + ".f[" + str(i) + "]" )
            # exFace = mc.polyExtrudeFacet(gear[0] + ".f[" + str(i + sections * 2) + "]")
            # mc.setAttr(exFace[0] + ".localTranslate", 0, 0, 3, type="double3")
            # mc.setAttr(exFace[0] + ".localScale", .75, 1, 1)
        # if(i % 4 == 0):
            # mc.select( gear[0] + ".f[" + str(i) + "]" )
            # exFace = mc.polyExtrudeFacet(gear[0] + ".f[" + str(i) + "]")
            # mc.setAttr(exFace[0] + ".localTranslate", 0, 0, radius - thickness - 3, type="double3")
            # mc.setAttr(exFace[0] + ".localScale", .8, 1, 1)
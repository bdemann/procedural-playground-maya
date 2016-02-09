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
			mc.setAttr(exFace[0] + ".localTranslate", 0, 0, 5, type="double3")
		
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
	
colCount = 20
rowCount = 50
# platform = [[0 for x in range(colCount)] for x in range(rowCount)]
# for i in range(rowCount):
	# row = "";
	# for j in range(colCount):
		# platform[i][j] = Platform(up = True, down = True, left = True, right = True);
		# mc.move(i*16, 0, j*16, platform[i][j].getName())
		# row = row + str(platform[i][j].getName())
	# print row

	
class Test:
	'Test class'
	
	def __init__(self, num = 1, num2 = 2, num3 = 1 + 2):
		self.num = num
		self.num2 = num2
		self.num3 = num3
		self.hConnect = range(0)
		self.vConnect = range(0)
		self.hConnect.append(1)
		self.hConnect.append(7)
		self.hConnect.append(37)
		print self.num3
		print self.hConnect

test = Test(5, 5)
	
class Maze:
	'Playground maze'
	
	def __init__(self, rowCount = 5, colCount = 5):
		#Set all entries in maze to 0 and use 0 to represent an uncreated platform
		self.platforms = [[0 for x in range(colCount)] for x in range(rowCount)]
		self.hConnect = range(0)
		self.vConnect = range(0)
		self.rowCount = rowCount
		self.colCount = colCount
	
	def generateMaze(self):
		self.generateNeighbors(0, 0)
		print "Number of rows "  + str(self.rowCount)
		print "Number of columns " + str(self.colCount)
		for i in range(self.rowCount):
			for j in range(self.colCount):
				if(self.platforms[i][j] != 0):
					mc.select(self.platforms[i][j].getName());
					mc.move(i*-20, 0, j*20, self.platforms[i][j].getName())
			
	def generateNeighbors(self, row, col):
		if(row > self.rowCount or col > self.colCount or row < 0 or col < 0):
			return
		if(self.platforms[row][col] != 0):
			return
		
		#Figure out up
		if(row <= 0):
			up = False
		else:
			platAbove = self.platforms[row - 1][col]
			#Check if there is platfrom to the north
			if(platAbove != 0):
				if(platAbove.hasDown()):
					up = True
				else:
					up = False
			else:
				#randomly generate if it goes north.
				up = random.choice([True, False])
		
		#Figure out right
		if(col >= self.colCount - 1):
			right = False
		else:
			platRight = self.platforms[row][col + 1]
			#Check if there is platfrom to the north
			if(platRight != 0):
				if(platRight.hasLeft()):
					right = True
				else:
					right = False
			else:
				#randomly generate if it goes north.
				right = random.choice([True, False])
		
		#Figure out left
		if(col <= 0):
			left = False
		else:
			platLeft = self.platforms[row][col - 1]
			#Check if there is platfrom to the north
			if(platLeft != 0):
				if(platLeft.hasRight()):
					left = True
				else:
					left = False
			else:
				#randomly generate if it goes north.
				left = random.choice([True, False])
		
		#Figure out down
		if(row >= self.rowCount - 1):
			down = False
		else:
			platBelow = self.platforms[row + 1][col]
			#Check if there is platfrom to the north
			if(platBelow != 0):
				if(platBelow.hasUp()):
					down = True
				else:
					down = False
			else:
				#randomly generate if it goes north.
				down = random.choice([True, False])
			
		print "Row is " + str(row) + " Col is " + str(col)
			
		self.platforms[row][col] = Platform(up = up, right = right, left = left, down = down)
		platform = self.platforms[row][col]
		if(platform.hasRight()):
			self.generateNeighbors(row, col + 1)
		if(platform.hasDown()):
			self.generateNeighbors(row + 1, col)
		if(platform.hasLeft()):
			self.generateNeighbors(row, col - 1)
		if(platform.hasUp()):
			self.generateNeighbors(row - 1, col)
	
maze = Maze(rowCount = rowCount, colCount = colCount)
maze.generateMaze()
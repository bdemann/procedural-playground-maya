import maya.cmds as mc
import random
		
class Platform:
	'Playground platform'
	platCount = 0
	
	def __init__(self, north = False, south = False, west = False, east = False, height = 1):
		self.height = height
		self.north = north;
		self.south = south;
		self.west = west;
		self.east = east;
		self.visted = False;
		Platform.platCount += 1
		self.draw()
		
	def displayCount(self):
		print "Total Platforms %d" % Platform.platCount
		
	def draw(self):
		base = range(1)
		base[0] = mc.polyCube(w = 10, h = 1, d = 10, sx = 3, sz = 3)[0]
		
		supports = range(4);
		for i in supports:
			supports[i] = mc.polyCube(h = 15)[0]
			mc.move(pow(-1, i/2) * 5, 0, pow(-1, i) * 5)
		self.name = mc.group(supports, base)
		
		# if(self.north or self.south or self.east or self.west):
			# mc.select(cl = True)
			# if(self.north):
				# mc.select(self.name + ".f[25]", tgl = True)
			# if(self.west):
				# mc.select(self.name + ".f[13]", tgl = True)
			# if(self.south):
				# mc.select(self.name + ".f[28]", tgl = True)
			# if(self.east):
				# mc.select(self.name + ".f[1]", tgl = True)
			# exFace = mc.polyExtrudeFacet()
			# mc.setAttr(exFace[0] + ".localTranslate", 0, 0, 5, type="double3")
		
	def getName(self):
		return self.name
		
	def hasNorth(self):
		return self.north
		
	def hasSouth(self):
		return self.south
		
	def hasEast(self):
		return self.east
		
	def hasWest(self):
		return self.west
	
class Connection:
	'Connection between two playgound platforms'
	conCount = 0
	
	def __init__(self, pRow, pCol):
		self.pRow = pRow
		self.pCol = pCol
		#print "Adding to [" + str(pRow) + "][" + str(pCol) + "]"
		Connection.conCount += 1
		
	def displayCount(self):
		print "Total Connections %d" % Connection.platCount
		
	def draw(self, seed):
		if(random.randint(1, 2) == 1):
			self.makeBridge()
		else:
			self.makeMonkeyBars()
	
	def makeBridge(self):
		planks = range(0)
		numOfPlanks = 7;
		for i in range(1, numOfPlanks + 1):
			planks.append(mc.polyCube(w = 8, h = .5, d = 1)[0])
			y = -.3 + (i/2)/10.0
			z = pow(-1, i) * ((i/2)/(numOfPlanks * 1.0) * 10)
			mc.move(0, y, z)
			rotateX = pow(-1, i) * (i/2) * -2
			mc.rotate(rotateX, 0, 0)
		return mc.group(planks)

	def makeMonkeyBars(self):
		bars = range(0)
		numOfBars = 5
		width = 3.0
		for i in range(1, numOfBars + 1):
			bars.append(mc.polyCylinder(r = 0.1, height = width, sx = 20, sy = 1, sz = 1, ax = [1, 0, 0])[0])
			z = pow(-1, i) * ((i/2)/((numOfBars + 1) * 1.0) * 10)
			mc.move(0, 5, z)
		
		rails = range(0)
		for i in range(2):
			rails.append(mc.polyCylinder(r = 0.2, h = 10, sx = 20, sy = 1, sz = 1, ax = [0, 0, 1])[0])
			mc.move(pow(-1, i) * (width/2), 5, 0)
			
		supports = range(0)
		for i in range(2):
			supports.append(mc.polyCylinder(r = 0.2, h = 10, sx = 20, sy = 1, sz = 1, ax = [1, 0, 0])[0])
			mc.move(0, 5, pow(-1, i) * 5)
		return mc.group(bars, rails, supports)
	
class Maze:
	'Playground maze'
	
	def __init__(self, rowCount = 5, colCount = 5):
		#Set all entries in maze to 0 and use 0 to represent an uncreated platform
		self.platforms = [[0 for x in range(colCount)] for x in range(rowCount)]
		self.hConnect = [[0 for x in range(colCount - 1)] for x in range(rowCount)]
		self.vConnect = [[0 for x in range(colCount)] for x in range(rowCount - 1)]
		self.rowCount = rowCount
		self.colCount = colCount
	
	def generateMaze(self):
		self.generateNeighbors(0, 0)
		for i in range(self.rowCount):
			for j in range(self.colCount):
				if(self.platforms[i][j] != 0):
					mc.select(self.platforms[i][j].getName());
					mc.move(i*-20, 0, j*20, self.platforms[i][j].getName())
				if(j < self.colCount -1 and self.hConnect[i][j] != 0):
					self.hConnect[i][j].draw(0)
					mc.move((self.hConnect[i][j].pRow*-20), 0, (self.hConnect[i][j].pCol*20) + 10)	
				if(i < self.rowCount -1 and self.vConnect[i][j] != 0):
					self.vConnect[i][j].draw(1)
					mc.move((self.vConnect[i][j].pRow*-20) - 10, 0, (self.vConnect[i][j].pCol*20))
					mc.rotate(0, 90, 0)
	
	def northChoice(self, row, col):
		if(row <= 0):
			return False
		else:
			platNorth = self.platforms[row - 1][col]
			#Check if there is platfrom to the north
			if(platNorth != 0):
				if(platNorth.hasSouth()):
					return True
				else:
					return False
			else:
				return self.coinFlip()
	
	def eastChoice(self, row, col):
		if(col >= self.colCount - 1):
			return False
		else:
			platEast = self.platforms[row][col + 1]
			#Check if there is platfrom to the east
			if(platEast != 0):
				if(platEast.hasWest()):
					return True
				else:
					return False
			else:
				return self.coinFlip()
	
	def westChoice(self, row, col):
		if(col <= 0):
			return False
		else:
			platWest = self.platforms[row][col - 1]
			#Check if there is platfrom to the west
			if(platWest != 0):
				if(platWest.hasEast()):
					return True
				else:
					return False
			else:
				return self.coinFlip()
	
	def southChoice(self, row, col):
		if(row >= self.rowCount - 1):
			return False
		else:
			platSouth = self.platforms[row + 1][col]
			#Check if there is platfrom to the south
			if(platSouth != 0):
				if(platSouth.hasNorth()):
					return True
				else:
					return False
			else:
				return self.coinFlip()
	
	def coinFlip(self):
		return random.choice([True, False])
	
	#returns true if there is a neighbor
	def generateNeighbors(self, row, col):
		if(row > self.rowCount or col > self.colCount or row < 0 or col < 0):
			return False
		if(self.platforms[row][col] != 0):
			return True
		
		#Figure out north
		north = self.northChoice(row, col)
		#Figure out east
		east = self.eastChoice(row, col)
		#Figure out west
		west = self.westChoice(row, col)
		#Figure out south
		south = self.southChoice(row, col)
			
		self.platforms[row][col] = Platform(north = north, east = east, west = west, south = south)
		platform = self.platforms[row][col]
		if(platform.hasEast()):
			if(self.generateNeighbors(row, col + 1) and col < self.colCount -1):
				print "Making East conn from [" + str(row) + "][" + str(col) + "] to [" + str(row) + "][" + str(col + 1) + "]"
				self.hConnect[row][col] = Connection(row, col)
		if(platform.hasSouth()):
			if(self.generateNeighbors(row + 1, col) and row < self.rowCount -1):
				print "Making South conn from [" + str(row) + "][" + str(col) + "] to [" + str(row + 1) + "][" + str(col) + "]"
				self.vConnect[row][col] = Connection(row, col)
		if(platform.hasWest()):
			if(self.generateNeighbors(row, col - 1) and col < self.colCount -1):
				print "Making West conn from [" + str(row) + "][" + str(col - 1) + "] to [" + str(row) + "][" + str(col) + "]"
				self.hConnect[row][col - 1] = Connection(row, col - 1)
		if(platform.hasNorth()):
			if(self.generateNeighbors(row - 1, col) and row < self.rowCount -1):
				print "Making North conn from [" + str(row -1 ) + "][" + str(col) + "] to [" + str(row) + "][" + str(col) + "]"
				self.vConnect[row - 1][col] = Connection(row - 1, col)
			
		return True

		
colCount = 5
rowCount = 5
maze = Maze(rowCount = rowCount, colCount = colCount)
maze.generateMaze()
print "Platforms: " + str(Platform.platCount)
print "Connections: " + str(Connection.conCount)
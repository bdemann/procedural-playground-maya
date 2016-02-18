import maya.cmds as mc
import random
		
class Platform:
	'Playground platform'
	platCount = 0
	headSpace = 10
	
	def __init__(self, north = False, south = False, west = False, east = False, height = 1):
		self.height = height
		self.north = north;
		self.south = south;
		self.west = west;
		self.east = east;
		self.visted = False;
		Platform.platCount += 1
		if(random.randint(1, 2) == 1):
			self.hasShape = True
		else:
			self.hasShape = False
		self.draw()
		
	def displayCount(self):
		print "Total Platforms %d" % Platform.platCount
		
	def draw(self):
		base = range(1)
		base[0] = mc.polyCube(w = 10, h = 1, d = 10, sx = 3, sz = 3)[0]
		mc.move(0, 8 * self.height, 0)
		print 8 * self.height
		shapes = range(0)
		if(self.hasShape):
			if(random.randint(1, 2) == 1):
				shapes.append(mc.polyCube()[0])
			else:
				shapes.append(mc.polyPyramid()[0])
			mc.expression( s = shapes[0] + ".rotateX = frame")
			mc.expression( s = shapes[0] + ".rotateY = frame")
			mc.expression( s = shapes[0] + ".rotateZ = frame")
			mc.move(0, (8 * self.height) + 1.5, 0, shapes[0])
		
		supports = range(4);
		for i in supports:
			height = (8 * self.height) + Platform.headSpace
			supports[i] = mc.polyCube(h = height)[0]
			yMove = (Platform.headSpace - (height - 1) / 2.0) + (8 * self.height)
			mc.move(pow(-1, i/2) * 5, yMove, pow(-1, i) * 5)
		self.name = mc.group(supports, base, shapes, name = "platform")
		
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
		self.name = "connection"
		
	def displayCount(self):
		print "Total Connections %d" % Connection.platCount
		
	def draw(self, seed):
		if(random.randint(1, 2) == 1):
			self.makeBridge()
		else:
			self.makeMonkeyBars()
	
	def getName(self):
		return self.name
	
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
		self.name = mc.group(planks, name = "bridge")
		return self.name

	def makeMonkeyBars(self):
		bars = range(0)
		numOfBars = 5
		width = 3.0
		for i in range(1, numOfBars + 1):
			bars.append(mc.polyCylinder(r = 0.1, height = width, sx = 20, sy = 1, sz = 1, ax = [1, 0, 0])[0])
			z = pow(-1, i) * ((i/2)/((numOfBars + 1) * 1.0) * 10)
			mc.move(0, 0, z)
		
		rails = range(0)
		for i in range(2):
			rails.append(mc.polyCylinder(r = 0.2, h = 10, sx = 20, sy = 1, sz = 1, ax = [0, 0, 1])[0])
			mc.move(pow(-1, i) * (width/2), 0, 0)
			
		supports = range(0)
		for i in range(2):
			supports.append(mc.polyCylinder(r = 0.2, h = 10, sx = 20, sy = 1, sz = 1, ax = [1, 0, 0])[0])
			mc.move(0, 0, pow(-1, i) * 5)
		monkeyBars = mc.group(bars, rails, supports)
		mc.move(0, Platform.headSpace - 2, 0, monkeyBars, r = True)
		self.name = mc.group(monkeyBars, name = "monkeyBars")
		return self.name
	
class Maze:
	'Playground maze'
	
	def __init__(self, rowCount = 5, colCount = 5):
		#Set all entries in maze to 0 and use 0 to represent an uncreated platform
		self.platforms = [[0 for x in range(colCount)] for x in range(rowCount)]
		self.hConnect = [[0 for x in range(colCount - 1)] for x in range(rowCount)]
		self.vConnect = [[0 for x in range(colCount)] for x in range(rowCount - 1)]
		self.rowCount = rowCount
		self.colCount = colCount
		self.camera = mc.camera()[0]
		mc.move(0, 5, 0, self.camera)
		self.time = 1
		self.name = mc.group(self.camera, name = "maze")
	
	def generateMaze(self):
		self.generateNeighbors(0, 0)
		for i in range(self.rowCount):
			for j in range(self.colCount):
				if(self.platforms[i][j] != 0):
					mc.select(self.platforms[i][j].getName());
					mc.move(i*-20, 0, j*20, self.platforms[i][j].getName())
					mc.parent(self.platforms[i][j].getName(), self.name)
				if(j < self.colCount -1 and self.hConnect[i][j] != 0):
					self.hConnect[i][j].draw(0)
					mc.move((self.hConnect[i][j].pRow*-20), self.platforms[i][j].height * 8, (self.hConnect[i][j].pCol*20) + 10)
					mc.parent(self.hConnect[i][j].getName(), self.name)
				if(i < self.rowCount -1 and self.vConnect[i][j] != 0):
					self.vConnect[i][j].draw(1)
					mc.move((self.vConnect[i][j].pRow*-20) - 10, self.platforms[i][j].height * 8, (self.vConnect[i][j].pCol*20))
					mc.rotate(0, 90, 0)
					mc.parent(self.vConnect[i][j].getName(), self.name)
	
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
	
	def cameraKeyframe(self, time):
		self.time += time
		mc.setKeyframe(self.camera, t = self.time)
	
	def cameraTurn(self, direction):
		if(direction == "north"):
			rotation = -90
		elif(direction == "west"):
			rotation = 0
		elif(direction == "south"):
			rotation = 90
		elif(direction == "east"):
			rotation = 180
		mc.rotate(0, rotation, 0, self.camera)
		self.cameraKeyframe(20)
		
	def cameraMove(self, x, z):
		height = (self.platforms[x][z].height * 8) + 2.5
		mc.move(x*-20, height, z*20, self.camera)
		self.cameraKeyframe(120)
		# if(self.platforms[x][z].hasShape):
			# mc.rotate(180, 0, 0, self.camera)
			# self.cameraKeyframe(45)
	
	def traverseMaze(self):
		self.visitBlock(0, 0);
		
	def visitBlock(self, row, col):
		if(row > self.rowCount or col > self.colCount or row < 0 or col < 0):
			return False
		if(self.platforms[row][col].visted):
			return False
			
		platform = self.platforms[row][col]
		platform.visted = True
		self.cameraMove(row, col)
		if(platform.hasEast() and not self.platforms[row][col + 1].visted):
			self.cameraTurn("east")
			if(self.visitBlock(row, col + 1) and col < self.colCount -1):
				self.cameraTurn("west")
				self.cameraMove(row, col)
		if(platform.hasSouth() and not self.platforms[row + 1][col].visted):
			self.cameraTurn("south")
			if(self.visitBlock(row + 1, col) and row < self.rowCount -1):
				self.cameraTurn("north")
				self.cameraMove(row, col)
		if(platform.hasWest() and not self.platforms[row][col - 1].visted):
			self.cameraTurn("west")
			if(self.visitBlock(row, col - 1) and col < self.colCount -1):
				self.cameraTurn("east")
				self.cameraMove(row, col)
		if(platform.hasNorth() and not self.platforms[row - 1][col].visted):
			self.cameraTurn("north")
			if(self.visitBlock(row - 1, col) and row < self.rowCount -1):
				self.cameraTurn("south")
				self.cameraMove(row, col)
			
		platform.visted = False
		return True
	
	#returns true if there is a neighbor
	def generateNeighbors(self, row, col):
		if(row > self.rowCount or col > self.colCount or row < 0 or col < 0):
			return False
		if(self.platforms[row][col] != 0):
			#~ if(not self.platforms[row][col].visted):
				#~ self.cameraMove(row, col)
			return True
		
		#Figure out north
		north = self.northChoice(row, col)
		#Figure out east
		east = self.eastChoice(row, col)
		#Figure out west
		west = self.westChoice(row, col)
		#Figure out south
		south = self.southChoice(row, col)
			
		self.platforms[row][col] = Platform(north = north, east = east, west = west, south = south, height = 3)
		platform = self.platforms[row][col]
		#~ platform.visted = True
		#~ self.cameraMove(row, col)
		if(platform.hasEast()):
			#~ self.cameraTurn("east")
			if(self.generateNeighbors(row, col + 1) and col < self.colCount -1):
				print "Making East conn from [" + str(row) + "][" + str(col) + "] to [" + str(row) + "][" + str(col + 1) + "]"
				self.hConnect[row][col] = Connection(row, col)
				#~ self.cameraTurn("west")
				#~ self.cameraMove(row, col)
		if(platform.hasSouth()):
			#~ self.cameraTurn("south")
			if(self.generateNeighbors(row + 1, col) and row < self.rowCount -1):
				print "Making South conn from [" + str(row) + "][" + str(col) + "] to [" + str(row + 1) + "][" + str(col) + "]"
				self.vConnect[row][col] = Connection(row, col)
				#~ self.cameraTurn("north")
				#~ self.cameraMove(row, col)
		if(platform.hasWest()):
			#~ self.cameraTurn("west")
			if(self.generateNeighbors(row, col - 1) and col < self.colCount -1):
				print "Making West conn from [" + str(row) + "][" + str(col - 1) + "] to [" + str(row) + "][" + str(col) + "]"
				self.hConnect[row][col - 1] = Connection(row, col - 1)
				#~ self.cameraTurn("east")
				#~ self.cameraMove(row, col)
		if(platform.hasNorth()):
			#~ self.cameraTurn("north")
			if(self.generateNeighbors(row - 1, col) and row < self.rowCount -1):
				print "Making North conn from [" + str(row -1 ) + "][" + str(col) + "] to [" + str(row) + "][" + str(col) + "]"
				self.vConnect[row - 1][col] = Connection(row - 1, col)
				#~ self.cameraTurn("south")
				#~ self.cameraMove(row, col)
			
		#~ platform.visted = False
		return True

		
colCount = 5
rowCount = 5
maze = Maze(rowCount = rowCount, colCount = colCount)
maze.generateMaze()
maze.traverseMaze()
mc.playbackOptions(max = maze.time)
print "Platforms: " + str(Platform.platCount)
print "Connections: " + str(Connection.conCount)

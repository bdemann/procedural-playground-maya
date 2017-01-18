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
grass = createShader("lambert", "grassColor", 0.350, 0.550, 0.350)
roofShader = createShader("lambert", "roofColor", 0.5, 0.0365, 0.0365)

colCount = int(raw_input())
rowCount = int(raw_input())
maxHeight = int(raw_input())

mc.polyPlane(w = 20 * rowCount, h = 20 * colCount, ax = (0, 1, 0))
setShader(grass)
mc.move((rowCount - 1) * -10, .1, (colCount -1) * 10)
	
class Platform:
	'Playground platform'
	platCount = 0
	headSpace = 10
	heightFactor = 8
	
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
		base[0] = self.makeBase()
		setShader(board)
		
		roof = range(1)
		roof[0] = self.makeRoof()
		mc.move(0, 4, 0)
		setShader(roofShader)
		
		shapes = range(0)
		if(self.hasShape):
			if(random.randint(1, 2) == 1):
				shapes.append(mc.polyCube(name = "mazeShape")[0])
			else:
				shapes.append(mc.polyPyramid(name = "mazeShape")[0])
			mc.expression( s = shapes[0] + ".rotateX = frame")
			mc.expression( s = shapes[0] + ".rotateY = frame")
			mc.expression( s = shapes[0] + ".rotateZ = frame")
			mc.move(0, 0 + 2.5, 0, shapes[0])
			setShader(shape)
		
		supports = range(4);
		for i in supports:
			height = (Platform.heightFactor * self.height) + Platform.headSpace
			supports[i] = mc.polyCube(h = height)[0]
			yMove = (Platform.headSpace - (height - 1) / 2.0) + 0
			mc.move(pow(-1, i/2) * 5, yMove, pow(-1, i) * 5)
			setShader(board)
		
		walls = range(0)
		if(not self.north):
			walls.append(self.buildWall())
			mc.move(5, 0, 0)
			mc.rotate(0, 90, 0)
			setShader(metal)
		if(not self.south):
			walls.append(self.buildWall())
			mc.move(-5, 0, 0)
			mc.rotate(0, 90, 0)
			setShader(metal)
		if(not self.west):
			walls.append(self.buildWall())
			mc.move(0, 0, -5)
			setShader(metal)
		if(not self.east):
			walls.append(self.buildWall())
			mc.move(0, 0, 5)
			setShader(metal)
			
		self.name = mc.group(supports, base, roof, shapes, walls, name = "platform")
		mc.move(0, (Platform.heightFactor * self.height), 0, self.name)
		mc.makeIdentity(self.name, apply = True, t = 1, s = 1, n = 2)
	
	def makeBase(self):
		numOfBoards = 10
		boardWidth = .9
		boards = range(0)
		for i in range(numOfBoards):
			boardLen = random.randint(1, 9)
			boards.append(mc.polyCube(w = boardWidth, h = .5, d = boardLen)[0])
			z = 5 - boardLen / 2.0
			x = (i * (10.0 / numOfBoards)) + (boardWidth/2.0) -5
			mc.move(x, 0, z)
			boardLen = 9.9 - boardLen
			boards.append(mc.polyCube(w = boardWidth, h = .5, d = boardLen)[0])
			z = boardLen / 2.0 - 5
			mc.move(x, 0, z)
			
		supports = range(0)
		supports.append(mc.polyCube(h = .5, w = boardWidth, d = 10)[0])
		mc.move(0, -.5, -5)
		mc.rotate(0, 90, 0)
		supports.append(mc.polyCube(h = .5, w = boardWidth, d = 10)[0])
		mc.move(0, -.5, 5)
		mc.rotate(0, 90, 0)
		supports.append(mc.polyCube(h = .5, w = boardWidth, d = 9)[0])
		mc.move(-5, -.5, 0)
		supports.append(mc.polyCube(h = .5, w = boardWidth, d = 9)[0])
		mc.move(5, -.5, 0)
		
		base = mc.group(boards, supports, name = "base")
		setShader(board)
		return base
	
	def makeRoof(self):
		planks = range(0)
		numOfPlanks = 16;
		roofHeight = 12.0
		platformWidth = 15.0
		for i in range(0, numOfPlanks):
			planks.append(mc.polyCube(w = 14, h = .5, d = 1)[0])
			y = roofHeight - ((i/2) * (roofHeight / numOfPlanks))
			z = pow(-1, i) * (i * ((platformWidth/2.0) / numOfPlanks))
			mc.move(0, y, z)
			rotateX = pow(-1, i) * 45
			mc.rotate(rotateX, 0, 0)
			mc.move(0, (i/2) * -.15, 0, r = True, os = True)
			setShader(board)
		roof = mc.group(planks, name = "bridge")
		return roof
	
	def buildWall(self):
		rail = range(1)
		rail[0] = mc.polyCylinder(r = 0.1, height = 10, sx = 20, sy = 1, sz = 1, ax = [1, 0, 0])[0];
		railHeight = 5.0
		mc.move(0, railHeight, 0)
		numOfBars = 7
		bars = range(numOfBars)
		for i in range(1, numOfBars + 1):
			bars[i - 1] = mc.polyCylinder(r = 0.1, height = 5, sx = 20, sy = 1, sz = 1, ax = [0, 1, 0])[0]
			x = pow(-1, i) * ((i/2)/((numOfBars + 1) * 1.0) * 10)
			mc.move(x, railHeight/2.0, 0)
		return mc.group(rail, bars, name = "wall")
	
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
	
	def __init__(self, pRow, pCol, height, dHeight, direction):
		self.pRow = pRow
		self.pCol = pCol
		self.height = height
		self.dHeight = dHeight
		self.direction = direction
		#print "Adding to [" + str(pRow) + "][" + str(pCol) + "]"
		Connection.conCount += 1
		self.name = "connection"
		
	def displayCount(self):
		print "Total Connections %d" % Connection.platCount
		
	def draw(self):
		if(self.dHeight == 0):
			opt = random.randint(1, 3)
			if(opt == 1):
				self.makeBridge()
			elif(opt == 2):
				self.makeMonkeyBars()
			elif(opt == 3):
				self.makeZipLine()
		elif(abs(self.dHeight) == 1):
			self.makeStairs()
		else:
			self.makeLadder()
		mc.move(0, self.height * Platform.heightFactor, 0, self.name)
		if(self.direction == "north"):
			mc.rotate(0, 90, 0)
		elif(self.direction == "south"):
			mc.rotate(0, -90, 0)
		elif(self.direction == "west"):
			mc.rotate(0, 180, 0)
		elif(self.direction == "east"):
			mc.rotate(0, 0, 0)
		mc.makeIdentity(self.name, apply = True, t = 1, r = 1, s = 1, n = 2)
	
	def getName(self):
		return self.name
	
	def makeLadder(self):
		height = abs(self.dHeight)
		bars = range(0)
		numOfBars = height * 5
		width = 3.0
		for i in range(1, numOfBars + 1):
			bars.append(mc.polyCylinder(r = 0.1, height = width, sx = 20, sy = 1, sz = 1, ax = [1, 0, 0])[0])
			y = ((height * 8.0)/numOfBars) * i
			mc.move(0, y, 0)
			setShader(metal)
		
		rails = range(0)
		for i in range(2):
			rails.append(mc.polyCylinder(r = 0.2, h = 8*height, sx = 20, sy = 1, sz = 1, ax = [0, 1, 0])[0])
			mc.move(pow(-1, i) * (width/2), height * 4.0, 0)
			setShader(metal)
			
		supports = range(0)
		for i in range(2):
			supports.append(mc.polyCylinder(r = 0.2, h = 10, sx = 20, sy = 1, sz = 1, ax = [1, 0, 0])[0])
			mc.move(0, i * height * 8.0, 0)
			setShader(metal)
		
		ladder = mc.group(bars, rails, supports)
		mc.move(0, 0, 5, ladder)
		
		path = mc.polyCube( w = 4, h = 1 , d = 10)[0]
		path = mc.group(path)
		setShader(board)
		
		self.name = mc.group(ladder, path, name = "ladder")
		
		# if( self.dHeight < 0 ):
			# mc.move(0, height * -8.0, 0, self.name, r = True)
			# mc.rotate(0, 180, 0, self.name)
			# print "The dHeight is negative"
		# else:
			# print "The dHeight is positive"
		
		mc.move(0, 0, 0, self.name + ".scalePivot", self.name + ".rotatePivot", absolute=True)
		
		return self.name
	
	def makeStairs(self):
		steps = range(0)
		numOfSteps = 7;
		stepDepth = 1;
		for i in range(numOfSteps):
			steps.append(mc.polyCube(w = 8, h = .5, d = 1)[0])
			y = i * (8.0 / numOfSteps)
			z = (i * (10.0 / numOfSteps)) + (stepDepth/2.0) -5
			mc.move(0, y, z)
			setShader(board)
		self.name = mc.group(steps, name = "stairs")
		mc.move(0, 0, 0, self.name + ".scalePivot", self.name + ".rotatePivot", absolute=True)
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
			setShader(board)
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
			setShader(metal)
		
		rails = range(0)
		for i in range(2):
			rails.append(mc.polyCylinder(r = 0.2, h = 10, sx = 20, sy = 1, sz = 1, ax = [0, 0, 1])[0])
			mc.move(pow(-1, i) * (width/2), 0, 0)
			setShader(metal)
			
		supports = range(0)
		for i in range(2):
			supports.append(mc.polyCylinder(r = 0.2, h = 10, sx = 20, sy = 1, sz = 1, ax = [1, 0, 0])[0])
			mc.move(0, 0, pow(-1, i) * 5)
			setShader(metal)
		monkeyBars = mc.group(bars, rails, supports)
		mc.move(0, Platform.headSpace - 2, 0, monkeyBars, r = True)
		self.name = mc.group(monkeyBars, name = "monkeyBars")
		return self.name
	
	def makeZipLine(self):
		line = mc.polyCube(d = 9, h = 1, w = 1, sx = 3)[0]
		setShader(board)
		
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
		setShader(board)
		
		exFace = mc.polyExtrudeFacet(line + ".f[10]")
		mc.setAttr(exFace[0] + ".localTranslate", 0, 0, -0.5, type="double3")
		setShader(metal)
		
		dbHeight = 2
		dropBar = mc.polyCylinder(r = 0.15, height = dbHeight, sx = 20, sy = 1, sz = 1, ax = [0, 1, 0])[0]
		mc.move(0, -1 * dbHeight/2, 0, dropBar)
		hHeight = 3
		handle = mc.polyCylinder(r = 0.15, height = hHeight, sx = 20, sy = 1, sz = 1, ax = [1, 0, 0])[0]
		mc.move(0, -1 * dbHeight, 0, handle)
		zip = mc.group(dropBar, handle)
		setShader(metal)
		handleBar = mc.group(zip)
		
		zipLine = mc.group(line, handleBar, name = "zipline")
		mc.move(0, Platform.headSpace - 1.5, 0, zipLine, r = True)
		self.name = mc.group(zipLine, name = "zipline")
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
		self.camOri = 1 # This variable will hold whether the camera is upside down or not. 1 = right side up -1 = up side down
		mc.move(0, 5, 0, self.camera)
		self.time = 1
		self.name = mc.group(self.camera, name = "maze")
	
	def generateMaze(self):
		self.generateNeighbors(0, 0, south = True, east = True)
		if(self.platforms[self.rowCount - 1][self.colCount - 1] == 0):
			self.generateNeighbors(self.rowCount - 1, self.colCount - 1)
		for i in range(self.rowCount):
			for j in range(self.colCount):
				if(self.platforms[i][j] != 0):
					#move the platform into the correct location
					mc.select(self.platforms[i][j].getName());
					mc.move(i*-20, 0, j*20, self.platforms[i][j].getName())
					mc.parent(self.platforms[i][j].getName(), self.name)
				if(j < self.colCount -1 and self.hConnect[i][j] != 0):
					#create any horizontal connection at this location
					self.hConnect[i][j].draw()
					mc.move((self.hConnect[i][j].pRow*-20), 0, (self.hConnect[i][j].pCol*20) + 10)
					# if(self.platforms[i][j].height < self.platforms[i][j + 1]):
						# mc.rotate(0, 180, 0)
					mc.parent(self.hConnect[i][j].getName(), self.name)
				if(i < self.rowCount -1 and self.vConnect[i][j] != 0):
					#create any vertical connections at this point.
					self.vConnect[i][j].draw()
					mc.move((self.vConnect[i][j].pRow*-20) - 10, 0, (self.vConnect[i][j].pCol*20))
					#mc.rotate(0, 90, 0)
					# if(self.platforms[i][j].height < self.platforms[i+1][j]):
						# mc.rotate(0, 180, 0, r = True)
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
		mc.setAttr(self.camera + '.ry', rotation)
		self.cameraKeyframe(20)
		
	def cameraMove(self, x, z):
		height = (self.platforms[x][z].height * 8) + 4.5
		mc.move(x*-20, height, z*20, self.camera)
		self.cameraKeyframe(120)
		# if(self.platforms[x][z].hasShape):
		#mc.setAttr(self.camera + '.localRotateZ', 180)
			# self.camOri *= -1
			# mc.rotate(0, 0, 180, self.camera, r = True, os=True)
			# self.cameraKeyframe(45)
	
	def traverseMaze(self):
		self.visitBlock(0, 0);
		
	def visitBlock(self, row, col):
		platform = self.platforms[row][col]
		platform.visted = True
		self.cameraMove(row, col)
		if(platform.hasEast() and not self.platforms[row][col + 1].visted):
			self.cameraTurn("east")
			self.visitBlock(row, col + 1)
			self.cameraTurn("west")
			self.cameraMove(row, col)
		if(platform.hasSouth() and not self.platforms[row + 1][col].visted):
			self.cameraTurn("south")
			self.visitBlock(row + 1, col)
			self.cameraTurn("north")
			self.cameraMove(row, col)
		if(platform.hasWest() and not self.platforms[row][col - 1].visted):
			self.cameraTurn("west")
			self.visitBlock(row, col - 1)
			self.cameraTurn("east")
			self.cameraMove(row, col)
		if(platform.hasNorth() and not self.platforms[row - 1][col].visted):
			self.cameraTurn("north")
			self.visitBlock(row - 1, col)
			self.cameraTurn("south")
			self.cameraMove(row, col)
			
		return True
	
	#returns true if there is a neighbor
	def generateNeighbors(self, row, col, north = False, south = False, east = False, west = False):
		if(row > self.rowCount or col > self.colCount or row < 0 or col < 0):
			return False
		if(self.platforms[row][col] != 0):
			return True
		
		# Determine if the platform has neighborining platforms unless the user said there for sure will be 
		#Figure out north
		if(not north):
			north = self.northChoice(row, col)
		#Figure out east
		if(not east):
			east = self.eastChoice(row, col)
		#Figure out west
		if(not west):
			west = self.westChoice(row, col)
		#Figure out south
		if(not south):
			south = self.southChoice(row, col)
		
		height = random.randint(1, maxHeight)
		
		self.platforms[row][col] = Platform(north = north, east = east, west = west, south = south, height = height)
		platform = self.platforms[row][col]
		if(platform.hasEast()):
			if(self.generateNeighbors(row, col + 1) and col < self.colCount -1):
				nextPlat = self.platforms[row][col + 1]
				connDHeight = nextPlat.height - platform.height
				if(nextPlat.height < platform.height):
					connHeight = nextPlat.height
					direction = "west"
				else:
					connHeight = platform.height
					direction = "east"
				self.hConnect[row][col] = Connection(row, col, connHeight, connDHeight, direction)
		if(platform.hasSouth()):
			if(self.generateNeighbors(row + 1, col) and row < self.rowCount -1):
				nextPlat = self.platforms[row + 1][col]
				connDHeight = nextPlat.height - platform.height
				if(nextPlat.height < platform.height):
					connHeight = nextPlat.height
					direction = "north"
				else:
					connHeight = platform.height
					direction = "south"
				self.vConnect[row][col] = Connection(row, col, connHeight, connDHeight, direction)
		if(platform.hasWest()):
			if(self.generateNeighbors(row, col - 1) and col < self.colCount -1):
				nextPlat = self.platforms[row][col - 1]
				connDHeight = nextPlat.height - platform.height
				if(nextPlat.height < platform.height):
					connHeight = nextPlat.height
					direction = "east"
				else:
					connHeight = platform.height
					direction = "west"
				self.hConnect[row][col - 1] = Connection(row, col - 1, connHeight, connDHeight, direction)
		if(platform.hasNorth()):
			if(self.generateNeighbors(row - 1, col) and row < self.rowCount -1):
				nextPlat = self.platforms[row - 1][col]
				connDHeight = nextPlat.height - platform.height
				if(nextPlat.height < platform.height):
					connHeight = nextPlat.height
					direction = "south"
				else:
					connHeight = platform.height
					direction = "north"
				self.vConnect[row - 1][col] = Connection(row - 1, col, connHeight, connDHeight, direction)
		return True

		
maze = Maze(rowCount = rowCount, colCount = colCount)
maze.generateMaze()
maze.traverseMaze()
mc.playbackOptions(max = maze.time)
print "Platforms: " + str(Platform.platCount)
print "Connections: " + str(Connection.conCount)

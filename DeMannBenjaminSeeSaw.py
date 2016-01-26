import maya.cmds as mc
import random

def setShader(shaderName):
	mc.sets(e = True, forceElement = shaderName)
	
def createBeam(width, height, length):
	#Create Main Post
	mainBeam = mc.polyCube(w = width, h = height, d = length, name = "mainBeam")
	setShader("boardColor")
	supportBeam = mc.polyCube(w = width, h = height, d = (length/2), name = "supportBeam")
	mc.move(0, (-1 * height), 0)
	setShader("boardColor")
	return mc.group(mainBeam, supportBeam)

#Create Supports
def createSupports():
	support = [0, 0]
	for k in range(0,2):
		side = pow(-1, k)
		
		#Create Nut for the Rod
		nut = mc.polyPipe(r = .35, h = 0.5, t = 0.1, ax = [1, 0, 0], name = "nut")
		mc.move((1.25 * side), -.5, 0, r = True)
		setShader("metalColor")
		
		#Create Angled Supports
		angledSupport = mc.polyCube(w = 0.5, h = 2.5, d = 0.5, name = "angledSupport")
		mc.move ((1.25 * side), -2, (-.75 * side), r = True) #Move each peice to it's proper side of the beam
		mc.rotate ((45 * side), 0, 0, os = True) 
		setShader("boardColor")
		
		#Create Downward Support
		downwardSupport = mc.polyCube(w = 0.5, h = 3, d = 1, name = "downwardSupport")
		mc.move((.75 * side), -1.5, 0, r = True)
		setShader("boardColor")
		
		#Create Base
		base = mc.polyCube (w = 0.5, h = 1, d = 5, name = "base")
		mc.move((1.25 * side), -3, 0, r = True)
		setShader("boardColor")
		
		support[k] = mc.group(nut, angledSupport, downwardSupport, base, name = ("support" + ("Right" if k == 0 else "Left")))
		
	axel = mc.polyCylinder(r = 0.25, h = 4, sx = 20, sy = 1, sz = 1, ax = [1, 0, 0], name = "axel")
	mc.move(0, -0.5, 0)
	setShader("metalColor")
	return mc.group(support , axel, name = "support")

def createBody(width, height, length):
	beam = createBeam(width, height, length)
	support = createSupports()
	return [beam, support]
	
#Create a number of seats on seat on every Row	
def createSeat(width, height, seatLength):

	seatWidth = 2.0
	seatDepth = 1.5
	seatThickness = 0.2
	seatHeight = 2.5
	
	#Create Handles
	handleBase = mc.polyCylinder(r = 0.1, h = 1, sx = 20, sy = 1, sz = 1, ax = [0, 1, 0], name = "handleBase")
	mc.move(0, .5, 0)
	handleBar = mc.polyCylinder(r = 0.1, h = 1, sx = 20, sy = 1, sz = 1, ax = [1, 0, 0], name = "handleBar")
	mc.move(0, 1, 0)
	handle = mc.group(handleBase, handleBar, name = "handle")
	setShader("metalColor")
	mc.move(0, height/2.0, seatLength/2.0 - seatDepth)
	
	#Create Seat Base
	seatBase = mc.polyCube (w = width, h = height, d = seatLength, name = "seatBase")
	setShader("boardColor")
	
	#Create Seat
	seat = mc.polyCube(w = seatWidth, h = seatThickness, d = seatDepth + seatThickness, name = "seat")
	mc.move(0, seatThickness/2.0, (seatLength - (seatDepth + seatThickness)) / 2.0)
	seatBack = mc.polyCube(w = seatWidth, h = seatHeight, d = seatThickness, sx = 8, sy = 4, sz = 0, name = "seatBack")
	mc.move(0, ((seatHeight/2.0) + seatThickness), (seatLength - seatThickness) / 2.0)
	seat = mc.group(seat, seatBack, name = "seat")
	setShader("seatColor")
	mc.move(0, height/2.0, 0)
	
	#Create Armrests
	armRests = [0, 0]
	for i in range(0,2):
		armRestWidth = 0.25
		armRestHeight = .65
		armRestThickness = 0.1
		armRestLength = 1.5
		arm = mc.polyCube(w = armRestWidth, h = armRestThickness, d = armRestLength, name = "armRest")
		mc.move(0, (armRestHeight + armRestThickness)/2.0, (armRestLength - armRestHeight)/-2.0)
		support = mc.polyCube(w = armRestWidth, h = armRestHeight, d = armRestHeight, name = "support")
		armRests[i] = mc.group(arm[0], support[0], name = ("armRest" + ("Right" if i == 0 else "Left")))
		setShader("armRest")
		armRstMvAmtX = (armRestWidth + seatWidth) / 2
		mc.move((armRstMvAmtX * pow(-1, i)), (0.1 + (armRestHeight/2.0) + height/2.0), (seatLength/2.0) - (armRestHeight/2.0) - 0.1)
		
	return mc.group(seat, armRests, seatBase, handle, name = "fullSeat")

def createSeeSaw(width, height, length, numOfSeats, numOfRows):
	#Create Main Body
	mainBody = createBody(width, height, length)
	arm = mc.group(mainBody[0], name = "arm");
	base = mc.group(mainBody[1], name = "bases");
	
	#Create additional Beams and supports to accomidate all the seats
	for j in range(0, (numOfSeats / 6)):
		beamPos = (((j+1) * 6) -1)
		for i in range(2):
			body = createBody(width, height, length)
			mc.select(body)
			mc.move((beamPos* pow(-1, i)), 0, 0)
			mc.parent(body[0], arm)
			mc.parent(body[1], base)

	#Create Seats and Handles
	for j in range(1, numOfRows + 1):
		for k in range(2):
			#Create a support for each row
			seatLength = 3
			
			#In order to move 
			yMoveAmt = ((((length/2) + (j * seatLength))-seatLength) * pow(-1, k))
			beam = mc.polyCube(w = ((numOfSeats * 3)-3), h = height, d = width, name = "horizSupportBeam")
			mc.move(0, 0, yMoveAmt)
			setShader("boardColor")
			mc.parent(beam, arm)
			
			for i in range(numOfSeats):
				seat = createSeat(width, height, seatLength)
				seatWidth = 2
				sideFactor = (seatWidth + 1) * (i/2) + (seatWidth + 1)/2.0
				side = (sideFactor * pow(-1, i))
				print("The side movement value is: " + str(side))
				adjustment = yMoveAmt + ((seatLength/2)* pow(-1, k))
				mc.move(side, 0, adjustment)
				if(pow(-1, k) == -1):
					mc.rotate(0, 180, 0)
				mc.parent(seat, arm)
				
	#Set the rocking motion
	rand = random.randint(0,100)
	#mc.expression( s = arm + ".rotateX = 30 * cos((frame-" + str(rand) + ") * .04)")
	mc.expression( s = arm + ".rotateX = 30 * sin(frame * .04)")
	return mc.group(arm, base, name = "seeSaw")
	
				
				
def createLights():
	mc.ambientLight(intensity = 0.8)
	mc.move(0, 10, 0)
	mc.directionalLight(intensity = 0.8)
	mc.move(0, 15, 0)
	mc.rotate(-82.754683, 0, 0)

def createShader(type, name, r, g, b):
	mc.shadingNode(type, asShader = True, name = (name + "Shader"))
	mc.sets(renderable = True, noSurfaceShader = True, empty = True, name = name)
	mc.setAttr((name + "Shader.color"), r, g, b, type = "double3")
	mc.defaultNavigation(connectToExisting = True, source = (name + "Shader"), destination = name)

numOfSeats = 2 # Number of seats perRow
numOfRows = 1 # Number of rows on each side

createShader("lambert", "boardColor", 0.871, 0.722, 0.529)
createShader("blinn", "seatColor", 0.5, 0.0365, 0.0365)
createShader("phong", "metalColor", 0.827, 0.827, 0.827)
createShader("lambert", "armRest", 0.2, 0.2, 0.2)

wide = .5
heigh = .5
len = 40

#createSeeSaw(wide, heigh, len, numOfSeats, numOfRows)

#mc.select(all = True)
#mc.move(-12, 0, 0, r = True)

#mc.polyCube(w = 1, h = 1, d = 1)
#move ( 2, 0, 0, r = True)


for i in range(1):
	length = random.randint(15, 40)
	numOfSeats = random.randrange(2, 12, 2)
	numOfRows = random.randint(1, 3)
	mc.select(all = True)
	mc.move(15, 0, 0, r = True)
	createSeeSaw(1, .5, length, numOfSeats, numOfRows)

#createSeeSaw(1, .5, 10, 6, 2)

#mc.select(all = True)
#mc.move(4, 0, 0, r = True)

#Move Everything to sit on top of the gid.
mc.select(all = True)
mc.move (0, 3.5, 0, r = True)

mc.playbackOptions(min=1, max=1000)
	
#createLights()
mc.select(clear = True)

import maya.cmds as mc
import random

def buildWall(dHeight):
	height = abs(dHeight)
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
	mc.move(0, 0, 0, ladder, r = True)
	name = mc.group(ladder, name = "ladder")
	return name
	
buildWall(3)

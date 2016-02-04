class Shape:
	'Shape that contains 5 variations'
	shapeCount = 0;
	
	def __init__(self, width, height, sType):
		self.width = width
		self.height = height
		self.sType = sType
		Shape.shapeCount++
		
	def displayCount(self):
		print "Total Shapes %d" % Shape.shapeCount
		
	def displayShape(self):
		print self.sType

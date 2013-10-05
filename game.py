from SimpleCV import *
import pygame
import itertools
import time
def main():
	
		simplecvimg = Image('board2.JPG')


		# blue = simplecvimg.colorDistance((2,7,63)) * 2  #scale up
		blue = simplecvimg.colorDistance((2,5,55)) * 1.5  #scale up

		red = simplecvimg.colorDistance((62,5,13)) 


		l1 = DrawingLayer((simplecvimg.width, simplecvimg.height))

		blue.show()

		cv.WaitKey(1000)
		redBlobs = (simplecvimg - red).findBlobs(minsize=200)
		blueLine = (simplecvimg - blue).findBlobs()
		

		simplecvimg.addDrawingLayer(l1)
		simplecvimg.applyLayers()


		if redBlobs != None:
			for r in redBlobs:
				#check for location and shape and size if necessary
				r.drawRect(layer=l1, color=Color.BLUE, width=2, alpha=255)

			print "RED BLOBS FOUND"
			for r in redBlobs:
				print "Loc: " + str(r.centroid()) + " Area: " + str(r.area())


		if blueLine != None:
			blueLine[0].drawOutline(layer=l1,color=Color.RED,width=3,alpha=128)

			# blue = blueLine[0].blobMask()
		c = blueLine[0].contour()
		
		# d = blue.fitContour(c)
		startPoint = (1000,10000)
		for x in c:
			if x[0] < startPoint[0]:
				startPoint = x
		print startPoint



		importantPoints = [startPoint]
		for point in c:
			y_delta = point[1]-importantPoints[-1][1]
			if point[0] > importantPoints[-1][0] and (y_delta > 10 or y_delta<-10):
				importantPoints.append(point)

		for p in importantPoints:
			l1.circle(p, 10)

		blue.addDrawingLayer(l1)
		blue.applyLayers()
		blue.show()
		while True:
			cv.WaitKey(10)	



if __name__ == '__main__':
	main()


	# 37 87 98
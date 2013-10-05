import cv
import cv2
from SimpleCV import *
import pygame
import itertools
import time
def main():
	
		simplecvimg = Image('board1.JPG')


		#640x480
		blue = simplecvimg.colorDistance((2,7,63)) * 1.5  #scale up
		red = simplecvimg.colorDistance((62,5,13)) 


		l1 = DrawingLayer((simplecvimg.width, simplecvimg.height))


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
			blueLine.show()
			cv.WaitKey(5000)
		blue.addDrawingLayer(l1)
		blue.applyLayers()
		blue.show()
		while True:
			cv.WaitKey(10)	



if __name__ == '__main__':
	main()


	# 37 87 98
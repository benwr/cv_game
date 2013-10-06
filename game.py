from SimpleCV import *
import pygame
import itertools
from pygame.locals import *
import os
import time
BGIMAGE = 'board5.JPG'
keymap = {}
allLines = []

class Point(object):
	'''Creates a point on a coordinate plane with values x and y.'''

	COUNT = 0

	def __init__(self, x, y):
		'''Defines x and y variables'''
		self.x = x
		self.y = y

def main():
		pygame.init()
		xSpeed = 0
		ySpeed = 0
		simplecvimg = Image(BGIMAGE)
		screen = pygame.display.set_mode((simplecvimg.width,simplecvimg.height))
		train = False
		player = pygame.image.load('player.png').convert()
		# blue = simplecvimg.colorDistance((2,7,63)) * 2  #scale up
		blue = simplecvimg.colorDistance((2,5,55)) * 1.5  #scale up
		# blue.show()
		# cv.WaitKey(10000)
		red = simplecvimg.colorDistance((62,5,13)) 

		l1 = DrawingLayer((simplecvimg.width, simplecvimg.height))

		# blue.show()

		redBlobs = (simplecvimg - red).findBlobs(minsize=200)
		blueLine = (simplecvimg - blue).findBlobs()

		simplecvimg.addDrawingLayer(l1)
		simplecvimg.applyLayers()


		if redBlobs != None:
			for r in redBlobs:
				#check for location and shape and size if necessary
				if r.isCircle(tolerance=.5):
					r.drawRect(layer=l1, color=(0,0,255), width=2, alpha=255)
				else:
					#end point!
					endPoint = r.centroid()
					endh = r.minRectHeight()
					endw = r.minRectWidth()
					endx = r.minRectX()
					endy = r.minRectY()
					r.drawRect(layer=l1, color=(0,255,255), width=2, alpha=255)

			print "RED BLOBS FOUND"
			for r in redBlobs:

				print "Loc: " + str(r.centroid()) + " Area: " + str(r.area())
				rh = r.minRectHeight()/2
				rw = r.minRectWidth()/2
				x = r.minRectX()
				y = r.minRectY()
				print x,y
				edge = (int(round(x,0)),int(round(y,0)))
				l1.circle(edge, 10)
				x, y = edge
				newI = simplecvimg.crop(x-rw,y-rh,rw*2,rh*2)
				# l1.rectangle(x-(rw/2),y-(rh/2),color=Color.GREEN)
				black = newI.colorDistance((255,255,255)) * 6
				# if train:
				# 	f = open('training.txt', 'a')

				# for x in range(4):
				# 	for y in range(4):
				# 		l = black.width/4
				# 		h = black.height/4
				# 		n = black.crop(l*x,l*y,l,h)
				# 		#up down left right
				# 		n.show()
				# 		z = list(n.meanColor())
				# 		if train:
				# 			f.write(str(z)+':1,0,0,0\n')

				# 		cv.WaitKey(100)

				if train:
					f.close()
				# black.show() 
				# for x in range(1000):
				# 	cv.WaitKey(10)

				#lets find an arrow  

		if blueLine != None:
			blueLine[0].drawOutline(layer=l1,color=(255,0,0),width=3,alpha=128)

			# blue = blueLine[0].blobMask()
		lines = []
		for blueBlob in blueLine:
			c = blueBlob.contour()
			
			# d = blue.fitContour(c)
			startPoint = (1000,10000)
			for x in c:
				if x[0] < startPoint[0]:
					startPoint = x
			end = (-10,-10)
			for x in c:
				if x[0] > end[0]:
					end = x
			print end



			importantPoints = [startPoint]
			for point in c:
				y_delta = point[1]-importantPoints[-1][1]
				if point[0] > importantPoints[-1][0] and (y_delta > 10 or y_delta<-10):
					importantPoints.append(point)
			importantPoints.append(end)
			past = importantPoints[0]
			curLines = []
			for p in importantPoints:
				l1.circle(p,10)
				curLines.append((past[0],past[1], p[0],p[1]))
				past = p
			allLines.append(curLines)
			lines.append(importantPoints)

		blue.addDrawingLayer(l1)
		blue.applyLayers()
		# blue.show()
		# for x in range(500):
		# 	cv.WaitKey(10)
		position = player.get_rect()
		background = pygame.image.load(BGIMAGE).convert()
		position = position.move(10, 0)     #move player
		# for x in range(1000):
		# 	cv.WaitKey(10)
		total = []
		for l in allLines:
			past = l[0]
			for x in l[1:]:
				total.append((past[:2],x[2:]))
				past = x
		for l in total:
			pygame.draw.lines(screen,(255,0,0),False,l,1)
			pygame.display.update()

			cv.WaitKey(10)

		print total
		while True:
			#LOTS OF KEY BULLSHIT
			event = pygame.event.poll()
			if event.type == KEYDOWN:
				keymap[event.scancode] = event.unicode
				print str(event.scancode) + " Down!"

			if event.type == KEYUP:
				print 'keyup %s pressed' % keymap[event.scancode]
				del keymap[event.scancode]
			# print keymap
			#END KEY BULLSHIT
			screen.blit(background, (0, 0))
			#game loop
			if 2 in keymap: # LEFT
				xSpeed += .5
			if 0 in keymap: # RIGHT
				xSpeed -= .5
			if 0 not in keymap and 2 not in keymap:  #decelerate x
				xSpeed *= .9
			if 49 in keymap and ySpeed == 0:
				ySpeed -= 8
			else:
				ySpeed += .4

			if xSpeed > 5:
				xSpeed = 5
			elif xSpeed < -5:
				xSpeed = -5
			elif xSpeed < .2 and xSpeed > -.2:
				xSpeed = 0

			
			for l in lines:
				pygame.draw.lines(screen,(255,0,0),False,l,1)

			#OBSTACLE CHECK HERE
			position = position.move(xSpeed, ySpeed)     #move player

			botLine = (position.x,position.y,position.x + 25,position.y+25)
			bl = ((botLine[0],botLine[1]),(botLine[2],botLine[3]))
			pygame.draw.lines(screen,(255,0,0),False,bl,5)

			for line in total:
				# print line
				compLine = (line[0][0],line[0][1],line[1][0],line[1][1])
				# print compLine
	
				# print seg_intersect(botLine,compLine)
				if seg_intersect(botLine, compLine):
					screen.blit(background, (0, 0))
					botLine = (position.x,position.y,position.x + 25,position.y+25)
					pygame.draw.lines(screen,(0,0,255),False,(compLine[:2],compLine[2:]),5)
					bl = ((botLine[0],botLine[1]),(botLine[2],botLine[3]))

					pygame.draw.lines(screen,(255,0,255),False,bl,5)
					# pygame.display.update()
					pygame.draw.lines(screen,(0,255,0),False,(compLine[:2],compLine[2:]),5)
					ySpeed = 0

			#endLines
			el1 = (endx-(endw/2),endy - (endh/2),endx-(endw/2),endy + (endh/2))
			print el1
			if seg_intersect(botLine,el1):
				print "WINNER"
				return



			if position.y > simplecvimg.height - 30:
				position.move(0,simplecvimg.height - 30-position.y)
				ySpeed = 0

			screen.blit(player, position) 
			


			pygame.display.update()
			# print "XSPEED: " + str(xSpeed)
			# print "YSPEED: " + str(ySpeed)

			cv.WaitKey(25)

def seg_intersect(a,b):
	a1 = Point(a[0],a[1])
	a2 = Point(a[2],a[3])
	b1 = Point(b[0],b[1])
	b2 = Point(b[2],b[3])
	return intersect(a1,a2,b1,b2)

def ccw(A,B,C):
    return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)

# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)
if __name__ == '__main__':
	main()


	# 37 87 98
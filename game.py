from SimpleCV import *
import pygame
import itertools
from pygame.locals import *
import os
import time
BGIMAGE = 'board3.JPG'
keymap = {}
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
				r.drawRect(layer=l1, color=(0,0,255), width=2, alpha=255)

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

			for p in importantPoints:
				blue.drawLine(past, p,color=(255,0,0),thickness=10)
				past = p
			lines.append(importantPoints)

		blue.addDrawingLayer(l1)
		blue.applyLayers()
		# blue.show()
		position = player.get_rect()
		background = pygame.image.load(BGIMAGE).convert()
		position = position.move(0, 200)     #move player

		while True:
			#LOTS OF KEY BULLSHIT
			event = pygame.event.poll()
			if event.type == KEYDOWN:
				keymap[event.scancode] = event.unicode
				print str(event.scancode) + "Down!"

			if event.type == KEYUP:
				print 'keyup %s pressed' % keymap[event.scancode]
				del keymap[event.scancode]
			print keymap
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
				ySpeed -= 10
			else:
				ySpeed += .75

			if xSpeed > 5:
				xSpeed = 5
			elif xSpeed < -5:
				xSpeed = -5
			elif xSpeed < .2 and xSpeed > -.2:
				xSpeed = 0

			

			position = position.move(xSpeed, ySpeed)     #move player
			#OBSTACLE CHECK HERE
			if position.y > 225:
				position.move(0,225-position.y)
				ySpeed = 0
			screen.blit(player, position) 
			for l in lines:
				pygame.draw.lines(screen,(255,0,0),False,l,1)

			pygame.display.update()
			print "XSPEED: " + str(xSpeed)
			print "YSPEED: " + str(ySpeed)

			cv.WaitKey(25)

if __name__ == '__main__':
	main()


	# 37 87 98
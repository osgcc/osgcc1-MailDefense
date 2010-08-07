# Mail Defense!
# Ring.py
# Very important
#
# This file is part of MailDefense.
#
# MailDefense is free software; you can redistribute it and/or modify
# it under the terms of the version 2 of GNU General Public License as
# published by the Free Software Foundation;
#
# MailDefense is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with MailDefense; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import copy, sys, pygame, random, time
from pygame.locals import *
from Header import *
from Enemy import *
from Explosion import *

#==============================================================
# Ring - represents the approaching rings
#==============================================================
class Ring:
	#activeRingColor = Color("purple")
	#passiveRingColor = Color("gray")
	
	tick = 0
	moveTicks = 10
	stepSize = 5
	
	def __init__(self):
		self.active = True

		# set color and size
		#self.color = self.activeRingColor
		self.size = C_WINSIZE
		self.width = C_BLOCKSIZE
		
		# store sizes for the 4 sides of the ring
		rectSize = [0 for i in range(4)]
		rectSize[TOP] = (self.size, self.width)
		rectSize[BOTTOM] = (self.size, self.width)
		rectSize[LEFT] = (self.width, self.size)
		rectSize[RIGHT] = (self.width, self.size)
		
		# ugly, we could do this another way, but whatever. (the images have different orientations)
		surfNames = ["ringbartop.png", "ringbarside.png", "ringbartop.png", "ringbarside.png"]
		self.surfs = [pygame.image.load(ImageBase + surfNames[i]) for i in range(4)]
		
		# create rects for the 4 sides
		self.rects = [self.surfs[i].get_rect() for i in range(4)]
		self.rects[TOP].move_ip(0,0)
		self.rects[BOTTOM].move_ip(0, self.size-self.width)
		self.rects[LEFT].move_ip(0,0)
		self.rects[RIGHT].move_ip(self.size-self.width, 0)
		
		# THIS IS TO MOVE THE topLeft OF EACH RING SURFACE
		self.mov = [0 for i in range(4)]
		self.mov[TOP] = (self.stepSize, self.stepSize)
		self.mov[BOTTOM] = (self.stepSize, -self.stepSize)
		self.mov[LEFT] = (self.stepSize, self.stepSize)
		self.mov[RIGHT] = (-self.stepSize, self.stepSize)
		
		#THIS IS FOR RESIZING
		self.rez = [0 for i in range(4)]
		self.rez[TOP] = (-2*self.stepSize,0)
		self.rez[BOTTOM] = (-2*self.stepSize,0)
		self.rez[LEFT] = (0,-2*self.stepSize)
		self.rez[RIGHT] = (0,-2*self.stepSize)
		
		# add enemies to the ring
		self.enemies = {0:Enemy(0), 1:Enemy(1), 2:Enemy(2), 3:Enemy(3)}
	
	# moves the ring closer to the mailbox
	def advance(self):
		self.tick += 1
		if self.tick == self.moveTicks:
			self.tick = 0
			for i in range(4):
				self.rects[i].move_ip(self.mov[i])
				self.rects[i].width += self.rez[i][0]
				self.rects[i].height += self.rez[i][1]
			for enemy in self.enemies.values():
				enemy.move(self.rects[enemy.side].topleft, self.size)
			self.size -= self.stepSize*2
			
	# redraws the ring to the screen
	def blit(self, screen):
		# resize each of the sides
		for i in range(4):
			# VooDoo
			self.surfs[i] = pygame.transform.scale(self.surfs[i], (self.rects[i].width, self.rects[i].height))
			screen.blit(self.surfs[i], self.rects[i])
		for enemy in self.enemies.values():
			enemy.blit(screen) 

	# a little complicated.  Explodes enemies on the ring
	# bomb is passed for its coordinates and ease of passing
	# expList is a reference to MailDef's explosion list
	def explode(self, side, bomb, expList):
		pos = -1 # are we to the left or the right of the bomb
		nearSide = -1 # can we get an adjacent enemy of the same color
		enSet = set(self.enemies.keys()) # I like python sets because I like programming in English
		if side in enSet:
			if ((side == TOP) or (side == BOTTOM)):
				pos = self.enemies[side].rect.centerx
				if (pos <= bomb.rect.centerx):
					if (RIGHT in enSet):
						nearSide = RIGHT
				else:
					if (LEFT in enSet):
						nearSide = LEFT
			else:
				pos = self.enemies[side].rect.centery
				if pos <= bomb.rect.centery:
					if (BOTTOM in enSet):
						nearSide = BOTTOM
				else:
					if (TOP in enSet):
						nearSide = TOP
			if self.enemies[side].etype == bomb.bombType: # right bomb?
				expList.append(Explosion(self.enemies.pop(side).rect)) # KILL IT
				if ((nearSide >= 0) and (self.enemies[nearSide].etype == bomb.bombType)): # near enemy exists adjacent and same type?
					expList.append(Explosion(self.enemies.pop(nearSide).rect)) # KILL IT

	# uh
	def isDead(self):
		return (len(self.enemies)==0)

	# disable the ring, used in a powerup
	def killAll(self, expList):
		for enemy in self.enemies.values():
			expList.append(Explosion(enemy.rect))
		self.enemies = {}
#------------------------end Ring------------------------------			

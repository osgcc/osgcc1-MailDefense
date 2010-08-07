# MAILMAN
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
from Bomb import *

#==============================================================
# MailMan - class to control the player
#	contains a queue of bombs, MainMan's blit functions also
#	redraws all of the bombs in the bomb queue
#==============================================================
class MailMan:
	# constant for player movement speed
	speed_c = 4
	# number of bombs
	bombLimit = 4

	def __init__(self):
		# initialize bomb queue and speed vector
		self.bombs = []
		self.speed = [0, 0]
		
		self.image = pygame.image.load(ImageBase + "mailman.png")
		self.rect = self.image.get_rect()
		self.rect.move_ip(((C_NUMBLOCKS/2)*C_BLOCKSIZE, ((C_NUMBLOCKS/2)-1)*C_BLOCKSIZE))
		
	# redraw the player and bombs
	def blit(self, screen):
		for bomb in self.bombs:
			bomb.blit(screen)
		screen.blit(self.image, self.rect)
	
	# if its still allowable, create a bomb and append it to the bomb queue
	def drop(self, bombType):
		if len(self.bombs) < self.bombLimit:
			self.bombs.append(Bomb(bombType, [self.rect.left, self.rect.top]))
			return True
		else:
			return False
	
	#detonates the bomb at index in bomb
	def detonate(self, index):
		return self.bombs.pop(index)
	
	# function to change players direction
	def setSpeed(self, speed):
		self.speed[0] += speed[0] * self.speed_c
		self.speed[1] += speed[1] * self.speed_c
		
	# actually move the players or stop the player if he is about to 
	#	hit a boundary
	def move(self):
		speed = copy.deepcopy(self.speed)
	
		if self.rect.left + speed[0] < 0 or self.rect.right + speed[0] > C_WINSIZE:
			speed[0] = 0
			
		if self.rect.top + speed[1] < 0 or self.rect.bottom + speed[1] > C_WINSIZE:
			speed[1] = 0
			
		self.rect.move_ip(speed)
#--------------------------end MailMan-------------------------

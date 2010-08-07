# Mail Defense!
# Enemy.py
# These baddies come in periodically on rings, one per side.
# Hit their side with the right type of bomb to kill them.
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

class Enemy:
	def __init__(self, side):
		self.rect = pygame.Rect(0, 0, C_BLOCKSIZE, C_BLOCKSIZE)
		# lets randomize this for fun and profit
		self.etype = r.randint(0, 3)
		self.image = pygame.image.load(ImageBase + C_COLORS[self.etype] + ".png")
		# which side of the ring are we on?
		self.side = side
		
		# yeah, this is ugly.  This puts the rect in the right place
		# percent helps us place the Enemy as the ring goes to the center
		if self.side == TOP:
			pos = r.randint(4, C_NUMBLOCKS-4)*C_BLOCKSIZE
			self.percent = float(pos)/float(C_WINSIZE)
			self.rect.move_ip(pos,0)
		elif self.side == BOTTOM:
			pos = r.randint(4, C_NUMBLOCKS-4)*C_BLOCKSIZE
			self.percent = float(pos)/float(C_WINSIZE)
			self.rect.move_ip(pos, (C_NUMBLOCKS-1)*C_BLOCKSIZE)
		elif self.side == LEFT:
			pos = r.randint(4, C_NUMBLOCKS-4)*C_BLOCKSIZE
			self.percent = float(pos)/float(C_WINSIZE)
			self.rect.move_ip(0, pos)
		else: # self.side == RIGHT
			pos = r.randint(4, C_NUMBLOCKS-4)*C_BLOCKSIZE
			self.percent = float(pos)/float(C_WINSIZE)
			self.rect.move_ip((C_NUMBLOCKS-1)*C_BLOCKSIZE, pos)
			
	# move it along, passing the TopLeft of the ring's side and its length
	def move(self, tl, sideLen):
		if ((self.side == TOP) or (self.side == BOTTOM)):
			self.rect.topleft = (tl[0]+self.percent*sideLen, tl[1])
		else:
			self.rect.topleft = (tl[0], tl[1]+self.percent*sideLen)
			
	def blit(self, screen):
		screen.blit(self.image, self.rect)

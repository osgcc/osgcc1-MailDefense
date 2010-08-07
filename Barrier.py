# Mail Defense
# Barrier.py
#	The last line of defense for the mailbox.
#	Upon collision with this, the user loses.
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

class Barrier:
	def __init__(self):
		self.color = Color("light gray")
		self.size = 5*C_BLOCKSIZE
		self.width = C_BLOCKSIZE
		
		# orient the rectangles correctly
		rectSize = [0 for i in range(4)]
		rectSize[TOP] = (self.size, self.width)
		rectSize[BOTTOM] = (self.size, self.width)
		rectSize[LEFT] = (self.width, self.size)
		rectSize[RIGHT] = (self.width, self.size)
		
		# and make some surfaces
		surfPics = ["fencetop.png", "fenceright.png", "fencetop.png", "fenceleft.png"]
		self.surfs = [pygame.image.load(ImageBase + surfPics[i]) for i in range(4)]
		
		base = (C_NUMBLOCKS/2*C_BLOCKSIZE-2*C_BLOCKSIZE, C_NUMBLOCKS/2*C_BLOCKSIZE-2*C_BLOCKSIZE)
		
		# this is the easiest rectangles to test for death collision
		self.outerRect = pygame.Rect(base[0], base[1], self.size, self.size)
		
		# move the rects to where they'll sit
		self.rects = [self.surfs[i].get_rect() for i in range(4)]
		self.rects[TOP].move_ip(base[0], base[1])
		self.rects[BOTTOM].move_ip(base[0], base[1]+self.size-self.width)
		self.rects[LEFT].move_ip(base[0],base[0])
		self.rects[RIGHT].move_ip(base[0]+self.size-self.width, base[0])
		
	def blit(self, screen):
		for i in range(4):
			screen.blit(self.surfs[i], self.rects[i])

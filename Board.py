# Mail Defense!
# Board.py
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
from Ring import *

#==============================================================
# Board - the playable area
#	Manages the Rings via a queue
#==============================================================
class Board:
	def __init__(self):
		self.rings = []
		
	# Add a ring to the ring queue
	def addRing(self):
		self.rings.append(Ring())
		
	# move the rings
	def updateRings(self):
		for ring in self.rings:
			ring.advance()
	
	# redraw everything on the screen
	def blit(self, screen):
		for ring in self.rings:
			ring.blit(screen)
#------------------------end Board-----------------------------

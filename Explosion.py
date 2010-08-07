# Mail Defense!
# Explosion.py
# 	keeps a little fire on the screen after enemy death or bomb explosion
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

class Explosion:
	def __init__(self, rect):
		self.rect = rect
		self.image = pygame.image.load(ImageBase + "fire.png")
		self.rect = self.image.get_rect()
		self.rect.move_ip(rect.left, rect.top)
		self.life = 0
		
	def blit(self, screen):
		screen.blit(self.image, self.rect)

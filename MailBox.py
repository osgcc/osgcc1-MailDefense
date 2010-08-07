# Mail Defense!
# MailBox.py
# PROTECT THIS AT ALL COSTS GOD DAMN IT!
# Really doesn't do anything besides sit there
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

# represents the mailbox in the center		
class MailBox:
	def __init__(self):
		self.rect = pygame.Rect(C_NUMBLOCKS/2*C_BLOCKSIZE,C_NUMBLOCKS/2*C_BLOCKSIZE, C_BLOCKSIZE, C_BLOCKSIZE)
		self.image = pygame.image.load(ImageBase + "mailbox.png")
	def blit(self, screen):
		screen.blit(self.image, self.rect)

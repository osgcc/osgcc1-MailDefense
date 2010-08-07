# Mail Defense!
# Header.py
# Various constant and almost constants.
# We're not really good at keeping constants constant.
# Fuck it, I'm tired.
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

# Size of sprites
C_BLOCKSIZE = 16

# how many sprites can fit screen at once
C_NUMBLOCKS = 41
C_WINSIZE = C_NUMBLOCKS*C_BLOCKSIZE


#C_MAXENEMIES = 4

# Color constants - used in grabbing pngs
C_COLORS = ["blue", "green", "red", "yellow"]

# DIRECTIONS!!!!
TOP = 0
RIGHT = 1
BOTTOM = 2
LEFT = 3

# Some control variables, random values
C_PLAY = 100
C_EXIT = 99
C_WIN = 98

# How many ticks do we keep the explosions around?
C_LIFELIMIT = 4

# How many ticks between ring creations?
# HACK JOB - lowercase is real constant
realConst_genIntervalMin = 150
realConst_genIntervalMax = 250
C_GENINTERVALMIN = 150
C_GENINTERVALMAX = 250

# How many ticks between powerup creations?
C_GENPUPMIN = 150
C_GENPUPMAX = 300

# How long will powerups stay around?
C_PLIFEMIN = 150
C_PLIFEMAX = 300

# How long do our bombs stay around?
# again HACK JOB
realConst_bombTimer = 300
C_BOMBTIMER = 300

# A doubly-devlish section of code
C_MUSEVENT = 666666

# How many powerup types
C_MAXPUPTYPE = 2

# Makes things easier
HighScoreFile = "HighScoreFile"
ImageBase = "images/"
MusicBase = "music/"
SoundBase = "sounds/"
RussianMusicName = "Svyashchennaya_voyna.mp3"
ExplodeSound = "somebodysetupusthebomb.wav"
VictorySound = "victory.wav"
AdvanceSound = "motion.wav"
#RussianMusicName = "Svyashchennaya_voyna.wav"

# random number generator
r = random.Random()
r.seed(time.gmtime())

# here are our levels.
lvlBGs = ["bg1.png", "bg2.png", "bg3.png", "bg4.png", "bg5.png", "bg6.png"]
#levels = [25, 50, 75, 100, 125] # for testing
# exp to get to next level
levels = [2000, 4000, 8000, 16000, 32000]

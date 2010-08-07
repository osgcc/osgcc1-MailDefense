#!/usr/bin/python
# Mail Defense
# Copyright 2007 Eric Conlon, Nick Farnan, and Joe Frambach
# Contact:					, nlf4@pitt.edu, and 
# Entry in the Pitt Geeks game programming contest
# 4-7-2007
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
from MailBox import *
from Enemy import *
from Barrier import *
from Ring import *
from Bomb import *
from MailMan import *
from Board import *
from Explosion import *
from PowerUp import *

#==============================================================
# MailDef - the main class
#	contains MailMan, MailBox, and Grid objects, as well as
#	the main event loop
#==============================================================
class MailDef:
	#CHANGED
	def __init__(self):
		pygame.init()
		pygame.mixer.music.set_endevent(C_MUSEVENT)
		self.music = pygame.mixer.music
		self.music.load(MusicBase+RussianMusicName)
		self.curVol = .5
		self.music.set_volume(self.curVol)
		self.music.play()
		self.playingMusic = True
		
		self.window = pygame.display.set_mode((C_WINSIZE, C_WINSIZE))
		pygame.display.set_caption("Mail Defense!")
		self.screen = pygame.display.get_surface()
		self.clock = pygame.time.Clock()
		self.initSounds()
		self.updateVol()
	
	def initSounds(self):
		self.explodeSound = pygame.mixer.Sound(SoundBase+ExplodeSound)
		self.victorySound = pygame.mixer.Sound(SoundBase+VictorySound)
		self.advanceSound = pygame.mixer.Sound(SoundBase+AdvanceSound)
		
	def updateVol(self):
		self.explodeSound.set_volume(self.curVol)
		self.victorySound.set_volume(self.curVol)
		self.advanceSound.set_volume(self.curVol)
		self.music.set_volume(self.curVol)
	
	def initVars(self):
		#initialize objects
		self.score = 0
		self.level = -1 # will be incremented soon
		return self.advanceLevel()
		
	def reinitVars(self):
		#reinitialize objects
		global C_GENINTERVALMAX, C_GENINTERVALMIN, C_BOMBTIMER
		self.mailMan = MailMan()
		self.board = Board()
		self.mailBox = MailBox()
		self.barrier = Barrier()
		self.explosions = []
		self.powerUps = []
		self.lastMultiplier = 0
		self.genRingTick = 1
		self.level += 1
		C_GENINTERVALMAX = copy.deepcopy(realConst_genIntervalMax)
		C_GENINTERVALMIN = copy.deepcopy(realConst_genIntervalMin)
		C_BOMBTIMER = copy.deepcopy(realConst_bombTimer)
		self.bgImage = pygame.image.load(ImageBase + lvlBGs[self.level])
		self.powerUpTick = r.randint(C_GENPUPMIN, C_GENPUPMAX)
	
	def advanceLevel(self):
		self.reinitVars()
		self.screen.blit(self.bgImage, self.screen.get_rect())
		
		if self.playingMusic:
			self.victorySound.play()
		
		if self.level != 5:
			font = pygame.font.Font(None, 32)
			text = font.render("SCORE: "+str(self.score)+"/"+str(levels[self.level]), 1, (255, 255, 255))
			textpos = text.get_rect(centerx=self.screen.get_width()*3/5)
			self.screen.blit(text, textpos)
			
			text = font.render("LEVEL "+str(self.level+1)+" / 5", 1, (255, 255, 255))
			textpos = text.get_rect(centerx=self.screen.get_width()/2, centery = 200)
			self.screen.blit(text, textpos)
			
			text = font.render("Hit ENTER or SPACE to continue", 1, (255, 255, 255))
			textpos = text.get_rect(centerx=self.screen.get_width()/2, centery = 240)
			self.screen.blit(text, textpos)
		else:
			font = pygame.font.Font(None, 32)
			text = font.render("GOOD WORK BRAVE MAILMAN!", 1, (10, 10, 10))
			textpos = text.get_rect(centerx=self.screen.get_width()/2, centery = 150)
			self.screen.blit(text, textpos)
			
			text = font.render("You've sent those Commies running -", 1, (10, 10, 10))
			textpos = text.get_rect(centerx=self.screen.get_width()/2, centery = 180)
			self.screen.blit(text, textpos)
			
			text = font.render("Our mail is safe once more!", 1, (10, 10, 10))
			textpos = text.get_rect(centerx=self.screen.get_width()/2, centery = 210)
			self.screen.blit(text, textpos)
			
			text = font.render("Game by:", 1, (10, 10, 10))
			textpos = text.get_rect(centerx=self.screen.get_width()/2, centery = 270)
			self.screen.blit(text, textpos)
			
			text = font.render("Eric Conlon", 1, (10, 10, 10))
			textpos = text.get_rect(centerx=self.screen.get_width()/2, centery = 300)
			self.screen.blit(text, textpos)
			
			text = font.render("Nick Farnan", 1, (10, 10, 10))
			textpos = text.get_rect(centerx=self.screen.get_width()/2, centery = 330)
			self.screen.blit(text, textpos)
			
			text = font.render("Joe Frambach", 1, (10, 10, 10))
			textpos = text.get_rect(centerx=self.screen.get_width()/2, centery = 360)
			self.screen.blit(text, textpos)
			
			text = font.render("Created for Pitt Geeks", 1, (10, 10, 10))
			textpos = text.get_rect(centerx=self.screen.get_width()/2, centery = 420)
			self.screen.blit(text, textpos)
			
			text = font.render("at the 1st OSGCC April 6 - April 7 2007!", 1, (10, 10, 10))
			textpos = text.get_rect(centerx=self.screen.get_width()/2, centery = 450)
			self.screen.blit(text, textpos)
			
			text = font.render("Hit ENTER or SPACE to continue", 1, (10, 10, 10))
			textpos = text.get_rect(centerx=self.screen.get_width()/2, centery = 480)
			self.screen.blit(text, textpos)
		
		pygame.display.flip()
		
		playKeys = set([K_RETURN, K_SPACE])
		
		keepGoing = True
		while (keepGoing):
			self.clock.tick(30)
			for event in pygame.event.get():
				if event.type == QUIT:
					return C_EXIT
				# handle keydown events	
				elif event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						if (self.level == 5):
							return C_WIN
						else:
							return C_EXIT
					elif event.key in playKeys:
						if (self.level == 5):
							return C_WIN
						else:
							return C_PLAY
					elif event.key == K_m:
						if self.playingMusic:
							self.playingMusic = False
							self.music.stop()
						else:
							self.playingMusic = True
							self.music.play()
					elif event.key == K_PERIOD:
						self.curVol += .1
						if self.curVol >= 1:
							self.curVol = 1.0
						self.updateVol()
					elif event.key == K_COMMA:
						self.curVol -= .1
						if self.curVol <= 0:
							self.curVol = 0.0
						self.updateVol()
					elif event.key in playKeys:
						pygame.event.clear()
						return C_PLAY
				elif event.type == C_MUSEVENT:
					if self.playingMusic:
						self.music.play()
	
	def getHighScores(self):
		hsf = open(HighScoreFile, "r")
		highScores = [(line.strip()).split("\t") for line in hsf.readlines()]
		hsf.close()
		return highScores
			
	def setHighScore(self, newScore):
		highScores = self.getHighScores()
		newHigh = -1
		name = ""
		for i in range(len(highScores)):
			if ((newHigh == -1) and (newScore > (int)(highScores[i][1]))):
				newHigh = i
				name = self.getName()
				break
		if (newHigh != -1):
			# New high
			highScores = highScores[0:newHigh] + [[name,str(newScore)]] + highScores[newHigh:-1]
			hsf = open(HighScoreFile, "w")
			for hs in highScores:
				hsf.write(hs[0]+"\t"+hs[1]+"\n")
			hsf.close()
		return newHigh
	
	def getName(self):
		#name = raw_input()
		#if len(name) == 0:
		#	name = "Anon"
		#return name
		return "Brave Mailman!"
		
	#CHANGED
	def menu(self, hsNum):
		highScores = self.getHighScores()
		playKeys = set([K_RETURN, K_SPACE])
		self.updateMenu(hsNum)
		while (True):
			self.clock.tick(30)
			for event in pygame.event.get():
				if event.type == QUIT:
					return C_EXIT
				# handle keydown events	
				elif event.type == KEYDOWN:
					# quit on escape key
					if event.key == K_ESCAPE:
						return C_EXIT
					elif event.key == K_m:
						if self.playingMusic:
							self.playingMusic = False
							self.music.stop()
						else:
							self.playingMusic = True
							self.music.play()
					elif event.key == K_PERIOD:
						self.curVol += .1
						if self.curVol >= 1:
							self.curVol = 1.0
						self.updateVol()
					elif event.key == K_COMMA:
						self.curVol -= .1
						if self.curVol <= 0:
							self.curVol = 0.0
						self.updateVol()
					elif event.key in playKeys:
						pygame.event.clear()
						return C_PLAY
				elif event.type == C_MUSEVENT:
					if self.playingMusic:
						self.music.play()
	
	#draw the menu
	def updateMenu(self, hsNum):
		#set the US/USSR dueling background awesome image
		self.screen.blit(pygame.image.load(ImageBase+"menu.png"), self.screen.get_rect())
		
		### From here down diplays menutext ###
		font = pygame.font.Font(None, 32)
		text = font.render("Mail Defense!", 1, (10, 10, 10))
		textpos = text.get_rect(centerx=self.screen.get_width()/2, centery=150)
		#self.screen.blit(text, textpos)
		self.screen.blit(pygame.image.load(ImageBase+"logo.png"), textpos)
		
		font = pygame.font.Font(None, 20)
		text = font.render("Protect the US Postal Service", 1, (10, 10, 10))
		textpos = text.get_rect(centerx=self.screen.get_width()/2, centery = 190)
		self.screen.blit(text, textpos)
		
		text = font.render("by laying the right mail bombs!", 1, (10, 10, 10))
		textpos = text.get_rect(centerx=self.screen.get_width()/2, centery = 210)
		self.screen.blit(text, textpos)
		
		text = font.render("Exploit the dirty Communitsts' weaknesses:", 1, (10, 10, 10))
		textpos = text.get_rect(centerx=self.screen.get_width()/2, centery = 230)
		self.screen.blit(text, textpos)
		
		text = font.render("Lay bombs with 1, 2, 3, or 4 and move with the arrow keys.", 1, (10, 10, 10))
		textpos = text.get_rect(centerx=self.screen.get_width()/2, centery = 250)
		self.screen.blit(text, textpos)
		
		text = font.render("High scores!", 1, (10, 10, 10))
		textpos = text.get_rect(centerx=self.screen.get_width()/2, centery = 290)
		self.screen.blit(text, textpos)
		
		# read in high scores from file and print them
		hiscores = self.getHighScores()
		for i in range(len(hiscores)):
			mes = "%-1d. %-20s%16s" % (i, hiscores[i][0], hiscores[i][1])
			if (i == hsNum):
				mes = "!!! "+mes+" !!!"
			text = font.render(mes, 1, (10, 10, 10))
			textpos = text.get_rect(left=self.screen.get_width()/3, centery = 320+15*i)
			self.screen.blit(text, textpos)
			
		text = font.render("Press ENTER or SPACE to Start,", 1, (10, 10, 10))
		textpos = text.get_rect(centerx=self.screen.get_width()/2, centery = 500)
		self.screen.blit(text, textpos)
		
		text = font.render("ESC to Quit, or m to Toggle Sound.", 1, (10, 10, 10))
		textpos = text.get_rect(centerx=self.screen.get_width()/2, centery = 520)
		self.screen.blit(text, textpos)
		
		pygame.display.flip()
	#end updateMenu
	
	# redraws everything on the game screen
	def updateDisplay(self):
		self.screen.blit(self.bgImage, self.screen.get_rect())
		for pup in self.powerUps:
			pup.blit(self.screen)
		self.mailBox.blit(self.screen)
		self.barrier.blit(self.screen)
		self.board.blit(self.screen)
		self.mailMan.blit(self.screen)
		for exp in self.explosions:
			exp.blit(self.screen)
		
		font = pygame.font.Font(None, 32)
		text = font.render("SCORE: "+str(self.score)+"/"+str(levels[self.level]), 1, (255, 255, 255))
		textpos = text.get_rect(centerx=self.screen.get_width()*3/5)
		self.screen.blit(text, textpos)
		pygame.display.flip()
		
	# main game event loop
	def play(self):
		res = self.initVars()
		if res == C_EXIT:
			return self.score
		pygame.event.clear()
		keepPlaying = True
		while (keepPlaying):
			self.clock.tick(30)
			self.score += 1
			for event in pygame.event.get():
				if event.type == QUIT:
					keepPlaying = False
					break
				# handle keydown events	
				elif event.type == KEYDOWN:
					# quit on escape key
					if event.key == K_ESCAPE:
						keepPlaying = False
						break
					elif event.key == K_m:
						if self.playingMusic:
							self.playingMusic = False
							self.music.stop()
						else:
							self.playingMusic = True
							self.music.play()
					elif event.key == K_PERIOD:
						self.curVol += .1
						if self.curVol >= 1:
							self.curVol = 1.0
						self.music.set_volume(self.curVol)
					elif event.key == K_COMMA:
						self.curVol -= .1
						if self.curVol <= 0:
							self.curVol = 0.0
						self.music.set_volume(self.curVol)
					
					#!!! temp key binding for rings !!!
					#elif event.key == K_r:
					#	self.board.addRing()
						
					# key bindings for starting to move
					elif event.key == K_w or event.key == K_UP:
						self.mailMan.setSpeed([0, -1])
					elif event.key == K_a or event.key == K_LEFT:
						self.mailMan.setSpeed([-1, 0])
					elif event.key == K_s or event.key == K_DOWN:
						self.mailMan.setSpeed([0, 1])
					elif event.key == K_d or event.key == K_RIGHT:
						self.mailMan.setSpeed([1, 0])
						
					# dropping bombs
					elif event.key == K_u or event.key == K_1:
						mks = self.mailMan.drop(0)
						if mks and self.playingMusic:
							self.advanceSound.play()
					elif event.key == K_i or event.key == K_2:
						mks = self.mailMan.drop(1)
						if mks and self.playingMusic:
							self.advanceSound.play()
					elif event.key == K_o or event.key == K_3:
						mks = self.mailMan.drop(2)
						if mks and self.playingMusic:
							self.advanceSound.play()
					elif event.key == K_p or event.key == K_4:
						mks = self.mailMan.drop(3)
						if mks and self.playingMusic:
							self.advanceSound.play()
				
				# handler for keyup events
				elif event.type == KEYUP:
					# stopping moving
					if event.key == K_w or event.key == K_UP:
						self.mailMan.setSpeed([0, 1])
					elif event.key == K_a or event.key == K_LEFT:
						self.mailMan.setSpeed([1, 0])
					elif event.key == K_s or event.key == K_DOWN:
						self.mailMan.setSpeed([0, -1])
					elif event.key == K_d or event.key == K_RIGHT:
						self.mailMan.setSpeed([-1, 0])
						
				elif event.type == C_MUSEVENT:
					if self.playingMusic:
						self.music.play()			
			
			# check if powerUp should be added to the screen
			#	add if necessary
			self.powerUpTick -= 1
			if self.powerUpTick == 0:
				self.powerUps.append(PowerUp())
				self.powerUpTick = r.randint(C_GENPUPMIN, C_GENPUPMAX)
				
			# check if a new ring should be decorated
			#	add if necessary
			self.genRingTick -= 1
			if self.genRingTick == 0:
				self.board.addRing()
				self.genRingTick = r.randint(C_GENINTERVALMIN, C_GENINTERVALMAX)
				
			# check if any items have timed up and need to
			#	be removed from the screen
			exp = self.checkBombs()
			if exp and self.playingMusic:
				self.explodeSound.play()
			self.checkPowerUps()
			self.updateExplosions()
			
			self.mailMan.move()
			self.board.updateRings()

			if (self.checkCollisions()):
				keepPlaying = False
				break
				
			self.modifyDifficulty()
			self.updateDisplay()
			if (self.score >= levels[self.level]):
				res = self.advanceLevel()
				if ((res == C_EXIT) or (res == C_WIN)):
					return self.score
		# end game event loop
			
		# if the game loop was exited, game is over, return the score
		return self.score

	def modifyDifficulty(self):
		global C_GENINTERVALMAX, C_GENINTERVALMIN, C_BOMBTIMER
		newMultiplier = self.score/500
		if newMultiplier <= self.lastMultiplier:
			return
		self.lastMultiplier = newMultiplier
		C_GENINTERVALMIN -= newMultiplier
		C_GENINTERVALMAX -= newMultiplier
		C_BOMBTIMER -= newMultiplier
			
	def collectPowerUp(self, pupType):
		if self.playingMusic:
			self.advanceSound.play()
		self.score+=100
		if pupType == 0:
			exp = self.killAllBombs()
			if exp and self.playingMusic:
				self.explodeSound.play()
		elif pupType == 1:
			exp = self.killAllEnemies()
			if exp and self.playingMusic:
				self.explodeSound.play()
		elif pupType == 2:
			exp = self.killNearestEnemies()
			if exp and self.playingMusic:
				self.explodeSound.play()
				
	def checkCollisions(self):
		# CHECK FOR PERSON/POWERUP COLLISIONS!
		if len(self.powerUps)>0:
			collideList = self.mailMan.rect.collidelistall(self.powerUps)
			collideList.reverse()
			for index in collideList:
				self.collectPowerUp(self.powerUps.pop(index).pupType)
		# CHECK FOR BOMB/RING COLLISIONS
		for ring in self.board.rings:
			for side in range(4):
				collideList = ring.rects[side].collidelistall(self.mailMan.bombs)
				collideList.sort()
				collideList.reverse()
				if len(collideList) > 0:
					if self.playingMusic:
						self.explodeSound.play()
					for index in collideList:
						bomb = self.mailMan.detonate(index)
						self.explosions.append(Explosion(bomb.rect))
						ring.explode(side, bomb, self.explosions)
						if ring.isDead():
							#CHANGE
							self.board.rings.remove(ring)
							break
		# CHECK FOR RING/BARRIER COLLISIONS
		for ring in self.board.rings:
			for side in range(4):
				collideList = ring.rects[side].collidelistall(self.barrier.rects)
				if len(collideList) > 0:
					return True
		return False
					
	# if the explosions have exploded, remove them from the game
	def updateExplosions(self):
		delList = []
		for expIndex in range(len(self.explosions)):
			self.explosions[expIndex].life += 1
			if (self.explosions[expIndex].life >= C_LIFELIMIT):
				delList.append(expIndex)
		delList.reverse()
		for expIndex in delList:
			del self.explosions[expIndex]
			 
	# check the bomb timers, if any are up, detonate them
	def checkBombs(self):
		detonateList = []
		flag = False
		for index in range(len(self.mailMan.bombs)):
			self.mailMan.bombs[index].timer -= 1
			if self.mailMan.bombs[index].timer == 0:
				detonateList.append(index)
				flag = True
		detonateList.reverse()
		for index in detonateList:
			bomb = self.mailMan.detonate(index)
			self.explosions.append(Explosion(bomb.rect))
		return flag
			
	#similar deal for bombs
	def checkPowerUps(self):
		killList = []
		for index in range(len(self.powerUps)):
			self.powerUps[index].lifeTime -= 1
			if self.powerUps[index].lifeTime == 0:
				killList.append(index)
		killList.reverse()
		for index in killList:
			self.powerUps.pop(index)
			
	def killAllBombs(self):
		flag = False
		detList = [i for i in range(len(self.mailMan.bombs))]
		detList.reverse()
		if len(detList)>0:
			flag = True
		for index in detList:
			bomb = self.mailMan.detonate(index)
			self.explosions.append(Explosion(bomb.rect))
		return flag
	
	def killAllEnemies(self):
		flag = False
		if len(self.board.rings)>0:
			flag = True
		for ring in self.board.rings:
			ring.killAll(self.explosions)
			self.board.rings.remove(ring)
		return flag
	
	def killNearestEnemies(self):
		flag = False
		if len(self.board.rings)>0:
			flag = True
			self.board.rings[0].killAll(self.explosions)
			self.board.rings.remove(self.board.rings[0])
		return flag
#--------------------------end MailDef-------------------------
		
############################################################################
def main():
	endScore = 0
	hsNum = -1
	game = MailDef()
	while (True):
		action = game.menu(hsNum)
		endScore = 0
		hsNum = -1
		if (action == C_PLAY):
			endScore = game.play()
			hsNum = game.setHighScore(endScore)
		else:
			break
	pygame.mixer.stop()
	
if __name__ == "__main__":
	main()

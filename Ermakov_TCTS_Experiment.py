#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Ermakov_Dmitry_MARVIN_TCTS.py
#  
#  Copyright 2019 Dmitry Ermakov <ermakov.py@ya.ru>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

#import libraries
import random
import math
from psychopy import visual, event, gui

#define dictionary to use it in gui dialog
dict_gui = {'Name' : '', 'Date (dd.mm.yy)' : '', 'Day (1 or 2)' : ''}
gui.DlgFromDict(dict_gui, title = 'Please fill these fields before starting an experiment')

#calculate how much pixels contains one cm of the screen
#PLEASE ENTER YOUR WITDH IN PIXELS AND CM
cm = int(1440/39.8)

#create a window
win = visual.Window(size = (1440, 900), units='pix', colorSpace='rgb', color = (1, 1, 1), fullscr = True)

#print the instruction for the participant and wait for him to read it and press space bar
Instructions = visual.TextStim(win = win, text = u'''Welcome! This experiment will contain four blocks. After each block you will have some time to rest. You will see two circles in each trial. Right circle will be surrounded by some other circles. Your task would be to make size of the right circle as close as you can to the left one by pressing "Left arrow" (to make circle smaller), "Right arrow" (to make circle bigger) and "Space bar" (to confirm your choice). \nNow you can press "Space bar" if you are ready to start.''', color = (-1, -1, -1))
Instructions.draw()
win.flip()
event.waitKeys(keyList=['space'])


#print headers of the table to file
with open(dict_gui['Name'] + '_' + dict_gui['Date (dd.mm.yy)'] + '_' + 'Day' + dict_gui['Day (1 or 2)'] + '.csv', 'w') as csv:
	columnTitle = 'CircleSize,ChosenSize,SurroundSize,SurroundAmount\n'
	csv.write(columnTitle)

########################################################################

########################################################################
#define class to store our conditions and make them equaly distributed between each other
class conditionsList:
	#instance constructor
	def __init__(self, trials, cond_1, cond_2, cond_3):
		
		self.trials = trials
		self.cond_1 = cond_1
		self.cond_2 = cond_2
		self.cond_3 = cond_3
		
		#define dictionary to store all combinations of our conditions and their repetitions
		self.condCounter = dict()
		for i in cond_1:
			self.condCounter[i] = dict()
			self.condCounter[i]['total'] = 0
			for j in cond_2:
				self.condCounter[i][j] = dict()
				self.condCounter[i][j]['total'] = 0
				for k in cond_3:
					self.condCounter[i][j][k] = 0
		

#_______________________________________________________________________

#define class method to give us a three element tuple that contains combination of left circle size, size of the surrounding circles and amount of them
	def random(self):
		#in that case we use 2 x 3 x 5 experimental design
		#method allows us to count the number of combinations and control them
		a = random.choice(self.cond_1)
		while self.condCounter[a]['total'] == self.trials / len(self.cond_1):
			a = random.choice(self.cond_1)
		self.condCounter[a]['total'] += 1
		
		b = random.choice(self.cond_2)
		while self.condCounter[a][b]['total'] == (self.trials / len(self.cond_1)) / len(self.cond_2):
			b = random.choice(self.cond_2)
		self.condCounter[a][b]['total'] += 1
		
		c = random.choice(self.cond_3)
		while self.condCounter[a][b][c] == ((self.trials / len(self.cond_1)) / len(self.cond_2)) / len(self.cond_3):
			c = random.choice(self.cond_3)
		self.condCounter[a][b][c] += 1
		
		return a, b, c
		
########################################################################

########################################################################

#define a function to build a central circle and surrounding ones
#we use cosine and sine to find x and y coordinates, because surrounding circles not always located exactly to the right or below
def surroundedCircle(center_size, num_of_surr, size_of_surr, distance):
	center_xy = [-8 * cm, 0]
	distance_centers = center_size*0.5 + size_of_surr*0.5 + distance
	degrees_list = [i * (360 / num_of_surr) for i in range(0, num_of_surr)]
	for i in degrees_list:
		i = math.radians(i)
		x = math.cos(i) * distance_centers
		y = math.sin(i) * distance_centers
		ebbngCircle.pos = ([center_xy[0] + x, center_xy[1] + y])
		ebbngCircle.size = size_of_surr
		ebbngCircle.draw()
	ebbngCircle.pos = (center_xy)
	ebbngCircle.size = (center_size)
	ebbngCircle.draw()
	
#define a function to build a circle that participants would be able to change
#at the start of every trial size of that circle is random number from the pool (0.85 to 2.15)	
def comparisonCircle(size):
	global simple_circle_size
	if size == 0:
		list_of_sizes = [i * 0.05 for i in range(17, 44)]
		simple_circle_size = random.choice(list_of_sizes)
	else:
		simple_circle_size = size
	simpleCircle.size = simple_circle_size * cm
	simpleCircle.draw()
########################################################################	

########################################################################

#construct instanses of our circles
ebbngCircle = visual.GratingStim(win = win, mask = "circle", size = 0, pos = [-8 * cm, 0], color = [-1, -1, -1], sf = 0)
simpleCircle = visual.GratingStim(win = win, mask = "circle", size = 0, pos = [8 * cm, 0], color = [-1, -1, -1], sf = 0)


#main loop: it provides us with four equal blocks with randomly distributed trials in each of them
for i in range(4):
	list_of_conditions = conditionsList(30, [0.8, 0.4, 0.0, -0.4, -0.8], [2, 4, 6], [1.3, 1.7])
	#these check was made to add 2 control conditions of 32 in which there is no surrounding circles
	#i decided not to add that condition to our class because such are rare for that type of experiments
	check_control_list = [1] * 30
	check_control_list.extend([0, 0])
	random.shuffle(check_control_list)
	size_control_list = [1.3, 1.7]
	random.shuffle(size_control_list)
	
	#loop inside the blocks
	for j in range(32):
		#we start from generating circles with our functions
		simple_circle_size = 0
		presses = [0]
		check = check_control_list.pop()
		if check == 0:
			cond_list = [0, 0, size_control_list.pop()]
		else:
			cond_list = list_of_conditions.random()
		#then we start infinite cycle to give an ability to participant to change right circle as he want
		while True:
			comparisonCircle(simple_circle_size)
			surroundedCircle(center_size = cond_list[2] * cm, num_of_surr = cond_list[1], size_of_surr = (cond_list[2] + cond_list[0]) * cm, distance = 0.6 * cm)
		
			win.flip()
			#then we register key presses to make circle bigger or smaller (but not smaller or bigger than 0.85 and 2.15), confirm his choice or close the experiment (you never know)
			presses = event.waitKeys(keyList = ['left', 'right', 'escape', 'space'])
			if presses[0] == 'left':
				if simple_circle_size >= 0.9:
					simple_circle_size -= (0.05)
				else:
					simple_circle_size = 0.85
			if presses[0] == 'right':
				if simple_circle_size <= 2.1:
					simple_circle_size += (0.05)
				else:
					simple_circle_size = 2.15
			if presses[0] == 'escape':
				win.close()
			#when the subject presses the space button, we save the data from this trial to the file
			if presses[0] == 'space':
				with open(dict_gui['Name'] + '_' + dict_gui['Date (dd.mm.yy)'] + '_' + 'Day' + dict_gui['Day (1 or 2)'] + '.csv', 'a') as csv:
					if check == 0:
						row = str(cond_list[2]) + ',' + str(simple_circle_size) + ',' + str(0) + ',' + str(cond_list[1]) + '\n'
					else:
						row = str(cond_list[2]) + ',' + str(simple_circle_size) + ',' + str(cond_list[2] + cond_list[0]) + ',' + str(cond_list[1]) + '\n'
					csv.write(row)
				break
	#after each block (except the last) we give our participant a break
	if i < 3:
		PauseBreak = visual.TextStim(win = win, text = u'''Now you have some time to rest. \nPress "Space bar" when you are ready to start.''', color = (-1, -1, -1))
	#after the last block we thank him and close the window
	else:
		PauseBreak.text = u'''Thank you for completing out experiment. \nPress "Space bar" to exit.'''
	PauseBreak.draw()
	win.flip()
	event.waitKeys(keyList=['space'])





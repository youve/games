#! /usr/bin/python3
# -*- coding: utf-8 -*-

import time, random, os
if os.name == 'posix':
	import readline

correct = 0
rounds = 0
streak = 0
seconds = []

msg = ''
playAgain = True
help = '''This example calculates 9th September 2014, the day this program was
written. There are several steps:
	Century: 1500s and 1900s were 0, 1800s and 2200s were 2, 1700s and 2100s 
were 4, 1600s and 2000s were 6, etc. Just remember that 1900s were 0 and you 
cycle through [0,2,4,6] counting backwards from 1900. For 2014, we hang onto the
number 6.
	Year: Separate the last two digits of the year from the century. For 2014 
this is '14'. First take this number mod 7 (0) and add it to the 6 from the 
previous step and hang onto the result: 6
	Then divide the year (14) by 4, discarding any reminder, getting 3. Add this
to the previous step: 6 + 3 = 9, and hang onto the result.
	Month: Memorise the number 144-025-036-146. You can remember this as 12^2, 
5^2, 6^2, 146, or however you like. The ninth number in this sequence is 6 and 
that is the number for September. Add this to the previous step, 9 + 6 = 15, and
remember the answer.
	Day: Add the day (or the day mod 7, whichever is easier) to the previous 
answer: 9 + 15 = 24
	Leap year: If the month is January or February in a leap year, subtract 1.
	Finally, take the answer mod 7 and get 3.
	Sunday = 1, Monday = 2, Tuesday = 3, Wednesday = 4, Thursday = 5, 
Friday = 6 and Saturday = 0 or 7.
	Therefore, this program was written on a Tuesday.'''

needHelp = input('Do you need help? y/N: ') or 'n'
if needHelp[0].lower() == 'y':
	print(help)

while playAgain:
	yearStart = input('Starting year (Enter = 1600): ')
	if not yearStart.isdigit():
		yearStart = 1600
	else:
		yearStart = int(yearStart)
	yearEnd = input('Ending year (Enter = 2100): ')
	if not yearEnd.isdigit():
		yearEnd = 2100
	else:
		yearEnd = int(yearEnd)

	year = random.randint(yearStart,yearEnd)
	month = random.randint(1,12)
	dayEnd = 0
	if month == 2:
		dayEnd = 28
	elif month in [9, 4, 6, 11]:
		dayEnd = 30
	else:
		dayEnd = 31
	day = random.randint(1,dayEnd)

	dayTuple = time.strptime(str(year) + ' ' + str(month) + ' ' + str(day), '%Y %m %d')
	answerCorrect = time.strftime('%A', dayTuple)

	startTime = time.time()
	answerGiven = ''
	while not answerGiven:
		answerGiven = input(time.strftime('What day of the week was %d %B %Y: ', dayTuple)).strip().title()
	endTime = time.time()

	

	if answerGiven == answerCorrect:
		correct = correct + 1
		rounds = rounds + 1
		streak = streak + 1
		msg = 'Correct!'
		seconds.append(endTime-startTime)
	else:
		rounds = rounds + 1
		streak = 0
		msg = 'Sorry, it was ' + answerCorrect + '! '

	msg = msg + ' [' + str(correct) + '/' + str(rounds) + '] ' + str(round(correct*100/rounds,2)) + '% Current streak: ' + str(streak) + '. '
	if len(seconds):
		msg = msg + 'Avg time for correct answer: ' + str(round(sum(seconds)/len(seconds),2)) + ' seconds.'
	print(msg + '\n')
	again = input('Again? Y/n: ') or 'y'
	if again.lower()[0] != 'y':
		playAgain = False
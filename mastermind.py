#! /usr/bin/python3
# -*- coding: utf-8 -*-

##############################
# Module: Mastermind
# Date: 2013-07-02
# Version: 0.1
'''
Port of an old dos game
'''
##############################
# Log:
# 2013-07-02 first version
##############################
import random
import readline
instructions = '''
#   #     #        ###  #####  ####  ####   #   #  ###  #   #  ###
## ##    # #      #   #   #    #     #   #  ## ##   #   ##  #  #  #
# # #   #####      #      #    ##    ####   # # #   #   # # #  #   #
#   #  #     #  #   #     #    #     #  #   #   #   #   #  ##  #  #
#   # #       #  ###      #    ####  #   #  #   #  ###  #   #  ###

I am thinking of a number. You are to try and guess it. I will tell you how many numbers\nare correct and of those how many are in the right position. Use this information to guess\n the right answer.\n\n\n
'''

def again():
	yes = input("Do you want to play again? Y/n ")
	if yes[0].upper() == "Y":
		mainloop()
	else:
		print("Bye! Thanks for playing with me!")
		exit()
def mainloop():
	print(instructions)
	guesses = input("Number of guesses? (Default: 10) ")
	try:
		guesses = int(guesses)
		if guesses < 1:
			guesses = 10
	except:
		guesses = 10
	length = input("Length of the number to guess? (Default: 4) ")
	try:
		length = int(length)
		if length < 1:
			length = 4
	except:
		length = 4
	max = '9'*length
	secret = str(random.randint(0,int(max)))
	while len(secret) != length:
		secret = '0' + secret
	while guesses > 0:
		guess = input("Guess: ")
		if len(guess) != length: 
			error = "You need to enter a " + str(length) + " digit number: "
			guess = input(error)
		rightnum = 0
		rightpos = 0
		count = 0
		seen = ''
		for num in guess:
			if num in secret and seen.count(num) < secret.count(num):
				rightnum = rightnum + 1
			if secret[count] == num:
				rightpos = rightpos + 1
			count = count + 1
			seen = seen + num
		guesses = guesses - 1
		print("Correct number: %s Correct position: %s Guesses remaining: %s" % (rightnum, rightpos, guesses))
		if rightpos == length:
			print("You win! My number was %s" % (secret))
			again()
	print("You lose! My number was %s" % (secret))
	again()

mainloop()

#! /usr/bin/python3
# -*- coding: utf-8 -*-
#
## Geek of All Trades version 0.2 Revision 10 (2014-2^6)
# play in english, Deutsch, ελληνικά, español, italiano, 
#magyar, македонски, polski, română, slovenský, srpski, or suomi!

# Board game: http://i.imgur.com/AujrAly.png
# play with ten sided dice (or playing cards) and index cards with math functions on them
# On your turn, draw a math card, then however many number cards you want
# Then solve the problem and covert the numbers into letters to make a word.
# You get points for each digit you get right and again for each digit you use in a word.
# Each digit is worth half the number of number cards you drew.

# When you land on the snowflake square, draw 20 number cards (or roll 20 ten sided dice)
# and memorise as much as you can in a minute. You get 1 point for each 4 numbers you memorise
# rounded down, so if you only remember one number, you still get a point.
# move one space forward for each point you get.


import random
import re
import math
import readline
import time
import sys

maths = [
	'x+y',
	'x-y',
	'x*y',
	'x/y',
	'x**2',
	'x**3',
	'math.factorial(x)',
	'x**2 - y**2',
	'2**x',
	'math.sqrt(x)'
	# cos(2kπ+π/6), sin(2κπ+π/3)
	]

hard = [
	'math.factorial(x)',
	'2**x',
	]

other = {
	'0' : ['s', 'z', 'c'],
	'1' : ['t', 'd', 'th'],	
	'2' : ['n'],
	'3' : ['m'],
	'4' : ['r'],
	'5' : ['l'],
	'6' : ['sh', 'ch', 'j'],
	'7' : ['k', 'g'],
	'8' : ['f', 'v'],
	'9' : ['p', 'b'],
	'free' : ['w', 'h', 'y', 'a', 'e', 'i', 'o', 'u']
}

languages = ['de','ελ','en','es','fi','it','hu','мк','pl','ro','sk','sr'] 

fi = {
	'0' : ['s','z','š','ž', 'c', '(kuten s)'],
	'1' : ['t','d'],
	'2' : ['n', 'ng'],
	'3' : ['m'],
	'4' : ['r'],
	'5' : ['l'],
	'6' : ['j','h'],
	'7' : ['k','g','q','c','(kuten k)'],
	'70' : ['x', 'ks'],
	'8' : ['f','v','w'],
	'9' : ['p','b'],
	'free' : ['a','e','i','o','u','y','ä','ö', 'å']
}

en = {
	'0' : ['s','ss', 'z', 'zz','ci', 'ce', 'cc', 'cy', 'c', '(like city)', 'sc', '(like scene)', 'x', '(like xylophone)'],
	'07' : ['sk', 'sc', '(like sceptic)'],
	'1' : ['t', 'tt', 'd', 'dd', 'dh', 'th'],	
	'10' : ['c', '(when pronounced like "ts")','z', 'zz', '(like pizza)'],
	'2' : ['n', 'nn', 'ng', '(like long)'],
	'3' : ['m', 'mm'],
	'4' : ['r', 'rr'],
	'5' : ['l', 'll'],
	'6' : ['sh', 'j', 'ch', 'ce', '(like cello)', 'ci', '(like special)', 'cc', 'd', '(like gradual)', 'dg', 'g', '(like page or collage)', 'gg', 's', '(like sugar or vision)', 'sc', '(like fascism)', 't', '(like ratio, question)', 'tc', '(like batch)', 'x', ('like luxury')],
	'7' : ['k', 'kk', 'g', 'gg', 'c', '(like cake)', 'cc', 'ch', '(like ached)', 'ck', 'q'],
	'70' : ['cc', '(like accept)', 'x', '(like exit)'],
	'8' : ['f', 'ff' 'v', 'vv', 'gh', '(like laugh)', 'p','pp', '(like sapphire)', 'w', '(when pronounced like v)'],
	'9' : ['p', 'pp', 'b', 'bb', 'gh', '(like hiccough)'],
	'free' : ['a', 'e', 'i', 'h', 'o', 'u', 'w', 'y', 'when silent or pronounced like h:', 'b', 'c', 'ch', 'd', 'g', 'k', 'l','m','n','p','r','s', 't','w','x','z']
}

ro = {
	'0' : ['s','z'],
	'1' : ['t','d'],
	'10' : ['ț'],
	'2' : ['n'],
	'3' : ['m'],
	'4' : ['r'],
	'5' : ['l'],
	'6' : ['ge','gi','ce','ci', 'ș','j'],
	'7' : ['c','g','che','chi','ghe','ghi','k','q'],
	'8' : ['f','v','w'],
	'9' : ['p','b'],
	'free' : ['a','ă','â','e','i','î','h','o','u','y']
}

it = {
	'0' : ['s','sce','sci','z'],
	'07' : ['sc'],
	'1' : ['t','d'],
	'2' : ['n','gn'],
	'3' : ['m'],
	'4' : ['r'],
	'5' : ['l','gl'],
	'6' : ['ci','ce','gi','ge'],
	'7' : ['ch','ca','co','cu','ga','ge','go','gh','k'],
	'70' : ['x'],
	'74': ['cr','gr'],
	'75' : ['gl'],
	'77' : ['cch','ggh'],
	'8' : ['f','v','v'],
	'9' : ['p','b'],
	'free' : ['a','e','h','i','j','o','u','é','ó','è','y']
}

de = {
	'0' : ['s','z','zz', 'ß','ss','c', '(weich)'],
	'1' : ['t','tt','dd', 'd','th'],
	'2' : ['n', 'nn'],
	'3' : ['m', 'mm'],
	'4' : ['r', 'rr'],
	'5' : ['l', 'll'],
	'6' : ['ch','g','(weich)','j','(wie Dschungel)','sch','dsch'],
	'7' : ['k','kk', 'ck','g','(hart)','c','(hart)'],
	'8' : ['f','ff','v','vv','w','ww','ph'],
	'9' : ['p','pp','b','bb'],
	'free' : ['a','ä','e','ë','h','i','ï','j','o','ö','u','ü','y']
}

hu = {
	'0' : ['sz', 'z'],
	'1' : ['t', 'ty', 'd', 'gy'],
	'2' : ['n', 'ny'],
	'3' : ['m'],
	'4' : ['r'],
	'5' : ['l'],
	'6' : ['s', 'cs', 'dzs', 'zs'],
	'7' : ['k', 'g'],
	'70' : ['x'],
	'8' : ['f', 'v', 'w'],
	'9' : ['p', 'b'],
	'10' : ['c', 'dz'],
	'free' : ['a', 'á', 'e', 'é', 'h', 'i', 'í', 'j', 'ly', 'o', 'ó', 'ö', 'ő', 'u', 'ú', 'ü', 'ű']
}

мк = {
	'0' : ['с','з'],
	'1' : ['д','т'],
	'10' : ['ѕ'],
	'2' : ['н','њ'],
	'3' : ['м'],
	'4' : ['р'],
	'5' : ['л','љ'],
	'6' : ['ш','ч','ж','џ'],
	'7' : ['к','г','ќ','ѓ'],
	'8' : ['ф','в'],
	'9' : ['п','б'],
	'free' : ['а','е','х','и','ј','о','у','ѐ','ѝ'] 
}

sr = {
	'0' : ['s', 'z',],
	'1' : ['t', 'ć', 'd', 'đ'],
	'2' : ['n', 'nj'],
	'3' : ['m'],
	'4' : ['r'],
	'5' : ['l', 'lj'],
	'6' : ['š', 'č', 'ž', 'dž'],
	'7' : ['k', 'g'],
	'8' : ['f', 'v'],
	'9' : ['p', 'b'],
	'10' : ['c', 'dz'],
	'free' : ['a', 'e', 'h', 'i', 'j', 'o', 'u']
}

pl = {
	'0' : ['s','z'],
	'1' : ['d','t'],
	'10' : ['c','dz'],
 	'2' : ['n', 'ń'],
	'3' : ['m'],
	'4' : ['r'],
	'5' : ['l'],
	'6' : ['ć','ś','ź','ż','cz','dź','dż','rz','sz'],
	'7' : ['g','h','k','ch'],
	'70' : ['x','ks'],
	'78' : ['q','kw'],
	'8' : ['f','w','v'],
	'9' : ['b','p'],
	'free' : ['a', 'ą', 'e', 'ę','i','j','ł','o','ó','u','y']
}

sk = {
	'0' : ['s','z'],
	'1' : ['d', 'ď', 't', 'ť'],
	'10' : ['c','dz'],
	'2' : ['n', 'ň'],
	'3' : ['m'],
	'4' : ['r'],
	'44' : ['ŕ'],
	'5' : ['l'],
	'55' : ['ĺ'],
	'6' : ['č', 'dž', 'š', 'ž'],
	'7' : ['ch','g','k'],
	'70' : ['ks', 'x'],
	'78' : ['kv', 'q'],
	'8' : ['f','v','w'],
	'9' : ['b', 'p'],
	'free' : ['a','á','ä','e','é','h','i','í','j','o','ó','ô','u','ú','y','ý']
}

ελ = {
	'0':['σ','ς','ζ'],
	'1':['τ','δ','θ'],
	'2':['ν'],
	'3':['μ'],
	'4':['ρ'], 
	'5':['λ'],
	'6':['γ', 'γγ','χ','τσ'],
	'7':['κ'],
	'8':['φ','β','αυ','ευ','αύ','εύ'],
	'9':['π'], 
	'free':['α','ε','ι','η','υ','ο','ω','ά','έ','ί','ή','ύ','ό','ώ','αϊ','αϋ','εϋ'],
	'70':['ξ'], 
	'90':['ψ']
	}

es = {
	'0' : ['s', 'z', 'x'],
	'1' : ['d', 't', 'c', 'z'],
	'2' : ['n', 'ñ'],
	'3' : ['m'],
	'4' : ['r', 'rr'],
	'5' : ['l', 'll'],
	'6' : ['ch', 'x', 'sh'],
	'7' : ['g', 'j', 'c', 'qu', 'k', 'w'],
	'8' : ['f'],
	'9' : ['b', 'v', 'p', 'w'],
	'free' : ['a','e','i','o','u','y', 'á', 'é', 'í', 'ó', 'ú', 'ý']
}

instructions='''
    GGGG  EEEEE  EEEEE  K  K     OOO   FFFFF      A    L    L  
   G      E      E      K K     O   O  F         A A   L    L  
   G  GG  EEE    EEE    KK      O   O  FFF      AAAAA  L    L  
   G   G  E      E      K K     O   O  F        A   A  L    L  
    GGGG  EEEEE  EEEEE  K  K     OOO   F        A   A  LLL  LLL
   
               TTTTT  RRRR     A    DDD  EEEEE   SSSS
                 T    R   R   A A   D  D E        S  S
                 T    RRRR   AAAAA  D  D EEE       S
                 T    R  R   A   A  D  D E      S   S
                 T    R   R  A   A  DDD  EEEEE   SSSS

 First I will tell you what type of math problem you will be solving. You 
 choose how many digits to work with. Then give the answer, using - for 
 negative numbers and . for decimals. If you don't know the entire answer, it's
 okay to just give the first few digits, but you will get less points. Then you
 will choose a language and convert the numbers into a word in that language 
 using a secret code. 
'''

def again():
	yes = input("Do you want to play again? Y/n ")
	if yes[0].upper() == "Y":
		mainloop()
	else:
		print("Bye! Thanks for playing with me!")
		exit()

def special(progress):
	memorise = random.randrange(10**20,10**21)
	print("You have landed on a special square! Now you need to try to memorise this number. Use the secret code that you have learned to encode it into words to make it easier to remember. You have one minute to memorise as much as you can. You will get partial credit if you don't memorise it all.")
	print(memorise)
	time.sleep(60)
	print('\r\n'*100)
	guess = False
	while not guess:
		try:
			guess = int(input("Type the 20 digit number you have memorised: "))
			guess = str(guess)
		except:
			"You need to type a number. Just guess for numbers in positions you aren't sure of: "
	correct = 0
	for index, number in enumerate(guess):
		if str(guess)[index] == str(memorise)[index]:
			correct = correct + 1
	progress = progress + math.ceil(correct/4)
	print('The answer was ' + str(memorise) + '. You got ' + str(correct) + ' digits correct, for a total of ' + str(math.ceil(correct/4)) + ' points!')
	print('Progress: ' + str(progress))
	return progress


def mainloop():
	if __name__ == '__main__':
		print(instructions)
		helpon = "Y"
		helpon = input("Do you want help with the secret code? Y/n ")
		if not helpon:
			helpon = True
		elif helpon[0].upper() == "N":
			helpon = False
		else:
			helpon = True
	else:
		helpon = False

	try:
		goal = int(input("What score do you want to play to? (Default 30): "))
		if not goal:
			goal = 30
	except:
		goal = 30

	progress = 0
	turn = 0

	while progress < goal:
		turn = turn + 1
		print("Turn " + str(turn) + ": "),
		if progress/goal == 0.5:
			progress = special(progress)
		mathproblem = random.choice(maths)
		digits = 0
		while not digits:
			try:
				digits = int(input("How many digit numbers do you want to work with to solve " + mathproblem + "? "))
				while digits < 0:
					digits = int(input("Pick a number greater than 0! "))
				if mathproblem in hard and digits > 1:
					digits = int(input("This could be computationally expensive. This is your last chance to type a sane number like 1 here: "))
			except:
				print ("Type a number bigger than zero!")
		x = random.randint(int((str(1)+str(0)*digits)[0:-1]),int(str(9)*digits))
		y = random.randint(int((str(1)+str(0)*digits)[0:-1]),int(str(9)*digits))
		mathproblem = re.sub('x', str(x), mathproblem)
		mathproblem = re.sub('y', str(y), mathproblem)
		guess = False
		while not guess:
			try:
				guess = float(input("Solve " + mathproblem + " : "))
			except:
				print ("You need to type a number!")
		try:
			answer = float(eval(mathproblem))
		except ZeroDivisionError:
			progress = progress - 1
			print("Zero division error, you lose one point!")
		if guess == int(guess): # if they entered an integer instead of a float, this allows for partial credit
			guess = int(guess)
		if str(answer).find(str(guess)) == 0:
			print("That's right! Now turn the numbers into letters into a word. ")
			guess = str(guess)
			if '.' in guess: # we don't care about decimal points anymore
				guess = re.sub('\.', '', guess)
			if '-' in guess: # nor about negative numbers
				guess = re.sub('\-', '', guess)
			if len(str(guess)) in [1,2]: 
				print(str(0.5*digits) + " for length " + str(len(str(guess))))
				progress = progress + 0.5*digits
			elif len(str(guess)) in [3,4]:
				print(str(1*digits) + " for length " + str(len(str(guess))))
				progress = progress + 1*digits
			elif len(str(guess)) in [5,6]:
				print(str(2*digits) + " for length " + str(len(str(guess))))
				progress = progress + 2*digits
			else:
				print(str(3*digits) + " for length " + str(len(str(guess))))
				progress = progress + 3*digits
			msg = "Select a language: "
			for l in languages:
				msg = msg + l + ", "
			msg = msg + "or other: "
			lang = input(msg)
			if helpon:
				if lang not in languages: # if they typed something else in, show them english without checking
					lang = 'other'
				longkey = 'None'
				for key in eval(lang).keys():
					if key in guess and len(key) > 1:
						longkey = key
				for number in guess:
					msg = number + ': '
					for letter in eval(lang)[number]:
						msg = msg + letter + ', '
					print(msg[:-2]) # trailing comma
					if number == longkey[0]:
						msg = longkey + ': '
						for letter in eval(lang)[longkey]:
							msg = msg + letter + ', '
						print(msg[:-2])
				msg = 'Free: '
				for letter in eval(lang)['free']:
					msg = msg + letter + ', '
				print(msg[:-2])
			if lang not in languages: #languages we have automatic handling for
				lang = False
			word = False
			while not word:
				try:
					word = str(input("Enter a word that matches the digits in your answer, or the starting digits.\nThe digits must be in order: "))
				except:
					print("You need to enter a word. If you did enter a word, you're probably running this in python2 instead of python3. Try entering the word in quotation marks or installing python3. You need quotes for the language setting too if you're doing this in python2. Run this by typing python3 geek.py instead of python geek.py if you have both installed.")
			if not lang:
				try:
					worddigits = int(input("How many digits did you use in your word? "))
				except:
					print("Enter a number!")
			else: 
				i = 0
				worddigits = 0
				guessindex = 0
				number = guess[0]
				while i < len(word):
					try:
						if word[i:i+2] in eval(lang)[str(number)]: # two letters worth one: sz, 
							worddigits = worddigits + 1
							print("Points for " + word[i:i+2])
							i = i + 2
							guessindex = guessindex + 1
							number = guess[guessindex]
						elif word[i] in eval(lang)[str(number)]:
							print("Points for " + word[i])
							worddigits = worddigits + 1
							i = i + 1
							guessindex = guessindex + 1
							number = guess[guessindex]
						elif word[i] in eval(lang)['free'] or word[i:i+2] in eval(lang)['free']: # hungarian ly, greek 'αϊ','αϋ','εϋ'
							i = i + 1
						elif len(guess[i-1:i+1]) == 2 and guess[i-1:i+1] in eval(lang).keys(): # is there even a key for this combination of numbers
							if word[i] in eval(lang)[guess[i-1:i+1]]: # single letter worth two (x)
								print("Points for " + word[i])
								worddigits = worddigits + 2
								i = i + 1
								guessindex = guessindex + 1
								number = guess[guessindex]
						else:
							worddigits = math.ceil(worddigits/2)
							print(word[i] + ' is not an allowed letter! You lose some points, and if any allowed letters\nwere used after this point they won\'t be counted.')
							break
					except IndexError:
						pass
					except:
						print(sys.exc_info())
			if worddigits in [1,2]: 
				progress = progress + 0.5*digits
			elif worddigits in [3,4]:
				progress = progress + 1*digits
			elif worddigits in [5,6]:
				progress = progress + 2*digits
			else:
				progress = progress + 3*digits
		else:
			print('Sorry, it was ' + str(answer))
		print('Progress: ' + str(progress) + " of " + str(goal))
	print('You win! You got there in ' + str(turn) + " turns, and received an average of " + str(round(progress/turn, 2)) + " points per turn.")
	again()

mainloop()
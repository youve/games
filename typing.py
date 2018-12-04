#!/usr/bin/python3
# simple typing speed counter

import time
import readline
import subprocess

def typeOwn():
    text = ''
    start = time.time()
    while True:
        newtext = input('').strip()
        if newtext: # reinsert new lines
            text = text + '\n' + newtext
            nexttext = ''
        else:
            break
    end = time.time()
    errors = 0
    return text.strip(), errors, end - start


def typeFortune():
    '''Get a short fortune for the user to type, and then check that what they typed matches it'''
    fortune = subprocess.getoutput('/usr/bin/fortune -s')
    fortune = fortune.split('\n')
    print('\n')
    for i, line in enumerate(fortune): # get rid of white space
        fortune[i] = line.strip()
        print(line)
    print('\n')
    text, errors, seconds = typeOwn()
    text = text.split('\n') #do it line by line so a single error early on doesn't throw it all out
    while len(text) < len(fortune): #line things up
        text = text.append('\n')
    for i, line in enumerate(fortune):
        while len(text[i]) < len(fortune[i]): #line things up
            text[i] = text[i] + " "
        for j in range(len(fortune[i])):
            if fortune[i][j] != text[i][j]:
                errors += 1
    text = '\n'.join(text) 
    return text, errors, seconds
    
if input('Type your [O]wn text or an [A]ssigned one? ').upper() == 'O':
    text, errors, seconds = typeOwn()
else:
    text, errors, seconds = typeFortune()

print(f'You typed {len(text)} characters in {round(seconds)} seconds. {round(len(text)*60/(seconds))} CPM or {round(len(text)*60/5/(seconds))} WPM. You made {errors} errors. ')

#todo: adjusted WPM/CPM for errors
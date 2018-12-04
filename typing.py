#!/usr/bin/python3
# simple typing speed counter

import time
import readline
import subprocess
import sys
import argparse

parser = argparse.ArgumentParser(description='Take a typing test.')
parser.add_argument('-f', '--fortune', type=str, help="Args to pass onto fortune. default: s", 
    default='s', nargs='*')
args = parser.parse_args()

def typeOwn(paragraphs=1):
    text = []
    start = time.time()
    while len(text) < paragraphs:
        text.append(sys.stdin.readline().strip())
    end = time.time()
    text = '\n'.join(text)
    errors = []
    return text, errors, round(end - start)


def typeFortune():
    '''Get a short fortune for the user to type, and then check that what they typed matches it'''
    fortune = subprocess.getoutput('/usr/bin/fortune ' + '-' + ' '.join(args.fortune))
    fortune = fortune.split('\n')
    print('\n')
    for i, line in enumerate(fortune): # get rid of white space
        fortune[i] = line.strip()
        print(line)
    print('\n')
    text, errors, seconds = typeOwn(len(fortune))
    text = text.split('\n') #do it line by line so a single error early on doesn't throw it all out
    for i, line in enumerate(fortune):
        while len(text[i]) < len(fortune[i]): #line things up
            text[i] = text[i] + " "
        for j in range(len(fortune[i])):
            if fortune[i][j] != text[i][j]:
                if j-5 > 0:
                    mistake = [fortune[i][j-5:j+5] + '\n'] #surrounding context of the error
                else: #mistake is near the beginning
                    mistake = [fortune[i][:j+5] + '\n']
                mistake.append(text[i][j-5:j])
                mistake.append('\033[4m' + text[i][j] + '\033[0m') # underline the error
                mistake.append(text[i][j+1:j+5])
                errors.append(''.join(mistake))
    text = '\n'.join(text) 
    return text, errors, seconds
    
if input('Type your [O]wn text or a [F]ortune cookie? ').upper() == 'O':
    text, errors, seconds = typeOwn()
else:
    text, errors, seconds = typeFortune()

#get stats ready for printing
colWidth = 1
characters = str(len(text))
CPM = str(round(len(text)*60/(seconds)))
WPM = str(round(len(text)*60/5/(seconds)))
errorRate = str(round(100 - 100*(len(text)-len(errors))/len(text),2))
errorCount = str(len(errors))
ACPM = str(round((len(text) - len(errors))*60/seconds))
AWPM = str(round((len(text) - len(errors))*60/5/seconds))
seconds = str(seconds)

# align columns
for item in (characters, seconds, CPM, WPM, errorRate, errorCount, ACPM, AWPM):
    if len(item) > colWidth:
        colWidth = len(item) + 2

#Print errors
print(f'\nErrors: {errorCount}')
for error in errors:
    print(error,'\n')

#Print stats
print('Statistics:')
print(f'Characters: {characters.rjust(colWidth)}\tSeconds: {seconds.rjust(colWidth)}\tCPM:  {CPM.rjust(colWidth)}\tWPM:  {WPM.rjust(colWidth)}')
if errors:
    print(f'Error rate: {errorRate.rjust(colWidth)}%\tErrors:  {errorCount.rjust(colWidth)}\tACPM: {ACPM.rjust(colWidth)}\tAWPM: {AWPM.rjust(colWidth)}')

#!/usr/bin/python3
# Make maths Pictures
# usage: ./mathsPictures.py ulam ulam.png -f 'crimson' -b 'midnightblue' -s 100
# creates a 100x100 pixel crimson ulam spiral on a midnightblue background
# ./mathsPictures.py xor xor.png -f 'darkgreen' creates a darkgreen tinted xor image.

from PIL import ImageColor
from PIL import Image
import argparse
import time
import math
import logging
#logging.disable()
logging.basicConfig(level=logging.DEBUG, format='%(lineno)s - %(asctime)s - %(levelname)s - %(message)s')


def xor(size): 
    '''Each pixel is the xor of the x and y coordinates, multiplied by the RGB value of the
    specified foreground colour. Background colour doesn't affect anything.
    Using x%256 XOR y%256 allows us to make pictures of any size'''
    im = Image.new('RGBA', (size,size), args.background)
    for x in range(0,size):
        for y in range(0,size):
            im.putpixel((x, y), (round(foreground[0]/255*(x%256^y%256)), round(foreground[1]/255*(x%256^y%256)), round(foreground[2]/255*(x%256^y%266))))
    im.save(args.file)
    print (f'\nImage saved to {args.file}.')

def ulam(size):
    '''Starting in the center and going in an anti-clockwise spiral, colour prime pixels with 
    the foreground colour. '''
    im = Image.new('RGBA', (size,size), args.background)
    start = time.time()
    directions = ['D', 'L', 'U', 'R']  # backwards so we can use negative indices to wrap around
    direction = 'R'
    count = 0
    sidelength = 1
    x, y = size//2, size//2
    if size%2 == 0:
        x, y = int(size/2 -1), int(size/2)
    print('Making image: ')
    start = time.time()
    for i in range(1,size**2):
        if i > 1 and i in range(1,size**2,size**2//20):
            percentDone = 100*i/size**2
            timeElapsed = time.time() - start
            #ETAs are very wrong because factorising big numbers is slower than factorising little numbers
            logging.debug(f'percentDone: {round(percentDone,2)}\ttimeElapsed: {round(timeElapsed,2)}\t')
            print(f'{round(percentDone)}% done. ETA in {round(timeElapsed*(100-percentDone)/percentDone)} seconds.')
        f = divisors(i)
        if f == 2: # prime
            im.putpixel((x, y), foreground)
        else:
            if ImageColor.getcolor(args.background, 'L') >= 128: # bright background gets darker when more composite
                im.putpixel((x, y), (round(3/f*(background[0])), round(3/f*(background[1])), round(3/f*(background[2]))))
            else: #darker background gets brighter when more composite
                im.putpixel((x, y), (min(255,round(f/3*(f + background[0]))), min(255,round(f/3*(f + background[1]))), min(255,round(f/3*(f + background[2])))))
        count +=1
        if direction == 'R':
            x = x+1
        elif direction == 'U':
            y = y-1
        elif direction == 'L':
            x = x-1
        elif direction == 'D':
            y = y+1
        if count == sidelength:
            if direction in ('U', 'D'):
                sidelength += 1
            count = 0
            direction = directions[directions.index(direction) - 1]
    im.save(args.file)
    print (f'\nImage saved to {args.file}.')

def prime(max):
    '''Return all primes below max. No longer used in ulam.'''
    primes = [2]
    for i in range(3,max):
        composite = False
        for prime in primes:
            if i%prime == 0:
                composite = True
                break
        if not composite:
            primes.append(i)
    return primes

def divisors(n):
    '''return the number of divisors a number has'''
    divisors = 0
    i = 1
    while i <= n**(1/2):
        if n % i == 0:
            if i*i == n:
                divisors += 1
            else:
                divisors += 2
        i += 1
    return divisors

modes={'xor' : xor, 'ulam' : ulam}

parser = argparse.ArgumentParser(description='Make an ulam spiral.')
parser.add_argument('-s', '--size', metavar="255", type=int, choices=range(1,4095), help="Image size.", 
    default='255', nargs='?')
parser.add_argument('-f', '--foreground', metavar="mediumpurple", type=str, help="foreground colour", default="mediumpurple", nargs="?")
parser.add_argument('-b', '--background', metavar="darkgray", type=str, help="Background colour", default="darkgray", nargs="?")
parser.add_argument('mode', help='ulam, xor', choices=modes.keys())
parser.add_argument('file', type=str, metavar='outputFilename.png', help='output file name')

args = parser.parse_args()

try: 
    foreground = ImageColor.getcolor(args.foreground, 'RGBA')
except ValueError:
    foreground = ImageColor.getcolor('mediumpurple', 'RGBA')
try:
    background = ImageColor.getcolor(args.background, 'RGBA')
except ValueError:
    background = ImageColor.getcolor('darkgray', 'RGBA')

modes[args.mode](args.size)
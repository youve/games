#!/usr/bin/python3
# Make maths Pictures
# usage: ./mathsPictures.py ulam ulam.png -f 'crimson' -b 'midnightblue' -s 100
# creates a 100x100 pixel crimson ulam spiral on a midnightblue background
# ./mathsPictures.py xor xor.png -f 'darkgreen' creates a darkgreen tinted xor image.

from PIL import Image, ImageColor, ImageDraw
import argparse
import time
import cmath
import logging
import random
from numba import jit, int32, complex128
#logging.disable()
logging.basicConfig(level=logging.DEBUG, format='%(lineno)s - %(asctime)s - %(levelname)s - %(message)s')

def xor(size): 
    '''Each pixel is the xor of the x and y coordinates, multiplied by the RGB value of the
    specified foreground colour. Background colour doesn't affect anything.
    Using x%256 XOR y%256 allows us to make pictures of any size'''
    print('Making an XOR.')
    im = Image.new('RGBA', (size,size), background)
    for x in range(0,size):
        for y in range(0,size):
            im.putpixel((x, y), (round(foreground[0]/255*(x%256^y%256)), round(foreground[1]/255*(x%256^y%256)), round(foreground[2]/255*(x%256^y%266))))
    im.save(args.file)
    im.show()
    print (f'\nImage saved to {args.file}.')

def gradiant(size):
    '''Produces wobbly lines varying in colour very slowly'''
    print('Making gradiant')
    im = Image.new('RGBA', (size,size), background)
    r = foreground[0]
    g = foreground[1]
    b = foreground[2]
    a = foreground[3]
    for x in range(0,size):
        for y in range(0,size):
            im.putpixel((x, y), (r, g, b, a))
            r = max(0, min(255, r + random.randint(-1,1)))
            g = max(0, min(255, g + random.randint(-1,1)))
            b = max(0, min(255, b + random.randint(-1,1)))
    im.save(args.file)
    im.show()
    print(f'\nImage saved to {args.file}.')

def makeSpiral(x, y, size, step=1): #clockwise=False
    '''Returns next x,y coordinate based on current x,y coordinates, and image size. 
    The spiral goes anticlockwise and always starts out going right. Even sized spirals
    finish at the top left; odd sized spirals finish at the bottom right.'''
    while step > 0:
        if size%2 == 1:
            if x <= y and x + y >= size -1: #right
                x = x + 1
            elif x > y and x + y <= size -1: #left
                x = x - 1
            elif x <= y and x + y < size -1: #down
                y = y + 1
            elif x > y and x + y > size -1: #up
                y = y - 1
        else:
            if x < y and x + y >= size -1: #right
                x = x + 1
            elif x >= y and x + y <= size -1: #left
                x = x - 1
            elif x < y and x + y < size -1: #down
                y = y + 1
            elif x >= y and x + y >= size: #up
                y = y - 1
        step -= 1
    return x, y

def ulam(size):
    '''Starting in the center and going in an anti-clockwise spiral, colour prime pixels with 
    the foreground colour. '''
    print('Making an ulam spiral.')
    im = Image.new('RGBA', (size,size), background)
    start = time.time()
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
            #logging.debug(f'percentDone: {round(percentDone,2)}\ttimeElapsed: {round(timeElapsed,2)}\t')
            print(f'{round(percentDone)}% done. ETA in {round(timeElapsed*(100-percentDone)/percentDone)} seconds.')
        f = divisors(i)
        if f == 2: # prime
            im.putpixel((x, y), foreground)
        else:
            if ImageColor.getcolor(args.background, 'L') >= 128: # bright background gets darker when more composite
                im.putpixel((x, y), (round(3/f*(background[0])), round(3/f*(background[1])), round(3/f*(background[2]))))
            else: #darker background gets brighter when more composite
                im.putpixel((x, y), (min(255,round(f/3*(f + background[0]))), min(255,round(f/3*(f + background[1]))), min(255,round(f/3*(f + background[2])))))
        x, y = makeSpiral(x, y, size)
    im.save(args.file)
    im.show()
    print (f'\nImage saved to {args.file}.')

def fib(size):
    '''Fibonacci nubmers are foreground, other numbers are background'''
    print('Making a Fibonacci spiral')
    im = Image.new('RGBA', (size,size), background)
    #draw = ImageDraw.Draw(im)
    x, y = size//2, size//2
    f = fibonacci(1,2)
    nextf = next(f)
    print(nextf)
    if size%2 == 0:
        x, y = int(size/2 -1), int(size/2)
    for i in range(1,size**2):
        if x%(size//20) == 0:
            print(f'{round(100*x/size)}% done.')
        if i == nextf:
            nextf = next(f)
            im.putpixel((x, y), foreground)
            #draw.line([(x, y), (makeSpiral(x,y, size, step=nextf - i))], fill=foreground)
            print(nextf)
        x,y = makeSpiral(x, y, size)
    im.save(args.file)
    # This image is pretty disappointing because the fibonacci's get big fast.
    im.show()
    print(f'\nImage saved to {args.file}.')

#@jit(int32,int32(int32))
def fibonacci(a=0,b=1):
    '''generator that yields the next fibonacci number'''
    while True:
        yield a
        a, b = b, a + b

def hilbert():
    '''Hilbert numbers are numbers that match the pattern 4×n +1'''
    i = 0
    while True:
        h = 4*i + 1
        i +=1
        yield h

@jit(int32[:](int32))
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

@jit(int32(int32))
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

modes={'xor' : xor, 'ulam' : ulam, 'gradiant' : gradiant, 'fib' : fib}

parser = argparse.ArgumentParser(description='Make maths pictures.')
parser.add_argument('-s', '--size', metavar="255", type=int, choices=range(1,4095), 
    help="Image size.", default='255', nargs='?')
parser.add_argument('-f', '--foreground', metavar="mediumpurple", type=str, nargs="?", 
    help="foreground colour", default="mediumpurple")
parser.add_argument('-b', '--background', metavar="darkgray", type=str, default="darkgray", 
    help="Background colour", nargs="?")
parser.add_argument('mode', help=', '.join(list(modes.keys())) choices=modes.keys())
parser.add_argument('file', type=str, metavar='outputFilename.png', help='output file name')

args = parser.parse_args()

try: 
    foreground = ImageColor.getcolor(args.foreground, 'RGBA')
except ValueError:
    foreground = ImageColor.getcolor('mediumpurple', 'RGBA')
    print(f'{args.foreground} isn\'t a valid colour. Using mediumpurple instead.')
try:
    background = ImageColor.getcolor(args.background, 'RGBA')
except ValueError:
    print(f'{args.background} isn\'t a valid colour. Using darkgray instead.')
    background = ImageColor.getcolor('darkgray', 'RGBA')
try:
    center = complex(args.center)
except ValueError:
    print(f'{args.center} isn\'t a valid complex number. Using 0+0j instead')
    center = 0j

modes[args.mode](args.size)
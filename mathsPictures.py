#!/usr/bin/python3
# Make maths Pictures
# usage: ./mathsPictures.py ulam ulam.png -f 'crimson' -b 'midnightblue' -s 100
# creates a 100x100 pixel crimson ulam spiral on a midnightblue background
# ./mathsPictures.py xor xor.png -f 'darkgreen' creates a darkgreen tinted xor image.

from PIL import ImageColor
from PIL import Image
import argparse
import time
import cmath
import logging
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
    print (f'\nImage saved to {args.file}.')

def ulam(size):
    '''Starting in the center and going in an anti-clockwise spiral, colour prime pixels with 
    the foreground colour. '''
    print('Making an ulam spiral.')
    im = Image.new('RGBA', (size,size), background)
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

def mandelbrot(size):
    '''Create a picture of a Mandelbrot. The foreground colour is an offset'''
    print('Making a Mandelbrot')
    im = Image.new('RGBA', (size,size), background)
    for x in range(0,size):
        if x%(size//20) == 0:
            print(f'{round(100*x/size)}% done.')
        for y in range(0,size):
            z = xyToComplex(x,y,size,center)
            escape = mandelbrotEscape(z)
            # RGB allows for 16**6 colours and escape is a number between 0 and tries
            foregroundDec = foreground[0]*256**2 + foreground[1]*256 + foreground[2]
            baseColourDec = escape*16**6//args.tries
            colour = '#{:06X}'.format((foregroundDec + baseColourDec)%16**6)
            colour = ImageColor.getcolor(colour, 'RGBA')
            im.putpixel((x, y), colour)
    im.save(args.file)
    print (f'\nImage saved to {args.file}.')

@jit(complex128(int32,int32,int32,complex128))
def xyToComplex(x,y, size, center=complex(0)):
    '''convert x y coordinates that have 0,0 at the top left to imaginary coordinates
    centred around the point specified with the -c flag. Returns a complex number'''
    zoom=args.zoom
    zReal, zImag = center.real, center.imag
    if x > size/2: #right half
        #suppose x is 180 and the image is 240 pixels wide
        #take x, subtract half the image so that 0 now represents the middle. 
        #now we have a number like 60 
        #divide by the size of the quadrant, getting 0.5 because we're halfway across the quadrant
        #and then divide by zoom to zoom in that much?
        zReal += (x - size/2)/(size*zoom/2)
    elif x < size/2: #left half
        zReal -= ((size/2) -x)/(size*zoom/2)
    if y > size/2: #top half
        zImag += (y - size/2)/(size*zoom/2)
    elif y < size/2: #bottom half
        zImag -= ((size/2) -y)/(size*zoom/2)
    return complex(zReal, zImag)

@jit(int32(complex128))
def mandelbrotEscape(z):
    '''
    Convert the complex number to polar coordinates. The r coordinate gives
    the radius from 0. If that stays less than 2 for 1000 tries, it's probably
    in the Mandelbrot set. If it ever gets bigger than 2, then squaring it will make it
    rapidly approach infinity and is definitely not in the Mandelbrot set.

    Return how many tries it took before the number got bigger than 2"
    '''
    tries = args.tries
    newz = z**2 + z
    bailout = tries
    while cmath.polar(newz)[0] < 2 and bailout > 0:
        newz = newz**2 + z
        bailout = bailout - 1
    return tries - bailout

modes={'xor' : xor, 'ulam' : ulam, 'mandelbrot' : mandelbrot}

parser = argparse.ArgumentParser(description='Make maths pictures.')
parser.add_argument('-s', '--size', metavar="255", type=int, choices=range(1,4095), 
    help="Image size.", default='255', nargs='?')
parser.add_argument('-f', '--foreground', metavar="mediumpurple", type=str, nargs="?", 
    help="foreground colour", default="mediumpurple")
parser.add_argument('-b', '--background', metavar="darkgray", type=str, default="darkgray", 
    help="Background colour", nargs="?")
parser.add_argument('-c', '--center', metavar='real,imag', type=complex, default='0+0j', nargs='?', 
    help='a complex number to centre the Mandelbrot set on')
parser.add_argument('-t', '--tries', metavar=10000, type=int, default=10000, nargs='?',
    help='how many times to iterate before deciding a number is in the Mandelbrot set. Larger = more accurate, slower')
parser.add_argument('-z', '--zoom', metavar=.5, type=float, default=.5, nargs='?', 
    help='how far to zoom in on the Mandelbrot set')
parser.add_argument('mode', help='ulam, xor, mandelbrot', choices=modes.keys())
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
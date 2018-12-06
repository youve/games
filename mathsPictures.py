#!/usr/bin/python3
# Make maths Pictures
# usage: ./mathsPictures.py ulam ulam.png -f 'crimson' -b 'midnightblue' -s 100
# creates a 100x100 pixel crimson ulam spiral on a midnightblue background
# ./mathsPictures.py xor xor.png -f 'darkgreen' creates a darkgreen tinted xor image.

from PIL import ImageColor
from PIL import Image
import argparse

def xor(size): 
    '''Each pixel is the xor of the x and y coordinates, multiplied by the RGB value of the
    specified foreground colour. Background colour doesn't affect anything.
    Using x%256 XOR y%256 allows us to make pictures of any size'''
    im = Image.new('RGBA', (size,size), args.background)
    for x in range(0,size):
        for y in range(0,size):
            im.putpixel((x, y), (round(foreground[0]/255*(x%256^y%256)), round(foreground[1]/255*(x%256^y%256)), round(foreground[2]/255*(x%256^y%266))))
    im.save(args.file)

def ulam(size):
    '''Starting in the center and going in an anti-clockwise spiral, colour prime pixels with 
    the foreground colour. '''
    im = Image.new('RGBA', (size,size), args.background)
    primes = prime(size**2)
    directions = ['D', 'L', 'U', 'R']  # backwards so we can use negative indices to wrap around
    direction = 'R'
    count = 0
    sidelength = 1
    x, y = size//2, size//2
    if size%2 == 0:
        x, y == size/2 -1, size/2
    for i in range(1,size**2):
        if i in primes:
            try:
                im.putpixel((x, y), foreground)
            except:
                #im.save(args.file)
                break
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

def prime(max):
    '''Return all primes below max'''
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
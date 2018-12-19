#!/usr/bin/python3
# usage: ./fractals.py --center=".5-1.3j" --tries 32768 --zoom 4 ship ship3.png --ssize 600 --foreground "#006"

import pygame
from pygame.locals import *
import argparse
import cmath
import math
import logging
import random
from numba import jit, int32, complex128
import sys
#logging.disable()
logging.basicConfig(level=logging.DEBUG, format='%(lineno)s - %(asctime)s - %(levelname)s - %(message)s')

#TODO listen for clicks even while building image and respond
#TODO speed things up by first doing big fuzzy pixels

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

@jit
def incColour(by):
    '''return colour''' #better than what I had
    if by == args.tries:
        return foreground
    step = (by * 16 ** 6) // args.tries
    increment = (step // (256 ** 2), step % (256 ** 2) // 256, step % 256)
    colour = list(foreground)
    for i, v in enumerate(increment): #maybe
        if foreground[i] + increment[i] < 256:
            colour[i] = foreground[i] + increment[i]
        else: colour[i] = 255 * 2 - foreground[i] - increment[i]
    return tuple(colour)

@jit
def nColor(by):
    '''return color''' # sometimes, but not usually pretty; also reduces available colours to 256.
    if by == args.tries:
        return foreground
    r = (foreground[0] + 256*(by/args.tries))%256
    g = (foreground[1] + 256*(by/args.tries))%256
    b = (foreground[2] + 256*(by/args.tries))%256
    return (r,g,b)

@jit
def smoothColor(by):
    '''return colour'''
    colour = pygame.Color(0,0,0,255)
    if by == args.tries:
        return colour
    for i, v in enumerate(foreground):
        colour[i] = int((v * (args.tries - by) / args.tries) + (background[i] * by / args.tries))
    colour.a = 255
    return colour

@jit
def bump():
    pixArray = pygame.PixelArray(windowSurface)
    for x in range(len(pixArray) - 1):
        for y in range(len(pixArray[0]) -1):
            newcolor = pygame.Color(pixArray[x][y] * 256 + 255) #otherwise it saves it as (0, r, g, b)
            if x == 0 and y == 0:
                logging.debug(newcolor)
            newcolor.r = max(min(int(newcolor.r + 256*((bumpArray[x+1][y+1] - bumpArray[x][y]) * 2)), 255), 0)
            newcolor.g = max(min(int(newcolor.g + 256*((bumpArray[x+1][y+1] - bumpArray[x][y]) * 2)), 255), 0)
            newcolor.b = max(min(int(newcolor.b + 256*((bumpArray[x+1][y+1] - bumpArray[x][y]) * 2)), 255), 0)
            newcolor.a = 255
            if x == 0 and y == 0:
                logging.debug(newcolor)
                logging.debug(bumpArray[x+1][y+1])
                logging.debug(pixArray[x][y])
            pixArray[x][y] = newcolor # why is it saving the colour's as (0, 144, 12, 14) 
            # instead of (144, 12, 14, 255)?
            if x == 0 and y == 0:
                logging.debug(pixArray[x][y])
        pygame.display.update()
    pixArray.close()

@jit
def anotherColor(by):
    '''return color''' # doesn't work
    if by == args.tries:
        return foreground
    bright = False
    step = (by*16**6)//args.tries
    if sum(foreground[:3])/3 >= 128: # bright
        bright = True
    r, g, b = 0, 0, 0
    for k, v in enumerate([r, g, b]):
        assignedMax = False
        assignedMin = False
        if bright: # in practice this usually sets r, g, b to 0 🙁
            if foreground[k] == min(foreground[:3]) and not assignedMin:
                v = min(0, foreground[k] - (step // (256 ** 2)))
                assignedMin = True
            elif foreground[k] == max(foreground[:3]) and not assignedMax:
                v = min(0, foreground[k] - (step % 256))
                assignedMax = True
            else:
                v = min(0, foreground[k] - (step % (256 ** 2) // 256))
        else: # in practice, this usually sets r, g, b to 255 🙁
            if foreground[k] == max(foreground[:3]) and not assignedMax:
                v = max(0, foreground[k] + (step // (256 ** 2)))
                assignedMax = True
            elif foreground[k] == min(foreground[:3]) and not assignedMin:
                v = max(0, foreground[k] + (step % 256))
                assignedMin = True
            else:
                v = max(0, foreground[k] + (step % (256 ** 2) // 256))
    return tuple((r, g, b))

def makeFractal(size, fType):
    '''Create a picture of a Mandelbrot. The foreground colour is an offset'''
    print(f'Making a {fType}')
    pixArray = pygame.PixelArray(windowSurface)
    global bumpArray
    bumpArray = [[]]
    for x in range(0, size):
        if x % (size // 20) == 0:
            print(f'{round(100 * x / size)}% done.')
        for y in range(0, size):
            z = xyToComplex(x , y , size , center)
            escape = iterEscape(z, fType)
            colour = smoothColor(escape)
            if x == 0 and y == 0:
                logging.debug(colour)
            pixArray[x][y] = colour
            if x == 0 and y == 0:
                logging.debug(pixArray[x][y])
            bumpArray[x].append(sum(colour[:3])/(256*3))
            #bumpArray[x].append(escape / args.tries)
        pygame.display.update()
        bumpArray.append([])
    bumpArray.append([0] * (size + 1))
    pixArray.close()

@jit(complex128(int32,int32,int32,complex128), cache=True)
def xyToComplex(x,y, size, center=complex(0)):
    '''convert x y coordinates that have 0,0 at the top left to imaginary coordinates
    centred around the point specified with the --center flag. Returns a complex number'''
    zReal, zImag = center.real, center.imag
    if x > size/2: #right half
        #suppose x is 180 and the image is 240 pixels wide
        #take x, subtract half the image so that 0 now represents the middle. 
        #now we have a number like 60.
        #divide by the size of the quadrant, which is size/2
        #getting 0.5 for this x because we're halfway across the quadrant
        #and also then divide by zoom to zoom in that much
        zReal += (x - size/2)/(zoom*size/2)
    elif x < size/2: #left half
        zReal -= ((size/2) -x)/(zoom*size/2)
    if y > size/2: #top half
        zImag += (y - size/2)/(zoom*size/2)
    elif y < size/2: #bottom half
        zImag -= ((size/2) -y)/(zoom*size/2)
    z = complex(zReal, zImag)
    if x == 0 and y == 0:
        print('Top left edge:', z)
    elif x == size -1 and y == size - 1:
        print('Bottom right edge: ', z)
    return z

@jit(int32(complex128, int32), cache=True)
def iterEscape(c, fType):
    '''
    Convert the complex number to polar coordinates. The r coordinate gives
    the radius from 0. If that stays less than 2 for many tries, it's probably
    in the Mandelbrot set. If it ever gets bigger than 2, then squaring it will make it
    rapidly approach infinity and is definitely not in the Mandelbrot set.

    Return how many tries it took before the number got bigger than 2"
    '''
    tries = args.tries
    z = equation[fType](c, c)
    bailout = tries
    while cmath.polar(z)[0] < 2 and bailout > 0:
        z = equation[fType](z, c)
        bailout = bailout - 1
    return tries - bailout

equation = {'mandelbrot' : lambda z, c : z ** 2 + c, 
            'ship' : lambda z, c : complex(abs(z.real), abs(z.imag))**2 + c,
            'test' : lambda z, c : z ** 1.75 - c,
            'magnet1' : lambda z, c: ((z ** 2 + (c - 1))/(2 * z + (c - 2))) ** 2,
            'magnet2' : lambda z, c : ((z ** 3 + 3 * (c - 1) * z + (c - 1) * (c - 2))
                 /(3 * z ** 2 + 3 * (c - 2) * c + (c - 1) * (c - 2) + 1)) ** 2,
            'sinh' : lambda z, c : cmath.sinh(z)**2 + c}

fg = pygame.Color(255)
fg.r, fg.g, fg.b = random.sample(range(0,256), k=3)
bg = pygame.Color(255 ^ fg[0], 255 ^ fg[1], 255 ^ fg[2])

parser = argparse.ArgumentParser(description='Make fractals.')
parser.add_argument('-s', '--size', metavar="255", type=int, choices=range(1,4095), 
    help="Image size.", default='255', nargs='?')
parser.add_argument('-f', '--foreground', metavar="crimson", type=str, nargs="?", 
    help="foreground colour", default=(fg))
parser.add_argument('-b', '--background', metavar="#003", type=str, nargs="?", 
    help="background colour", default=(bg))
parser.add_argument('--center', metavar='real,imag', type=complex, default='0+0j', nargs='?', 
    help='a complex number to centre the fractal on. You must specify it like --center="-.1-.1j" \
    with the equal sign or the argparser gets confused.')
parser.add_argument('-t', '--tries', metavar=255, type=int, default=2048, nargs='?',
    help='how many times to iterate. Default should be fine. Reduce it if it\'s slow.')
parser.add_argument('-z', '--zoom', metavar=.5, type=float, default=.5, nargs='?', 
    help='how far to zoom in on the fractal')
parser.add_argument('mode', help=', '.join(list(equation.keys())), choices=equation.keys())
parser.add_argument('file', type=str, metavar='outputFilename', help='output file name')

args = parser.parse_args()
center = 0j
zoom = args.zoom

#foreground, background = None, None

if not isinstance(args.foreground, pygame.Color):
    try: 
        foreground = pygame.Color(args.foreground)
    except ValueError:
        foreground = fg
        print(f'{args.foreground} isn\'t a valid colour. Using {fg} instead.')
else:
    foreground = args.foreground

if not isinstance(args.background, pygame.Color):
    try:
        background = pygame.Color(args.background)
    except ValueError:
        background = bg
        print(f'{args.background} isn\'t a valid colour. Using {bg} instead.')
else:
    background = args.background

try:
    center = complex(args.center)
except ValueError:
    print(f'{args.center} isn\'t a valid complex number. Using 0+0j instead')
    center = 0j

#set up pygame
pygame.init()
windowSurface = pygame.display.set_mode((args.size, args.size))
windowSurface.fill(foreground)
windowTitle = args.mode.capitalize() + ' : ' + str(center)
pygame.display.set_caption(windowTitle)

makeFractal(args.size, args.mode)

#Run the game loop.
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_s:
                filename = args.file + str(center) + 'x' + str(zoom) + '.png'
                pygame.image.save(windowSurface, filename)
                print (f'\nImage saved to {filename}.')
            elif event.key == K_b:
                bump()
        elif event.type == MOUSEBUTTONDOWN:
            x, y = event.pos
            center = xyToComplex(x, y, args.size, center)
            windowTitle = args.mode.capitalize() + ' : ' + str(center)
            pygame.display.set_caption(windowTitle)
            zoom = zoom * 2
            makeFractal(args.size, args.mode)


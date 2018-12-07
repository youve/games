#! /usr/bin/python3
# -*- coding: utf-8 -*-

##############################
# Module: Numberules
# Author: Plotinus
# Date: 2013-07-03
# Version: 0.2
'''
Guess the rule game
'''
##############################
# Log:
# 2013-07-05 added pronic numbers
# 2013-07-02 first version
##############################
import random, readline
instructions='''
0   0  1   1  2   2  333   44444  5555   6   6  7      88888   9999
00  0  1   1  22 22  3  3  4      5   5  6   6  7      8        9  9
0 0 0  1   1  2 2 2  333   444    5555   6   6  7      888       9
0  00  1   1  2   2  3  3  4      5  5   6   6  7      8      9   9
0   0   111   2   2  333   44444  5   5   666   77777  88888   9999

I am thinking of a type of number. I will give you 3 numbers between 0 and 9999 that match\nthe rule. Type in a number that you think matches the rule. I will tell you if it matches\nor not. If you are able to tell me five numbers that match my rule, you win. If you make\n10 wrong guesses, you lose.\n\n\n
'''
import random
def again():
    yes = input('Do you want to play again? Y/n ') or 'Y'
    if yes[0].upper() == 'Y':
        mainloop()
    else:
        print('Bye! Thanks for playing with me!')
        exit()

def prime():
    '''Primes are numbers that are only divisible by themselves and 1'''
    primes = [2]
    for i in range(3,10000):
        composite = False
        for prime in primes:
            if i%prime == 0:
                composite = True
                break
        if not composite:
            primes.append(i)
    return primes


def palindrome():
    '''Palindromes are numbers that are the same backwards and forwards like 1234321'''
    palindromes = []
    for i in range(10,9999):
        if str(i)[::-1] == str(i):
            palindromes.append(i)
    return palindromes

def square():
    '''Perfect squares are numbers that are multiplied by themselves, like 96×96=9216'''
    squares = []
    for i in range(0,100):
        squares.append(i**2)
    return squares

def cube():
    '''Perfect cubes are numbers that are multiplied by themselves three times, like
5×5×5 = 125'''
    cubes = []
    for i in range(0,22):
        cubes.append(i**3)
    return cubes

def triangle():
    '''Triangle numbers are 0, 0+1, 0+1+2, 0+1+2+3, 0+1+2+3+4, etc.'''
    triangles = [0]
    for i in range(1,141):
        triangles.append(triangles[-1] + len(triangles))
    return triangles

def star():
    '''Star numbers are centered figurate numbers that represent a centered six-pointed
star. The pattern is 6×n×(n-1) + 1.'''
    stars = []
    for n in range (1,43):
        if (6*n*(n-1) + 1) < 10000:
            stars.append(6*n*(n-1)+1)
    return stars

def tetrahedral():
    '''Tetrahedral numbers are figurate numbers that represent a pyramid with a triangular
base and three sides, called a tetrahedron.'''
    tetrahedra = []
    for n in range (1,100):
        if n*(n+1)*(n+2)/6 < 10000:
            tetrahedra.append(int(n*(n+1)*(n+2)/6))
    return tetrahedra

def even_or_odd(which=True):
    '''Even numbers are divisible by two. Odd numbers aren't.'''
    evens = []
    odds = []
    for i in range(0,10000):
        if i%2 == 0:
            evens.append(i)
        else:
            odds.append(i)
    if which:
        return evens
    else:
        return odds

def powerful():
    '''Powerful numbers are numbers where all of their prime factors are perfect powers for
example (3^3)x(2^2) = 108 is a powerful number, and so is 256 = 2^8, but 567 is not a
powerful number because it is 7×(3^4).'''
    pass

def achilles():
    '''Achilles numbers are numbers where all of the prime factors are perfect powers but
they are not themselves perfect powers. For example 108 is an achilles number because it is
(2^2)×(3^3), but it is not a perfect power itself. 36 is not an achilles number because
even though all of its prime factors are perfect powers (2^2)×(3^2), it is also a perfect
power: 6^2.'''
    pass

def nonhypotenuse():
    '''Non hypotenuse numbers are numbers that cannot form the hypotenuse of a right
triangle with integer sides. They are numbers that have no prime factors of the form 4k+1'''
    pass

def practical():
    '''Practical numbers are any positive integer n such that all smaller positive integers
can be represented as sums of distinct divisors of n. For example, 12 is practical because
all the numbers from 1 to 11 can be expressed as sums of its divisors:
1,2,3,4, and 6. For example 11=6+3+2, 8=6+2, etc.'''
    pass

def abundant():
    '''Abundant numbers are numbers for which the sum of its proper divisors is greater
than the number itself, for example 12 is divisible by 1,2,3,4, and 6. 6+4+3+2+1=16, which
is greater than 12.'''
    pass

def ulam():
    '''The standard Ulam Sequence starts with 1 and 2. The next number in the sequence is
the smallest integer that is the sum of two distinct earlier terms in exactly one way. For
example the next number is 3, and after that 4 (because 1+3 = 4, and 2+2 doesn't count
because they are not distinct), and after that is not 5 because 5 is 1+4 or 2+3.'''
    pass

####
#To add:
#
#Arithmetic numbers Highly abundant numbers Hyperperfect numbers Primitive abundant numbers Refactorable numbers Superabundant numbers
#
#semiprimes
#
#Highly cototient numbers Highly totient numbers Noncototients Nontotients Perfect totient numbers Sparsely totient numbers
#
#Deficient numbers Semiperfect numbers
#
#Erdős–Woods numbers Frugal numbers Harmonic divisor numbers Highly composite numbers Regular numbers Sphenic numbers Størmer numbers Super-Poulet numbers
#
#Equidigital numbers Extravagant numbers Friedman numbers Happy numbers Harshad numbers Kaprekar numbers Keith numbers Lychrel numbers Primeval numbers Repdigits Self numbers Strictly non-palindromic numbers Trimorphic numbers
#
#Narcissistic numbers

def pronic():
    '''Pronic numbers, also called rectangular numbers, are the product of two consecutive
integers: n(n+1).'''
    pronics = []
    for i in range (0,100):
        pronics.append(i*(i+1))
    return pronics

def fourth():
    '''Fourth powers are numbers that have been multiplied by themselves 4 times for
example 4×4×4×4=256'''
    fourths = []
    for i in range (0,10):
        fourths.append(i**4)
    return fourths

def undulating():
    '''Non-trivial undulating numbers are numbers that are at least three digits long and
take the form abababab. A and B are different numbers'
    '''
    undulators = []
    for i in range (100,10000):
        i = str(i)
        if i[0] == i[2] and i[0] != i[1]:
            if len(i) == 3 or i[1] == i[3]:
                undulators.append(int(i))
    return undulators

def lucky():
    '''To find the lucky numbers, you begin with a list of integers, starting with 1. You
get rid of every second number, leaving only the odd numbers. The second number left is 3,
so now you get rid of every third number in the remaining list. The next number left is 7,
so now we get rid of every seventh number, and so on.'''
    luckies = []
    for i in range (1,10000):
        luckies.append(i)
    del luckies[1::2]
    x = 3
    pos = luckies.index(x)
    while x in luckies:
        try:
            del luckies[x-1::x]
            pos = pos+1
            x = luckies[pos]
        except:
            return luckies

def proth():
    '''Proth numbers are numbers that fit the formula k×2^n + 1, where k are odd positive
integers, and 2^n > k.'''
    proths = []
    for k in range(1,99,2):
        for n in range(1,14):
            if 2**n > k and k*2**n+1<10000:
                proths.append(k*2**n+1)
    return set(proths)

def multiple(x):
    '''Divisibility by three: add up the digits of the number (e.g. 3711 3+7+1+1 = 12) if
    the resulting number is divisible by 3, then the number is divisible by three.

Divisibility by five: if the number ends in a 5 or a 0, then it is divisible by five.

Divisibility by seven: since 1001 is divisible by 7, substract 1001 from the number until
    it is less than 4 digits long. since 98 is divisible by 7, subtract 100 and add 2
    until the number is less than 3 digits long. then try substracting 70 or
    subtracting 10 adding 3 until you can tell whether it's divisible by 7 or not.

Divisibility by eleven: multiply the last digit of the number by 11 and subtract it from
    the number, then remove the trailing zero (e.g. 7392-22 = 7370/10 = 737). if it
    seems easier, you can instead subtract the last digit from 10, multiply that by 11
    and add that to the number (e.g. 737+33 = 770).remove the trailing 0 again and you
    have 77 which is obviously divisible by 11.
    '''
    multiples = []
    for i in range(0,10000,x):
        multiples.append(i)
    return multiples

def thabit():
    '''Thabit numbers are numbers that match the pattern 3×2^n - 1'''
    thabits = []
    for i in range(0,12):
        thabits.append(3*2**i-1)
    return thabits

def hilbert():
    '''Hilbert numbers are numbers that match the pattern 4×n +1'''
    hilberts = []
    for i in range(0,2500):
        hilberts.append(4*i+1)
    return hilberts

def leyland():
    '''Leyland numbers are numbers that match that pattern x^y + y^x, where x and y are
greater than 1.'''
    leylands = []
    for x in range(2,16):
        for y in range(2,16):
            if x >= y and x**y+y**x <10000: # x>=y avoids duplication
                leylands.append(x**y+y**x)
    return leylands

def fib():
    '''The fibonacci numbers start with 0, 1, and each subsequent number is the sum of the
previous two: 0+1 = 1, 1+1 = 2, 1+2 =3, 2+3=5, 3+5=8, and so on.'''
    fibs = [0,1]
    while fibs[-1] < 10000:
        fibs.append(fibs[-1]+fibs[-2])
    del fibs[-1]
    return set(fibs)

def jacobsthal():
    '''The jacobsthal numbers are like the fibonacci numbers. the series starts with 0 and
1. each subsequent number is the sum of the previous number and twice the number before
that: 0×2+1 = 1, 1×2+1 = 3, 1×2+3=5, 3×2+5=11, 5×2+11= 21, and so on.'''
    jacobsthals = [0,1]
    while jacobsthals[-1] < 10000:
        jacobsthals.append(jacobsthals[-1]+jacobsthals[-2]*2)
    del jacobsthals[-1]
    return set(jacobsthals)

def pell():
    '''The pell numbers are like the fibonacci numbers. The series starts with 0 and 1.
Each subsequent number is the sum of twice the previous number and the number before that:
0, 1, 1*2+0 = 2, 2*2+1 = 5, 5*2+3 =13, and so on.'''
    pells = [0,1]
    while pells[-1] < 10000:
        pells.append(pells[-1]*2+pells[-2])
    del pells[-1]
    return set(pells)

def pelllucas():
    '''The pell lucas numbers are recursively defined numbers. the series starts with 2 and
2. Each subsequent number is the sum of twice the previous number and the number before
that: 2, 2, 2*2+2=6, 2*6+2=14, 2*14+6=34, and so on.'''
    pelllucases = [2,2]
    while pelllucases[-1] < 10000:
        pelllucases.append(pelllucases[-1]*2+pelllucases[-2])
    del pelllucases[-1]
    return set(pelllucases)

def leonardo():
    '''The leonardo numbers are like the fibonacci numbers. the series starts with 1 and 1.
Each subsequent number is the sum of the previous two numbers +1: 1+1+1 = 3, 1+3+1 = 5,
3+5+1 = 9, 5+9+1 = 15, and so on.'''
    leonardos = [1,1]
    while leonardos[-1] < 10000:
        leonardos.append(leonardos[-1]+leonardos[-2]+1)
    del leonardos[-1]
    return set(leonardos)

def perrin():
    '''The perrin numbers are defined by the recursively. the first three numbers are 3, 0,
and 2. the subsequent numbers are 'the last but one number + the number before that'. so:
3, 0, 2, 3+0=3, 0+2 = 2, 2+3 = 5, 3+2 = 5, 2+5 = 7, 5+5 = 10, and so on.'''
    perrins = [3,0,2]
    while perrins[-1] < 10000:
        perrins.append(perrins[-2]+perrins[-3])
    del perrins[-1]
    return set(perrins)

def polite(which=True):
    '''The polite numbers are numbers that can be expressed as the sum of 2 or more
consecutive integers. the impolite numbers are the perfect powers of two.'''
    polite = []
    powersoftwo = []
    for i in range(0,14):
        powersoftwo.append(2**i)
    for i in range(1,10000):
        if i not in powersoftwo:
            polite.append(i)
    if which:
        return polite
    else:
        return powersoftwo

def motzkin():
    '''Each nth motzkin number represents the number of different ways of drawing
non-intersecting chords on a circle between n points.'''
    ###    motzkins = [1,2,4,9,21,51,127,323,835,2188,5798]
    pass

def mainloop():
    series = random.choice([prime, palindrome, square, cube, triangle, even_or_odd, fourth,
        undulating, lucky, proth, multiple, thabit, hilbert, leyland, fib, jacobsthal, leonardo,
        pell, pelllucas, fib, jacobsthal, leonardo, pell, tetrahedral, pronic])
    which = None
    if series == multiple:
        which = random.choice([3,5,7,11])
    elif series in (even_or_odd, polite):
        which = random.choice([True, False]) 
    if which:
        secret = series(which)
    else:
        secret = series()
    sample = random.sample(secret,3)
    excluded = []
    print(instructions)
    guesses = 10
    correct = 0
    while guesses > 0 and correct < 5:
        nonesense = False
        print('Guesses remaining: ', guesses)
        print('Correct answers: ', correct)
        print('Included:', sample)
        if excluded: print('Excluded:', excluded)
        try:
            guess = int(input('Guess a number that matches these numbers: '))
        except:
            guess = 'nonesense'
            print('I don\'t know what that means.')
            nonesense = True
        if guess in sample or guess in excluded:
            print('You already know about that number!')
        elif guess in secret:
            sample.append(guess)
            correct += 1
        elif nonesense:
            pass
        else:
            excluded.append(guess)
            guesses -= 1
    if correct == 5:
        print('You win!')
        print('Rule:', series.__doc__)
    else:
        print('You lose!')
        print('Rule:', series.__doc__)
    again()

mainloop()

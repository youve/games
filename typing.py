#!/usr/bin/python3
# simple typing speed counter

import time
import readline

input('Press enter when you\'re ready to begin typing, then press enter again when you\'re done.')
start = time.time()

text = input('Go: ')

end = time.time()

print(f'You typed {len(text)} characters in {round(end - start)} seconds. {round(len(text)*60/(end - start))} CPM or {round(len(text)*60/5/(end - start))} WPM ')

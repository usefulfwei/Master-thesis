# -*- coding: utf-8 -*-

# author:Lichang

import msvcrt


print('enter q to quit')

while True:
    if ord(msvcrt.getch()) in [81,113]:
        break

print('goes out')
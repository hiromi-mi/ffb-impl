# SPDX-License-Identifier: CC0-1.0
# Maintainer: hiromi_mi
# Original Author: [Sego](https://esolangs.org/wiki/User:Sgeo)
# Python 3 Implementation of [Foobar and Foobaz and Barbaz, oh my!](https://esolangs.org/wiki/Foobar_and_Foobaz_and_Barbaz,_oh_my!)

the_code = []
dot_value = 0 #Yes, I know Python needs no variable declaration!
bang_value = 0
from pyparsing import Word, nums, oneOf, ParseException
import sys
lvars = '?!.' + nums
rvars = '!.'
line = Word(lvars) + "and" + Word(lvars) + "and" + Word(lvars) + ", oh my" + oneOf('! . ...')

the_code = open(sys.argv[1]).read().splitlines()

def process_code(code): #A bit inaccurate, compiles
    p_code = [] #Should be a list of 4-tuples.
    for i in code:
        try:
            i = line.parseString(i)
        except ParseException:
            print(i)
            raise
        
        del i[5]
        del i[3]
        del i[1]
        i = tuple(i)
        p_code.append(i)
    return p_code


def do_code(p_code):
    global dot_value
    global bang_value
    nextline = 0
    while True:
        i = nextline
        v = p_code[i]
        v = list(v)
        using_out = False
        using_next = False
        using_bang = False
        for j, k in enumerate(v):
            if k == '!':
                v[j] = bang_value
                if j==3:
                    using_bang = True
            elif k == '.':
                v[j] = dot_value
                if j==3:
                    using_out = True
            elif k == '?':
                try:
                    t = ord(input()[0])
                    if t >=0 and t <256:
                        v[j] = t
                    else:
                        raise ValueError
                except IndexError:
                    v[j]=0
            elif k == '...':
                v[j] = i
                using_next = True
            #elif int(k) < 0 or int(k) >= 256:
            #    raise ValueError
            else:
                v[j] = int(v[j])

        #print "At instruction " + str(i) + ":",str(v)
        ans = (v[0] & v[1]) | (v[2] & v[3])
        if using_out:
            sys.stdout.write(chr(ans))
            dot_value = ans
        if using_next:
            nextline = ans
        else:
            nextline+=1
        if using_bang:
            bang_value = ans
        #print nextline

if __name__=='__main__':
    p_code = process_code(the_code)
    try:
        do_code(p_code)
    except IndexError:
        print()
        sys.exit()

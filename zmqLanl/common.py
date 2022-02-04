#!/usr/bin/env python
def get_list(x):
    '''Returns a list [x] if x is not a list'''
    if isinstance(x, list):
        return x
    else:
        return [x]

def toListByteStrings(listOfStrings):
    '''Converts a list of strings f to a list of byte strings'''
    return [f.encode('utf-8') for f in get_list(listOfStrings)]

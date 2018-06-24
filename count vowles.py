# -*- coding: utf-8 -*-
"""
Created on Sun Jun 24 12:49:38 2018

@author: natew
"""

def count_vowels():
    vowels = 'aeiou'
    string = str(input("Please enter a your sentence:  "))
    string=string.lower()
    vowel_count=0
    for char in string:
        for vowel in vowels:
            if char == vowel:
                vowel_count+=1
    return vowel_count

print("The number of vowels is {}".format(count_vowels()))

    
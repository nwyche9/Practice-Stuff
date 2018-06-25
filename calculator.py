# -*- coding: utf-8 -*-
"""
Created on Sun Jun 24 15:24:43 2018

@author: natew
"""

def calc(a, b, op):
    if op not in '+-/*^':
        return 'Please only use one of these characters: "+,-,/,*,^"!'
    
    if op =='+':
        return(str(a) + ' '+ op+ ' '+str(b) + ' = ' + str(a + b))
    if op =='-':
        return(str(a)+' '+op+' '+str(b)+' = '+str(a-b))
    if op =='/':
        return(str(a)+' '+op+' '+str(b)+' = '+str(a/b))
    if op == '*':
        return(str(a)+' '+op+' '+str(b)+' = '+str(a*b))
    if op == '^':
        return(str(a)+' '+op+' '+str(b)+' = '+str(a**b))
        

def main():
    
    a = int(input('What is your first number??:  '))
    b=int(input('What is your second number??:  '))
    op = input('What operation would you like to preform??\n Choices are "+,-,/,*,^":  ')
    
    
    print(calc(a,b,op))
    
    
if __name__=='__main__':
    
    
    main()
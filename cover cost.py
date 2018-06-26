# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 19:04:37 2018

@author: natew
"""



#width and height using a cost entered

w = float(input('What is the width??:  '))



h = float(input('What is the height??: '))



ppm = float(input('What is the price per meter?? :'))

cost = lambda w,h,ppm: w*h*ppm

print(cost(w,h,ppm))




    














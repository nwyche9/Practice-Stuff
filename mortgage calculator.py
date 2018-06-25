# -*- coding: utf-8 -*-
"""
Created on Sun Jun 24 21:51:17 2018

@author: natew
"""

months = int(input("Enter mortgage term (in months): "))
rate = float(input("Enter interest rate: "))
loan = float(input("Enter loan value: "))

monthly_rate=rate/100/12

payment=(monthly_rate/(1-(1+monthly_rate)**(-months)))* loan

print("Your monthly payment for a {}".format(months/12)+" year mortgage at a {}".format(rate)+" interest rate with a {}".format(loan)+" interest rate and a {}".format(loan)+" loan amount is {}.".format(payment))
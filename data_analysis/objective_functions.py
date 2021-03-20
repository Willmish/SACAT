# Written by Szymon Duchniewicz March, 2021
'''
class ObjectiveFunctions collecting objective functions of all time complexities analysed by SACAT.

'''

from math import log

class ObjectiveFunctions:
    @staticmethod
    def logarithmic_objective(x, a, b):
        return a * log(x, 10) + b

    @staticmethod
    def linear_objective(x, a, b): # TODO what about An + Blogn + C
        return a * x + b

    @staticmethod
    def linearithmic_objective(x, a, b, c): # TODO what about Anlogn + Blogn +Cn +D
        # Since parameters passed can be numpy.ndarray and math.log() is a non vector function, separate
        # return values exist 
        if isinstance(x, int) or isinstance(x, float):
            return (a*x*log(x, 10) + b * x + c)
        return [(a*i*log(i, 10) + b * i + c) for i in x]
    
    @staticmethod
    def quadratic_objective(x, a, b, c):
        return a * x*x + b * x + c

    @staticmethod
    def cubic_objective(x, a, b, c, d):
        return a * x**3 + b * x*x + c * x + d
    

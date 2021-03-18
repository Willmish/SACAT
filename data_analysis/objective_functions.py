# Written by Szymon Duchniewicz March, 2021
'''
class ObjectiveFunctions collecting objective functions of all time complexities analysed by SACAT.

'''

class ObjectiveFunctions:
    @staticmethod
    def quadratic_objective(x, a, b, c):
        return a * x*x + b * x + c

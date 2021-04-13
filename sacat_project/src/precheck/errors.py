"""
Errors for the user code check.

Written by Andrzej Szablewski, March 2021.
"""

class RestrictedCodeError(Exception):
    def __init__(self, message, restrictedElement):
        self.restrictedElement = restrictedElement
        self.message = message
        super().__init__(self.message, self.restrictedElement)

    def __str__(self):
        return self.message + ": " + str(self.restrictedElement)

class RestrictedCodeError(Exception):
    def __init__(self, message, restrictedElement):
        self.restrictedElement = restrictedElement
        self.message = message
        super().__init__(self.message, self.restrictedElement)
# Written by Szymon Duchniewicz March, 2021
'''
ResultsStorage class holds the results from a single TestStorage being analysed by the DataAnalyser.
'''

class ResultsStorage:
    def __init__(self, type: str):
        self.test_type = type
        self.times_results = None
        self.operations_results = None
        self.space_results = None

    def __str__(self):
        result = ''
        result += f"Test type: {self.test_type} \n"
        result += f"Time results: {self.times_results}\n"
        result += f"Operations results: {self.operations_results}\n"
        result += f"Space results: {self.space_results}\n"
        return result


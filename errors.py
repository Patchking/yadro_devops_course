class UnexpetedAPIAnswerException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None
    def __str__(self):
        if self.message:
            return self.message
        else:
            return "Error has occured while requesting or handling response from API"
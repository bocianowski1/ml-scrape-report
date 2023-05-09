class PlotError(Exception):
    """Raised when there is an error in plotting a graph"""
    def __init__(self, message="\nSomething went wrong while plotting the graph\n"):
        self.message = message
        super().__init__(self.message)

class InputError(Exception):
    """Raised when there is an error in the input"""
    def __init__(self, message="\nSomething went wrong with the input\n"):
        self.message = message
        super().__init__(self.message)
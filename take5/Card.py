class Card:

    def __init__(self, value, bulls):
        self.value = value
        self.bulls = bulls

    def __str__(self):
        return str(self.value)
    
    def getValue(self):
        return self.value
    
    def getBulls(self):
        return self.bulls
    
    def setValue(self, value):
        self.value = value

    def setBulls(self, bulls):
        self.bulls = bulls

    
    
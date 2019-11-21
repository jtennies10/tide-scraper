'''
Class representing a Low Tide object, holding the tide's time and height
'''

class LowTide():
    def __init__(self, time, height):
        self.time = time
        self.height = height

    def __str__(self):
        return 'Low tide at %s with a height of %s\n' % (self.time, self.height)
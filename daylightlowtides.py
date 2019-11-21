'''
Class that holds a location and an array of LowTide objects that 
fall within daylight
'''

class DaylightLowTides():
    

    def __init__(self, location, low_tides):
        self.location = location
        self.low_tides = low_tides


    def __str__(self):
        str_builder = 'Location: %s\n' % self.location
        for tide in self.low_tides:
            str_builder = str_builder + str(tide)

        return str_builder
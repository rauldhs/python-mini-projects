from random import randint

class Die:
    """a class to represent one die"""

    def __init__(self,num_sides=6):
        """assume six sided die"""
        self.num_sides = num_sides
    
    def roll(self):
        """return values from roled dice"""
        return randint(1,self.num_sides)
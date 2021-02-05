from enum import IntFlag

''' simple helper class to enumerate directions in the grid levels '''
class Direction(IntFlag):
    Stay = 0
    North = 1
    East = 2
    South = 4
    West = 8
    All = 15
        
    # get the enum name without the class
    def __str__(self): return self.name  
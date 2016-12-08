from enum import Enum

class Dir(Enum):
    north = 1
    east  = 2
    south = 3
    west  = 4

class Clause(object):
    def __init__(self, i,j,d):
        self.i   = i
        self.j   = j
        self.dir = d

    def unify_rep(self):
        if (self.d == Dir.west):
            self.i -= 1
            self.d == Dir.east

        if (self.d == Dir.south):
            self.j -= 1
            self.d = Dir.north

    def __str__(self):
        return "q(" + str(self.i) + "," + str(self.j) + "," + str(self.dir.name[0]) + ")"
        

def read_input():
    in_str = input()
    toks = in_str.split()
    r = toks[0]
    c = toks[1]
    rep = toks[2:]
    return (rep,show)


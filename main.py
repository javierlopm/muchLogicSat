from enum import Enum

class Dir(Enum):
    north = 1
    east  = 2
    south = 3
    west  = 4

class Clause(object):
    def __init__(self,i,j,d):
        self.i   = i
        self.j   = j
        self.dir = d
        self.neg = False

        self.unify_rep()

    def unify_rep(self):
        if (self.dir == Dir.west and self.i > 1):
            self.i -= 1
            self.dir = Dir.east

        if (self.dir == Dir.south and self.j > 1):
            self.j -= 1
            self.dir = Dir.north
        return self

    def negate(self):
        self.neg = not self.neg
        return self

    def __str__(self):
        neg = "-" if self.neg else ""
        res = ( neg +"q("+ str(self.i) + "," + 
                           str(self.j) + "," + 
                           str(self.dir.name[0])  + ")")
        return res
        

# Read from IO representation
# in_str = input()
in_str = "5 5 ..32. 222.3 0..1. 2.2.. .2323"
toks   = in_str.split()
rows = toks[0]
cols = toks[1]
rep = toks[2:]


cnf_clauses = []

for i,line in enumerate(rep):
    for j,char in enumerate(line):
        try:
            case = int(char)
        except:
            continue

        if   (case == 0):
            pass
        elif (case == 1):
            # Add any of the edges
            cnf_clauses += [ Clause(i,j,d) for d in Dir ]
            for d1 in Dir:
                for d2 in Dir:
                    if (d1.value < d2.value):
                        cnf_clauses += [ Clause(i,j,d1).negate() 
                                       , Clause(i,j,d2).negate() ]


        elif (case == 2):
            pass
        elif (case == 3):
            pass
        elif (case == 4):
            # Add all edges
            for d in Dir:
                cnf_clauses += [ Clause(i,j,d)]

from enum import Enum

# Correr con: python3 main.py > primerEj.cnf
# Hacer debug = True abajo para ver representacion para humanos de lo que esta pasando jajjajaja

class Dir(Enum):
    north = 1
    east  = 2
    south = 3
    west  = 4

class Clause(object):
    # Universo de clausulas con valores unicos
    universe = set()

    def __init__(self,i,j,d):
        self.i   = i
        self.j   = j
        self.dir = d
        self.neg = 1

        self.unify_rep()

        # Add to universe and get unique id (for sat)
        Clause.universe.add(self.to_tuple())

    def unify_rep(self):
        # Convierte a cualquier clausula en su version
        # con direccion este o norte
        if (self.dir == Dir.west and self.i > 1):
            self.i -= 1
            self.dir = Dir.east

        if (self.dir == Dir.south and self.j > 1):
            self.j -= 1
            self.dir = Dir.north
        return self

    def negate(self):
        # Negado de una clausula
        self.neg = - self.neg
        return self

    def __str__(self):
        # Representacion como string
        neg = "-" if (self.neg ==-1) else ""
        res = ( neg +"q("+ str(self.i) + "," + 
                           str(self.j) + "," + 
                           str(self.dir.name[0])  + ")")
        return res

    def to_tuple(self):
        # Necesario para que las clausulas tengan identificador unico
        return (self.i,self.j,self.dir)

    def get_sat_val(self):
        # Solo se usar al final, afecta a la variable estatica global
        # Obtiene el valor unico de una clausula para minisat
        my_tup = self.to_tuple()
        try:
            i = Clause.universe.index(my_tup)
        except:
            Clause.universe = list(Clause.universe)
            i = Clause.universe.index(my_tup)

        return (self.neg * i )
    


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

        # Number restrictions over cells
        if   (case == 0):
            # Remove all edges
            for d in Dir:
                cnf_clauses += [ [ Clause(i,j,d).negate() ] ]
        elif (case == 1):
            # Add any of the edges
            cnf_clauses += [ [ Clause(i,j,d) for d in Dir ] ]

            for d1 in Dir:
                for d2 in Dir:
                    if (d1.value < d2.value):
                        cnf_clauses +=[ [ Clause(i,j,d1).negate() 
                                       , Clause(i,j,d2).negate() ] ]
        elif (case == 2):
            # convertir esta vaina a una formula cerrada o hacer todas de forma manual
            # ( !E ||  !n ||  !s) && ( !E ||  !n ||  !w) && ( !E ||  !s ||  !w) && (E || n || s) && (E || n || w) && (E || s || w) && ( !n ||  !s ||  !w) && (n || s || w)
            pass
        elif (case == 3):
            # Add all edges but one
            cnf_clauses += [ [ Clause(i,j,d).negate() for d in Dir ] ]

            for d1 in Dir:
                for d2 in Dir:
                    if (d1.value < d2.value):
                        cnf_clauses += [ [ Clause(i,j,d1) , Clause(i,j,d2) ] ]
        elif (case == 4):
            # Add all edges
            for d in Dir:
                cnf_clauses += [ [ Clause(i,j,d) ] ]

        # Interior vs exterior clauses
        pass

        # Reachable cells
        pass

        # Interior cells reachable
        pass

debug = False
if debug:
    # All restrictions for cells with number 2 (Wolfram alfa muestra como queda al pasar a cnf)
    print("Rest for #2")
    for d1 in Dir:
        for d2 in Dir:
            if d1.value < d2.value:
                no = list(set(Dir) - set([d1,d2]))
                l = [d1.name[0],d2.name[0],no[0].name[0],no[1].name[0]]

                print(("({0}&&{1}&& (¬{2}) &&(¬{3}))").format(l[0],l[1],l[2],l[3]),end="||")

    # (¬e ∨ ¬n ∨ ¬s) ∧ (¬e ∨ ¬n ∨ ¬w) ∧ (¬e ∨ ¬s ∨ ¬w) ∧ (e ∨ n ∨ s) ∧ (e ∨ n ∨ w) ∧ (e ∨ s ∨ w) ∧ (¬n ∨ ¬s ∨ ¬w) ∧ (n ∨ s ∨ w)
    # en cnf es
    # ( !E ||  !n ||  !s) && ( !E ||  !n ||  !w) && ( !E ||  !s ||  !w) && (E || n || s) && (E || n || w) && (E || s || w) && ( !n ||  !s ||  !w) && (n || s || w)
    print("\n\n")

    print("Rest for #3")
    # All restrictions for cells with number 3 
    for d1 in Dir:
        no = list(set(Dir) - set([d1]))
        l = [d1.name[0],no[0].name[0],no[1].name[0],no[2].name[0]]
        print(("((¬{0})&&{1}&&{2}&&{3})").format(l[0],l[1],l[2],l[3]),end="||")
    # ((¬n)&&e&&s&&w)||((¬e)&&s&&n&&w)||((¬s)&&e&&n&&w)||((¬w)&&s&&n&&e)
    # en cnf es
    # 
    print("\n\n")

    # Mostrando respuestas con nuestro tipo de datos
    for clause in cnf_clauses:
        print("{",end="")
        for pred in clause:
            print(str(pred) ,end=",")
        print("},")

    print()

# Mostrando respuestas tipo cnf
def print_sat_clause(x):
    for i in x:
        print(i.get_sat_val(),end=" ")

    for i in range(0,5-len(x)):
        print(0,end=" ")
    print()
    # print("diference " + str(4-len(x) ) )


print("c This Formular is generated by mcnf")
print("c")
print("c    horn? no ")
print("c    forced? no ")
print("c    mixed sat? no ")
print("c    clause length = 5 ")
print("c")

list(map(print_sat_clause,cnf_clauses))


from enum import Enum

# Correr con: python3 main.py > primerEj.cnf
# Hacer debug = True abajo para ver representacion para humanos de lo que esta pasando jajjajaja
debug = True

class Dir(Enum):
    north = 1
    west  = 2
    east  = 3
    south = 4

# Universo de clausulas con valores unicos
universe = set()

class Clause(object):
    

    def __init__(self,i,j,add=True):
        # Clausula de tipo q(fila,columna,direccion, agregar_al_universo)
        self.i   = i
        self.j   = j
        self.neg = 1

    def negate(self):
        # Negado de una clausula
        self.neg = - self.neg
        return self

    def __neg__(self):
        return self.negate()

    def to_tuple(self):
        pass

    def get_sat_val(self):
        # Solo se usar al final, afecta a la variable estatica global
        # Obtiene el valor unico de una clausula para minisat
        my_tup = self.to_tuple()
        try:
            i = universe.index(my_tup)
        except:
            global universe
            universe = list(universe)
            i = universe.index(my_tup) 

        return (self.neg * (i+1) )

class Q(Clause):
    # Universo de clausulas con valores unicos

    def __init__(self,i,j,d,add=True):
        # Clausula de tipo q(fila,columna,direccion, agregar_al_universo)
        self.dir = d
        super(Q,self).__init__(i,j,add)
        self.unify_rep()

        # Add to universe and get unique id (for sat)
        if add:
            universe.add(self.to_tuple())


    def unify_rep(self):
        # Convierte a cualquier clausula en su version
        # con direccion este o norte
        # Clausula 0 mantiene un solo formato de direccion
        if (self.dir == Dir.west and self.j > 1):
            self.j  -= 1
            self.dir = Dir.east

        if (self.dir == Dir.north and self.i > 1):
            self.i  -= 1
            self.dir = Dir.south
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




class IjClause(Clause):

    def __init__(self,i,j,t,add=True):
        # Clausula de tipo q(fila,columna,direccion, agregar_al_universo)
        self.type = t
        super(IjClause,self).__init__(i,j,add)

    def __str__(self):
        # Representacion como string
        neg = "-" if (self.neg ==-1) else ""
        res = ( neg + self.type +"("+ str(self.i) + "," + 
                           str(self.j) + ")")
        return res

    def to_tuple(self):
        # Necesario para que las clausulas tengan identificador unico
        return (self.i,self.j,self.type)


class Z(IjClause):
    def __init__(self,i,j,add=True):
        # Clausula de tipo q(fila,columna,direccion, agregar_al_universo)
        super(Z,self).__init__(i,j,'z',add)

        if add:
            universe.add(self.to_tuple())

class R(IjClause):
    def __init__(self,i,j,add=True):
        # Clausula de tipo q(fila,columna,direccion, agregar_al_universo)
        super(R,self).__init__(i,j,'r',add)

        if add:
            universe.add(self.to_tuple())



# Read from IO representation
# in_str = input()

# Entrada fija
in_str = "5 5 ..32. 222.3 0..1. 2.2.. .2323"
toks   = in_str.split()
rows = int(toks[0]) #modificado
cols = int(toks[1]) #modificado
rep = toks[2:]


cnf_clauses = []

# Impresion de tablero de forma rápida
if debug:
    for i in range(0,6):
        print(".",end=" ")
    print()

for i,line in enumerate(rep,1):
    # impresion de tablero
    if debug:
        print(".",end="")

    for j,char in enumerate(line,1):
        try:
            case = int(char)
            if debug:
                print(str(case),end=".")
        except:
            if debug:
                print(" ",end=".")
            continue

        # Number restrictions over cells
        if   (case == 0):
            # Remove all edges
            for d in Dir:
                cnf_clauses += [ [ -Q(i,j,d) ] ]
        elif (case == 1):
            # Add any of the edges
            cnf_clauses += [ [ Q(i,j,d) for d in Dir ] ]

            for d1 in Dir:
                for d2 in Dir:
                    if (d1.value < d2.value):
                        cnf_clauses +=[ [ -Q(i,j,d1) 
                                        , -Q(i,j,d2) ] ]
            pass                                       
        elif (case == 2):
            # Todas las formas de tener dos aristas de un cuadro en cnf
            # ( !E ||  !n ||  !s) && ( !E ||  !n ||  !w) && ( !E ||  !s ||  !w) && (E || n || s) && (E || n || w) && (E || s || w) && ( !n ||  !s ||  !w) && (n || s || w)
            cnf_clauses += [[-Q(i,j,Dir.east)
                            ,-Q(i,j,Dir.north)
                            ,-Q(i,j,Dir.south)]]

            cnf_clauses += [[-Q(i,j,Dir.east)
                            ,-Q(i,j,Dir.north)
                            ,-Q(i,j,Dir.west)]]

            cnf_clauses += [[-Q(i,j,Dir.east)
                            ,-Q(i,j,Dir.south)
                            ,-Q(i,j,Dir.west)]]

            cnf_clauses += [[Q(i,j,Dir.east)
                            ,Q(i,j,Dir.north)
                            ,Q(i,j,Dir.south)]]

            cnf_clauses += [[Q(i,j,Dir.east)
                            ,Q(i,j,Dir.north)
                            ,Q(i,j,Dir.west)]]

            cnf_clauses += [[Q(i,j,Dir.east)
                            ,Q(i,j,Dir.south)
                            ,Q(i,j,Dir.west)]]

            cnf_clauses += [[-Q(i,j,Dir.north)
                            ,-Q(i,j,Dir.south)
                            ,-Q(i,j,Dir.west)]]

            cnf_clauses += [[Q(i,j,Dir.north)
                            ,Q(i,j,Dir.south)
                            ,Q(i,j,Dir.west)]]

        elif (case == 3):
            # Add all edges but one
            cnf_clauses += [ [ (-Q(i,j,d)) for d in Dir ] ]

            for d1 in Dir:
                for d2 in Dir:
                    if (d1.value < d2.value):
                        cnf_clauses += [ [ Q(i,j,d1) , Q(i,j,d2) ] ]
        elif (case == 4):
            # Add all edges
            for d in Dir:
                cnf_clauses += [ [ Q(i,j,d) ] ]


        ####COMENTAR DESDE ACA PARA QUE CORRA
        ## Esta todo en cnf falta decidir como representaremos r y z dado que tienen que ser variables/constantes diferentes a las q
        ##todo sigue dendro del doble ciclo para i,j

        # Interior vs exterior clauses
        N=Dir.north
        S=Dir.south
        E=Dir.east
        W=Dir.west 
        #Clausulas tipo 2

        for j in range(1,cols):
            cnf_clauses+= [[Q(1,j,W),Z(1,j)],[-Q(1,j,W),-Z(1,j)]]
            cnf_clauses+= [[Q(cols,j,E),Z(cols,j)],[-Q(cols,j,E),-Z(cols,j)]]

        for i in range(1,rows):
            cnf_clauses+= [[Q(i,1,S),Z(i,1)],[-Q(i,1,S),-Z(i,1)]]
            cnf_clauses+= [[Q(i,rows,N),Z(i,rows)],[-Q(i,rows,N),-Z(i,rows)]]

        for i in range(2,rows-1):
            for j in range(2,cols-1):
                #(=>)
                #( !E ||  !N ||  !P ||  !S || V) && ( !E ||  !N ||  !P ||  !S ||  !W) && ( !E ||  !N ||  !P || U || V) && ( !E ||  !N ||  !P || U ||  !W) && ( !E ||  !P || R ||  !S || V) && ( !E ||  !P || R ||  !S ||  !W) && ( !E ||  !P || R || U || V) && ( !E ||  !P || R || U ||  !W) && ( !N ||  !P ||  !S || T || V) && ( !N ||  !P ||  !S || T ||  !W) && ( !N ||  !P || T || U || V) && ( !N ||  !P || T || U ||  !W) && ( !P || R ||  !S || T || V) && ( !P || R ||  !S || T ||  !W) && ( !P || R || T || U || V) && ( !P || R || T || U ||  !W)
                
                cnf_clauses+=  [[ -Q(i,j,E) ,  -Q(i,j,N) ,  -Z(i,j) ,  -Q(i,j,S) , Z(i-1,j)] ,
                 [ -Q(i,j,E) ,  -Q(i,j,N) ,  -Z(i,j) ,  -Q(i,j,S) ,  -Q(i,j,W)] ,
                 [ -Q(i,j,E) ,  -Q(i,j,N) ,  -Z(i,j) , Z(i,j-1) , Z(i-1,j)] ,
                 [ -Q(i,j,E) ,  -Q(i,j,N) ,  -Z(i,j) , Z(i,j-1) ,  -Q(i,j,W)] ,
                 [ -Q(i,j,E) ,  -Z(i,j) , Z(i,j+1) ,  -Q(i,j,S) , Z(i-1,j)] ,
                 [ -Q(i,j,E) ,  -Z(i,j) , Z(i,j+1) ,  -Q(i,j,S) ,  -Q(i,j,W)] ,
                 [ -Q(i,j,E) ,  -Z(i,j) , Z(i,j+1) , Z(i,j-1) , Z(i-1,j)] ,
                 [ -Q(i,j,E) ,  -Z(i,j) , Z(i,j+1) , Z(i,j-1) ,  -Q(i,j,W)] ,
                 [ -Q(i,j,N) ,  -Z(i,j) ,  -Q(i,j,S) , Z(i+1,j) , Z(i-1,j)] ,
                 [ -Q(i,j,N) ,  -Z(i,j) ,  -Q(i,j,S) , Z(i+1,j) ,  -Q(i,j,W)] ,
                 [ -Q(i,j,N) ,  -Z(i,j) , Z(i+1,j) , Z(i,j-1) , Z(i-1,j)] ,
                 [ -Q(i,j,N) ,  -Z(i,j) , Z(i+1,j) , Z(i,j-1) ,  -Q(i,j,W)] ,
                 [ -Z(i,j) , Z(i,j+1) ,  -Q(i,j,S) , Z(i+1,j) , Z(i-1,j)] ,
                 [ -Z(i,j) , Z(i,j+1) ,  -Q(i,j,S) , Z(i+1,j) ,  -Q(i,j,W)] ,
                 [ -Z(i,j) , Z(i,j+1) , Z(i+1,j) , Z(i,j-1) , Z(i-1,j)] ,
                 [ -Z(i,j) , Z(i,j+1) , Z(i+1,j) , Z(i,j-1) ,  -Q(i,j,W)] ]

                 #(<=)
                 #(E || P ||  !T) && (N || P ||  !R) && (P || S ||  !U) && (P ||  !V || W)

                cnf_clauses+=[[Q(i,j,E) , Z(i,j) ,  -Z(i+1,j)] ,
                 [Q(i,j,N) , Z(i,j) ,  -Z(i,j+1)] ,
                 [Z(i,j) , Q(i,j,S) ,  -Z(i,j-1)] ,
                 [Z(i,j) ,  -Z(i-1,j) , Q(i,j,W)]]



        # M = 5 # ?
        # if ( (i == 1) and (1 <= j and j <= M) ):
        #     cnf_clauses += [ [Q(1,j,Dir.west),Z(1,j)] ]
        #     cnf_clauses += [-Z(1,j),-Q(1,j,Dir.west)]
            # if ( (i == N) and (1 <= j and j <= M) ):
            #     q(N,j,e) v z(N,j) and
            #     -z(N,j) v -q(N,j,e)

            # if ( (1 <= i and i <= N) and (j == 1) ):
            #     q(i,1,s) v z(i,1) and
            #     -z(i,1) v -q(i,1,s)

            # if ( (1 <= i and i <= N) and (j == M) ):
            #     q(i,M,n) v z(i,M) and
            #     -z(i,M) v -q(i,M,n)

            # if ((1 < i and i< N) and (1 < j and j< M)):
            #     #-z(i,j) v [-q(i,j,n) & z(i,j+1)] v [-q(i,j,e) & z(i+1,j)] v [-q(i,j,s) & z(i,j-1)] v [-q(i,j,w) & z(i-1,j)]
            #     #CNF
            #     (z(i-1,j) ∨ ¬z(i,j) ∨ ¬q(i,j,n) ∨ ¬q(i,j,e) ∨ ¬q(i,j,s))
            #     (z(i-1,j) ∨ ¬z(i,j) ∨ ¬q(i,j,n) ∨ ¬q(i,j,e) ∨ z(i,j-1))
            #     (z(i-1,j) ∨ ¬z(i,j) ∨ ¬q(i,j,n) ∨ z(i+1,j) ∨ ¬q(i,j,s))
            #     (z(i-1,j) ∨ ¬z(i,j) ∨ ¬q(i,j,n) ∨ z(i+1,j) ∨ z(i,j-1))
            #     (z(i-1,j) ∨ ¬z(i,j) ∨ z(i,j+1) ∨ ¬q(i,j,e) ∨ ¬q(i,j,s))
            #     (z(i-1,j) ∨ ¬z(i,j) ∨ z(i,j+1) ∨ ¬q(i,j,e) ∨ z(i,j-1))
            #     (z(i-1,j) ∨ ¬z(i,j) ∨ z(i,j+1) ∨ z(i+1,j) ∨ ¬q(i,j,s))
            #     (z(i-1,j) ∨ ¬z(i,j) ∨ z(i,j+1) ∨ z(i+1,j) ∨ z(i,j-1))
            #     (¬z(i,j) ∨ ¬q(i,j,n) ∨ ¬q(i,j,e) ∨ ¬q(i,j,s) ∨ ¬q(i,j,w))
            #     (¬z(i,j) ∨ ¬q(i,j,n) ∨ ¬q(i,j,e) ∨ z(i,j-1) ∨ ¬q(i,j,w))
            #     (¬z(i,j) ∨ ¬q(i,j,n) ∨ z(i+1,j) ∨ ¬q(i,j,s) ∨ ¬q(i,j,w))
            #     (¬z(i,j) ∨ ¬q(i,j,n) ∨ z(i+1,j) ∨ z(i,j-1) ∨ ¬q(i,j,w))
            #     (¬z(i,j) ∨ z(i,j+1) ∨ ¬q(i,j,e) ∨ ¬q(i,j,s) ∨ ¬q(i,j,w))
            #     (¬z(i,j) ∨ z(i,j+1) ∨ ¬q(i,j,e) ∨ z(i,j-1) ∨ ¬q(i,j,w))
            #     (¬z(i,j) ∨ z(i,j+1) ∨ z(i+1,j) ∨ ¬q(i,j,s) ∨ ¬q(i,j,w))
            #     (¬z(i,j) ∨ z(i,j+1) ∨ z(i+1,j) ∨ z(i,j-1) ∨ ¬q(i,j,w))
                
            #     #[-q(i,j,n) & z(i,j+1)] v [-q(i,j,e) & z(i+1,j)] v [-q(i,j,s) & z(i,j-1)] v [-q(i,j,w) & z(i-1,j)] => z(i,j)
            #     #CNF
            #     (¬z(i-1,j) ∨ ¬z(i,j) ∨ q(i,j,w))
            #     (¬z(i,j) ∨ q(i,j,n) ∨ ¬z(i,j+1))
            #     (¬z(i,j) ∨ q(i,j,e) ∨ ¬z(i+1,j))
            #     (¬z(i,j) ∨ q(i,j,s) ∨ ¬z(i,j-1))

            # Reachable cells
            #r(c,c)
            # r(c(i,j),c(i,j))

            # for x in range(N):
            #     for y in range(M):
            #         #North
            #         #r(c(i,j),c(x,y)) and -q(c(x,y),N) => r(c(i,j),c(x,y-1))
            #         if (y != 1):
            #             ¬r(c(i,j),c(x,y)) v q(c(x,y),N) v r(c(i,j),c(x,y-1))

            #         #South
            #         #r(c(i,j),c(x,y)) and -q(c(x,y),S) => r(c(i,j),c(x,y+1))
            #         if (y != M):
            #             ¬r(c(i,j),c(x,y)) v q(c(x,y),S) v r(c(i,j),c(x,y+1))

            #         #East
            #         #r(c(i,j),c(x,y)) and -q(c(x,y),E) => r(c(i,j),c(x+1,y))
            #         if (x != N):
            #             ¬r(c(i,j),c(x,y)) v q(c(x,y),E) v r(c(i,j),c(x+1,y))

            #         #West
            #         #r(c(i,j),c(x,y)) and -q(c(x,y),W) => r(c(i,j),c(x-1,y))
            #         if (y != M):
            #             ¬r(c(i,j),c(x,y)) v q(c(x,y),W) v r(c(i,j),c(x-1,y))

            # Interior cells reachable
            #z(c) & z(c') => r(c,c')
            # for x in range(N):
            #     for y in range(M):
            #         ¬z(i,j) v ¬z(x,y) v r(c(i,j),c(x,y))


        


        #Adjacent segments
        #COMENTAR HASTA ACA

        # q(i,j,N) and q(i,j,E) => (¬q(i,j+1,N) or ¬q(i-1,j,E))
        #( P && Q => (~R || ~W))
        #((¬P || ¬Q ) or (~R || ~W))
        #COMENTAR SI ALGO NO FURULA
        #CASO BLAI, UNA PARTE

        #for i in range(1,rows-1):
        #    for j in range(1,cols-1):
        #        cnf_clauses += [[Q(i,j,N).negate(),Q(i,j,E).negate(),Q(i,j+1,N).negate(),Q(i-1,j,E).negate()]]
        #        cnf_clauses += [[Q(i,j,N).negate(),Q(i,j,W).negate(),Q(i,j-1,N).negate(),Q(i-1,j,W).negate()]]
        #        cnf_clauses += [[Q(i,j,S).negate(),Q(i,j,E).negate(),Q(i,j+1,S).negate(),Q(i+1,j,E).negate()]]
        #        cnf_clauses += [[Q(i,j,S).negate(),Q(i,j,W).negate(),Q(i,j-1,S).negate(),Q(i+1,j,W).negate()]]

    if debug:
        print()



# Fin del cuadro
if debug:
    for i in range(0,6):
        print(".",end=" ")
    print("\n\n")


if debug:
    # Mostrando clausulas con nuestro tipo de datos
    for clause in cnf_clauses:
        print("{",end="")
        for pred in clause:
            print(str(pred) ,end=",")
        print("},")

    print("\n\n")



# Call minisat
f = open('int_file', 'w')

def print_sat_clause(x):
    # Mostrando respuestas tipo cnf
    for i in x:
        print(str(i))
        f.write(str(i.get_sat_val()))
        f.write(" ")
    f.write("0\n")
    # print("diference " + str(4-len(x) ) )


# Generando archivo para minisar
f.write("c This Formular is generated by mcnf\n")
f.write("c\n")
f.write("c    horn? no \n")
f.write("c    forced? no \n")
f.write("c    mixed sat? no \n")
f.write("c    clause length = 3 \n")
f.write("c\n")
f.write("p cnf {} {}\n".format(len(universe),len(cnf_clauses)))

list(map(print_sat_clause,cnf_clauses))

f.close()

# Llamada a minisat
from subprocess import call
import os
devnull = open(os.devnull, 'w')

call(["./miniSat","int_file","salida.txt"],stdout=devnull)


with open('salida.txt', 'r') as myfile:
    data=myfile.read()

def get_dir(object):
    try:
        res = c.dir.name[0]
    except Exception as e:
        res = c.type

    return res

# Iterate results
try:
    result = []
    for i in (data.split("\n")[1].split()[:-1]):
        # Convert int result to clauses back again
        (r,c,d) = universe[abs(int(i))-1]
        if isinstance(d,Dir):
            c = Q(r,c,d,False)

            if int(i) < 0:
                c.negate()
            
            result += [c]
        else:
            if (d=="r"):
                c = R(r,c,False)
            else:
                c = Z(r,c,False)


    # Sort result, first by row, direction, and column at last
    from operator import attrgetter

    s0 = sorted(result,key=attrgetter("j"))
    s1 = sorted(s0,key=lambda c: c.dir.value )
    s2 = sorted(s1,key=attrgetter("i"))

    if debug:
        list(map(lambda c: print(c),s2))

    index = 0

    print("5 5 " + in_str)
    print("5 5 ",end="")

    # Print result in given format
    for i in range(1,6):
        for d in Dir:
            for j in range(1,6):
                # Casos especiales: norte y oeste
                # Solo la primera fila tiene nortes
                if (i > 1) and (d is Dir.north):
                    break

                # Solo hay un oeste al princio de cada linea
                if (j > 1 and (d is Dir.west)):
                    break

                if ((s2[index].to_tuple() == (i,j,d))):
                    if (s2[index].neg == 1):
                        print(1,end="")
                    else:
                        print("0",end="")
                    index += 1
                else:
                    # print("No se encontro {} {} con {}".format(i,j,d.name))
                    print("0",end="")

            if (d is Dir.south) or (d is Dir.east) or ((d is Dir.north) and i==1):
                print(" ",end="")

except Exception as e:
    print(e)
    print("UNSATISFIABLE")

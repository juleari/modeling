import metro, math, string

names = ["A0", "A1", "B0", "B1", "C0", "C1"]

r1 = [ metro.thA0, metro.thA1, metro.thB0, metro.thB1, metro.thC0, metro.thC1 ]
r3 = [ metro.rA0, metro.rA1, metro.rB0, metro.rB1, metro.rC0, metro.rC1 ]

def overline( x ):
    return float( sum(x) / len(x) )

def cov( x, y ):
    sx, sy = overline( x ), overline( y )

    return sum([ ( xi - sx ) * ( yi - sy ) for xi, yi in zip( x, y ) ])

def sigma( x ):
    sx = overline( x )

    return math.sqrt( sum([ ( xi - sx ) ** 2 for xi in x ]) )

def Pirson( x, y ):
    return cov( x, y ) / ( sigma( x ) * sigma( y ) )

def getRang( x ):
    return [ 1 + i / 5000 for i in x ]

def rangPirson( x, y ):
    rx, ry = getRang( x ), getRang( y )
    n      = 1.0 * len(x)
    
    return sum([ 1.0 * ( x / n - y / n ) ** 2 / y for x, y in zip( rx, ry ) ])

def rangSpirman( x, y ):
    rx, ry = getRang( x ), getRang( y )
    n      = len( x )

    return 1 - 6.0 * sum([ (x - y) ** 2 for x, y in zip(rx, ry) ])\
                   / ( n * (n ** 2 - 1) )

if __name__ == '__main__':
    print string.join( ["%s:\n"\
                        "   Pirson:  %s\n"\
                        "   Rangs:   %s\n"\
                        "            %s\n"\
                        "   RPirson: %s\n"\
                        "   RSpirman:%s\n" %\
                        ( name, 
                          Pirson( r1i, r3i ), 
                          getRang( r1i ), 
                          getRang( r3i ), 
                          rangPirson( r1i, r3i ),
                          rangSpirman( r1i, r3i ) ) \
                          for name, r1i, r3i in zip( names, r1, r3 )],
                        "\n" )

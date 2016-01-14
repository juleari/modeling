import metro
import math

names = ["A0", "A1", "B0", "B1", "C0", "C1"]

r1 = [ metro.thA0, metro.thA1, metro.thB0, metro.thB1, metro.thC0, metro.thC1 ]
r3 = [ metro.rA0, metro.rA1, metro.rB0, metro.rB1, metro.rC0, metro.rC1 ]

def id( x ):
    return x

def ln( x ):
    return math.log( x )

def expected( f, selection ) :
    s = 0

    for x in selection:
        s += f( x )

    return float( s ) / len( selection )

def dispersion( f, selection ) :
    s = 0
    m = expected( f, selection )

    for x in selection:
        s += ( f( x ) - m ) ** 2

    return float( s ) / len( selection )

def normalize( m, xs ) :
    return [ float( x ) / m for x in xs ]

def calcA(m1, m2, b):
    return math.e ** ( m1 - b * m2 )

def calcB(d1, d2):
    return math.sqrt( d1 / d2 )

def calcAB(r1, r2):
    b = calcB ( dispersion( ln, r1 ),
                dispersion( ln, r2 ) )

    a = calcA ( expected( ln, r1 ),
                expected( ln, r2 ),
                b )

    return a, b

def calcPrice( p, b, x2s, x2 ):
    return sum([ p[i] * b[i] * x2s[i] for i in range(3) ]) / x2

def calcProb( full, part ):
    return sum(part) / sum(full)

def calcProbs( s, f, d, l ):
    return [ calcProb( s, f ), calcProb( s, d ), calcProb( s, l ) ]

def calcConnect( x1, x2, r1, r2 ):

    print "\n%s vs %s:" % (x1, x2)
    for i in range(6):
        a, b = calcAB( r1[i], r2[i] )

        print "%s: a = %14s, b = %14s" % (names[i], a, b)

def calcdiff(k1, k2, start, stop, it):

    arr = []
    l1, l2 = float( len(k1) ), float( len(k2) )

    arr.append([ (i, sum([ 1 for l in k1 if l < i + 5 ])) \
                    for i in range(start, stop, it) ])
    arr.append([ (i, sum([ 1 for l in k2 if l < i + 5 ])) \
                    for i in range(start, stop, it) ])

    diffarr = [ abs((arr[0][i][1] / l1) - (arr[1][i][1] / l2))\
                for i in range( len(arr[0]) ) ]

    print "differences: %s\nmax dirrerence: %s" % ( diffarr, max( diffarr ) )
    return arr

for i in range(6):
    print names[i]
    a, b = calcAB( r1[i], r3[i] )
    Z = calcdiff( r1[i], [ a * (k ** b) for k in r3[i] ], \
                  metro.Dstart, metro.Dstop, metro.Diter )
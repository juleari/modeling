import data, metro
import math

# selections #
r1 = data.gr
r2 = data.lr

k1 = data.gk
k2 = data.lk

names = ["A0", "A1", "B0", "B1", "C0", "C1"]

r1 = [ metro.qthA0, metro.qthA1, metro.qthB0, metro.qthB1, metro.qthC0, metro.qthC1 ]
r2 = [ metro.qrA0, metro.qrA1, metro.qrB0, metro.qrB1, metro.qrC0, metro.qrC1 ]

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

if __name__ == "__main__":

    for i in range(6):
        a, b = calcAB( r1[i], r2[i] )

        print "%s: a: %s, b: %s\n" % (names[i], a, b)

        print "th: dispersion: %s, math: %s\n" % (dispersion( ln, r1[i] ), expected( ln, r1[i] ))
        print "r: dispersion: %s, math: %s\n" % (dispersion( ln, r2[i] ), expected( ln, r2[i] ))

    #k1c = [ a * (k ** b) for k in k2 ]
    #m = max( k1 + k1c )
    #print "k1: %s\n\nk2: %s \n\n" % (k1, k1c)

    #print "delta: %s" % abs( expected( id, normalize( m, k1 ) ) - expected( id, normalize( m, k1c ) ))

    #b = calcB ( dispersion( ln, range(1, 21) ),
    #            dispersion( ln, [2 * i for i in range(1, 21)] ) )
    
    #a = calcA ( expected( ln, range(1, 21) ),
    #            expected( ln, [2 * i for i in range(1, 21)] ),
    #            b )

    #k1c = [ a * (k ** b) for k in [2 * i for i in range(1, 21)] ]

    #print "k", range(1, 21)
    #print "k1c", k1c
    #print "a: ", a, " b: ", b 
    #print "d1", dispersion( ln, range(1, 21) ), "d2", dispersion( ln, [2 * i for i in range(1, 21)] ) 
    #print "m1:", expected( ln, range(1, 21) ), "m2:", expected( ln, [2 * i for i in range(1, 21)] )

# -*- coding: cp1251 -*-
import math, string
from rk import rk4

def tdma( p, q, f, n, a, b, ya, yb ):

    ai, bi, ci, di, xi = [], [], [], [], []

    h = (b - a) / n
    
    for i in range( n - 1 ):

        a += h
        ai.append( 1 - p(a) * h / 2.0 )
        bi.append( -2 + h**2 * q(a) )
        ci.append( 1 + p(a) * h / 2.0 )
        di.append( h**2 * f(a) )

    di[0]    -= ( 1 - p(a) * h / 2.0 ) * ya
    di[ -1 ] -= ( 1 + p(a) * h / 2.0 ) * yb

    for i in range( 1, n - 1 ):

        gi = ai[i] / bi[ i - 1 ]

        bi[i] -= gi * ci[ i - 1 ]
        di[i] -= gi * di[ i - 1 ]

    xi = ai
    xi[ -1 ] = di[ -1 ] / bi [ -1 ]

    for i in range( n - 3, -1 , -1 ):
        xi[ i ] = ( di[i] - ci[i] * xi[ i + 1 ] ) / bi[i]

    xi = [ ya ] + xi + [ yb ]

    return xi

def main():

    n = int( raw_input() )
    
    a = 0.0
    b = 1.0

    ya = 1.0
    yb = math.exp(1.0)

    def p( x ):
        return -2

    def q( x ):
        return 2

    def f( x ):
        return math.exp(x)

    rez  = tdma( p, q, f, n, a, b, ya, yb )
    corr = [ math.exp( a + i * (b - a) / n) for i in range( n + 1 ) ]

    print string.join( [ "получено: %.8f, должно быть: %.8f, погрешность: %.8f" % ( rez[i], corr[i], abs(rez[i] - corr[i]) ) for i in range( n + 1 ) ], "\n" )

main()
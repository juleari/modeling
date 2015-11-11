import metro
#import draw
import math

x = metro.thA0 + metro.thA1 + metro.thB0 + metro.thB1 + metro.thC0 + metro.thC1
y = metro.rA0 + metro.rA1 + metro.rB0 + metro.rB1 + metro.rC0 + metro.rC1
c = metro.kA0 + metro.kA1 + metro.kB0 + metro.kB1 + metro.kC0 + metro.kC1

def dev( X ):
    l = len( X )
    return sum([ sum ([ (x[i] - (1.0 / l) * sum([ x1[i] for x1 in X ])) ** 2 for i in [0, 1] ]) for x in X ])

def D( X, Y ):
    return dev( X + Y ) - ( dev(X) + dev(Y) )

def iter( z ):

    d = []
    l = len(z)

    if l == 6:
        return z

    for i in range( l ):
        
        X = z[i]
        
        for j in range(i + 1, l):
            
            Y = z[j]
            d.append( [ D( X, Y ), i, j] )
        
    m = min(d)
    i, j = m[1], m[2]
    
    z[i] += z[j]
    z.pop(j)

    return iter(z)


#if __name__ == "__main__":

z = [[i] for i in zip(x, y,c)]
iter(z)

#print "1: %s\n2: %s\n3: %s\n4: %s\n5: %s\n6: %s" % ( z[0], z[1], z[2], z[3], z[4], z[5] )
#print "1: %s\n2: %s" % ( z[0], z[1] )

Z = z
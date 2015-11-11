# -*- coding: cp1251 -*-
import rtree, math

triangles, Ndel, NchD, NDF = {}, 0, 0, 0

class Vertex( object ):

    def __init__( self, x, y ):

        self.x = x
        self.y = y

    def write( self ):

        print "(%s, %s)" % (self.x, self.y)

class Edge( object ):

    def __init__( self, v1, v2 ):

        self.vs = [v1, v2]

        self.p1 = (v1.x + 500, 720 - v1.y)
        self.p2 = (v2.x + 500, 720 - v2.y)

        self.trs = []

    def addTriangle( self, tr ):

        self.trs.append( tr )

    def delEdge( self, tr ):

        global edges

        trs = self.trs

        if tr in trs: self.trs.pop( trs.index(tr) )

class Triangle( object ):

    def __init__( self, e1, e2, e3 ):

        global Ntri

        self.es = [ e1, e2, e3 ]
        
        vs = []
        [ vs.extend(e.vs) for e in self.es ]
        self.vs = list( set( vs ) )

        self.id = -1

        self.trs = []

        self.getS()

        global Ntri

    def getBounds( self ):

        left   = min( self.vs, key = lambda v: v.x ).x
        right  = max( self.vs, key = lambda v: v.x ).x
        bottom = min( self.vs, key = lambda v: v.y ).y
        top    = max( self.vs, key = lambda v: v.y ).y

        return ( left, bottom, right, top )

    def getS(self):

        vs = self.vs

        if len( vs ) == 3:
        
            a  = sum([  vs[i].x * vs[ (i + 1) % 3 ].y - \
                        vs[i].y * vs[ (i + 1) % 3 ].x   \
                        for i in range(3) ])

            self.s  = float(a) / 2

        else: self.s = 0

    def include(self, v):

        #### Returns 
        #    3              if v in triangle 
        #    number of edge if on triangle
        #    -1             if outside of triangle

        trs = [ Triangle( e, Edge( e.vs[0], v ), Edge( e.vs[1], v ) ) for e in self.es ]
        s0  = [ i for i in range(3) if trs[i].s == 0 ]

        if len( s0 ): return s0[0]
        else: return 3 if abs( self.s ) >= sum([ abs(t.s) for t in trs ]) else -1

    def ints(self, tr):

        vs = self.vs

        if vs[0] in tr.vs:

            k1 = 0

            if vs[1] in tr.vs:  k2, extra = 1, 2
            else:               k2, extra = 2, 1 

        else: k1, k2, extra = 1, 2, 0

        v0 = [ tr.vs[i] for i in range(3) if tr.vs[i] != vs[k1] and tr.vs[i] != vs[k2] ][0]
        v1 = vs[ k1 ]
        v2 = vs[ extra ]
        v3 = vs[ k2 ]

        self.delaunay(v0, v1, v2, v3)

    def write(self):

       [ v.write() for v in self.vs ]

class RTree( object ):

    def __init__( self, bounds ):

        self.idx = rtree.index.Index()
        self.num = 0

        self.insert( bounds )

    def delete( self, i ):

        global triangles, Ndel

        if i not in triangles: return

        tr = triangles[i]

        self.idx.delete( i, tr.getBounds() )

        for neib in tr.trs:

            if len(neib.trs) and tr in neib.trs: neib.trs.pop( neib.trs.index( tr ) )

        [ e.delEdge( tr ) for e in tr.es ]

        del( triangles[i] )

        Ndel += 1

    def insert( self, bounds ):

        self.idx.insert( self.num, bounds )
        self.num += 1

    def intersection( self, bounds ):

        return [ i for i in self.idx.intersection( bounds, objects = True ) ]

def triang():

    global triangles

    def addTriangles( rect, v ):

        global triangles

        tr = triangles[ rect.id ]

        [ e.delEdge( tr ) for e in tr.es ]

        #### First triangle
        e1     = tr.es[0]

        e2, e3 = Edge( e1.vs[0], v ), Edge( e1.vs[1], v )
        
        insertTriangle( Triangle( e1, e2, e3 ) )

        #### Second triangle
        e1 = tr.es[1]

        if e2.vs[0] in e1.vs: 

            v1 = e1.vs[0] if e1.vs[0] != e2.vs[0] else e1.vs[1]
            e4 = e3

        else:

            v1 = e1.vs[0] if e1.vs[0] != e3.vs[0] else e1.vs[1]
            e4, e2 = e2, e3
        
        e3 = Edge( v1, v )

        insertTriangle( Triangle( e1, e2, e3 ) )

        #### Third triangle
        e1 = tr.es[2]

        insertTriangle( Triangle( e1, e3, e4 ) )

        #### Remove old
        tree.delete( rect.id )

    def addTwo( rect, inc, v ):

        tr = triangles[ rect.id ]
        [ e.delEdge( tr ) for e in tr.es ]

        e  = tr.es[ inc ]

        #### First tringle
        e1 = Edge( e.vs[0], v )
        e2 = [ tr.es[i] for i in range(3) if i != inc and e.vs[0] in tr.es[i].vs ][0]
        v1 = e2.vs[0] if e2.vs[0] != e1.vs[0] else e2.vs[1]
        e3 = Edge( v1, v )

        t = Triangle( e1, e2, e3 )
        insertTriangle( t )

        #### Second triangle
        e4 = Edge( e.vs[1], v )
        e2 = [ tr.es[i] for i in range(3) if i != inc and e.vs[1] in tr.es[i].vs ][0]

        t = Triangle( e4, e2, e3 )
        insertTriangle( t )

        tree.delete( tr.id )

        if len( e.trs ) == 2:

            neib = e.trs[0] if e.trs[0] != tr else e.trs[1]
            e.delEdge( neib )

            #### First tringle
            e2 = [ neib.es[i] for i in range(3) if i != inc and e.vs[0] in neib.es[i].vs ][0]
            v1 = e2.vs[0] if e2.vs[0] != e1.vs[0] else e2.vs[1]
            e3 = Edge( v1, v )

            t = Triangle( e1, e2, e3 )
            insertTriangle( t )

            #### Second triangle
            e2 = [ tr.es[i] for i in range(3) if i != inc and e.vs[1] in tr.es[i].vs ][0]

            t = Triangle( e4, e2, e3 )
            insertTriangle( t )

            tree.delete( neib.id )

    def addPoint(v):

        bounds = ( v.x, v.y, v.x, v.y )
        inrect = tree.intersection( bounds )

        if 0 in triangles: addTriangles( inrect[0], v )
        else:
                
            for rect in inrect:
                
                inc = triangles[ rect.id ].include(v)

                if   inc == -1: continue
                elif inc ==  3: addTriangles( rect, v )
                else: addTwo( rect, inc, v )
                
                break

    def checkDelaunay( tr ):

        global NchD, NDF

        for e in tr.es:

            if len( e.trs ) == 2:

                neib = e.trs[0] if e.trs[0].id != tr.id else e.trs[1]

                v1 = e.vs[0]
                v3 = e.vs[1]

                v0 = [ v for v in tr.vs   if v != v1 and v != v3 ][0]
                v2 = [ v for v in neib.vs if v != v1 and v != v3 ][0]

                NchD += 1

                if not delaunay( v0, v1, v2, v3 ):

                    NDF += 1

                    e1 = Edge(v0, v2)

                    es1= [ ei for ei in tr.es   if ei != e ]
                    es2= [ ei for ei in neib.es if ei != e ]

                    if v1 in es1[0].vs: [e2, e3] = es1
                    else:               [e3, e2] = es1

                    if v1 in es2[0].vs: [e4, e5] = es2
                    else:               [e5, e4] = es2

                    t1 = Triangle( e1, e2, e4 )
                    t2 = Triangle( e1, e3, e5 )

                    tree.delete( tr.id )
                    tree.delete( neib.id )

                    insertTriangle( t1 )
                    insertTriangle( t2 )

                    break

    def delaunay( v0, v1, v2, v3 ):

        ca = (v0.x - v1.x) * (v0.x - v3.x) + (v0.y - v1.y) * (v0.y - v3.y)
        cb = (v2.x - v1.x) * (v2.x - v3.x) + (v2.y - v1.y) * (v2.y - v3.y)

        if   ca <  0 and cb <  0: return False
        elif ca >= 0 and cb >= 0: return True

        sa = abs((v0.x - v1.x) * (v0.y - v3.y) - (v0.x - v3.x) * (v0.y - v1.y))
        sb = abs((v2.x - v1.x) * (v2.y - v3.y) - (v2.y - v1.y) * (v2.x - v3.x))

        return (sa * cb + ca * sb) >= 0

    def getPoints( text ):
        
        vstr = [ t.split() for t in text.split("\n") ]

        return [ Vertex( int(t[0]), int(t[1]) ) \
                    for t in vstr ]

    def insertTriangle( t ):

        t.id = tree.num
        triangles[ tree.num ] = t
        tree.insert( t.getBounds() )

        [ e.trs.append( t ) for e in t.es ]

        checkDelaunay( t )

    vertices = getPoints( open("data1000").read() )

    x1 = min( vertices, key = lambda v: v.x ).x
    x2 = max( vertices, key = lambda v: v.x ).x
    y1 = min( vertices, key = lambda v: v.y ).y - 10
    y2 = max( vertices, key = lambda v: v.y ).y

    l  = max( x2 - x1, y2 - y1 ) / 2 * 2

    x1 = ( x2 + x1 ) / 2 - l 
    x2 = x1 + l * 2
    y2 = y1 + l * 2

    v1, v2, v3   = Vertex( x1, y1 ), Vertex( x2, y1 ), Vertex( ( x2 + x1 ) / 2, y2 )
    e1, e2, e3   = Edge( v1, v2 ), Edge( v2, v3 ), Edge( v1, v3 )

    edges = [e1, e2, e3]

    triangles[0] = Triangle( e1, e2, e3 )
    triangles[0].id = 0

    [ e.trs.append( triangles[0] ) for e in edges ]

    bounds = ( x1, y1, x2, y2 )
    tree   = RTree( bounds )

    for v in vertices: addPoint(v)

    print "количество точек:              ", str(len(vertices))
    print "всего удалено треугольников:   ", str(Ndel)
    print "треугольников в триангуляции:  ", str(len( triangles.keys() ))
    print "проверок на условие Делоне:    ", str(NchD)
    print "неудачных проверок:            ", str(NDF) 

    return triangles
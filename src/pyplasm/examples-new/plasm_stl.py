import math
from copy import deepcopy

class Vector3D (object):
    """
    class Vector implements basic 3d vector operations.
    """

    def __init__ (self, *args):
        import types

        if not len (args):
            self.v = [0] * 3
        elif len (args) == 1:
            if type (args [0]) == types.InstanceType:
                self.v = deepcopy (args [0].v)
            else:
                self.v = args [0]
        elif len (args) == 3:
            self.v = deepcopy (args)

    def __getitem__ (self, i):
        return self.v [i]

    def __add__ (self, w):
        return self.add (w)

    def __sub__ (self, w):
        return self.sub (w)

    def __mul__ (self, w):
        return self.cross (w)

    def __neg__ (self):
        return self.neg ()

    def __abs__ (self):
        return self.size ()

    def __pos__ (self):
        return self.norm ()

    def add (self, w):
        """
        Vector addition.

        @param {Vector3D} w vector
        @return {Vector3D} addition of two vectors
        """
        v = self.v
        return Vector3D (v[0] + w[0], v[1] + w[1], v[2] + w[2])

    def sub (self, w):
        """
        Vector substraction

        @param {Vector3D} w vector
        @return {Vector3D} substraction of two vectors
        """
        v = self.v
        return Vector3D (v[0] - w[0], v[1] - w[1], v[2] - w[2])

    def cmul (self, c):
        """
        Vector multiplication by scalar

        @param {Real} c scalar constant
        @return {Vector3D} scaled vector
        """
        v = self.v
        return Vector3D (c*v[0], c*v[1], c*v[2])

    def cross (self, w):
        """
        Vector cross product.

        @param {Vector3D} w vector
        @return {Vector3D} cross product of two vectors
        """
        v = self.v
        return Vector3D (v[1]*w[2] - v[2]*w[1],
                         v[2]*w[0] - v[0]*w[2],
                         v[0]*w[1] - v[1]*w[0])

    def dot (self, w):
        """
        Vector dot product

        @param {Vector3D} w vector
        @return {Real} dot product of two vectors
        """
        v = self.v
        return v[0]*w[0] + v[1]*w[1] + v[2]*w[2]

    def size2 (self):
        """
        Square of vector size.

        @return {Real} square of vector size
        """
        return self.dot (self)

    def size (self):
        """
        Vector size

        @return {Real} vector size.
        """
        return math.sqrt (self.size2 ())

    def neg (self):
        """
        Vector negate

        @return {Vector3D} negate of this vector
        """

        v = self.v
        return Vector3D (-v[0], -v[1], -v[2])

    def norm (self):
        """
        Vector normalization

        @return {Vector3D} normalized vector
        """
        v = self.v
        s = self.size ()
        return Vector3D (v[0]/s, v[1]/s, v[2]/s)


class Mesh3D (object):

    def __init__ (self):
        self.vertices = None
        self.faces = None
    
    def makeIndicesFromVertices (self):
        """
        Make face's indices form triplets of vertices. 
        """
        if len (self.vertices) % 9:
            raise Exception ("Wron number of vertices")

        self.faces = [None] * (len (self.vertices) / 9)
        for i in xrange (0, len (self.faces)):
            ii = 3*i
            self.faces [i] = (ii, ii + 1, ii + 2)

    def computeFaceNormals (self):
        """
        Compute face normals.

        @return {List.<Vector3D>} list of normals
        """

        def mkVec (i, j):
            ii = 3*self.faces [i][j]
            return Vector3D (self.vertices[ii], self.vertices[ii+1], self.vertices[ii+2])

        normals = [None] * len (self.faces)
        n = None
        v = self.vertices
        for i in xrange (0, len (self.faces)):
            v1 = mkVec (i, 0)
            v2 = mkVec (i, 1)
            v3 = mkVec (i, 2)
            try:
                normals [i] = +((v2-v1)*(v3-v1))
            except:
                # print v1.v, v2.v, v3.v
                normals [i] = (0,0,0)

        return normals

    def toSTLFormatData (self):
        """
        Export current mesh to ASCII STL format (see
        http://www.ennex.com/~fabbers/StL.asp or
        http://en.wikipedia.org/wiki/STL_(file_format))

        @return {String} ASCII STL format of scene
        """

        normals = self.computeFaceNormals ()
        vs = self.vertices
        m = min (self.vertices)
        stl = "solid nclab_export\n"

        if m < 0: 
            m = -m 
        else:
            m = 1.0

        for i, face in enumerate (self.faces):            
            stl = stl + " facet normal %1e %2e %3e\n" % (normals [i][0], normals [i][1], normals [i][2])
            stl = stl + "  outer loop\n"
            for vi in face:
                v = 3 * vi
                stl = stl + "   vertex %1e %2e %3e\n" % (vs [v] + m, vs [v+1] + m, vs [v+2] + m)
            stl = stl + "  endloop\n endfacet\n"
        stl = stl + "endsolid nclab_export\n"

        return stl

    def fromJSON (self, jsonData):
        if jsonData.has_key ('vertices'): self.vertices = jsonData ['vertices']
        if jsonData.has_key ('indices'):
            self.faces = []
            for i in xrange (0, len (jsonData ['indices']), 3):
                self.faces.append (jsonData ['indices'][i, i + 3])

        if not self.faces:
            self.makeIndicesFromVertices ()

    def fromPlasm (self, obj):
        from pyplasm.xge import Plasm
        vector = Plasm.getTriangles(obj)
        vertices = [ vector[i] for i in xrange(vector.size()) ]
        self.fromJSON ({'vertices' : vertices})

def toSTL (obj, fname = "design.stl"):
    """
    Return stl represantation of PLASM object.

    @param {PlasmObject} obj PLASM object
    @param {String} fname file name
    @return {String} STL representation of PLASM object
    """
    m = Mesh3D ()
    m.fromPlasm (obj)
    stl = m.toSTLFormatData ()
    f = file (fname, "wt")
    f.write (stl)
    f.close ()
    return stl

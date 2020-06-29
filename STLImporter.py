from struct import unpack
from geometry import *

HEADER_SIZE =80
COUNT_SIZE =4

class stlImporter():
    def __init__(self,filename):
        self.triangles = []
        f=open(filename,"rb")
        header = f.read(HEADER_SIZE)
        facet_count = unpack("<I",f.read(COUNT_SIZE))[0]
#         print(facet_count)
        self.parse(f,facet_count)
        f.close()
        self.maximums = [self.maxx,self.maxy,self.maxz,self.minx,self.miny,self.minz]
#         print ("deltax",self.maxx-self.minx)
#         print ("deltay",self.maxy-self.miny)
#         print ("deltaz",self.maxz-self.minz)
#         print ("minz,maxz",self.minz,self.maxz)
        self.nbTriangles = len(self.triangles)
        print ("nbTriangles",self.nbTriangles)
    def parse(self,f,facet_count):
        self.maxx=self.maxy=self.maxz = -float("inf")
        self.minx=self.miny=self.minz = float("inf")
        for i in range(1, facet_count + 1):
            a1 = unpack("<f", f.read(4))[0]
            a2 = unpack("<f", f.read(4))[0]
            a3 = unpack("<f", f.read(4))[0]
            
            n = [float(a1), float(a2), float(a3)]
            
            v11 = unpack("<f", f.read(4))[0]
            v12 = unpack("<f", f.read(4))[0]
            v13 = unpack("<f", f.read(4))[0]
            self.checkMaxMin(v11,v12,v13)
            p1 = [float(v11), float(v12), float(v13)]
            
            v21 = unpack("<f", f.read(4))[0]
            v22 = unpack("<f", f.read(4))[0]
            v23 = unpack("<f", f.read(4))[0]
            self.checkMaxMin(v21,v22,v23)
            p2 = [float(v21), float(v22), float(v23)]
            
            v31 = unpack("<f", f.read(4))[0]
            v32 = unpack("<f", f.read(4))[0]
            v33 = unpack("<f", f.read(4))[0]
            self.checkMaxMin(v31,v32,v33)
            p3 = [float(v31), float(v32), float(v33)]
            
            # not used (additional attributes)
            f.read(2)
            self.triangles.append(Triangle3D(Point3D(p1),Point3D(p2),Point3D(p3),Vecteur(n)))
            
    def checkMaxMin(self,x,y,z):
        if x > self.maxx : 
            self.maxx = x
        if y > self.maxy :
            self.maxy = y
        if z > self.maxz :
            self.maxz =z 
        if x < self.minx :
            self.minx =x
        if y < self.miny :
            self.miny = y
        if z < self.minz :
            self.minz =z


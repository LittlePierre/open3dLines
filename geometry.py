import math
# from pygame.tests.freetype_tags import exclude
# from code import interact

class Slice():
    def __init__(self,polygon):
        self.polygon = polygon #list of 2D points
        self.minx = self.miny = float("inf")
        self.maxx = self.maxy = -float("inf")
        self.minmax()

    def minmax(self):
        for point in self.polygon:
            x,y = point.x, point.y
            if x< self.minx :
                self.minx =x
            if x > self.maxx :
                self.maxx =x
            if y < self.miny :
                self.miny =y
            if y > self.maxy :
                self.maxy =y

    def interX(self,other):
        pass

    def interY(self,other):
        pass

    def insideX(self,other):
        pass

    def insideY(self,other):
        pass

    def excludeX(self,other):
        return self.maxx< other.minx or self.minx> other.maxx 

    def excludeY(self,other):
        return self.maxy< other.miny or self.miny> other.maxy 

    def isExclude(self,other):
        return self.excludeX(other) and self.excludeY(other)

    def isInter(self,other):
        pass

    def isInside(self,other):
        if self.isExclude(other) or other.isExclude(self):
            return False
        if self.isInter(other):
            pass
        if self.inside(other):
            print("hellow world")


class Vecteur():
    def __init__(self,coordsTuple=None):
        if coordsTuple is None :
            coordsTuple = [0,0,1]
        [self.x,self.y,self.z] = coordsTuple
    def __str__(self):
        return "vect [x=%2f,y=%2f,z=%2f,module=%2f]"%(self.x,self.y,self.z,self.module())
    def module(self):
        return math.sqrt(self.x**2+self.y**2+self.z**2)
    def ProduitScalaire(self,other):
        return self.x*other.x+self.y*other.y+self.z*other.z
    def ProduitVectoriel(self,other):
        PVx = self.y*other.z-self.z*other.y
        PVy=self.z*other.x-self.x*other.z
        PVz = self.x*other.y-self.y*other.x
        return Vecteur([PVx,PVy,PVz])
    def addition(self,other):
        return Vecteur([self.x+other.x,self.y+other.y,self.z+other.z])
    def soustraction(self,other):
        return Vecteur([self.x-other.x,self.y-other.y,self.z-other.z])
    def __sub__(self,other):
        return Vecteur([self.x-other.x,self.y-other.y,self.z-other.z])
    def divise(self,scale):
        return Vecteur([self.x/scale,self.y/scale,self.z/scale])
    def multiply(self,scale):
        scale = float(scale)
        return Vecteur([self.x*scale,self.y*scale,self.z*scale])
    def normalize(self):
        return self.divise(self.module())
    def isNull(self):
        if self.x == 0 and self.y ==0 and self.z==0 :
            return True
        else :
            return False
    def rotate (self,norm,alpha):#retourne rotation de self autour de norm, de alpha degres
        #https://fr.wikipedia.org/wiki/Rotation_vectorielle
        alpha = alpha * math.pi/180.0
        v1 = self.multiply(math.cos(alpha))
        v2 =norm.multiply(self.ProduitScalaire(norm)*(1.0-math.cos(alpha)))
        v3 = norm.ProduitVectoriel(self).multiply(math.sin(alpha))
        rotated = v1.addition(v2).addition(v3)
        return rotated
class Point2D():
    def __init__(self,coordsTuple):
        [self.x,self.y]=coordsTuple
    def __str__(self):
        return "Point2D [x=%2f,y=%2f]"%(self.x,self.y)
    def translate(self,translation):
        x= self.x+translation[0]
        y =self.y+translation[1]
        return Point2D([x,y])
    def scale(self,scalexy):
        x = self.x*scalexy[0]
        y = self.y*scalexy[1]
        return Point2D([x,y])
    def isEqual(self,other):
        if not isinstance(other,Point2D):
            return False
        if (self.x - other.x)**2 + (self.y - other.y)**2 < 0.01 :
            return True
        return False
    def dist(self,x,y):
        return math.sqrt((self.x-x)**2+(self.y-y)**2)


class Line2D():
    def __init__(self,p1=None,p2=None):
        self.p1 = p1 if p1 is not None and isinstance(p1, Point2D) else Point2D()
        self.p2 = p2 if p2 is not None and isinstance(p2,Point2D) else Point2D()
    def __str__(self):
        result = "Line2D : %s %s"%(self.p1,self.p2)
        return result
    def isEqual(self,other):
        if not isinstance(other,Line2D):
            return False
        return self.p1.isEqual(other.p1) and self.p2.isEqual(other.p2)
    def dist(self,x,y):
        x1 = self.p1.x
        x2 = self.p2.x
        y1 = self.p1.y
        y2 = self.p2.y
        xM = float(x)
        yM = float(y)
        matrice = Matrix([
                          [x1-x2,y1-y2,0.],
                          [1.,0.,x1-x2],
                          [0.,1.,y1-y2]
                          ])
        res = Matrix(
                     [[xM*(x1-x2)+yM*(y1-y2)],
                     [x1],
                     [y1]]
                     )
        X = matrice.invert()*res
        xH = X.M[0][0]
        yH =X.M[1][0]
        k = X.M[2][0]
        pH = Point2D([xH,yH])
        if k> 0 and k<1 :
            dist = pH.dist(xM, yM)
        elif k<0 :
            dist = self.p1.dist(xM, yM)
        else :
            dist = self.p2.dist(xM,yM)
        return dist

class Point3D():
    def __init__(self,coordsTuple=None):
        if coordsTuple is None : 
            coordsTuple = [0,0,0]
        [self.x,self.y,self.z]=coordsTuple
    def __str__(self):
        return "Point3D [x=%2f,y=%2f,z=%2f]"%(self.x,self.y,self.z)
    def Vect(self,P2):
        return Vecteur([P2.x-self.x,P2.y-self.y,P2.z-self.z])
    def scale(self,scale):
        return Point3D([self.x*scale,self.y*scale,self.z*scale])
    def add(self,other):
        return Point3D([self.x+other.x,self.y+other.y,self.z+other.z])

class Line3D():
    def __init__(self,p1=None,p2=None):
        self.p1 = p1 if p1 is not None and isinstance(p1, Point3D) else Point3D()
        self.p2 = p2 if p2 is not None and isinstance(p2,Point3D) else Point3D()
    def __str__(self):
        result = "Line3D : %s %s"%(self.p1,self.p2)
        return result
    def center(self):
        return self.p1.add(self.p2).scale(0.5)
        

class Triangle3D():
    def __init__(self,Point1,Point2,Point3,Normale):
        self.p1 = Point1
        self.p2 = Point2
        self.p3 = Point3
        self.n = Normale
        self.cam = None
        self.bary =Point3D([(Point1.x+Point2.x+Point3.x)/3.0,(Point1.y+Point2.y+Point3.y)/3.0,(Point1.z+Point2.z+Point3.z)/3.0])
        self.dist = float("inf")
        self.visible = True
        self.points2D = []
    def droite(self,Point1,Point2,Point3):
        [xa,ya] = [Point1.x,Point1.y]
        [xb,yb] = [Point2.x,Point2.y]
        [xc,yc ] = [Point3.x,Point3.y]
        a = ya-yb
        b = xb-xa
        c = yb*xa-ya*xb
        signe = math.copysign(1, a*xc+b*yc+c)
        return[a,b,c,signe]
#     def belongsToTriangle(self,triangle,):
    def setCam(self,cam):
        self.cam = cam
        self.calcDist()
    def setwindow(self,window):
        self.window = [self.windowx,self.windowy]= window
        self.getPixelPosISO()

    def scaleto2DWidnow(self,minx,miny,scale):
        for index in range(4):
            self.points2D[index]= self.points2D[index].translate([-minx,-miny]).scale([scale,-scale]).translate([0,self.windowy])
    def calcDist (self):
        if self.cam is not None :
            self.dist = Vecteur([self.bary.x-self.cam.pos.x,self.bary.y-self.cam.pos.y,self.bary.z-self.cam.pos.z]).ProduitScalaire(self.cam.norm)
    def getPixelPosISO(self):
        
        for point in [self.p1,self.p2,self.p3,self.bary]:
            VecteurOM = Vecteur([point.x,point.y,point.z])
            pixelPosx = VecteurOM.ProduitScalaire(self.cam.horizVector)
            pixelPosy = VecteurOM.ProduitScalaire(self.cam.vertVector)
            p2d =  Point2D([pixelPosx,pixelPosy])
            self.points2D.append(p2d)
#         return self.points2D
    def selfBelongsToTriangle(self,triangle):
        q1,q2,q3  = triangle.points2D[0],triangle.points2D[1],triangle.points2D[2]
        d1 = self.droite(q1,q2,q3)
        d2 =self.droite(q1,q3,q2)
        d3 =self.droite(q2,q3,q1)
        cond1 =( math.copysign(1,d1[0]*self.points2D[3].x+d1[1]*self.points2D[3].y+d1[2])==d1[3])
        cond2 = (math.copysign(1,d2[0]*self.points2D[3].x+d2[1]*self.points2D[3].y+d2[2])==d2[3])
        cond3 = (math.copysign(1,d3[0]*self.points2D[3].x+d3[1]*self.points2D[3].y+d3[2])==d3[3])
#         print("cond1",cond1)
#         print("cond2",cond2)
#         print("cond3",cond3)
        return cond1 and cond2 and cond3
        
    def isbehind(self,triangle):
#         p1,p2,p3 = self.points2D[0],self.points2D[1],self.points2D[2]
        depth1 = self.dist
        depth2 = triangle.dist
        if depth1 <= depth2 :
            return False
        return self.selfBelongsToTriangle(triangle)




class Matrix():
    def __init__(self,M=None):
        if M is None :
            return
        if isinstance(M,Vecteur):
            M= [[M.x],[M.y],[M.z]]
        if isinstance(M, Point3D):
            M= [[M.x],[M.y],[M.z]]
        if not isinstance(M ,list) : 
            raise Exception("non conform matrix")
        self.M = M
        self.n = len (self.M)
        self.det = None
        if not isinstance(M[0],list):
            raise Exception("non conform matrix")
        self.m = len (self.M[0])
        for line in self.M :
            if not isinstance(line,list) or len (line) != self.m:
                raise Exception("non conform matrix")
    def __str__(self):
        result = "---\n"
        matrix =  self.M
        for row in matrix :
            result += str(row)+"\n"
        result +="----\n"
        return result
    def cleanCopy(self):
        T = []
        for i in range(self.n):
            line = []
            for j in range(self.m):
                line.append(self.M[i][j])
            T.append(line)
        return T

    def identity(self,n):
        M = []
        for index in range(n):
            line = [0.0]*n
            line[index] = 1.0
            M.append(line)
        return Matrix(M)
    
    def sanityCheck(self,result):
        result = result.M
        # check size of matrix,sizeof result
        if not isinstance(result,list) or len(result) != self.n:
            raise Exception("Non conform result")
        if not isinstance(result[0],list):
            raise Exception("Non conform result")
        sizeofResult = len(result[0])
        for row in result :
            if not isinstance(row, list) or len(row)!= sizeofResult:
                raise Exception("Non conform result") 


    def augmente(self,result):
        M = self.cleanCopy()
        r = result.M
        Maug = []
        index = 0
        for line in M:
            Maug.append(line)
            lineres = r[index]
            Maug[index] += lineres
            index +=1
        result = Matrix(Maug)
        return result

    def diminue(self,m):#enleve les m colonnes de gauche dans inverted et celles restant a droite dans solution
        M= self.M
#         inverted = []
        solution = []
        for row in M :
#             inverted.append(row[:m])
            solution.append(row[m:])
        inverted = Matrix(solution)
        return ([self,inverted])

    def gaussJordan(self,result):
        self.det = 1.0
        self.perm = 1
        n = self.n
        m = self.m
        try :
            self.sanityCheck(result)
        except Exception as e :
            print (e)
            return None
        Maug=self.augmente(result)
        M = Maug.M
        for  k in range(m):#k parcourt les colonnes de la matrice non augmentee
            for i in range(k,n):#on recherche l'indice de la ligne du maximum
                if abs(M[i][k]) > abs(M[k][k]):
                    M[k], M[i] = M[i],M[k] #on permute les lignes k et i (ligne du pivot et ligne du maxi
                    self.perm = -1
            q = M[k][k]
            self.det *= q*self.perm
            self.perm =1
            if q != 0 :
                for j in range(Maug.m):
                    M[k][j] = M[k][j]/q# on normalise la ligne du pivot pour que le pivot vale 1 Diviser la ligne k par A[k,j]
            for j in range(n):
                q2 = M[j][k]
                #|   |   Pour i de 1 jusqu'a n               (On simplifie les autres lignes)
                #|   |   |   Si i!=r alors
                #|   |   |   |   Soustraire a la ligne i la ligne r multipliee par A[i,j] (de facon a annuler A[i,j])
                if j!=k:
                    for l in range(Maug.m):
                            M[j][l] -= q2*M[k][l]# * M[k][k] (1.0)
        M2=Matrix(M)
        [augmented,inverted] = M2.diminue(m)
        if self.det !=0:
            inverted.det = 1.0/self.det
        return [augmented,inverted]
    def determinant(self):
        self.gaussJordan(Matrix().identity(self.n))
        return self.det
    def invert(self):
        if self.m != self.n :
            raise Exception("Size error")
        identity = Matrix().identity(self.n)
        gj  = self.gaussJordan(identity)
        inversed = gj[1]
        return inversed
    def scalarmult(self,multiplicand=1.0):
        result = []
        for row in self.M :
            newrow = [i * multiplicand for i in row]
            result.append(newrow)
        return Matrix(result)
    def matricemult(self,multiplicand):
        M=self.M
        N = multiplicand.M
        result = []
        for i in range(len(M)):
            rowM = M[i]
            newline = []
            for k in range(multiplicand.m):
                total = 0
                for j in range(len(rowM)):
                    total += rowM[j]*N[j][k]
                newline.append(total)
            result.append(newline)
        return Matrix(result)
    def vectmult(self,multiplicand):
        VColumn = Matrix(multiplicand)
        return self*VColumn
     
    def __mul__(self,multiplicand):
        if isinstance (multiplicand,float) or isinstance(multiplicand,int):
            return self.scalarmult(multiplicand)
        if isinstance(multiplicand,Matrix):
            return self.matricemult(multiplicand)
        if isinstance(multiplicand,Vecteur):
            return self.vectmult(multiplicand)
    def __add__(self,other):
        return
    
    def transpose(self):
        transposed = []
        for j in range(self.m) :
            transposedrow = []
            for i in range(self.n) :
                transposedrow.append(self.M[i][j])
            transposed.append(transposedrow)
        return Matrix(transposed)
            
    def getcolumnAsMatrix(self,columnnb = 1):
        M = self.M
        newMatrix = []
        for nbligne in range(self.n):
            newMatrix.append([M[nbligne][columnnb-1]])
        return Matrix(newMatrix)
    def getcolumnAsVector(self,columnb = 1):
        M = self.M
        return Vecteur([M[0][columnb-1],M[1][columnb-1],M[2][columnb-1]   ])
    #, add,  #orthonormize
if __name__ == "__main__":
    m1 = Matrix([
                 [2.1,0],
                 [0,0.9]])
#     v = Matrix([[1.],[1.]])
#     
#     mv = m1*v
#     print(mv)
#     sys
    m2 = Matrix([[1.],
                [1.]])
    m3 = m1.invert()
    print("m1",m1)
    print("invert",m3)
    m4 = m3.invert()
    print("invert2",m4)
    
    sys
    print(m1)
    print(m2)
    print (m1*m2)
    
    
    
    x= Vecteur([1,0,0])
    M = Matrix(x)
    print(M)
    print (M.getcolumnAsMatrix())
    print (M.getcolumnAsVector())
    
    y= Vecteur([0,1,0])
    z =x.ProduitVectoriel(y)
    yz = y.ProduitVectoriel(z)#x
    zx = z.ProduitVectoriel(x)#y
    print("yz",yz)
    print("zx",zx)
#     sys.exit()
    point = Point3D([0,0,0])
    normale = Vecteur([0,0,1])
    triangle1 = Triangle3D(point,point,point,normale)
    triangle2 = Triangle3D(point,point,point,normale)
    triangle1.dist = 5 
    triangle2.dist = 10
    p1 = Point2D([0,0])
    p2 = Point2D([200,0])
    p3 = Point2D([0,200])
    pb = Point2D([66,66])
    q1 = Point2D([50,50])
    q2 = Point2D([50,55])
    q3 = Point2D([55,50])
    qb = Point2D([52,52])
    triangle1.points2D = [p1,p2,p3,pb]
    triangle2.points2D = [q1,q2,q3,qb]
    print ("triangle1 is behind triangle2")
    print (triangle1.isbehind(triangle2))
    print ("triangle2 is behind triangle1")
    print (triangle2.isbehind(triangle1))



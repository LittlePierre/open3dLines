from geometry import Vecteur,Point2D,Point3D,Matrix

class SingletonCamera(object):
    __instance = None
    def __new__(cls,*args,**kwargs):
        if SingletonCamera.__instance is None:
            SingletonCamera.__instance = object.__new__(cls)
        return SingletonCamera.__instance


class Camera(SingletonCamera):
    def __init__(self,pos=Point3D(),norm=Vecteur([0,0,1])):
        SingletonCamera.__init__(self)
        if not hasattr(self, "initialized"):
            self.initialized = True
            self.pos = pos
            self.Model2CamtranslationVector = Vecteur([self.pos.x,self.pos.y,self.pos.z])
            self.depth = 0.0
            self.scale = 1.0
            self.norm = norm.normalize()
            self.horiz = Vecteur([1,0,0])
            self.vert = Vecteur([0,1,0])
            self.setRotationMatrix()
            self.setMatrixCam2View()

    def setDepth(self,depth):
        print ("depth",depth)
        self.depth = depth
    def setCamPos(self,pos=Point3D):
        self.pos = pos
        self.Model2CamtranslationVector = Vecteur([self.pos.x,self.pos.y,self.pos.z])

    def setCamOffsetVector(self):
        self.camOffsetVector = Vecteur([self.offsetx,self.offsety,0.0])

    def setRotationMatrix(self):
        normCol = Matrix(self.norm)
        horizCol = Matrix(self.horiz)
        vertCol = Matrix(self.vert)
        m = horizCol.augmente(vertCol)
        self.rotationMatrixFromModel = m.augmente(normCol)
#         return self.rotationMatrixFromModel

    def setMatrixCam2View(self):
        self.Matrixcam2View = Matrix([
                                      [self.scale,0.],
                                      [0.,-self.scale]
                                   ])
#         print("zzz",self.Matrixcam2View)
    def model2Cam(self, point3D):
        m=Matrix(point3D)
        rotated = self.rotationMatrixFromModel*m
        rotatedV = rotated.getcolumnAsVector()
        translatedV = rotatedV.addition(self.Model2CamtranslationVector)
#         return Point3D([translatedV.x,translatedV.y,translatedV.z])
        return Point3D([translatedV.x,translatedV.y,self.depth])

    def cam2Model(self,point3D):
        v = Vecteur([point3D.x,point3D.y,point3D.z])
        untranslated = v-self.Model2CamtranslationVector
        unrotatedAsMatrix = self.rotationMatrixFromModel.invert()*untranslated
        unrotatedAsVecteur = unrotatedAsMatrix.getcolumnAsVector()
        result = Point3D([ unrotatedAsVecteur.x,unrotatedAsVecteur.y,unrotatedAsVecteur.z  ])
        return result

    def cam2View(self,point3D):
        p2dCam = Matrix([[point3D.x],[point3D.y]])
        p2viewscaled = self.Matrixcam2View*p2dCam
        x= p2viewscaled.M[0][0]+self.offsetx
        y= p2viewscaled.M[1][0]+self.offsety
        return Point2D([x,y])

    def view2Cam(self,point2D,depth = None):
        if depth is None :
            depth = self.depth
        p2dViewuntranslated = Matrix( [[point2D.x-self.offsetx],[point2D.y-self.offsety]])
#         print("p2...",p2dViewuntranslated)
        inverted = self.Matrixcam2View.invert()
#         print("intverted",inverted)
        p2dCam = inverted*p2dViewuntranslated
        p3dCam = Point3D([p2dCam.M[0][0],p2dCam.M[1][0],depth])
        return p3dCam

    def model2View(self,point3D):
        pcam = self.model2Cam(point3D)
        return self.cam2View(pcam)

    def view2Model(self,point2D,depth=None):
        pcam = self.view2Cam(point2D, depth)
        p = self.cam2Model(pcam)
        return p

    def setScaleAndOffset(self,scale=1.0,offsetx=None,offsety=None):
        self.scale = scale if scale is not None else self.scale
        self.offsetx = offsetx if offsetx is not None else self.offsetx
        self.offsety = offsety if offsety is not None else self.offsety
        self.setMatrixCam2View()
        self.setCamOffsetVector()



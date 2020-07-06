from geometry import Vecteur,Point2D,Point3D,Matrix
from ctypes import *

class POINT3D(Structure):
    _fields_ = [("x", c_double),
        ("y", c_double),
        ("z",c_double)]
class Matrice3D(Structure):
    _fields_= [("m11",c_double),
               ("m12",c_double),
               ("m13",c_double),
               ("m21",c_double),
               ("m22",c_double),
               ("m23",c_double),
               ("m31",c_double),
               ("m32",c_double),
               ("m33",c_double),
        ]
class Parameters2d(Structure):
    _fields_ =[("scale",c_double),
               ("offsetx",c_int),
               ("offsety",c_int)]
class Point2(Structure):
    _fields_ = [("x",c_int),
                ("y",c_int)
                ]
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
            try :
                import platform
                if platform.system() == "Windows" :
                    self.library = cdll.LoadLibrary("./libs/libopen3dLinesLib.dll")
                else :
                    self.library = cdll.LoadLibrary("./libs/libopen3dLinesLib.so")
                self.library.fastModel2View.argtypes = [POINT3D,Matrice3D,POINT3D,Parameters2d]
                self.library.fastModel2View.restype = Point2
                self.libraryloaded = True
                print ("libopen3dLinesLib loaded")
            except :
                self.libraryloaded = False
                self.library = None
                print ("try to build lib to get faster")
            self.initialized = True
            self.libraryloaded = False
            self.library = None
            self.ctypeModel2CamtranslationVector= POINT3D()
            self.pos = pos
            self.setCamPos(pos)
#             self.Model2CamtranslationVector = Vecteur([self.pos.x,self.pos.y,self.pos.z])
            self.depth = 0.0
            self.scale = 1.0
            self.norm = norm.normalize()
            self.horiz = Vecteur([1,0,0])
            self.vert = Vecteur([0,1,0])
            self.ctypesRotationMatrixFromModel = Matrice3D()
            self.ctypesParameters2D = Parameters2d()
            self.setRotationMatrix()
            self.setMatrixCam2View()

    def setDepth(self,depth):
        print ("depth",depth)
        self.depth = depth
    def getCamPos(self):
        return Point3D([self.pos.x,self.pos.y,self.pos.z])

    def setCamPos(self,pos=Point3D):
        self.pos = pos
        self.Model2CamtranslationVector = Vecteur([self.pos.x,self.pos.y,self.pos.z])
        self.ctypeModel2CamtranslationVector.x = pos.x
        self.ctypeModel2CamtranslationVector.y = pos.y
        self.ctypeModel2CamtranslationVector.z = pos.z
    def setCamOffsetVector(self):
        self.camOffsetVector = Vecteur([self.offsetx,self.offsety,0.0])
        self.ctypesParameters2D.offsetx =self.offsetx
        self.ctypesParameters2D.offsety = self.offsety

    def setRotationMatrix(self):
        normCol = Matrix(self.norm)
        horizCol = Matrix(self.horiz)
        vertCol = Matrix(self.vert)
        m = horizCol.augmente(vertCol)
        self.rotationMatrixFromModel = m.augmente(normCol)
        self.ctypesRotationMatrixFromModel.m11 = self.rotationMatrixFromModel.M[0][0]
        self.ctypesRotationMatrixFromModel.m12 = self.rotationMatrixFromModel.M[0][1]
        self.ctypesRotationMatrixFromModel.m13 = self.rotationMatrixFromModel.M[0][2]
        self.ctypesRotationMatrixFromModel.m21 = self.rotationMatrixFromModel.M[1][0]
        self.ctypesRotationMatrixFromModel.m22 = self.rotationMatrixFromModel.M[1][1]
        self.ctypesRotationMatrixFromModel.m23 = self.rotationMatrixFromModel.M[1][2]
        self.ctypesRotationMatrixFromModel.m31 = self.rotationMatrixFromModel.M[2][0]
        self.ctypesRotationMatrixFromModel.m32 = self.rotationMatrixFromModel.M[2][1]
        self.ctypesRotationMatrixFromModel.m33 = self.rotationMatrixFromModel.M[2][2]
#         return self.rotationMatrixFromModel

    def setMatrixCam2View(self):
        self.Matrixcam2View = Matrix([
                                      [self.scale,0.],
                                      [0.,-self.scale]
                                   ])
        self.ctypesParameters2D.scale = self.scale
#         print("zzz",self.Matrixcam2View)
    def model2Cam(self, point3D):
#         print ("model2Cam")
#         print ("transVector",self.Model2CamtranslationVector)
        m=Matrix(point3D)
        rotated = self.rotationMatrixFromModel*m
        rotatedV = rotated.getcolumnAsVector()
        transvInCamView = self.rotationMatrixFromModel*self.Model2CamtranslationVector
        transvInCamView = transvInCamView.getcolumnAsVector()
        translatedV = rotatedV.addition(transvInCamView)
#         return Point3D([translatedV.x,translatedV.y,translatedV.z])
        return Point3D([translatedV.x,translatedV.y,self.depth])

    def cam2View(self,point3D):
        p2dCam = Matrix([[point3D.x],[point3D.y]])
        p2viewscaled = self.Matrixcam2View*p2dCam
        x= p2viewscaled.M[0][0]+self.offsetx
        y= p2viewscaled.M[1][0]+self.offsety
        return Point2D([x,y])

    def cam2Model(self,point3D,pos=None):
#         print ("poscam",pos)
#         print ("Point3D clicked (cam view)",point3D)
#         print ("rotation Matrix",self.rotationMatrixFromModel)
        if pos is None :
            pos = self.pos
        v = Vecteur([point3D.x,point3D.y,point3D.z])
        posInCam = self.rotationMatrixFromModel*Vecteur([pos.x,pos.y,pos.z])
        posInCam =posInCam.getcolumnAsVector()
#         print ("poscam InCam",posInCam)
        untranslated = v-posInCam
#         print ("untranslated",untranslated)
        unrotatedAsMatrix = self.rotationMatrixFromModel.invert()*untranslated
        unrotatedAsVecteur = unrotatedAsMatrix.getcolumnAsVector()
        result = Point3D([ unrotatedAsVecteur.x,unrotatedAsVecteur.y,unrotatedAsVecteur.z  ])
#         print ("point clicked in Model",result)
        return result

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
        if self.libraryloaded:
            point =POINT3D()
            point.x = point3D.x
            point.y = point3D.y
            point.z = point3D.z

            p2d  = self.library.fastModel2View(point,
                                                  self.ctypesRotationMatrixFromModel,
                                                  self.ctypeModel2CamtranslationVector,
                                                  self.ctypesParameters2D)
            return Point2D([p2d.x,p2d.y])
        else :
            pcam = self.model2Cam(point3D)
            return self.cam2View(pcam)

    def view2Model(self,point2D,depth=None,pos =None):
        if pos is None :
            pos=self.pos
        pcam = self.view2Cam(point2D, depth)
#         print ("pclicked cam",pcam)
        p = self.cam2Model(pcam,pos=pos)
#         print ("pclicked model",p)
        return p

    def setScaleAndOffset(self,scale=1.0,offsetx=None,offsety=None):
        self.scale = scale if scale is not None else self.scale
        self.offsetx = offsetx if offsetx is not None else self.offsetx
        self.offsety = offsety if offsety is not None else self.offsety
        self.setMatrixCam2View()
        self.setCamOffsetVector()



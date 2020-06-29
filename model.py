from geometry import Point3D,Line3D,Line2D,Vecteur,Point2D
from Utils import IdGenerator
from Camera import Camera
from Layer import Layers,Layer
from magnetism import Magnetism
import math
DELETE_ACTIONS = 1
ADD_ACTIONS = 2

class History():
    def __init__(self):
        self.historyList = []
        self.indexhisory=0
    def do(self):
        if self.indexhisory > len(self.historyList)-1:
            print ("nothing to redo")
            return 
        parameters = self.historyList[self.indexhisory]
        self.indexhisory+=1
        func = parameters.get("action").get("do")
        args = parameters.get("args")
        self._execute(func,args)
    def undo(self):
        if self.indexhisory <1 :
            print ("nothing to undo")
            return
        parameters = self.historyList[self.indexhisory-1]
        self.indexhisory-=1
        if self.indexhisory <0 :
            self.indexhisory = 0
        func = parameters.get("action").get("undo")
        args = parameters.get("args")
        self._execute(func,args)
        pass
    def _execute(self,func,args):
#         print ("execute - args",args,func)
        func(args,updateHistory=False)
    def add(self,parameters):
        self.historyList = self.historyList[:self.indexhisory]
        self.indexhisory+=1
        self.historyList.append(parameters)
#         print("index",self.indexhisory)
#         print("list",self.historyList)
    def reset(self):
        pass
    def remove(self):
        pass

class SingletonModel(object):
    __instance = None
    def __new__(cls,*args,**kwargs):#, val):
        if SingletonModel.__instance is None:
            SingletonModel.__instance = object.__new__(cls)
        return SingletonModel.__instance

class Model(SingletonModel):
    def __init__(self):
        SingletonModel.__init__(self)
        if not hasattr(self, "initialized"):
            print ("initialize model")
            self.initialized = True
            self.elements2d = {}
            self.elements3d = {}
            self.idGenerator = IdGenerator()
            self.cam = Camera()
            self.magnetism = Magnetism(self)
            self.history = History()
            self.actionsDict = {
                                ADD_ACTIONS:{"do":self.addElements,
                                                          "undo":self.delete,},
                                DELETE_ACTIONS:{"do":self.delete,
                                                     "undo":self.addElements,},
                                }
            self.layers = Layers()
#             self.dummyInit()
#             self.photogramInit()
    def addElements(self,elements,layer=None,updateHistory = True):
        actionCode = ADD_ACTIONS
        if not isinstance(elements, list):
            elements = [elements]
        args = []
        for element in elements :
            element3d = None
            ident = None
            if isinstance(element, dict):
                ident = element.get("ident",None)
                element3d  = element.get("element",None)
                layer = element.get("layer",None)
            if ident is  None:
                ident = self.idGenerator.getNewId()
            if layer is None :
                layer = self.layers.getActiveLayer()
            if element3d is None :
                element3d = element
            self.elements3d[ident]={"element":element3d,"layer":layer}
            args.append({"ident":ident,
                         "element":element3d,
                         "layer":layer})
        if updateHistory:
            self.history.add({
                                 "action":self.actionsDict.get(actionCode),
                                 "args":args})

    def delete(self,elements,updateHistory=True):
        actionCode = DELETE_ACTIONS
        print("delete",elements)
        args = []
        for element in elements :
            if isinstance(element,dict):
                ident = element.get("ident",None)
#                 element3d  = element.get("element",None)
#                 layer = element.get("layer",None)
            else :
                ident = element
            elt3d = self.elements3d.pop(ident)
            self.elements2d.pop(ident)
            args.append({"ident":ident,
                         "element":elt3d.get("element"),
                         "layer":elt3d.get("layer")})
        if updateHistory:
            self.history.add({
                                 "action":self.actionsDict.get(actionCode),
                                 "args":args})


    def refresh2dModel(self):
        self.elements2d = {}
        for id,obj in self.elements3d.items():
            element3d = obj.get("element",None)
            layer = obj.get("layer",self.layers.getActiveLayer())
            element2d = self.projetToView(element3d)
            if element2d is not None:
                self.elements2d[id]={"element":element2d,"layer":layer}

    def projetToView(self,element):#,layer=None):
#         if layer is None :
#             layer = self.layers.getActiveLayer()
        if isinstance(element, Line3D) :
            p1 = element.p1
            p2 = element.p2
            p1View = self.cam.model2View(p1)
            p2View = self.cam.model2View(p2)
            return Line2D(p1View,p2View)
        if isinstance(element,Point3D):
            return self.cam.model2View(element)

    def getElementById(self):
        pass
    def getLayerElements(self):
        pass
    def getNearestFromSelection(self,x,y):
        self.refresh2dModel()
        idselect = None
        minDist = float('inf')
        for ident,obj in self.elements2d.items():
            element2d = obj.get("element",None)
            layer = obj.get("layer",None)
            if layer.visible :
                dist = element2d.dist(x,y)
                if dist<minDist:
                    minDist = dist
                    idselect = ident
        return idselect
    def getNearestEnd(self,x,y):
        p3d2dId = None
        self.refresh2dModel()
        minDist = float('inf')
        for ident,obj in self.elements3d.items():
            element3d = obj.get("element",None)
            layer = obj.get("layer",None)
            if layer.visible :
                if isinstance(element3d, Line3D):
                    p1 = element3d.p1
                    p2 = element3d.p2
                    p1View = self.cam.model2View(p1)
                    p2View = self.cam.model2View(p2)
                    d1 = p1View.dist(x, y)
                    d2 = p2View.dist(x, y)
                    if d1 < minDist :
                        minDist = d1
                        p3d2dId = [p1,p1View,ident]
                    if d2 <minDist:
                        minDist = d2
                        p3d2dId = [p2,p2View,ident]
        return p3d2dId

    def getNearestCenter(self,x,y):
        p3d2dId = None
        self.refresh2dModel()
        minDist = float('inf')
        for ident,obj in self.elements3d.items():
            element3d = obj.get("element",None)
            layer = obj.get("layer",None)
            if layer.visible :
                if isinstance(element3d, Line3D):
                    p1 = element3d.center()
                    p1View = self.cam.model2View(p1)
                    d1 = p1View.dist(x, y)
                    if d1 < minDist :
                        minDist = d1
                        p3d2dId = [p1,p1View,ident]
        return p3d2dId
    def getNearestNoMag(self,x,y):
        p1_2d = Point2D([x,y])
        p1_3d =self.cam.view2Model(p1_2d)
        return [p1_3d,p1_2d,None]
    def getParallel(self,idSelected,parallelDist,x,y):
        if idSelected is None:
            return None
        element3d = self.elements3d[idSelected].get("element")
        if isinstance(element3d,Line3D):
            pMouseCam = self.cam.view2Cam(Point2D([float(x),float(y)]))
            p1cam = self.cam.model2Cam(element3d.p1)
            p2cam = self.cam.model2Cam(element3d.p2)
            vectNorm = Vecteur([p1cam.y-p2cam.y,
                                p2cam.x-p1cam.x,
                                0.0])
            if vectNorm.module()>0 :
                vectNorm=vectNorm.normalize().multiply(float(parallelDist))
            vectp1 = Vecteur([p1cam.x,p1cam.y,self.cam.depth])
            vectp2 = Vecteur([p2cam.x,p2cam.y,self.cam.depth])
            vectp1_xy = Vecteur([pMouseCam.x-p1cam.x,pMouseCam.y-p1cam.y,0.0])
            dir = vectNorm.ProduitScalaire(vectp1_xy)
            if dir > 0 :
                vectp3 = vectp1.addition(vectNorm)
                vectp4 = vectp2.addition(vectNorm)
            else :
                vectp3 = vectp1.soustraction(vectNorm)
                vectp4 = vectp2.soustraction(vectNorm)
            p3 = Point3D([vectp3.x,vectp3.y,self.cam.depth])
            p4 = Point3D([vectp4.x,vectp4.y,self.cam.depth])
            line3d = Line3D(self.cam.cam2Model(p3),self.cam.cam2Model(p4))
            p5 = self.cam.cam2View(p3)
            p6 = self.cam.cam2View(p4)
            line2d = Line2D(p5,p6)
            return [line3d,line2d]
    def getrectangleSelection(self,coininfGauche,coinSupDroit):
        pass
    def RotateSelection(self,selList,keep,nbrepeat,center,axis,alpha):
        if nbrepeat == 1:
            nbrepeat = 2
        listToRotate = []
        for identifier in selList : 
            listToRotate.append(self.elements3d[identifier].get("element",None))
        ListRotated = []
        for element in listToRotate :
            for nbrot in range(nbrepeat-1):
                angle = alpha*(nbrot+1)
                ListRotated.append(element.rotate(center,axis,angle))
        self.addElements(ListRotated,layer=None, updateHistory=True)
        if not keep :
            self.delete(selList, updateHistory=True)
    def TranslateSelection(self,selList,translation,keep,nb):
        if nb ==1 :
            nb= 2
#         print ("translate Selection",selList,translation,keep,nb)
        listToTranslate = []
        for identifier in selList : 
            listToTranslate.append(self.elements3d[identifier].get("element",None))
        ListTranslated = []
        for element in listToTranslate :
            for nbtrans in range(nb-1):
                trans = translation.scale(nbtrans+1)
                ListTranslated.append(element.translate(trans))
        self.addElements(ListTranslated,layer=None, updateHistory=True)
        if not keep :
            self.delete(selList, updateHistory=True)

    def popElement(self,id):
        pass

    def getAssociatedElement(self,element):
        pass

    def addStl(self,stl):
        for triangle in stl.triangles:
            self.addElements(triangle.lines,
                                 # layer, updateHistory
                                 )

    def dummyInit(self):
        line = Line3D(Point3D([0,0,0]),Point3D([100,0,0]))
        self.addElements(line)
        line = Line3D(Point3D([0,0,0]),Point3D([0,100,0]))
        self.addElements(line)
        line = Line3D(Point3D([0,100,0]),Point3D([100,100,0]))
        self.addElements(line)
        line = Line3D(Point3D([100,0,0]),Point3D([100,100,0]))
        self.addElements(line)
         
        line = Line3D(Point3D([0,0,100]),Point3D([100,0,100]))
        self.addElements(line)
        line = Line3D(Point3D([0,0,100]),Point3D([0,100,100]))
        self.addElements(line)
        line = Line3D(Point3D([0,100,100]),Point3D([100,100,100]))
        self.addElements(line)
        line = Line3D(Point3D([100,0,100]),Point3D([100,100,100]))
        self.addElements(line)
         
        line = Line3D(Point3D([0,0,0]),Point3D([0,0,100]))
        self.addElements(line)
        line = Line3D(Point3D([100,0,0]),Point3D([100,0,100]))
        self.addElements(line)
        line = Line3D(Point3D([0,100,0]),Point3D([0,100,100]))
        self.addElements(line)
        line = Line3D(Point3D([100,100,0]),Point3D([100,100,100]))
        self.addElements(line)
        line = Line3D(Point3D([0,0,0]),Point3D([100,100,100]))
        self.addElements(line)
    
    def photogramInit(self):
        Rt2=  [[-0.22232591,0.26331397,-0.93874221,0.74086751],
               [-0.37569762,-0.911621, -0.16672866,0.14538883],
               [ 0.8996791,-0.31561512,-0.3016034,-0.65572664]]


        pts3D= [[-1.32131714e-01,-4.25992109e-02,7.64224300e-01],
                [-4.67894793e-02,1.92619952e-06,6.34911518e-01],
                [ 2.07473713e-01,-4.11896507e-02,7.56924057e-01],
                [ 1.19740946e-01,-8.11438758e-02,8.88253746e-01],
                [-5.10655401e-02,6.55515450e-02,6.49154059e-01],
                [ 2.06270751e-01,2.46866220e-02,7.77478121e-01],
                [ 1.12463674e-01,-1.33275751e-02,9.10479497e-01]]
        last = [0,0,0]
        for p3d in pts3D :
            if last is not None:
                line = Line3D(Point3D(p3d).scale(300.0),Point3D(last).scale(300.0))
                self.addElements(line)
            last = p3d
        line =Line3D(Point3D(last).scale(300.0),Point3D([0.74086751,#-0.22232591,
                                                         0.14538883,#-0.911621,
                                                         -0.65572664,#-0.3016034
                                                         ]).scale(300.0))
        self.addElements(line)




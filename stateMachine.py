from geometry import Point2D,Point3D, Line3D,Line2D
from Camera import Camera
from model import Model
import Utils
from Utils import ColorClass,StateMachineList
import wx
# import wx

class GenericStateMachine():
    def __init__(self,cadWindow):
        self.cadWindow = cadWindow
        self.root = cadWindow.root
        self.pnl = cadWindow.pnl
        self.model = Model()
        self.cam = Camera()
        self.idSelectedList= []
#         self.mouseactive = False
        self.magnetism = self.model.magnetism
    def rotate(self):
        pass
    def setActive(self):
        pass
    def exit(self):
        pass
    def movemouse(self,x,y):
        pass
    def notifyAddCmd(self,command):
        pass
class LineStateMachine(GenericStateMachine):
    def __init__(self,cadWindow):
        GenericStateMachine.__init__(self,cadWindow)
#         self.cadWindow = cadWindow
#         self.root = cadWindow.root
#         self.cadWindow.root.rightPanel.setCommandLabel("Enter first Point")
        self.nextAction = self.selectFirst
        self.first2d = None
        self.second2d = None
        self.first3d = None
        self.second3d = None
        self.current = None
#         self.mouseactive = True
        self.idle = True
        self.lastMagneticPoint = None
#     def idle(self,*args,**kwargs):
#         pass
    def setActive(self):
        self.cadWindow.pnl.rightPanel.setCommandLabel(_("Enter first point"))
#         self.cadWindow.SetFocus()
        self.cadWindow.SetCursor(wx.Cursor(wx.CURSOR_CROSS))
    def exit(self):
        self.cadWindow.pnl.rightPanel.setCommandLabel("")
    def notifyClick(self,event):
        x=float(getattr(event, "x",0.))
        y=float(getattr(event, "y",0.))
        [point3d,point2d,ident]=self.magnetism.getMagneticPoint(x, y)
        self.nextAction(point2d,point3d)
    def notifyAdd3dPoint(self,point3d):
        point2d = self.cam.model2View(point3d)
        self.nextAction(point2d,point3d)
        self.nextAction(point2d,point3d)
    def notifyAddCmd(self,command):
        try :
            coords =command.split(",")
            coord = map(float,coords)
            point = Point3D(coord)
            self.notifyAdd3dPoint(point)
        except :
            pass
    def notifyMoveMouse(self,event):
        x=float(getattr(event, "x",0.))
        y=float(getattr(event, "y",0.))
        newP = self.magnetism.getMagneticPoint(x, y)[1]
#         print ("lastMag",self.lastMagneticPoint)
#         print ("isEqual",newP.isEqual(self.lastMagneticPoint))
        if not newP.isEqual(self.lastMagneticPoint) and self.magnetism.flags != 0:
            self.cadWindow.refresh()
            p1 = Point2D([newP.x-5,newP.y])
            p2 = Point2D([newP.x+5,newP.y])
            p3 = Point2D([newP.x,newP.y-5])
            p4 = Point2D([newP.x,newP.y+5])
            self.cadWindow.drawLine(p1,p2,color = ColorClass.select)
            self.cadWindow.drawLine(p3,p4,color = ColorClass.select)
        self.lastMagneticPoint = newP
        self.movemouse(newP.x,newP.y)
    def selectFirst(self,point2d,point3d):
        self.idle = False
        self.current = self.first2d = point2d
        self.first3d = point3d
#         self.mouseactive = True
        self.nextAction = self.firstSelected
    def firstSelected(self,point2d,point3d):
        self.current = point2d
        self.nextAction = self.selectSecond
        self.cadWindow.pnl.rightPanel.setCommandLabel(_("Enter second Point"))
    def selectSecond(self,point2d,point3d):
        self.current = self.last2d = point2d
        self.last3d = point3d
        self.model.addElements(Line3D(self.first3d,self.last3d))
        self.current = self.last2d
        self.first2d = self.last2d
        self.first3d = self.last3d
        self.cadWindow.refresh()
        self.nextAction = self.firstSelected
    def movemouse(self,newx,newy):
        new = Point2D([newx,newy])
        self.cadWindow.drawLine(self.first2d,self.current,color=ColorClass.erase,width=3)
        self.cadWindow.drawLine(self.first2d,new,color=ColorClass.fromActiveLayer)
        self.current  = new
    def rotate(self):
#         self.first3d = self.cam.view2Model(self.first2d)
        if self.first3d is not None:
            self.first2d = self.cam.model2View(self.first3d)
    def reiinit(self):
        self.cadWindow.drawLine(self.first2d,self.current,color=ColorClass.erase,width=3)
        self.rightPanel = self.pnl.rightPanel
        self.rightPanel.setCommandLabel(_("Enter first Point"))
        if self.idle :
            self.cadWindow.setStateMachine(StateMachineList.selectStateMachine)
        else :
            self.__init__(self.cadWindow)
        
class SelectStateMachine(GenericStateMachine):
    def __init__(self,cadWindow):
        GenericStateMachine.__init__(self,cadWindow)
        self.nextAction = self.leftPressed

    def setActive(self):
        self.cadWindow.pnl.rightPanel.setCommandLabel(_("Select entities"))
        self.cadWindow.SetCursor(wx.Cursor(wx.CURSOR_DEFAULT))
        self.cadWindow.pnl.leftPanel.lineComboCtrl.SetValue(_("Add Line"))
#         self.cadWindow.SetFocus()
    def exit(self):
        self.cadWindow.pnl.rightPanel.setCommandLabel("")
    def notifyClick(self,event):
        x=int(getattr(event, "x",0))
        y=int(getattr(event, "y",0))
        self.nextAction(x,y)
    def notifyMoveMouse(self,event):
        x=int(getattr(event, "x",0))
        y=int(getattr(event, "y",0))
        self.movemouse(x,y)
    def leftPressed(self,x,y):
        idSelected = self.model.getNearestFromSelection(x,y)
        if idSelected is not None :
            if idSelected in self.idSelectedList :
                self.idSelectedList.pop(self.idSelectedList.index(idSelected))
            else :
                self.idSelectedList.append(idSelected)
        print (self.idSelectedList)
        self.cadWindow.refresh()
        self.nextAction = self.leftReleased
    def leftReleased(self,x,y):
        self.nextAction = self.leftPressed
    def reiinit(self):
        self.__init__(self.cadWindow)
        

class ParallelStateMachine(GenericStateMachine):
    def __init__(self,cadWindow):
        GenericStateMachine.__init__(self,cadWindow)
        self.nextAction = self.leftPressed
        self.parallelDist = 10.0
        self.lastParallel = None
    def setActive(self):
        self.cadWindow.pnl.rightPanel.setCommandLabel(_("Enter distance"))
        self.cadWindow.SetCursor(wx.Cursor(wx.CURSOR_DEFAULT))
#         self.cadWindow.SetFocus()
    def exit(self):
        self.cadWindow.pnl.rightPanel.setCommandLabel("")
    def notifyClick(self,event):
        x=int(getattr(event, "x",0))
        y=int(getattr(event, "y",0))
        self.nextAction(x,y)
    def notifyMoveMouse(self,event):
        x=int(getattr(event, "x",0))
        y=int(getattr(event, "y",0))
        idSelected = self.model.getNearestFromSelection(x,y)
#         element3d = self.model.elements3d[idSelected].get("element")
        parallel = self.model.getParallel(idSelected,self.parallelDist,x,y)
        if self.lastParallel is not None:
            if not parallel[1].isEqual(self.lastParallel[1]):
                self.cadWindow.drawLine(self.lastParallel[1].p1,
                                        self.lastParallel[1].p2,
                                        color=ColorClass.erase,
                                        width=3)
                self.cadWindow.drawLine(parallel[1].p1,
                                        parallel[1].p2,
                                        color = ColorClass.select)
#                 p1 =self.model.cam.model2View(element3d.p1)
#                 p2 = self.model.cam.model2View(element3d.p2)
#                 self.cadWindow.drawLine(p1,p2,color=ColorClass.select)
        self.lastParallel = parallel
#         self.movemouse(x,y)
    def rotate(self):
        if self.lastParallel is not None :
            self.cam.setRotationMatrix()
            self.lastParallel = [self.lastParallel[0],
                                 Line2D([self.cam.model2View(self.lastParallel[0].p1),
                                         self.cam.model2View(self.lastParallel[0].p2),])
                             ]
    def leftPressed(self,x,y):
        self.model.addElements(self.lastParallel[0])
        self.cadWindow.refresh()
        self.nextAction = self.leftReleased
    def leftReleased(self,x,y):
        self.nextAction = self.leftPressed
    def notifyAddCmd(self,command):
        try :
            self.parallelDist = float(command)
        except :
            pass
    def reiinit(self):
        parallelDist = self.parallelDist
        self.__init__(self.cadWindow)
        self.parallelDist = parallelDist
        self.cadWindow.setStateMachine(StateMachineList.selectStateMachine)

class TranslateStateMachine(GenericStateMachine):
    def __init__(self,cadWindow):
        GenericStateMachine.__init__(self,cadWindow)
        self.nextAction = self.selectFirst
        self.first2d = None
        self.second2d = None
        self.first3d = None
        self.second3d = None
        self.current = None
#         self.mouseactive = True
        self.idle = True
        self.lastMagneticPoint = None

    def setActive(self):
        self.__init__(self.cadWindow)
        self.cadWindow.pnl.rightPanel.setCommandLabel(_("Enter first point"))
        self.cadWindow.SetCursor(wx.Cursor(wx.CURSOR_CROSS))
    def exit(self):
        self.cadWindow.pnl.rightPanel.setCommandLabel("")
    def notifyClick(self,event):
        x=float(getattr(event, "x",0.))
        y=float(getattr(event, "y",0.))
        [point3d,point2d,ident]=self.magnetism.getMagneticPoint(x, y)
        self.nextAction(point2d,point3d)
    def notifyAdd3dPoint(self,point3d):
        point2d = self.cam.model2View(point3d)
        self.nextAction(point2d,point3d)
#         self.nextAction(point2d,point3d)
    def notifyAddCmd(self,command):
        try :
            coords =command.split(",")
            coord = map(float,coords)
            point = Point3D(coord)
            self.notifyAdd3dPoint(point)
        except :
            pass
    def notifyMoveMouse(self,event):
        x=float(getattr(event, "x",0.))
        y=float(getattr(event, "y",0.))
        newP = self.magnetism.getMagneticPoint(x, y)[1]
#         print ("lastMag",self.lastMagneticPoint)
#         print ("isEqual",newP.isEqual(self.lastMagneticPoint))
        if not newP.isEqual(self.lastMagneticPoint) and self.magnetism.flags != 0:
            self.cadWindow.refresh()
            p1 = Point2D([newP.x-5,newP.y])
            p2 = Point2D([newP.x+5,newP.y])
            p3 = Point2D([newP.x,newP.y-5])
            p4 = Point2D([newP.x,newP.y+5])
            self.cadWindow.drawLine(p1,p2,color = ColorClass.select)
            self.cadWindow.drawLine(p3,p4,color = ColorClass.select)
        self.lastMagneticPoint = newP
#         self.movemouse(newP.x,newP.y)
    def selectFirst(self,point2d,point3d):
        self.idle = False
        self.current = self.first2d = point2d
        self.first3d = point3d
#         self.mouseactive = True
        self.nextAction = self.firstSelected
    def firstSelected(self,point2d,point3d):
        self.current = point2d
        self.nextAction = self.selectSecond
        self.cadWindow.pnl.rightPanel.setCommandLabel(_("Enter second Point"))
    def selectSecond(self,point2d,point3d):
        self.current = self.last2d = point2d
        self.last3d = point3d
        translation = self.last3d.sub(self.first3d)
#         self.model.addElements(Line3D(self.first3d,self.last3d))
#         self.current = self.last2d
#         self.first2d = self.last2d
#         self.first3d = self.last3d
#         self.cadWindow.refresh()
        self.pnl.leftPanel.notifyTranslate(translation)
        self.reiinit()
#         self.nextAction = self.firstSelected
    def movemouse(self,newx,newy):
        new = Point2D([newx,newy])
        self.cadWindow.drawLine(self.first2d,self.current,color=ColorClass.erase,width=3)
        self.cadWindow.drawLine(self.first2d,new,color=ColorClass.fromActiveLayer)
        self.current  = new
    def rotate(self):
        pass
    def reiinit(self):
#         self.rightPanel = self.pnl.rightPanel
#         self.rightPanel.setCommandLabel(_("Enter first Point"))
        self.cadWindow.setStateMachine(StateMachineList.selectStateMachine)
#         else :
#             self.__init__(self.cadWindow)



if __name__ == "__main__":
    pass

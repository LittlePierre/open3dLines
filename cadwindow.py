import wx
from model import Model
from Camera import Camera
from stateMachine import LineStateMachine,SelectStateMachine,\
    ParallelStateMachine,TranslateStateMachine, RotateStateMachine,\
    CircleStateMachine
from geometry import Line3D,Vecteur,Point3D,Line2D,Polyligne2D,Point2D
from Utils import ColorClass,StateMachineList#,CADWindowStates,
from numpy.core.defchararray import center


class CADWindow(wx.Window):
    def __init__(self, pnl,root):
#         super(CADWindow, self).__init__(parent)#,#style=wx.NO_FULL_REPAINT_ON_RESIZE
#         SingletonCADWindow.__init__(self)
        wx.Window.__init__(self, pnl,size=(1,-1),style= wx.RESIZE_BORDER |
                            wx.ALWAYS_SHOW_SB |
                            wx.HSCROLL |
                            wx.VSCROLL |
                            wx.WANTS_CHARS
                            )#,style=wx.HSCROLL | wx.VSCROLL)
#                 size=(self.windowx,self.windowy))
        self.root = root
        self.pnl = pnl
        self.initDrawing()
#         self.makeMenu()
        self.initBuffer()
        self.bindEvents()
    
    def initDrawing(self):
#         self.SetBackgroundColour('BLACK')
        self.size = self.GetSize()
        self.bgcolor = wx.Colour(0,0,0)
        self.SetBackgroundColour(self.bgcolor)
        self.model = Model()
        self.history = self.model.history
        self.cam = Camera()
        self.cam.setScaleAndOffset(scale = 1.0,offsetx=self.size.width//2,offsety =self.size.height//2)
        self.stateMachine = LineStateMachine(self)
        self.stateMachine = SelectStateMachine(self)
        self.maxx=self.maxy = -float("inf")
        self.minx=self.miny= float("inf")
        self.minx = 0
        self.miny =0
        self.middlepressed = False
        self.ctrlPressed = False
        self.translateView = False
#         self.currentState = CADWindowStates.Idle

    def bindEvents(self):
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_IDLE, self.onIdle)
        self.Bind(wx.EVT_SIZE, self.onSize)          # Prepare for redraw
        self.Bind(wx.EVT_LEFT_DOWN,                      self.leftclick)
        self.Bind(wx.EVT_LEFT_UP,                  self.leftclickrelease)
        self.Bind(wx.EVT_RIGHT_DOWN,                      self.rightclick)
        self.Bind(wx.EVT_MIDDLE_DOWN,                      self.middleclick)
        self.Bind(wx.EVT_MIDDLE_UP,                  self.middleclickrelease)
        self.Bind(wx.EVT_MOTION, self.motion)
        self.Bind(wx.EVT_MOUSEWHEEL, self.mouseWheel)
        self.Bind(wx.EVT_CHAR,                    self.onChar)
        self.Bind(wx.EVT_KEY_DOWN,              self.onKeyDown)
        self.Bind(wx.EVT_KEY_UP,                self.onKeyUp)

    def initBuffer(self):
        ''' Initialize the bitmap used for buffering the display. '''
        self.size = self.GetSize()
        (sizex,sizey)=self.size
        if sizex<1 :
            self.size.width =1
        if sizey < 1 :
            self.size.height =1
        self.cam.setScaleAndOffset(offsetx = self.size.width//2,offsety = self.size.height//2 )
#         self.offsetx = self.size.width//2#400.0#float (self.windowx/2.0)
#         self.offsety =self.size.height//2#300.0#float (self.windowy/2.0)
        print("buffer size",self.size)
        self.buffer = wx.Bitmap(width=self.size.width, height=self.size.height)#EmptyBitmap(size.width, size.height)
        dc = wx.BufferedDC(None, self.buffer)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        self.refresh(None)
        self.reInitBuffer = False
        
    def onSize(self, event):
#         print ("000onSize")
        ''' Called when the window is resized. We set a flag so the idle
            handler will resize the buffer. '''
        self.reInitBuffer = True
    def onIdle(self, event):
#         print("idle")
        ''' If the size was changed then resize the bitmap used for double
            buffering to match the window size.  We do it in Idle time so
            there is only one refresh after resizing is done, not lots while
            it is happening. '''
        if self.reInitBuffer:
#             print ("going to init buff")
            self.initBuffer()
            self.Refresh(False)
    def onPaint(self, event):
#         print("paint")
        ''' Called when the window is exposed. '''
        # Create a buffered paint DC.  It will create the real
        # wx.PaintDC and then blit the bitmap to it when dc is
        # deleted.  Since we don't need to draw anything else
        # here that's all there is to it.
        dc = wx.BufferedPaintDC(self, self.buffer)

    def onKeyDown(self,event):
#         print ("key down")
        code = event.GetKeyCode()
#         print(code)
        if code == 308:
            self.ctrlPressed = True
        event.Skip()
    def onKeyUp(self,event):
#         print ("key up")
        code = event.GetKeyCode()
#         print(code)
        if code == 308:
            self.ctrlPressed = False
            self.translateView = False
        event.Skip()
    def onChar(self,event):
        print ("Event Char")
        code = event.GetKeyCode()
        print(code)
        dictactions = {
                       wx.WXK_RIGHT:self.leftView,
                       wx.WXK_NUMPAD6:self.leftView,
                       "6":self.leftView,
                       wx.WXK_LEFT:self.rightView,
                       wx.WXK_NUMPAD4:self.rightView,
                       "4":self.rightView,
                       wx.WXK_HOME:self.frontView,
                       wx.WXK_NUMPAD5:self.frontView,
                       "5":self.frontView,
                       wx.WXK_UP:self.downView,
                       wx.WXK_NUMPAD8:self.downView,
                       "8":self.downView,
                       wx.WXK_DOWN:self.upView,
                       wx.WXK_NUMPAD2:self.upView,
                       "2":self.upView,
#                        wx.WXK_UP:
#                        wx.WXK_DOWN:
                       wx.WXK_CONTROL_Q:self.quit,
                       wx.WXK_CONTROL_R:self.refresh,
                       "r":self.refresh,
                       wx.WXK_CONTROL_A:self.selecAll,
                       wx.WXK_CONTROL_I:self.invertSelection,
                       wx.WXK_CONTROL_Z:self.undo,
                       wx.WXK_CONTROL_Y:self.redo,
                       wx.WXK_DELETE:self.deleteSelection,
                       }
        action = dictactions.get(code,None)
        if action is None :
            action = dictactions.get(chr(code),None)
        if action is not None :
            action(event)

    def onCtrl(self,event):
        print("Ctrl")
    def selecAll(self,event):
        self.stateMachine.selectAll()
    def invertSelection(self,event):
        self.stateMachine.invertSelection()
    def refresh(self,event=None):
        lines = []
        pens = []
        dc = wx.BufferedDC(None, self.buffer)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        self.cam.setRotationMatrix()
#         self.cam.setScaleAndOffset()
        self.cam.setMatrixCam2View()
        self.model.refresh2dModel()
        for id,obj in self.model.elements2d.items():
            element = obj.get("element",None)
            layer = obj.get("layer",self.model.layers.getActiveLayer())
            width = layer.width
            visible = layer.visible
            if isinstance(element,Polyligne2D) and visible:
                for ligne in element.lines2d :
                    p1 = ligne.p1
                    p2 = ligne.p2
                    if p1 is not None and p2 is not None :
                        x1,y1,x2,y2 = map(int,[p1.x,p1.y, p2.x,p2.y])
                        lines.append([x1,y1,x2,y2])
                        pens.append(self.getPenColor(layer, ColorClass.fromElementLayer, width))
            if isinstance(element, Line2D) and visible:
                p1 = element.p1
                p2 = element.p2
                if p1 is not None and p2 is not None :
                    x1,y1,x2,y2 = map(int,[p1.x,p1.y, p2.x,p2.y])
                    lines.append([x1,y1,x2,y2])
                    pens.append(self.getPenColor(layer, ColorClass.fromElementLayer, width))
        self.drawLines(lines,pens)
#                 self.drawLine(p1, p2,ColorClass.fromElementLayer,layer = layer,width=width)
        lines = []
        pens = []
        for ident in self.stateMachine.idSelectedList :
            element2d = self.model.elements2d[ident].get("element",None)
            if isinstance(element2d, Line2D):
                p1 = element2d.p1
                p2 = element2d.p2
                if p1 is not None and p2 is not None :
                    x1,y1,x2,y2 = map(int,[p1.x, p1.y, p2.x, p2.y])
                    lines.append([x1,y1,x2,y2])
                    pens.append(self.getPenColor(layer, color=ColorClass.select))
            elif isinstance(element2d,Polyligne2D) :
                for ligne in element2d.lines2d :
                    p1 = ligne.p1
                    p2 = ligne.p2
                    if p1 is not None and p2 is not None :
                        x1,y1,x2,y2 = map(int,[p1.x,p1.y, p2.x,p2.y])
                        lines.append([x1,y1,x2,y2])
                        pens.append(self.getPenColor(layer, color=ColorClass.select))
#                 self.drawLine(element2d.p1,element2d.p2,color = ColorClass.select)
        self.drawLines(lines,pens)
        self.Refresh(False)
        self.SetFocus()
    def getPenColor(self,layer=None,color=ColorClass.default,width=1):
        if layer is None :
            layer = self.model.layers.getActiveLayer()
        colordict = {
                     ColorClass.default:wx.RED,
                     ColorClass.fromActiveLayer:self.model.layers.getActiveLayer().color,
                     ColorClass.erase:self.bgcolor,
                     ColorClass.select:wx.Colour(128,128,128),
                     ColorClass.fromElementLayer:layer.color
                     }
        pencolor = colordict.get(color,wx.RED)
        return wx.Pen(pencolor,width=width)

    def frontView(self,event):
        self.cam.norm = Vecteur([0,0,1])
        self.cam.horiz = Vecteur([1,0,0])
        self.cam.vert = Vecteur([0,1,0])
        self.cam.setRotationMatrix()
        self.stateMachine.rotate()
        self.refresh(event)
    def rightView(self,event):
        self.cam.norm = Vecteur([-1,0,0])
        self.cam.horiz = Vecteur([0,0,-1])
        self.cam.vert = Vecteur([0,1,0])
        self.cam.setRotationMatrix()
        self.stateMachine.rotate()
        self.refresh(event)
    def leftView(self,event):
        self.cam.norm = Vecteur([1,0,0])
        self.cam.horiz = Vecteur([0,0,1])
        self.cam.vert = Vecteur([0,1,0])
        self.cam.setRotationMatrix()
        self.stateMachine.rotate()
        self.refresh(event)
    def downView(self,event):
        self.cam.norm = Vecteur([0,1,0])
        self.cam.horiz = Vecteur([1,0,0])
        self.cam.vert = Vecteur([0,0,1])
        self.cam.setRotationMatrix()
        self.stateMachine.rotate()
        self.refresh(event)
    def upView(self,event):
        self.cam.norm = Vecteur([0,-1,0])
        self.cam.horiz = Vecteur([1,0,0])
        self.cam.vert = Vecteur([0,0,-1])
        self.cam.setRotationMatrix()
        self.stateMachine.rotate()
        self.refresh(event)
    def rearView(self,event):
        pass
    def drawLines(self,lines, pens):
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        dc.DrawLineList(lines,pens)
    def drawLine(self,point1,point2,color=None,layer = None,width=1):
        if point1 is None or point2 is None :
            return
        if layer is None :
            layer = self.model.layers.getActiveLayer()
        colordict = {
                     ColorClass.default:wx.RED,
                     ColorClass.fromActiveLayer:self.model.layers.getActiveLayer().color,
                     ColorClass.erase:self.bgcolor,
                     ColorClass.select:wx.Colour(128,128,128),
                     ColorClass.fromElementLayer:layer.color
                     }
        pencolor = colordict.get(color,wx.RED)
        x1,y1,x2,y2 = map(int,[point1.x,point1.y,point2.x,point2.y])
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        dc.SetPen(wx.Pen(pencolor,width=width))
        dc.DrawLine(x1, y1, x2, y2)

    def leftclick(self,event):
        if self.ctrlPressed == False :
            self.stateMachine.notifyClick(event)
        else : 
#             print ("ctrl Clk")
            self.translateView = True
            firsttranslatex,firsttranslatey = event.x,event.y
#             print ("clicked on ",firsttranslatex,firsttranslatey)
            self.initialpos = self.cam.view2Model(Point2D([firsttranslatex,firsttranslatey]))
#             print ("intialPos",self.initialpos)
#         self.stateMachine.leftClick(event)
#         if self.stateMachine.getState()==3 :
#             self.addline()

    def leftclickrelease(self,event):
#         print ('left release')
        if self.translateView == False :
            self.stateMachine.notifyClick(event)
        else :
            self.translateView = False
#         self.stateMachine.releaseLeftClick(event)
# #         point1,point2 = self.stateMachine.lineStart,self.stateMachine.lineEnd
#         self.refresh(event)
#         self.drawLine(point1,point2)
    def motion(self,event):
        if self.middlepressed:
            self.rotate(event)
            return
        if self.translateView:
#             print ("translate")
            self.translate(event)
            return
#         elif self.stateMachine.mouseactive:
        self.stateMachine.notifyMoveMouse(event)
#         if self.stateMachine.getState()<= 2 and self.stateMachine.getState()>0:
#             point1 = self.stateMachine.lineStart
#             previouspos = self.stateMachine.previousPos
#             self.drawLine(point1, previouspos, wx.Pen(wx.BLACK, 4))
#             self.stateMachine.moveMouse(event)
#             self.drawLine(point1,self.stateMachine.currentPos)

    def rotate(self,event):
        self.currentRotatex,self.currentRotatey = event.x,event.y
        x = self.currentRotatex-self.lastRotatex
        y = -self.currentRotatey+self.lastRotatey
        horiz = self.cam.horiz.multiply(x)
        vertic = self.cam.vert.multiply(y)
        self.lastRotatex,self.lastRotatey=self.currentRotatex,self.currentRotatey
        vRotation = horiz.addition(vertic)
        vRotation = self.cam.norm.ProduitVectoriel(vRotation)
#         vRotation = vRotation.ProduitVectoriel(self.cam.norm)
        self.cam.norm = self.cam.norm.rotate(vRotation,vRotation.module()/8.0).normalize()
        self.cam.horiz = self.cam.horiz.rotate(vRotation,vRotation.module()/8.0).normalize()
        self.cam.vert = self.cam.vert.rotate(vRotation,vRotation.module()/8.0).normalize()
        self.cam.horiz = self.cam.vert.ProduitVectoriel(self.cam.norm).normalize()
        self.cam.vert = self.cam.norm.ProduitVectoriel(self.cam.horiz).normalize()
        self.cam.setRotationMatrix()
        self.stateMachine.rotate()
        self.refresh(event)
    def translate(self,event):
        self.currenttranslatex,self.currenttranslatey = event.x,event.y
        currentpos = self.cam.view2Model(Point2D([self.currenttranslatex,
                                                  self.currenttranslatey]),
                                         pos=self.initialpos)
#         print ("current pos",currentpos)
        self.cam.setCamPos(Point3D([currentpos.x,currentpos.y,currentpos.z]) )
        self.refresh(event)
#         self.cam.setScaleAndOffset(scale=None,offsetx=x,offsety=y)
    def middleclick(self,event):
        print ("middle click")
        self.lastRotatex,self.lastRotatey = event.x,event.y
        self.middlepressed = True
#         print("middleclick",event)
    def middleclickrelease(self,event):
        self.middlepressed = False
    def rightclick(self,event):
        self.stateMachine.reiinit()
        self.refresh(None)
#         self.drawLine(self.stateMachine.lineStart,self.stateMachine.previousPos,wx.Pen(wx.BLACK, 4))
#         self.drawLine(self.stateMachine.lineStart,self.stateMachine.currentPos,wx.Pen(wx.BLACK, 4))
#         self.drawLine(self.stateMachine.lineStart, Point2D([event.x,event.y]),self.bgcolor)
#         self.stateMachine.rightClick(event)
    def mouseWheel(self,event):
        signe = event.GetWheelRotation()
        if signe > 0 :
            self.pluszoom(event)
        else :
            self.minuszoom(event)
    def fit2Win(self):
        [maxx,maxy,maxz,minx,miny,minz]=self.model.getMaxs()
        pmin = Point3D([minx,miny,minz])
        pmax = Point3D([maxx,maxy,maxz])
        pmin2d = self.cam.model2View(pmin)
        pmax2d =self.cam.model2View(pmax)
        scale = max(abs(pmax2d.x - pmin2d.x )/ self.size[0],abs(pmax2d.y- pmin2d.y)/self.size[1])
        offsetx=(pmax2d.x + pmin2d.x )/2.-self.size[0]/2.
        offsety =(pmax2d.y+pmin2d.y/2.)-self.size[1]/2.
        self.cam.setScaleAndOffset(scale=0.5/scale*self.cam.scale,offsetx=int(self.cam.offsetx-offsetx),offsety=int(self.cam.offsety-offsety))
        self.cam.setRotationMatrix()
        self.stateMachine.rotate()
        self.refresh()
#         print([maxx,maxy,maxz,minx,miny,minz])
    def pluszoom(self,event):
        x,y = event.x,event.y
#         self.cam.scale *=1.1
        self.cam.setScaleAndOffset(scale=self.cam.scale*1.1)#,offsetx=x,offsety=y)
        self.cam.setRotationMatrix()
        self.stateMachine.rotate()
        self.refresh(event)
    def minuszoom(self,event):
        x,y = event.x,event.y
#         self.cam.scale /=1.1
        self.cam.setScaleAndOffset(scale=self.cam.scale/1.1)#,offsetx=x,offsety=y)
        self.cam.setRotationMatrix()
        self.stateMachine.rotate()
        self.refresh(event)
    def deleteSelection(self,event):
        listindex = []
        for index in self.stateMachine.idSelectedList:
            listindex.append(index)
        self.model.delete(listindex)
        self.stateMachine.idSelectedList = []
        self.refresh(None)
    def undo(self,event):
        self.history.undo()
        self.refresh(None)
    def redo(self,event):
        self.history.do()
        self.refresh(None)
    def quit(self,event):
        print("CAD QUIT from window")
        print (event)
        self.root.Close(True)
    def setStateMachine(self,statem):
        dictStateMachines = {
                             StateMachineList.lineStateMachine : LineStateMachine,
                             StateMachineList.selectStateMachine : SelectStateMachine,
                             StateMachineList.parallelStateMachine : ParallelStateMachine,
                             StateMachineList.translateStateMachine : TranslateStateMachine,
                             StateMachineList.rotateStateMachine : RotateStateMachine,
                             StateMachineList.circleStateMachine : CircleStateMachine,
                             }
        stateMachineclass = dictStateMachines.get(statem,LineStateMachine)
        self.stateMachine.exit()
        self.stateMachine = stateMachineclass(self)
        self.stateMachine.setActive()




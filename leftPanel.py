import wx
from Camera import Camera
from Utils import StateMachineList
from geometry import Vecteur


class ListAddArcViewComboPopup(wx.ComboPopup):
    def __init__(self,pnl,root):
        wx.ComboPopup.__init__(self)
        self.lc = None
        self.pnl = pnl
    def Init(self):
        self.value = -1
        self.curitem = -1
    def Create(self, parent):
        self.lc = wx.ListCtrl(parent,style=wx.LC_LIST | wx.LC_SINGLE_SEL | wx.SIMPLE_BORDER)
        self.lc.Bind(wx.EVT_LIST_ITEM_SELECTED,self.onSelectAction)
#         self.lc.InsertColumn(0, '', width=90)
        return True
    def GetStringValue(self):
        if self.value >= 0:
            return self.lc.GetItemText(self.value)
        return ""
    def SetStringValue(self, val):
        idx = self.lc.FindItem(-1, val)
        if idx != wx.NOT_FOUND:
            self.lc.Select(idx)
    def GetControl(self):
        return self.lc
    def AddItem(self, txt):
        self.lc.InsertItem(self.lc.GetItemCount(), txt)

    def onSelectAction(self,event):
        actionIndex = event.Index
        self.value = actionIndex
        dictActions = {0:self.AddCircleCamPlane,#"text":_("Add Circle (cam plane)")},
                       1:self.AddArcCamPlane,#"text":_("Add Arc (cam plane)")},
                       2:self.AddEllipticArc,#"text":_("Add 3d Elliptic Arc")}
                          }
        action = dictActions.get(actionIndex)#.get("func")
#         text =  dictActions.get(actionIndex).get("text")
        text = self.lc.GetItemText(actionIndex)
        action()
        self.Dismiss()
        self.pnl.leftPanel.ArcComboCtrl.SetValue(text)
    def AddCircleCamPlane(self):
        self.pnl.cadWindow.setStateMachine(StateMachineList.circleStateMachine)
    def AddArcCamPlane(self):
        return
        self.pnl.cadWindow.setStateMachine(StateMachineList.parallelStateMachine)
    def AddEllipticArc(self):
        return



class ListAddLineViewComboPopup(wx.ComboPopup):
    def __init__(self,pnl,root):
        wx.ComboPopup.__init__(self)
        self.lc = None
        self.pnl = pnl
    def Init(self):
        self.value = -1
        self.curitem = -1
    def Create(self, parent):
        self.lc = wx.ListCtrl(parent,style=wx.LC_LIST | wx.LC_SINGLE_SEL | wx.SIMPLE_BORDER)
        self.lc.Bind(wx.EVT_LIST_ITEM_SELECTED,self.onSelectAction)
#         self.lc.InsertColumn(0, '', width=90)
        return True
    def GetStringValue(self):
        if self.value >= 0:
            return self.lc.GetItemText(self.value)
        return ""
    def SetStringValue(self, val):
        idx = self.lc.FindItem(-1, val)
        if idx != wx.NOT_FOUND:
            self.lc.Select(idx)
    def GetControl(self):
        return self.lc
    def AddItem(self, txt):
        self.lc.InsertItem(self.lc.GetItemCount(), txt)
    def onSelectAction(self,event):
        actionIndex = event.Index
        self.value = actionIndex
        dictActions = {0:self.Add3dLine,#"text":_("Add 3d Line")},
                       1:self.AddParalel,#"text":_("Add parallel(cam plane)")}
                          }
        action = dictActions.get(actionIndex)#.get("func")
#         text =  dictActions.get(actionIndex).get("text")
        text = self.lc.GetItemText(actionIndex)
        action()
        self.Dismiss()
        self.pnl.leftPanel.lineComboCtrl.SetValue(text)
    def Add3dLine(self):
        self.pnl.cadWindow.setStateMachine(StateMachineList.lineStateMachine)
    def AddParalel(self):
        self.pnl.cadWindow.setStateMachine(StateMachineList.parallelStateMachine)
class LeftPanel():
    def __init__(self,pnl,root):
        self.pnl = pnl
        self.root = root
        self.cam = Camera()
        self.buttonsSizer = wx.BoxSizer(wx.VERTICAL)
        self.depthlabel = wx.StaticText(pnl, label=_("Working cam depth"),size=(140,-1))
        self.depthcontrol = wx.TextCtrl(pnl, value="",size=(140,-1),style=wx.TE_PROCESS_ENTER)#,style=wx.TE_MULTILINE)#|wx.TE_PROCESS_ENTER)
        self.lineComboCtrl = wx.ComboCtrl(pnl,value= _("Add Line"),style =wx.TE_READONLY)
        self.popupAddLineCtrl = ListAddLineViewComboPopup(pnl,root)
        self.lineComboCtrl.SetPopupControl(self.popupAddLineCtrl)
        self.popupAddLineCtrl.AddItem(_("Add 3d line"))
        self.popupAddLineCtrl.AddItem(_("Add parallel(cam plane)"))
        
        self.ArcComboCtrl = wx.ComboCtrl(pnl,value= _("Add Arc"),style =wx.TE_READONLY)
        self.popupAddArcCtrl = ListAddArcViewComboPopup(pnl,root)
        self.ArcComboCtrl.SetPopupControl(self.popupAddArcCtrl)
        self.popupAddArcCtrl.AddItem(_("Add Circle (cam plane)"))
        self.popupAddArcCtrl.AddItem(_("Add Arc (cam plane)"))
        self.popupAddArcCtrl.AddItem(_("Add 3d Elliptic Arc"))
        
        self.buttonTranslate = wx.Button(pnl,label=_("Translate selected"),size=(-1,-1))
        self.buttonRotate = wx.Button(pnl,label=_("Rotate selected"),size=(-1,-1))
        self.buttonsSizer.Add(self.depthlabel, 0, wx.EXPAND)
        self.buttonsSizer.Add(self.depthcontrol, 0, wx.EXPAND)
        self.buttonsSizer.Add(self.lineComboCtrl,0,wx.EXPAND)
        self.buttonsSizer.Add(self.ArcComboCtrl,0,wx.EXPAND)
        self.buttonsSizer.Add(self.buttonTranslate,0,wx.EXPAND)
        self.buttonsSizer.Add(self.buttonRotate,0,wx.EXPAND)
        self.depthcontrol.Bind(wx.EVT_TEXT_ENTER, self.onTextEnter,self.depthcontrol)
        self.buttonTranslate.Bind(wx.EVT_BUTTON,self.onTranslateSelection)
        self.buttonRotate.Bind(wx.EVT_BUTTON,self.onRotateSelection)
#         self.buttonDrawline.Bind(wx.EVT_BUTTON,self.onDrawline,self.buttonDrawline)
#         self.SetSizerAndFit(self.buttonsSizer)

#     def OnClick(self,event):
#         event.Skip()
    
    def onTextEnter(self,event):
        depth = event.GetString()
        try :
            self.cam.setDepth(float(depth))
        except :
            pass
        self.pnl.cadWindow.SetFocus()

    def onRotateSelection(self,event):
        self.selectionList = self.pnl.cadWindow.stateMachine.idSelectedList
        if len(self.selectionList)>0:
            self.pnl.cadWindow.setStateMachine(StateMachineList.rotateStateMachine)
    def onTranslateSelection(self,event):
        self.selectionList = self.pnl.cadWindow.stateMachine.idSelectedList
        if len(self.selectionList)>0:
            self.pnl.cadWindow.setStateMachine(StateMachineList.translateStateMachine)
    def notifyTranslate(self,translation):
        self.dialog = wx.Dialog(self.root,title=_("Translate"))
        dialog = self.dialog
        Sizer = wx.BoxSizer(wx.VERTICAL)
        self.nbRepeatST = wx.StaticText(dialog,label=_("nb repeat inc original"),size = (140,-1))
        nbrepeatTC = wx.TextCtrl(dialog, value="1",size=(140,-1))
        self.keepST = wx.StaticText(dialog,label=_("keep original"),size = (140,-1))
        keepCB = wx.CheckBox(dialog)
        buttonSizer = dialog.CreateStdDialogButtonSizer(flags = wx.OK| wx.CANCEL)
        dialog.CreateSeparatedSizer(buttonSizer)
        Sizer.Add(self.nbRepeatST, 0,wx.EXPAND)
        Sizer.Add(nbrepeatTC, 0,wx.EXPAND)
        Sizer.Add(self.keepST, 0,wx.EXPAND)
        Sizer.Add(keepCB, 0,wx.EXPAND)
        Sizer.Add(buttonSizer,0,wx.EXPAND)
        dialog.SetSizer(Sizer)
        if dialog.ShowModal() == wx.ID_OK:
            try :
                nbrepeat =int(nbrepeatTC.GetLineText(0))
                keep = keepCB.GetValue()
                self.pnl.cadWindow.model.TranslateSelection(self.selectionList,translation,keep,nbrepeat)
                self.pnl.cadWindow.refresh()
            except :
                pass

    def notifyRotate(self,center):
        print("ROTATE")
        self.dialog = wx.Dialog(self.root,title=_("Rotate"))
        dialog = self.dialog
        Sizer = wx.BoxSizer(wx.VERTICAL)
        self.nbRepeatST = wx.StaticText(dialog,label=_("nb repeat inc original"),size = (140,-1))
        nbrepeatTC = wx.TextCtrl(dialog, value="1",size=(140,-1))
        self.keepST = wx.StaticText(dialog,label=_("keep original"),size = (140,-1))
        keepCB = wx.CheckBox(dialog)
        self.vectorST = wx.StaticText(dialog,label=_("Vector 'x','y','z' or x,y,z coordinates"),size = (140,-1))
        rotationvector = wx.TextCtrl(dialog,value="",size=(140,-1))
        self.angleST = wx.StaticText(dialog,label=_("angle (degrees)"),size = (140,-1))
        angle = wx.TextCtrl(dialog,value="",size=(140,-1))
        buttonSizer = dialog.CreateStdDialogButtonSizer(flags = wx.OK| wx.CANCEL)
        dialog.CreateSeparatedSizer(buttonSizer)
        Sizer.Add(self.nbRepeatST, 0,wx.EXPAND)
        Sizer.Add(nbrepeatTC, 0,wx.EXPAND)
        Sizer.Add(self.keepST, 0,wx.EXPAND)
        Sizer.Add(keepCB, 0,wx.EXPAND)
        Sizer.Add(self.vectorST,0,wx.EXPAND)
        Sizer.Add(rotationvector,0,wx.EXPAND)
        Sizer.Add(self.angleST,0,wx.EXPAND)
        Sizer.Add(angle,0,wx.EXPAND)
        Sizer.Add(buttonSizer,0,wx.EXPAND)
        dialog.SetSizer(Sizer)
        if dialog.ShowModal() == wx.ID_OK:
            try :
                nbrepeat =int(nbrepeatTC.GetLineText(0))
                keep = keepCB.GetValue()
                vector = rotationvector.GetLineText(0)
                if vector=="x":
                    x,y,z = 1.,0.,0.
                elif vector == "y":
                    x,y,z = 0.,1.,0.
                elif vector =="z":
                    x,y,z = 0.,0.,1.
                else :
                    x,y,z = map(float,vector.split(","))
                print ("xyz",x,y,z)
                alpha = float(angle.GetLineText(0))
                self.pnl.cadWindow.model.RotateSelection(self.selectionList,
                                                         keep,
                                                         nbrepeat,
                                                         center,
                                                         Vecteur([x,y,z]),
                                                         alpha
                                                         )
                self.pnl.cadWindow.refresh()
            except :
                pass




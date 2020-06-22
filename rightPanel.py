import wx
from geometry import Point3D,Line3D
from model import Model
from Utils import __builtin__

class RightPanel():
    def __init__(self,pnl,root):
        self.point1 = None
        self.point2 = None
        self.root = root
        self.pnl = pnl
        self.cadWindow = self.pnl.cadWindow
        self.model = Model()
        self.colordata = self.model.layers.getActiveLayer().color
        self.layersKlass = self.pnl.cadWindow.model.layers
        self.rightsizer = wx.BoxSizer(wx.VERTICAL)
        self.cmdlinelabel = wx.StaticText(self.pnl,
#                                            label=_("Enter First Point"),
                                           label ="",
                                           size=(140,-1))
        self.cmdlinecontrol = wx.TextCtrl(self.pnl, value="",size=(140,-1),style=wx.TE_PROCESS_ENTER)#,style=wx.TE_MULTILINE)#|wx.TE_PROCESS_ENTER)
        self.layerSizer = wx.BoxSizer(wx.VERTICAL)
        self.layerButtonSizer=wx.BoxSizer(wx.HORIZONTAL)
        self.addLayerButton = wx.Button(self.pnl,label=_("Add Layer"),size=(-1,-1))
        self.delLayerButton = wx.Button(self.pnl,label=_("Del Layer"),size=(-1,-1))
        self.AllvisibleLayerButton = wx.Button(self.pnl,label=_("Show All"),size=(-1,-1))
        self.AllInvisbleLayerButton = wx.Button(self.pnl,label=_("Hide All"),size=(-1,-1))
        self.layerButtonSizer.Add(self.AllvisibleLayerButton,1,wx.EXPAND)
        self.layerButtonSizer.Add(self.AllInvisbleLayerButton,1,wx.EXPAND)
        self.layerButtonSizer.Add(self.addLayerButton,1,wx.EXPAND)
        self.layerButtonSizer.Add(self.delLayerButton,1,wx.EXPAND)
        self.layerlistCtrl = wx.ListCtrl(self.pnl,
                         style=wx.LC_REPORT
                        | wx.BORDER_SUNKEN
#                          | wx.BORDER_NONE
#                          | wx.LC_EDIT_LABELS
                         #| wx.LC_SORT_ASCENDING    # disabling initial auto sort gives a
                         #| wx.LC_NO_HEADER         # better illustration of col-click sorting
                         #| wx.LC_VRULES
                         #| wx.LC_HRULES
                         #| wx.LC_SINGLE_SEL
                         )
        self.layerPopulate()
        self.layerSizer.Add(self.layerButtonSizer,0,wx.EXPAND)
        self.layerSizer.Add(self.layerlistCtrl,1,wx.EXPAND)
        self.rightsizer.Add(self.cmdlinelabel, 0, wx.EXPAND)
        self.rightsizer.Add(self.cmdlinecontrol, 0, wx.EXPAND)
        self.rightsizer.Add(self.layerSizer, 1, wx.EXPAND)
#         self.rightsizer.SetMinSize(140,-1)

        self.cmdlinecontrol.Bind(wx.EVT_TEXT_ENTER, self.onTextEnter,self.cmdlinecontrol)
        self.addLayerButton.Bind(wx.EVT_BUTTON,self.onAddLayer,self.addLayerButton)
        self.AllvisibleLayerButton.Bind(wx.EVT_BUTTON,self.onAllVisible,self.AllvisibleLayerButton)
        self.AllInvisbleLayerButton.Bind(wx.EVT_BUTTON,self.onMaskAll,self.AllInvisbleLayerButton)
        self.pnl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.layerlistCtrl)
        self.pnl.Bind(wx.EVT_LIST_ITEM_CHECKED,self.onCheckUncheckItem,self.layerlistCtrl)
        self.pnl.Bind(wx.EVT_LIST_ITEM_UNCHECKED,self.onCheckUncheckItem,self.layerlistCtrl)
        self.pnl.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.onDblClick,self.layerlistCtrl)
#         self.pnl.Bind(wx.EVT_CHAR,self.onChar)
        self.cadWindow.SetFocus()
#         self.cmdlinecontrol.Bind(wx.EVT_CHAR, self.onChar,self.cmdlinecontrol)

    def OnItemSelected(self,event):
        print("selected")
        activeLayerId = event.GetData()
        self.layersKlass.setActiveLayerId(activeLayerId)
#         print(event.GetItem().GetTextColour())
#         self.currentItem = event.Index
#         print(event.GetData())
#         print (event.Index,self.currentItem)
    def onCheckUncheckItem(self,event):
#         item = event.GetItem()
        item =event.Index
        visible = self.layerlistCtrl.IsItemChecked(item)
        LayerId=self.layerlistCtrl.GetItemData(item)
        self.cadWindow.model.layers.setVisibility(LayerId,visible)
        self.cadWindow.refresh(None)



    def onTextEnter(self,event):
        command = event.GetString()
        coords =command.split(",")
        self.pnl.cadWindow.stateMachine.notifyAddCmd(command)
#         try :
#             coord = map(float,coords)
#             self.point = Point3D(coord)
# #             self.pnl.cadWindow.stateMachine.notifyAdd3dPoint(self.point)
#         except :
#             pass
        self.cmdlinecontrol.Clear()
#         self.pnl.cadWindow.SetFocus()
    def onDblClick(self,event):
        print ("activate")
        activeLayerId = event.GetData()
        self.layersKlass.setActiveLayerId(activeLayerId)
        layer = self.layersKlass.getActiveLayer()
        layercolor = layer.color
        self.colordata = self.model.layers.getActiveLayer().color
        self.EditAdd(layer)
    def onAddLayer(self,event):
        self.EditAdd(None)
    def EditAdd(self,layer=None):
        if layer is not None :
            name = str(layer.name)
            width =str(layer.width)
        else :
            name = width =""
        self.dialog = wx.Dialog(self.root,title=_("Add Layer"))
        dialog = self.dialog
        nameSizer = wx.BoxSizer(wx.HORIZONTAL)
#         visibleSizer = wx.BoxSizer(wx.HORIZONTAL)
        colorSizer = wx.BoxSizer(wx.HORIZONTAL)
        widthSizer = wx.BoxSizer(wx.HORIZONTAL)
        layerSizer = wx.BoxSizer(wx.VERTICAL)
        nameST = wx.StaticText(dialog, label=_("name"),size=(140,-1))
#         visibleST = wx.StaticText(dialog, label="visible",size=(140,-1))
        colorST = wx.StaticText(dialog, label=_("color"),size=(140,-1))
        widthST = wx.StaticText(dialog, label=_("width"),size=(140,-1))
        nameTC = wx.TextCtrl(dialog, value=name,size=(140,-1))
#         visibleTC = wx.TextCtrl(dialog, value="",size=(140,-1))
#         colorTC = wx.TextCtrl(dialog, value="",size=(140,-1))
        bitmapColor = wx.Bitmap(width=10,height=10)
        (red,green,blue) = self.colordata.Get( includeAlpha=False)
        bitmapColor=bitmapColor.FromRGBA(10, 10, red=red, green=green, blue=blue, alpha=255)
        colorBtn = wx.BitmapButton(dialog,id=wx.ID_ANY,bitmap=bitmapColor,size=(-1,-1))
        self.colorBtn = colorBtn
        widthTC = wx.TextCtrl(dialog, value=width,size=(140,-1))
        nameSizer.Add(nameST,0,wx.EXPAND)
        nameSizer.Add(nameTC,0,wx.EXPAND)
#         visibleSizer.Add(visibleST,0,wx.EXPAND)
#         visibleSizer.Add(visibleTC,0,wx.EXPAND)
        colorSizer.Add(colorST,0,wx.EXPAND)
        colorSizer.Add(colorBtn,0,wx.EXPAND)
        widthSizer.Add(widthST,0,wx.EXPAND)
        widthSizer.Add(widthTC,0,wx.EXPAND)
        layerSizer.Add(nameSizer,0,wx.EXPAND)
#         layerSizer.Add(visibleSizer,0,wx.EXPAND)
        layerSizer.Add(colorSizer,0,wx.EXPAND)
        layerSizer.Add(widthSizer,0,wx.EXPAND)
        buttonSizer = dialog.CreateStdDialogButtonSizer(flags = wx.OK| wx.CANCEL)
        dialog.CreateSeparatedSizer(buttonSizer)
        layerSizer.Add(buttonSizer,0,wx.EXPAND)
        dialog.SetSizer(layerSizer)
        dialog.Bind(wx.EVT_BUTTON, self.colorPicker, colorBtn)
        if dialog.ShowModal() == wx.ID_OK:
            color = self.colordata
            visible = True
            width =widthTC.GetLineText(0)
            name = nameTC.GetLineText(0)
            if layer is None :
                self.cadWindow.model.layers.addLayer(name,color,width)
            else :
                lid = self.layersKlass.getActiveLayerId()
                self.layersKlass.setColor(lid,color)
                self.layersKlass.setWidth(lid,width)
                self.layersKlass.setName(lid,name)
            self.layerPopulate()
            activeLayerId = self.cadWindow.model.layers.getActiveLayerId()
            index = self.getItemByLayerId(activeLayerId)
            self.layerlistCtrl.Select(index)
            self.layerlistCtrl.CheckItem(index,True)

    def colorPicker(self,event):
        colorPicker = wx.ColourDialog(self.root)
        if colorPicker.ShowModal() == wx.ID_OK:
            colordata = colorPicker.GetColourData().GetColour()
            self.colordata = colordata
            bitmapColor = wx.Bitmap(width=10,height=10)
            (red,green,blue) = self.colordata.Get( includeAlpha=False)
            bitmapColor=bitmapColor.FromRGBA(10, 10, red=red, green=green, blue=blue, alpha=255)
            self.colorBtn.Bitmap = bitmapColor
    def onAllVisible(self,event):
        self.setAllVisibility(True)

    def onMaskAll(self,event):
        self.setAllVisibility(False)

    def setAllVisibility(self,visible):
        for item in range (self.layerlistCtrl.GetItemCount()):
            LayerId=self.layerlistCtrl.GetItemData(item)
            self.layerlistCtrl.CheckItem(item,visible)
#             self.cadWindow.model.layers.setVisibility(LayerId,visible)
        self.cadWindow.refresh(None)
    def setCommandLabel(self,value):
        self.cmdlinelabel.SetLabel(value)

    def layerPopulate(self):
        self.layerlistCtrl.ClearAll()
        self.layerlistCtrl.AppendColumn(_("visible"))
        self.layerlistCtrl.AppendColumn(_("color"))
        self.layerlistCtrl.AppendColumn(_("name"))
        self.layerlistCtrl.AppendColumn(_("width"))
        self.layerlistCtrl.EnableCheckBoxes(enable=True)
        self.layers = self.layersKlass.layers
        self.ImageList = wx.ImageList(16,16)#,initialCount = 0)#mask=False,initialCount = 0)
        for layerid,layer in self.layers.items() :
            name = layer.name
            visible = layer.visible
            color = layer.color
            key = layerid
            width = layer.width
            dummy =""
            line = self.layerlistCtrl.Append(list(map(str,[dummy,color,name,width])))
            self.layerlistCtrl.SetItemData(line, layerid) 
            self.layerlistCtrl.CheckItem(line,visible)
            (red,green,blue) = color.Get( includeAlpha=False)
            bmpcolor = wx.Bitmap(16,16)
            bmpcolor = bmpcolor.FromRGBA(16,16,red=red, green=green, blue=blue, alpha=255)
            self.idxcpmpr = self.ImageList.Add(bmpcolor)
        self.layerlistCtrl.SetImageList(self.ImageList, wx.IMAGE_LIST_SMALL)
        for index in range(self.layerlistCtrl.GetItemCount()):
            self.layerlistCtrl.SetItem(index,1,"",index)

    def getItemByLayerId(self,LayerId):
        foundIndex = None
        for index in range(self.layerlistCtrl.GetItemCount()):
            data=self.layerlistCtrl.GetItemData(index)
            if data == LayerId:
                foundIndex = index
        return foundIndex




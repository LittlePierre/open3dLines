import wx
class LowerPanel():
    def __init__(self,pnl,root):
        self.pnl = pnl
        self.magnetismKlass = self.pnl.cadWindow.model.magnetism
        self.lowerSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.magnetismTxt = wx.StaticText(self.pnl,label=_("Magnetism"))
#         self.magnetismNoneChkBx =  wx.CheckBox(self.pnl,label=_("None"))
        self.magnetismEndChkBx =  wx.CheckBox(self.pnl,label=_("End"))#wx.Button(self.pnl,label=_("Edge"),size=(-1,-1))
        self.magnetismCenterChkBx = wx.CheckBox(self.pnl,label=_("Center")) #wx.Button(self.pnl,label=_("Middle"),size=(-1,-1))
        self.lowerSizer.Add(self.magnetismTxt, 0,wx.EXPAND)
#         self.lowerSizer.Add(self.magnetismNoneChkBx, 0,wx.EXPAND)
        self.lowerSizer.Add(self.magnetismEndChkBx, 0,wx.EXPAND)
        self.lowerSizer.Add(self.magnetismCenterChkBx, 0,wx.EXPAND)

        self.magnetismEndChkBx.Bind(wx.EVT_CHECKBOX,self.onChk)
        self.magnetismCenterChkBx.Bind(wx.EVT_CHECKBOX,self.onChk)
    def onChk(self,event):
        centerFlag = self.magnetismKlass.flagCenter * self.magnetismCenterChkBx.IsChecked()
        endFlag = self.magnetismKlass.flagEnd * self.magnetismEndChkBx.IsChecked()
        flags = centerFlag | endFlag
        self.magnetismKlass.setFlags(flags)
        

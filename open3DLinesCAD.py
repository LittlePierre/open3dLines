import wx
from cadwindow import CADWindow
from rightPanel import RightPanel
from leftPanel import LeftPanel
from lowerPanel import LowerPanel
from STLImporter import stlImporter


class Panel(wx.Panel):
    def __init__(self, root):
        wx.Panel.__init__(self, root)#, style=wx.WANTS_CHARS)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.middleSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.cadWindow = CADWindow(self,root)
        self.cadWindow.SetFocus()
        self.leftPanel = LeftPanel(self,root)
        self.rightPanel = RightPanel(self,root)
        self.middleSizer.Add(self.leftPanel.buttonsSizer, 1, wx.EXPAND)
        self.middleSizer.Add(self.cadWindow, 4, wx.EXPAND)
        self.middleSizer.Add(self.rightPanel.rightsizer, 1, wx.EXPAND)

        self.lowerPanel = LowerPanel(self,root)
        self.mainSizer.Add(self.middleSizer, 1, wx.EXPAND)
        self.mainSizer.Add(self.lowerPanel.lowerSizer,0,wx.EXPAND)
        self.SetSizerAndFit(self.mainSizer)

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title,size=(-1,-1))#, size=(self.windowx,self.windowy))
        size = wx.GetDisplaySize()
        self.SetMinSize((800,400))
        self.CreateStatusBar()
        # Setting up the menu.
        filemenu= wx.Menu()
#         menuOpen = filemenu.Append(wx.ID_OPEN, "&Open"," Open a file to edit")
#         menuAbout= filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")
        importStl = filemenu.Append(wx.ID_ANY,_("Import stl"))
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
        self.panel = Panel(self)
        self.setFocus()
        self.Show(True)
        self.Maximize(True)
#         self.ShowFullScreen(True)
        self.Bind(wx.EVT_MENU, self.quit, menuExit)
        self.Bind(wx.EVT_MENU,self.importSTL,importStl)
    def setFocus(self):
        self.panel.cadWindow.SetFocus()

    def quit(self,event):
        print (event)
        print("mainquit")
        self.Close(True)

    def importSTL(self,event):
        dialog = wx.FileDialog(None,
                               message="Import STL",
                               wildcard="STL files (*.stl)|*.stl",
                               style = wx.FD_OPEN)
        if dialog.ShowModal() == wx.ID_CANCEL:
            return
        pathname = dialog.GetPath()
#         import time
#         t0 =time.time()
        stl = stlImporter(pathname)
#         t1 = time.time()
        self.panel.cadWindow.model.addStl(stl)
#         t2 = time.time()
        self.panel.cadWindow.refresh(None)
#         t3 = time.time()
#         print (t3-t2)


if __name__ == "__main__":
        app = wx.App(False)
        gui = MainWindow(None, "test")
#         import wx.lib.inspection
#         wx.lib.inspection.InspectionTool().Show()
        app.MainLoop()



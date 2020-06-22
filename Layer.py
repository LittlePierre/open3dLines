import wx
class Layer():
    def __init__(self,name,color,width,visible=True):
        self.name = name
        self.color = color
        self.width = width
        self.visible = visible


class Layers():
    def __init__(self):
        self.layers = {}
        self.layerId =0
        self.activeLayerId = 0
        self.addLayer("defaultLayer", wx.Colour(255,0,0), 1)
    def addLayer(self,name,color,width=1):
        try :
            self.layers[self.layerId] =Layer(str(name),color,int(width))
            self.setActiveLayerId(self.layerId)
            self.layerId +=1
        except Exception as e:
            pass
    def delLayer(self,layerId):
        self.layers.pop(layerId)
    def setVisibility(self,LayerId,visible=True):
        layer = self.layers.get(LayerId)
        layer.visible = visible
    def setName(self,LayerId,name):
        try :
            layer = self.layers.get(LayerId)
            layer.name = str(name)
        except :
            pass
    def setWidth(self,LayerId,width):
        try :
            layer = self.layers.get(LayerId)
            layer.width = int(width)
        except :
            pass
    def setColor(self,LayerId,color):
        layer = self.layers.get(LayerId)
        layer.color = color
    def setActiveLayerId(self,layerId):
        self.activeLayerId = layerId
    def getActiveLayerId(self):
        return self.activeLayerId
    def getActiveLayer(self):
        return self.layers.get(self.activeLayerId)

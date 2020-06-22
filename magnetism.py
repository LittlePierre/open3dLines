class Magnetism():
    flagEnd = 1
    flagCenter =2
    def __init__(self,model):
        self.model = model
        self.flags = 0#Magnetism.flagEnd | Magnetism.flagCenter

    def setFlags(self,flags):
        self.flags = flags

    def getMagneticPoint(self,x,y,flags = None):
        if flags is None :
            flags = self.flags
        if flags == 0 :
            return self.getNearestNoMag(x, y)
        if flags & Magnetism.flagEnd :
            nearer = self.getNearestEnd(x, y)
        else :
            nearer = None
        if flags & Magnetism.flagCenter :
            nearer = self.nearer(nearer,self.getNearestCenter(x,y),x,y)
        if nearer is not None:
            return nearer
        else : 
            return self.getNearestNoMag(x, y)
    
    def getNearestEnd(self,x,y):
        return self.model.getNearestEnd(x,y)
    def getNearestCenter(self,x,y):
        return self.model.getNearestCenter(x,y)
    def getNearestNoMag(self,x,y):
        return self.model.getNearestNoMag(x,y)
    def nearer(self,item1,item2,x,y):
        if item1 is None :
            return item2
        if item2 is None :
            return item1
        p1_2d = item1[1]
        p2_2d = item2[1]
        if p1_2d.dist(x,y)<p2_2d.dist(x,y):
            return item1
        else :
            return item2
        


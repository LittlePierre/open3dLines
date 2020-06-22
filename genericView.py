class GenericView():
    def __init__(self,window):
        [self.windowx,self.windowy] = window
        self.maxx=self.maxy = -float("inf")
        self.minx=self.miny= float("inf")
        self.scale = 1
        self.minx = 0
        self.miny =0
    def checkminmax(self,p):
        if p.x > self.maxx : 
            self.maxx = p.x
        if p.y > self.maxy :
            self.maxy = p.y
        if p.x < self.minx :
            self.minx =p.x
        if p.y < self.miny :
            self.miny = p.y
    def fitToWindow(self,listLines):
        for line in listLines :
            [p1,p2] = line
            self.checkminmax(p1)
            self.checkminmax(p2)
        deltax = self.maxx - self.minx
        deltay = self.maxy - self.miny
        scalex = self.windowx /deltax
        scaley = self.windowy /deltay
        self.scale = min(scalex,scaley)
    def drawAllLines(self,listLines):
        for line in listLines :
            [p1,p2] = line
            p1=p1.translate([-self.minx,-self.miny]).scale([self.scale,-self.scale]).translate([0,self.windowy])
            p2=p2.translate([-self.minx,-self.miny]).scale([self.scale,-self.scale]).translate([0,self.windowy])
            self.drawLine(p1,p2)
    def draw3d(self,triangles):
        sortedTriangles =sorted(triangles,key=lambda triangle : triangle.dist,reverse = True)
        for triangle in sortedTriangles :
            p1= triangle.points2D[0]
            p2 = triangle.points2D[1]
            p3 = triangle.points2D[2]
            p1=p1.translate([-self.minx,-self.miny]).scale([self.scale,-self.scale]).translate([0,self.windowy])
            p2=p2.translate([-self.minx,-self.miny]).scale([self.scale,-self.scale]).translate([0,self.windowy])
            p3=p3.translate([-self.minx,-self.miny]).scale([self.scale,-self.scale]).translate([0,self.windowy])
            self.plot3D(p1,p2,p3)

    def drawSlices(self,listSlices):
        currentcolor = 0
        for slice in listSlices :
            currentcolor+=1
            if currentcolor >2 :
                currentcolor = 0 
            polygon = []
            for point2d in slice.polygon :
                point2d=point2d.translate([-self.minx,-self.miny]).scale([self.scale,-self.scale]).translate([0,self.windowy])
                polygon.append([point2d.x,point2d.y])
            self.drawCurrentSlice(polygon,currentcolor)

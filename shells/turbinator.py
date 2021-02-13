# Generate a turbinated shell (which is to say conical, not in a plane 
# like a planispiral shell). The Fuse method can be formed to be 
# conical but you working against the paper. The goal here is for a 
# natural 3d spiral, going all the way to scalariform (whorls not 
# touching each other). And of course, curved folds so the paper 
# creates a life-like shell.
#
# Similar to the fuse_shellgen, the parameters are:
# ca - central angle (the one with the midline through it)
# u = inital length of the normal
# N - number of iterations
# However, the spiraling angle is split into two
# saL - spiraling angle on the left
# saR - spiraling angle on the right
#
# Since the interior line lengths will be the same, the edges of 
# the paper will be different length. Instead of isosocele triangles,
# this method will make for unbalanced triangles. 
# 
# The geomtry for figuring out the lines was tough, mostly careful, 
# repeated use of the Law of Sines as well as other triangle rules. The 
# terminology I'm using for the code depends heavily on the diagram. 
# Look in the pics directory for a relevant diagram.
#

# sar < sal dextral
# sal < sar sinistral
# larger sa makes for a smaller protoconch, slower growth
# addAngle negative acts as a growth retardant so outer shell does not get too big, positive causes a faster growth (smaller protoconch)

# car + cal smaller means a larger protoconch and slower, smoother growth
#   making it larger makes for a smaller protoconch but chunkier whorls
# unbalanced ca gives height to the coil but unbalanced tails

from math import *
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import collections  as mc
from matplotlib.patches import Ellipse, Wedge, Polygon
from matplotlib.path import Path
import itertools

class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def lengthTo(self, p):
        x2 = (self.x-p.x)**2
        y2 = (self.y-p.y)**2
        len = sqrt(x2 + y2)
        return len

    def pts(self):
        return [self.x, self.y]
        
    def negative(self):
        return point(self.x, -self.y)
    
    def pointFrom(self, length, angle):
        x = self.x + length*sin(radians(angle))
        y = self.y + length*cos(radians(angle))
        return point(x, y)
        

class side:
    def __init__(self, pointA, pointB):
        self.pointA = pointA
        self.pointB = pointB
    def length(self):
        return self.pointA.lengthTo(self.pointB)

def add_plot(ax, pt1, pt2, curve_fun, color):
    ptb = curve_fun(pt1, pt2)
#    ax.plot(ptb.x, ptb.y, color+'x')
    bezier(ax, pt1, pt2, ptb, color)

    
def bezier(ax, pt1, pt2, ptb, color):
    npoints = 2
    numbers = [i for i in range(npoints)]
    bezier_path = np.arange(0.0, 1.01, 0.01)

    x1y1 = x1, y1 = pt1.x, pt1.y
    x2y2 = x2, y2 = pt2.x, pt2.y
    xbyb = xb, yb = ptb.x, ptb.y

    # Compute and store the Bezier curve points
    x = (1 - bezier_path)** 2 * x1 + 2 * (1 - bezier_path) * bezier_path * xb + bezier_path** 2 * x2
    y = (1 - bezier_path)** 2 * y1 + 2 * (1 - bezier_path) * bezier_path * yb + bezier_path** 2 * y2

    ax.plot(x, y, color)

def law_sines(length, ang_denom, ang_mult):
    val = length*sin(radians(ang_mult)) / sin(radians(ang_denom))
    return abs(val)

# use for straight line versions
def ptb_straightline(pt1, pt2):
    return pt1

def make_plot(prefix='tb', show_plot=True, 
            caR=15.0, caL=15.0, saL=12.0, saR=15.0, u=1.0, N=15, 
            curve_fun=ptb_straightline, kite=0, cutProtoconch = True, addAngle=0.0):
    
    figure, ax = plt.subplots()
    name = '{}_cal{}_car{}_sal{}_sar{}_N{}_add{}'.format(prefix, int(caL), int(caR), int(saL), int(saR), N, int(100*addAngle))

    # angles from known 
    angBR = 90 + (caR)
    angBL = 90 + (caL)
    angCL = 180 - angBL - saL
    angCR = 180 - angBR - saR

    # known length
    BL_BR = u    

    # initial protoconch triangle
    pointA = point(0,0)
    A_BL = law_sines(BL_BR, caL + caR, 90-caR)
    A_BR = law_sines(BL_BR, caL + caR, 90-caL)
    pointBR = pointA.pointFrom(A_BR, caR)
    pointBL = pointA.pointFrom(A_BL, -caL)

    if cutProtoconch:
        outerPolyVertices = [pointBR.pts(), pointBL.pts()]
    else:
        outerPolyVertices = [pointBR.pts(), pointA.pts(), pointBL.pts()]
    prevA = pointA

    for i in range(N + 1):
        angCL = 180 - angBL - saL   # recalculate as it depends on saL which can change
        angCR = 180 - angBR - saR   # recalculate as it depends on saR which can change

        # this is a magical incantation supported by the unholy art of geometry
        saSinRatio = sin(radians(saR)) / sin(radians(saL))
        numerator = BL_BR * sin(radians(angBL)) * sin(radians(angBR))
        denom_A =  saSinRatio * sin(radians(angCL)) * sin(radians(angBR))
        denom_B = sin(radians(angCR)) * sin(radians(angBL))
        A_CR =  numerator / (denom_A + denom_B)

        A_CL = law_sines(A_CR, saL, saR)
        A_BL = law_sines(A_CL, angBL, angCL)
        A_BR = law_sines(A_CR, angBR, angCR)

        pointA = pointBL.pointFrom(A_BL, 90.0)
        pointBR = pointA.pointFrom(A_BR, 90.0)
        pointCR = pointA.pointFrom(A_CR, 90-saR)
        pointCL = pointA.pointFrom(A_CL, -(90-saL))


        if i != N: # last pass is for the outer cut
        
            if curve_fun==ptb_straightline:
                add_plot(ax, pointBL, pointBR, color='r', 
                    curve_fun=curve_fun)
            else:
                add_plot(ax, pointA, pointBR, color='r', 
                    curve_fun=curve_fun)
                add_plot(ax, pointA, pointBL, color='r', 
                    curve_fun=curve_fun)

            add_plot(ax, pointA, pointCL, color='b', 
                curve_fun=curve_fun)
            add_plot(ax, pointA, pointCR, color='b', 
                curve_fun=curve_fun)
            
            if i == (N-kite):
                kiteBL = pointBL
                kiteBR = pointBR
            
            if cutProtoconch==False and i == 0:
                add_plot(ax, prevA, pointA, color='g', curve_fun=ptb_straightline)

            pointBL = pointCL
            pointBR = pointCR
            BL_BR = pointCL.lengthTo(pointCR)
            prevA = pointA

            saL += saL*addAngle
            saR += saR*addAngle
    
    if kite == 0:
        outerPolyVertices.extend([pointCL.pts(), pointCR.pts()]) 
    else:
        halfC = pointCL.lengthTo(pointCR)/2.0
        
        outerPolyVertices.extend([kiteBL.pts(), pointCL.pointFrom(halfC, 90).pts(),kiteBR.pts()]) 
        
    poly = Polygon(outerPolyVertices, facecolor='1.0', edgecolor='k', transform=ax.transData)
    #p = ax.add_patch(poly)
    
    path = Path(outerPolyVertices)
    ax.set_clip_path(path)
    ax.set_clip_on(True)
    
    add_plot(ax, pointA, pointCL, color='m', 
                curve_fun=curve_fun)
    #add_plot(ax, pointA, pointCR, color='m', 
 #           curve_fun=curve_fun)
    
    plt.axis('off')
    plt.box(False)
    
    ax.set_aspect(1), ax.autoscale()
    plt.savefig(name + ".svg")
    if show_plot: plt.title(name), plt.show()

# Use an x division less than two or the curves fight the angle of growth
def ptb_sumxdiv0975_avey(pt1, pt2):
    divisor = 2.0 * 0.975
    xb = (pt1.x+pt2.x)/divisor
    yb = (pt1.y+pt2.y)/divisor
    return point(xb, yb)

def ptb_sumxdiv095_avey(pt1, pt2):
    divisor = 2.0 * 0.95
    xb = (pt1.x+pt2.x)/divisor
    yb = (pt1.y+pt2.y)/divisor
    return point(xb, yb)
    
def ptb_sumxdiv090_avey(pt1, pt2):
    divisor = 2.0 * 0.90
    xb = (pt1.x+pt2.x)/divisor
    yb = (pt1.y+pt2.y)/divisor
    return point(xb, yb)


#import pdb; pdb.set_trace()
add = 0.0

# 25 25 17 15 20 0
name = 'tst_'

#all of these worked
make_plot(prefix=name+'975', caL =25, caR = 25, saL=17, saR=17, u=1.0, N=15,  curve_fun=ptb_sumxdiv0975_avey, addAngle=0, kite=1, cutProtoconch = False)
#make_plot(prefix=name+'95', caL =25, caR = 25, saL=17, saR=17, u=1.0, N=15,  curve_fun=ptb_sumxdiv095_avey, addAngle=0)
#make_plot(prefix=name, caL =25, caR = 25, saL=20, saR=20, u=1.0, N=20,  curve_fun=ptb_straightline, addAngle=0.0)
#make_plot(prefix=name+'975', caL =25, caR = 25, saL=12.5, saR=12.5, u=1.0, N=20,  curve_fun=ptb_sumxdiv095_avey, addAngle=0.0)
#make_plot(prefix=name+'975', caL =25, caR = 25, saL=10.0, saR=10.0, u=1.0, N=20,  curve_fun=ptb_sumxdiv095_avey, addAngle=0.0)

#make_plot(prefix='t5', caL=0.0, caR=30.0, saR=15.0, saL=15.0, u=1.0, N=12, curve_fun=ptb_straightline, addAngle=0)

# those grew too fast... 
#make_plot(prefix=name, caL =15, caR = 15, saL=20, saR=20, u=1.0, N=20,  curve_fun=ptb_straightline, addAngle=0.0)

#make_plot(prefix=name, caL =20, caR = 20, saL=20, saR=20, u=1.0, N=20,  curve_fun=ptb_straightline, addAngle=0.0)

#make_plot(prefix=name, caL =15, caR = 15, saL=15, saR=15, u=1.0, N=20,  curve_fun=ptb_straightline, addAngle=0.0)

#make_plot(prefix=name, caL =10, caR = 10, saL=25, saR=25, u=1.0, N=20,  curve_fun=ptb_straightline, addAngle=0.0)

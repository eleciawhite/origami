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

from math import *
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import collections  as mc
from matplotlib.patches import Ellipse, Wedge, Polygon
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

def make_plot(ax, ca, saL, saR, u=1.0, N=15, curve_fun=ptb_straightline, ratio=0.5, addAngle=0.0):

    # angles
    angBx = 90 + (ca/2.0)
    aveSa = (saL + saR) / 2.0
    angCL = 180 - angBx - saL
    angCR = 180 - angBx - saR
    angDL = 90 + aveSa - saL
    angDR = 90 + aveSa - saR

    # initial protoconch triangle
    saRatio = saR/aveSa
    A_BR = u * saRatio
    A_BL = u * (1-saRatio)
    pointA0 = point(0,0)
    A0_A = law_sines(A_BR, ca*saRatio, 180-angBx)
    pointA = pointA0.pointFrom(A0_A, 90 - angDR)

    pointBR = pointA.pointFrom(A_BR, 90)
    pointBL = pointA.pointFrom(A_BL, -90)

    outerPolyVertices = [pointBR.pts(), pointA0.pts(), pointBL.pts()]
    add_plot(ax, pointA0, pointA, color='c', 
            curve_fun=curve_fun)

    print(angDR, angDL, saRatio)
    print(pointA0.pts(), pointA.pts(), pointBR.pts(), pointBL.pts())

    for i in range(N):
        saL += addAngle
        saR += addAngle

        aveSa = (saL + saR) / 2.0
        angCL = 180 - angBx - saL
        angCR = 180 - angBx - saR
        angDL = 90 + aveSa - saL
        angDR = 90 + aveSa - saR

        A_CR = law_sines(A_BR, angCR, angBx)
        pointCR = pointA.pointFrom(A_CR, 90-saR)

        A_CL = law_sines(A_BL, angCL, angBx)
        pointCL = pointA.pointFrom(A_CL, -90+saL)

        A_D = law_sines(A_CL, angDL, saL)
        pointD = pointA.pointFrom(A_D, 90- angDR)

        print("lengths should all be the same")
        print(pointA.lengthTo(pointD), A_D, law_sines(A_CL, angDL, saL), law_sines(A_CR, angDR, saR))

        add_plot(ax, pointA, pointBR, color='r', 
            curve_fun=curve_fun)
        add_plot(ax, pointA, pointBL, color='m', 
            curve_fun=curve_fun)

        add_plot(ax, pointA, pointCL, color='b', 
            curve_fun=curve_fun)
        add_plot(ax, pointA, pointCR, color='c', 
            curve_fun=curve_fun)
        
        add_plot(ax, pointA, pointD, color='g', 
            curve_fun=curve_fun)

        pointBL = pointCL
        pointBR = pointCR
        pointA = pointD
        A_BR = pointA.lengthTo(pointBR)
        A_BL = pointA.lengthTo(pointBL)
    
    # finish making outer triangle for cutting
    saL += addAngle
    saR += addAngle

    angCL = 180 - angBx - saL
    angCR = 180 - angBx - saR

    A_CR = law_sines(A_BR, angCR, angBx)
    pointCR = pointA.pointFrom(A_CR, 90-saR)

    A_CL = law_sines(A_BL, angCL, angBx)
    pointCL = pointA.pointFrom(A_CL, -90+saL)

    outerPolyVertices.extend([pointCL.pts(), pointCR.pts()]) 
    poly = Polygon(outerPolyVertices, facecolor='1.0', edgecolor='k')
    ax.add_patch(poly)
    plt.axis('off')
    ax.set_aspect(1), ax.autoscale()

# Use an x division less than two or the curves fight the angle of growth
def ptb_sumxdiv0975_avey(pt1, pt2):
    xb = (pt1.x+pt2.x)/(2.0*0.975)
    yb = (pt1.y+pt2.y)/2.0
    return point(xb, yb)

show_plot = True

figure, ax = plt.subplots()
name = 'tb9_ca30_sar15_sal30_N15'
make_plot(ax, ca=30, saR=15, saL=30, u=1.0, N=15, curve_fun=ptb_straightline, addAngle=0)
plt.savefig(name + ".svg")
if show_plot: plt.title(name), plt.show()

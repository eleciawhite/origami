# Generate a turbinated shell (which is to say conical, not in a plane # like a planispiral shell). The Fuse method can be formed to be 
# conical but you working against the paper. The goal here is for a 
# natural 3d spiral, going all the way to scalariform (whorls not 
# touching each other).

# The geometery from this came from experimenting with random right 
# triangle scraps. I found that I could fold along the center line of 
# the paper, then fold across normal to the long edge of the right 
# triangle (valleys). Then fold mountains generally to Fuse's method:
# from where the normal line crosses the midline to where the normal 
# line meets the edge of the paper. 
# 
# Depending on the distance between the normal lines and the shape of 
# the scrap, the result is a conical spiral with raw edges only at the 
# large end.
# 
# The geomtry for figuring out the lines was tough, mostly careful, 
# repeated use of the Law of Sines as well as other triangle rules. The 
# terminology I'm using for the code depends heavily on the diagram. 
# Look in the pics directory for a relevant diagram.
#
# The parameters are:
# ca - central angle (the one with the midline through it)
# sa - spiraling angle 
# u = inital length of the normal
# N - number of iterations
# ratio - ca doesn't need to be perfectly bisected, this is how much is on the left:right (default:0.5)

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

def make_plot(ax, ca, sa, u=1.0, N=15, curve_fun=ptb_straightline, ratio=0.5, addAngle=0.0):

    pointA = point(0,0)
    A_BL = law_sines(u, ca, 90-ca)
    pointBL = point(0, A_BL)
    pointBR = point(u, A_BL)
    outerPolyVertices = [pointBR.pts(), pointA.pts(), pointBL.pts()]
    caL = ca*(1-ratio)
    normal_length = u

    pointD = point((1-ratio)*normal_length, A_BL)
    
    add_plot(ax, pointA, pointD, color='g', 
            curve_fun=curve_fun)
            
    pointA = pointD

    for i in range(N):
        sa += addAngle
        
        A_BL = pointA.lengthTo(pointBL)
        BL_CL = law_sines(A_BL, 90-sa, sa)
        pointCL = pointBL.pointFrom(BL_CL, 0)

        A_CL = law_sines(A_BL, 90-sa, 90)
        CL_D = law_sines(A_CL, 90-caL, 90+caL-sa)

        pointD = pointCL.pointFrom(CL_D, 90)
        pointCR = pointD.pointFrom(ratio*CL_D/(1-ratio), 90)

        # normal line
        add_plot(ax, pointA, pointBR, color='r', 
            curve_fun=curve_fun)
        add_plot(ax, pointA, pointBL, color='m', 
            curve_fun=curve_fun)

        add_plot(ax, pointA, pointCL, color='b', 
            curve_fun=curve_fun)
        add_plot(ax, pointA, pointCR, color='c', 
            curve_fun=curve_fun)

    
        pointBL = pointCL
        pointBR = pointCR
        pointA = pointD
        normal_length = pointBL.lengthTo(pointBR)
    
    # finish making outer triangle for cutting
    A_BL = pointA.lengthTo(pointBL)
    BL_CL = law_sines(A_BL, 90-sa, sa)
    pointCL = pointBL.pointFrom(BL_CL, 0)
    A_CL = law_sines(A_BL, 90-sa, 90)
    CL_D = law_sines(A_CL, 90-caL, 90+caL-sa)

    pointD = pointCL.pointFrom(CL_D, 90)
    pointCR = pointD.pointFrom(ratio*CL_D/(1-ratio), 90)
    
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
name = 'tb3_ca30_sa35_N20_min050'
make_plot(ax, ca=30, sa=35, u=1.0, N=20, curve_fun=ptb_straightline, addAngle=-0.5)
plt.savefig(name + ".svg")
if show_plot: plt.title(name), plt.show()

figure, ax = plt.subplots()
name = 'tb3_ca30_sa40_N25_min125'
make_plot(ax, ca=30, sa=40, u=1.0, N=25, curve_fun=ptb_straightline, addAngle=-1.25)
plt.savefig(name + ".svg")
if show_plot: plt.title(name), plt.show()


figure, ax = plt.subplots()
name = 'tb3_ca45_sa40_N20_min15'
make_plot(ax, ca=45, sa=40, u=1.0, N=20, curve_fun=ptb_straightline, addAngle=-1.5)
plt.savefig(name + ".svg")
if show_plot: plt.title(name), plt.show()

figure, ax = plt.subplots()
name = 'tb3_ca45_sa45_N15_min2'
make_plot(ax, ca=45, sa=45, u=1.0, N=15, curve_fun=ptb_straightline, addAngle=-2)
plt.savefig(name + ".svg")
if show_plot: plt.title(name), plt.show()

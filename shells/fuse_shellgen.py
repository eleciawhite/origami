# Generate a nautilus shell from triangles
# This method is based in the one decribed in Spirals 
# by Tomoko Fuse for Ammonites.

# The flat method is controlled by a cental angle (ca)  and 
# an angle of spirality (sa). With a starting length (u), and a 
# number of iterations (N), this is enough to create 
# the ammonite pattern.

# Start with an isoceles triangle where the central angle (ca)
# is the one that is the odd one out. The starting length is the 
# leg opposite ca and is 2u. Drop a bisector from ca to get a pair
# of right triangles. This is the tip of the ammonite.

# Next, add a triangle from the center line (bisector) such
# that it has an angle sa from u. Extend this and extend the legs
# of the isosceles triangle until they meet. 
# Add a line from this point to the center line (perpindicular
# to the centerline), this becomes u_prime
#
# The resulting shape is a right trapezoid with a diagonal.
# Mirror this on the other side of the centerline. 
# Set u=u_prime and repeat N times.
#
# While the diagonak cuts the trapezoid into a right 
# triangle and a scalene trianle, sadly, we know information 
# for the scalene trianle but need information for the right 
# triangle which means we need
#
# The Law of Cosines: Pythagorean theorem for non-right triangles
# a*a = b*b + c*c - 2ac cos(angle_a)
# The Law of Sines
#   a/sin(angle_a) = b/sin(angle_b) = c/sin(angle_c)
# Much algebra will be done. I will not show my work.
#
# A straight line approach leads to flat origami. I'm
# planning to modify 
# the algorithm to use bezier curves to get 
# a self-shaping curved nautilus.

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


def add_plot(ax, pt1, pt2, ptb, color):
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

# We are given two angles of a triangle and one side, which is not the side adjacent to the two given angles. Return all three point coordinates.
# https://www.mathsisfun.com/algebra/trig-solving-triangles.html
# https://www.triangle-calculator.com/
def triangle_find_vertices_aas(angleA, angleC, sideAB):
    lengthBC= sideAB.length()*sin(radians(angleA))/sin(radians(angleC))
    angleB = 180 - abs(angleA) - abs(angleC)
    #print(angleA, angleB, angleC)
    lengthAC = sideAB.length()*sin(radians(angleB))/sin(radians(angleC))
    pointC = sideAB.pointA.pointFrom(lengthAC, angleA)
    #print('AC len {} BC len {} AB len {} BC {} AC {}'.format(lengthAC, lengthBC, sideAB.length(), pointC.lengthTo(sideAB.pointB), pointC.lengthTo(sideAB.pointA)))
    return [sideAB.pointA, sideAB.pointB, pointC]
    
def make_plot(ax, ca, sa, u, N, curve_fun):
    angleC = 90.0 - ca/2.0 - sa
    angleA = sa

    pointA = point(0,0)
    pointB = pointA.pointFrom(u, 0)
    
    sideTop = side(pointB, pointB.negative())
    angleOpTop= 3.0*ca
    angleIso = (180.0 - angleOpTop)/2.0
    pointX, pointY, pointZ = triangle_find_vertices_aas(angleIso, -angleOpTop, sideTop)
    # Small fat triangle on the top
    outerPolyVertices = [pointX.pts(), pointZ.pts(), pointY.pts()]
    
    for i in range(N):
        sideAB = side(pointA, pointB)
        pointA, pointB, pointC = triangle_find_vertices_aas(angleA, angleC, sideAB)
        
        add_plot(ax, pointA, pointB, color='r', 
            ptb=curve_fun(pointA, pointB))
        add_plot(ax, pointA, pointB.negative(), color='r', 
            ptb=curve_fun(pointA, pointB.negative()))
        add_plot(ax, pointA, pointC, color='b', 
            ptb=curve_fun(pointA, pointC))
        add_plot(ax, pointA, pointC.negative(), color='b', 
            ptb=curve_fun(pointA, pointC.negative()))
            
        # for debugging:
        #ptb_ab = curve_fun(pointA, pointB)
        #ax.plot(ptb_ab.x, ptb_ab.y, 'rx')
        #ptb_ac = curve_fun(pointA, pointC)
        #ax.plot(ptb_ac.x, ptb_ac.y, 'bx')
            
        lengthAB = sideAB.length()
        lengthAC = pointA.lengthTo(pointC) 
        newLengthAB = lengthAC * sin(radians(90-angleA))
        lengthANewA = lengthAC * sin(radians(angleA))

        pointA = pointA.pointFrom(lengthANewA, 90)
        pointB = pointC

    # make outer triangle for cutting
    sideAB = side(pointA, pointB)
    pointA, pointB, pointC = triangle_find_vertices_aas(angleA, angleC, sideAB)
    outerPolyVertices.extend([pointC.negative().pts(), pointC.pts()])
    #print(outerPolyVertices)
    
    poly = Polygon(outerPolyVertices, facecolor='1.0', edgecolor='k')
    ax.add_patch(poly)
    plt.axis('off')
    ax.set_aspect(1), ax.autoscale()
        
# use for straight line versions
def ptb_pt1(pt1, pt2):
    return pt1
    
def ptb_sumxdiv195_avey(pt1, pt2):
    xb = (pt1.x+pt2.x)/1.95
    yb = (pt1.y+pt2.y)/2.0
    return point(xb, yb)
    
def ptb_sumxdiv205_avey(pt1, pt2):
    xb = (pt1.x+pt2.x)/2.05
    yb = (pt1.y+pt2.y)/2.0
    return point(xb, yb)
    
def ptb_sumxdiv210_avey(pt1, pt2):
    xb = (pt1.x+pt2.x)/2.10
    yb = (pt1.y+pt2.y)/2.0
    return point(xb, yb)

ca = 30.0 # central angle, book uses 30 to 45 degrees
sa = 15.0 # spirality angle book uses 12 to 15 degrees
u  = 1.0  # initial length
N  = 20  # number of iterations

show_plot = True
figure, ax = plt.subplots()
name = 'fusesgen_straight_ca30_sa15_N20'
make_plot(ax, ca=30, sa=15, u=1, N=20, curve_fun=ptb_pt1)
plt.savefig(name + ".svg")
if show_plot: plt.title(name), plt.show()

figure, ax = plt.subplots()
name = 'fusesgen_straight_ca45_sa15_N15'
make_plot(ax, ca=45, sa=15, u=1, N=15, curve_fun=ptb_pt1)
plt.savefig(name + ".svg")
if show_plot: plt.title(name), plt.show()

figure, ax = plt.subplots()
name = 'fusesgen_straight_ca45_sa12_N20'
make_plot(ax, ca=45, sa=12, u=1, N=20, curve_fun=ptb_pt1)
plt.savefig(name + ".svg")
if show_plot: plt.title(name), plt.show()

figure, ax = plt.subplots()
name = 'fusesgen_bez195_ca30_sa15_N20'
make_plot(ax, ca=30, sa=15, u=1, N=20, curve_fun=ptb_sumxdiv195_avey)
plt.savefig(name + ".svg")
if show_plot: plt.title(name), plt.show()

figure, ax = plt.subplots()
name = 'fusesgen_bez210_ca45_sa15_N15'
make_plot(ax, ca=45, sa=15, u=1, N=15, curve_fun=ptb_sumxdiv210_avey)
plt.savefig(name + ".svg")
if show_plot: plt.title(name), plt.show()

figure, ax = plt.subplots()
name = 'fusesgen_bez205_ca45_sa12_N20'
make_plot(ax, ca=45, sa=12, u=1, N=20, curve_fun=ptb_sumxdiv205_avey)
plt.savefig(name + ".svg")
if show_plot: plt.title(name), plt.show()

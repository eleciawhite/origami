# Generate a nautilus shell from triangles
# This method is based in the one described in Origami4
# "Paper Nautili: A Model for Three Dimensional Planispiral Growth"
# by Arle Lommel

# Starting with a right triangle ABC where A is the origin, 
# B is up and C is to the side. The goal is to calculate
# the next triangle BDC where r*len BA = len CD
# and another triable CFD where F is the midpoint of BD
# the end product is to draw CD and CF for some number of 
# iterations
#
# A straight line approach leads to flat origami. I've 
# modified the algorithm to use bezier curves to get 
# a self-shaping curved nautilus.

from math import sqrt
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

def make_plot(r, N, ax, cf_fun, cd_fun, offset, double=True, beta=1.0, gamma=1.0):

    a = point(gamma,0)
    b = point(gamma, beta)
    c = point(gamma*2, 0)
    
    if double:
        ori = offset(0, point(0,beta/r))
        outerPolyVertices=[ori.negative().pts(), ori.pts()]
    else:
        outerPolyVertices=[a.pts(), b.pts()]

    for i in range(0, N):
        
        if double is True:
            a = offset(i, a)
            b = offset(i, b)
            c = offset(i, c)
          
        ba = b.lengthTo(a)
        d = point(c.x, c.y + r * ba )
        diff_ba_dc = (r-1)*ba

        f = point(b.x + 0.5 * (c.x - b.x), b.y + 0.5 * diff_ba_dc)

        # now, fold lines on cd and on cf

        if double is True:
            nf = f.negative()
            nc = c.negative()
            nd = d.negative()
            add_plot(ax, c.negative(), f.negative(), color='r', ptb=cf_fun(c.negative(), f.negative()))
            add_plot(ax, c.negative(), d.negative(), color='b', ptb=cd_fun(c.negative(), d.negative()))

        add_plot(ax, c, f, color='r', ptb=cf_fun(c,f))
        add_plot(ax, c, d, color='b', ptb=cd_fun(c,d))

        # for debugging:
        #ptb_cf = cf_fun(c,f)
        #ax.plot(ptb_cf.x, ptb_cf.y, 'rx')
        #ptb_cd = cd_fun(c,f)
        #ax.plot(ptb_cd.x, ptb_cd.y, 'bx')

        # move the generator over
        newc = point(c.x + (gamma/beta)*r*ba, c.y)
        a = c
        b = d
        c = newc
    
    # finish outer polygon for cut line
    if double is True:
        o = offset(N, d)
        o.x += gamma
        outerPolyVertices.extend([o.pts(), o.negative().pts()])
    else:
        outerPolyVertices.extend([d.pts(), c.pts()])
    
    poly = Polygon(outerPolyVertices, facecolor='1.0', edgecolor='k')
    ax.add_patch(poly)
    ax.set_aspect(1)
    plt.axis('off')


def ptb_1x_avey(pt1, pt2):
    xb = pt1.x
    yb = (pt1.y+pt2.y)/2.0
    return point(xb, yb)
    
def ptb_1x105_avey(pt1, pt2):
    xb = 1.05*pt1.x
    yb = (pt1.y+pt2.y)/2.0
    return point(xb, yb)
    
def ptb_sumxdiv21_avey(pt1, pt2):
    xb = (pt1.x+pt2.x)/2.1
    yb = (pt1.y+pt2.y)/2.0
    return point(xb, yb)
    
def ptb_sumxdiv21_y0(pt1, pt2):
    xb = (pt1.x+pt2.x)/2.1
    return point(xb, 0.0)

def ptb_pt1(pt1, pt2):
    return pt1

show_plot = True

# when doubled, the offset function is how much the two sides are separated
def offset_mult02(i, p, mult=0.02):
    offset = mult*i
    return point(p.x, p.y+offset)

figure, ax = plt.subplots()
name = "shellgen_Lommel_r108_16"
make_plot(r=1.08, N=16, ax=ax, cf_fun=ptb_pt1, cd_fun=ptb_pt1, offset=offset_mult02)
plt.savefig(name + ".svg")
if show_plot: plt.title(name), plt.show()

figure, ax = plt.subplots()
name = "nautilus_halfshell"
make_plot(r=1.08, N=16, ax=ax, double=False, 
    cf_fun=ptb_sumxdiv21_avey, cd_fun=ptb_sumxdiv21_avey, offset=offset_mult02)
plt.savefig(name + ".svg")
if show_plot: plt.title(name), plt.show()


figure, ax = plt.subplots()
name = "shellgen_d3_r108_n10"
make_plot(r=1.08, N=10, ax=ax, 
    cf_fun=ptb_sumxdiv21_avey, cd_fun=ptb_sumxdiv21_avey, offset=offset_mult02)
plt.savefig(name + ".svg")
if show_plot: plt.title(name), plt.show()

figure, ax = plt.subplots()
name = "shellgen_d3_r120_n10"
make_plot(r=1.20, N=10, ax=ax, 
    cf_fun=ptb_sumxdiv21_avey, cd_fun=ptb_sumxdiv21_avey, offset=offset_mult02)
plt.savefig(name + ".svg")
if show_plot: plt.title(name), plt.show()

figure, ax = plt.subplots()
name = "shellgen_d3_r130_n10"
make_plot(r=1.3, N=10, ax=ax, 
    cf_fun=ptb_sumxdiv21_avey, cd_fun=ptb_sumxdiv21_avey, offset=offset_mult02)
plt.savefig(name + ".svg")
if show_plot: plt.title(name), plt.show()

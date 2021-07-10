# Turbinator2.py
#
# Outputing turbinate shells like turbinator.py 
# but with the triangle path methods used in curlpool.py
# all so we can extend it to conches.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Polygon

from matplotlib.path import Path
import matplotlib.path as mplpath
import matplotlib as mpl
from math import *
import logging

import copy

from point import Point # local file

def add_plot(patch_list, pt1, pt2, pt3, curve_fun12, curve_fun13, color):
    codes = [ # front load codes
            Path.MOVETO, # pt1
            Path.CURVE3, # Draw a quadratic Bezier curve from the current position, with the given control point, to the given end point.
            Path.CURVE3, # pt2 endpoint
            Path.MOVETO, # pt3
            Path.CURVE3, # Draw a quadratic Bezier curve from the current position, with the given control point, to the given end point.
            Path.CURVE3, # pt3 endpoint

        ]
    pt12 = curve_fun12(pt1, pt2)
    pt13 = curve_fun13(pt1, pt3)
    vertices = [(pt1.x, pt1.y), (pt12.x, pt12.y), (pt2.x, pt2.y)]
    vertices.extend([(pt3.x, pt3.y), (pt13.x, pt13.y), (pt1.x, pt1.y)])
    patch = patches.PathPatch(Path(vertices=vertices, codes=codes), 
        facecolor='1.0', alpha=1.0, edgecolor=color)

    patch_list.append(patch)

def getSlopeAndIntercept(pt1, pt2):
    x1, y1 = pt1
    x2, y2 = pt2
    if (x2-x1) != 0:
        slope = (y2-y1) / (x2-x1)
        intercept = y1 - slope*x1
    else :
        slope = np.nan
        intercept= np.nan

    return slope, intercept

def cutPatchAtIntersection(curve, linepts, epsilon = 0.0035):
    linepath = Path(linepts)
    lineslope, lineintercept = getSlopeAndIntercept(linepts[0], linepts[1])
    if lineslope == np.nan:
        print("line is nan")
        return curve

    curvepath = curve.get_path()
    if (curvepath.intersects_path(linepath)):
        for i in range(len(curvepath.vertices)):            
            # where does a straight line segment from curvepath intersect line path?
            pt1 = curvepath.vertices[i] 
            pt2 = curvepath.vertices[i-1] # take from last for the first pass
            cslope, cintercept = getSlopeAndIntercept(pt1, pt2)
            if cslope is np.nan:
                print("curve is nan: {}".format(i))
                continue
            intersectionx = (cintercept - lineintercept)/(lineslope - cslope)
            intersectiony = (lineslope*intersectionx) + lineintercept
            print("intersection found: {} {} {}".format(i, intersectionx, intersectiony))
            curvepath.vertices[i-1]=(intersectionx,intersectiony)
#        print(curve.get_path())
#        print(linepath)
    return curve 

#    ((x1,y1),(x2,y2)) = line

#    for i in range(curve.shape[0]):
#        xc, yc = curve[i]
#        d = dist(x1, y1, x2, y2, xc, yc)
#        if d < epsilon:
#           return curve[:i]
#    return curve



def law_sines(length, ang_denom, ang_mult):
    val = length*sin(radians(ang_mult)) / sin(radians(ang_denom))
    return abs(val)

# use for straight line versions
def ptb_straightline(pt1, pt2):
    return pt1

def make_plot(prefix='ch', show_plot=True, 
            caR=15.0, caL=15.0, saL=12.0, saR=15.0, N=15, 
            curve_fun=ptb_straightline, kite=0, 
            cutProtoconch = True, cut_bottom_func = None):

    fig, ax = plt.subplots()
    name = '{}_cal{}_car{}_sal{}_sar{}_N{}'.format(
        prefix, int(caL), int(caR), int(saL), int(saR), N)
    logging.info(name)

    # angles from known 
    angBR = 90 + (caR)
    angBL = 90 + (caL)
    angCL = 180 - angBL - saL
    angCR = 180 - angBR - saR

    # known length
    BL_BR = 1.0

    # initial protoconch triangle
    pointA = Point(0,0)
    A_BL = law_sines(BL_BR, caL + caR, 90-caR)
    A_BR = law_sines(BL_BR, caL + caR, 90-caL)
    pointBR = pointA.pointFrom(A_BR, caR)
    pointBL = pointA.pointFrom(A_BL, -caL)

    if cutProtoconch:
        outerPolyVertices = [pointBR.pts(), pointBL.pts()]
    else:
        outerPolyVertices = [pointBR.pts(), pointA.pts(), pointBL.pts()]
    prevA = pointA

    patch_list =[]

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
            add_plot(patch_list, pointA, pointBR, pointCR, curve_fun, curve_fun, color='r')
            add_plot(patch_list, pointA, pointBL, pointCL,curve_fun, curve_fun, color='g')
            
            if i == (N-kite):
                kiteBL = pointBL
                kiteBR = pointBR
            
            if cutProtoconch==False and i == 0:
                add_plot(patch_list, prevA, pointA, color='g', curve_fun=ptb_straightline)

            pointBL = pointCL
            pointBR = pointCR
            BL_BR = pointCL.lengthTo(pointCR)
            prevA = pointA
    
    if cut_bottom_func is None:
        outerPolyVertices.extend([pointCL.pts(), pointCR.pts()]) 
    else:
        outerPolyVertices, patch = cut_bottom_func(patch_list, outerPolyVertices, pointCL, pointCR)

    print("outer poly vertice")
    print(outerPolyVertices)
    cutpoly = Polygon(outerPolyVertices, facecolor='1.0', alpha=1.00, edgecolor='k')
    ax.add_patch(cutpoly)

    for patch in patch_list:
        ax.add_patch(patch)
       
    plt.axis('off')
    plt.box(False)
    
    ax.set_aspect(1), ax.autoscale()
    plt.savefig(name + ".svg")

    if show_plot: plt.title(name), plt.show()



def longer_bottom(scorepatches, cutverts, lastleft, lastright):
    hdist=Point.fromVertices(cutverts[0]).lengthTo(lastleft)    
    height=.3*hdist

    # cut line is the easiest
    extendL = lastleft.pointFrom(height, 0)
    extendR = lastright.pointFrom(height, 0)
    cutverts.extend([lastleft.pts(), extendL.pts()]) 
    cutverts.extend([extendR.pts(), lastright.pts()]) 


    numcreases = 7
    xdist = (lastleft.lengthTo(lastright)) / (numcreases+1)

    lastpoint = extendL.pts()
    lastpointbottom = True
    edgecolor = 'm'
    for i in range(numcreases):
        # every xdist/numcreases drop a vertical
        top = lastleft.pointFrom((i+1)*xdist,90)
        bottom = top.pointFrom(height,0)
        
        if (lastpointbottom):
            print("last point bottom")
            vertices = [lastpoint, top.pts(),bottom.pts()]
            lastpoint = top.pts()
        else:
            print("last point top")
            vertices = [lastpoint, bottom.pts()]
            lastpoint = bottom.pts()
            
        print(vertices)
        patch = patches.PathPatch(Path(vertices), facecolor='1.0', alpha=0.50, edgecolor=edgecolor)
        scorepatches.append(patch)
        lastpointbottom = not lastpointbottom

    vertices=[lastpoint, extendR.pts()]
    patch = patches.PathPatch(Path(vertices), facecolor='1.0', alpha=0.50, edgecolor=edgecolor)
    scorepatches.append(patch)


    return cutverts, scorepatches
    outerPolyVertices.extend([pointCL.pts(), pointCR.pts()]) 
    cutpoly = Polygon(outerPolyVertices, facecolor='1.0', alpha=1.00, edgecolor='k')


    newrow = []
    cuts = []
    for i, triangle in enumerate(rows[0]):
        angle =  atan_deg(rows[1][i].pt_a.pts(), triangle.pt_a.pts())
        newPoint = triangle.pt_a.pointFrom(length, angle)

        if i != 0:
            newpath = StraightPath(triangle.pt_a, newPoint)
            newrow.append(newpath)
            m2 = newPoint.midpoint(prevPoint)
            newrow.append(StraightPath(m1, m2))
        cuts.append(newPoint.pts())
        prevPoint = newPoint
        m1 = triangle.pt_a.midpoint(triangle.pt_c)

    # add the last one point and midline
    angle =  atan_deg(triangle.pt_b.pts(), triangle.pt_c.pts())
    newPoint = triangle.pt_c.pointFrom(length, angle)
    cuts.append(newPoint.pts())
    m2 = newPoint.midpoint(prevPoint)
    newrow.append(StraightPath(m1, m2))

    return newrow, cuts


# Use an x division less than two or the curves fight the angle of growth
def ptb_sumxdiv0975_avey(pt1, pt2):
    divisor = 2.0 * 0.975
    xb = (pt1.x+pt2.x)/divisor
    yb = (pt1.y+pt2.y)/divisor
    return Point(xb, yb)

def ptb_sumxdiv095_avey(pt1, pt2):
    divisor = 2.0 * 0.95
    xb = (pt1.x+pt2.x)/divisor
    yb = (pt1.y+pt2.y)/divisor
    return Point(xb, yb)
    
def ptb_sumxdiv090_avey(pt1, pt2):
    divisor = 2.0 * 0.90
    xb = (pt1.x+pt2.x)/divisor
    yb = (pt1.y+pt2.y)/divisor
    return Point(xb, yb)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    make_plot(prefix='t2straight', caL =0, caR = 15, 
        saL=35, saR=25, N=10, kite=0, curve_fun=ptb_straightline, 
        cut_bottom_func=longer_bottom)
    
    #make_plot(prefix='c', caL =25, caR = 25, 
    #    saL=20, saR=14, N=10, curve_fun=ptb_straightline)


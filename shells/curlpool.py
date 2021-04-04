# Generate a whirlpool (or screw shell) from triangles
# This method is based on the in the one decribed in Spirals 
# by Tomoko Fuse for Whirlpool Spirals but I've added curves
# to get a more flowing appearance (less step-like). 
# See ../spirals/whirlpool.py for a more true-to-the-book version.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
import matplotlib.path as mplpath
import matplotlib as mpl
from math import *

import copy

def distance(a, b):
    x2 = (a[0] - b[0])**2
    y2 = (a[1] - b[1])**2
    return sqrt(x2 + y2)

class wp_angles:
    def __init__(self):
        self.beta = 0
        self.alpha = 0
        self.gamma = 0

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @classmethod
    def fromVertices(cls, v):
        ret = cls(v[0],v[1])
        return ret

    def lengthTo(self, p):
        x2 = (self.x-p.x)**2
        y2 = (self.y-p.y)**2
        return sqrt(x2 + y2)

    def midpoint(self, p):
        return self.meetpoint(p, 0.5)
        
    def meetpoint(self, p, ratio):
        x = (self.x * ratio) + p.x * (1.0-ratio)
        y = (self.y * ratio) + p.y * (1.0-ratio)
        return Point(x, y)

    def pts(self):
        return [self.x, self.y]
        
    def negative(self):
        return Point(self.x, -self.y)
    
    def pointFrom(self, length, angle):
        x = self.x + length*sin(radians(angle))
        y = self.y + length*cos(radians(angle))
        return Point(x, y)

def atan_deg(pt1, pt2):
    x = pt2[0] - pt1[0]
    y = pt2[1] - pt1[1]
    print("atan %f %f => %f"%(x, y, degrees(atan2(x,y))))
    return degrees(atan2(x,y))

def law_sines(length, ang_denom, ang_mult):
    val = length*sin(radians(ang_mult)) / sin(radians(ang_denom))
    return abs(val)

class CurvedTriangle(mplpath.Path):
    # CurvedTriangle class encapsulates the mpl.Path class 
    # so we can still use vertices as the triangle endpoints
    # while also having curved legs
    def __init__(self, vertices, curve=1.0):
        self.curve = curve
        self.setPointsFromTriangleVertices(vertices)
        if (curve == 0):
            path_vertices = vertices
            path_codes = [
                Path.MOVETO,
                Path.LINETO,
                Path.LINETO,
                Path.LINETO          
            ] 
        else:
            path_codes = [
                Path.MOVETO,
                Path.CURVE3, # Draw a quadratic Bezier curve from the current position, with the given control point, to the given end point.
                Path.CURVE3, # endpoint
                Path.LINETO,
                Path.LINETO           
            ] 
 
            #controlpoint is in the direction of C
            midpoint_ab = self.pt_a.midpoint(self.pt_b)
            controlpoint = midpoint_ab.meetpoint(self.pt_c, curve).pts()

            print(vertices[0], vertices[1])
            print(midpoint_ab.pts(), controlpoint)
            path_vertices = [
                vertices[0], # A
                controlpoint,# Control point
                vertices[1], # B
                vertices[2], # C
                vertices[0], # A (back to)   
            ]
        super(CurvedTriangle, self).__init__(vertices = path_vertices,
                            codes = path_codes)

    @classmethod
    def fromPath(cls, path):
        obj = cls.__new__(cls) # does not call __init__
        super(CurvedTriangle,obj).__init__(vertices = path._vertices,
                            codes = path._codes)
        obj.curve = None
        triangle_vertices = obj.getTriangleVertices()
        obj.setPointsFromTriangleVertices(triangle_vertices)
        return obj

    def getTriangleVertices(self):
        vertices = self._vertices
        codes = self._codes
        triangle_vertices = []
        controlPoint = True
        for i, code in enumerate(codes):
            if code == Path.MOVETO or code == Path.LINETO:
                triangle_vertices.append(vertices[i])
            if code == Path.CURVE3:
                if controlPoint == True:
                    controlPoint = False # next one will be end point
                else:
                    triangle_vertices.append(vertices[i])
                    controlPoint = True # reset for next pair

        return triangle_vertices

    def setPointsFromTriangleVertices(self, vertices):
        self.pt_a = Point.fromVertices(vertices[0])
        self.pt_b = Point.fromVertices(vertices[1])
        self.pt_c = Point.fromVertices(vertices[2])

    def transformed(self, xform):
        xform_path = super(CurvedTriangle, self).transformed(xform) 
        return CurvedTriangle.fromPath(xform_path)    

    def printTriangleVertices(self):
        print("a {:2.2f} {:2.2f} b {:2.2f} {:2.2f} c {:2.2f} {:2.2f}".format(
            self.pt_a.x, self.pt_a.y, self.pt_b.x, self.pt_b.y,
            self.pt_c.x, self.pt_c.y))

def make_basic_triangle_path(origin, ac_len, basic, curve):
    a = origin
    c = a.pointFrom(ac_len, 0.0)  
    ab_len = law_sines(ac_len, basic.beta, basic.gamma)
    b = a.pointFrom(ab_len, basic.alpha)
    vertices = [(a.x, a.y), (b.x, b.y), (c.x, c.y), (a.x, a.y)]
    path = CurvedTriangle(vertices, curve)
    return path

def make_plot(prefix='wp', show_plot=True, 
            polygon_sides=3, rotation_rho=10, spirality_sigma=20, 
            N=10, curve = 0, glue_tab = False,
            cut_tip = True, cut_bottom_func=None,
            angle_offsets = None):

    fig, ax = plt.subplots()
    name = '{}_poly{}_rho{}_sig{}_cur{}_N{}'.format(prefix,
        polygon_sides, int(rotation_rho), int(spirality_sigma), 
        int(curve*100), N)
    
    # Check variable validity
    max_rho = 180.0 / polygon_sides
    max_sigma = 90.0 - max_rho
    if not (0.0 <= rotation_rho and rotation_rho <= max_rho):
        print(name + ": rotation_rho out of range")
        return
    if not (0.0 <= spirality_sigma and spirality_sigma <= max_sigma):
        print(name + ": spirality_sigma out of range")
        return
        
    exterior_base = 90.0 + rotation_rho/2.0       
    poly = wp_angles()
    poly.beta = 360.0/polygon_sides
    poly.alpha = (180.0 - poly.beta)/2.0
    poly.gamma = 2.0 * poly.alpha

    basic = wp_angles()
    basic.beta = exterior_base - poly.alpha
    basic.alpha = spirality_sigma
    basic.gamma = 180.0 - basic.alpha - basic.beta
    print(basic.alpha, basic.beta, basic.gamma)

    #FIXME: Check validity

    # standard whirlpool
    if angle_offsets is None:
        original_angle_offsets = [rotation_rho*x  for x in list(range(polygon_sides))]
        angle_offsets = [rotation_rho*x  for x in list(range(polygon_sides))]
    
    ac_len = 10.0
    row_origin = Point(0.0, 0.0)
    rows = []
    triangles = []
    for layer in range(N):
        # create a basic triangle of ac_len with angles given
        path = make_basic_triangle_path(row_origin, ac_len, basic, curve)       
        path.printTriangleVertices()
        color = ["red", "green", "blue", "orange", "yellow", "cyan"]
        start = row_origin
        row = []

        for n in range(polygon_sides):
            r = mpl.transforms.Affine2D().rotate_deg_around(
                path.pt_a.x, path.pt_a.y, 
                -angle_offsets[n])
            path = path.transformed(r)
                

            # put triangle in position at the angle_offset and position
            row.append(path)
            print(color[n])
            print(path)
            path.printTriangleVertices()

            path = make_basic_triangle_path(origin = path.pt_c, ac_len = ac_len, basic = basic, curve = curve)  

        # end poly for
        rows.append(row) # big matrix of paths so we can make a cut path

        # Calculate angle offsets then move row_origin
        ac_len = row[0].pt_b.lengthTo(row[1].pt_b) 
        angoff = atan_deg(row[0].pt_b.pts(), row[1].pt_b.pts()) - original_angle_offsets[1]

        for n in range(polygon_sides):
            angle_offsets[n] = original_angle_offsets[n] + angoff
        a = row[0].pt_b.pointFrom(-ac_len, angoff)

        row_origin = Point(a.x, a.y)
        print(row_origin.x, row_origin.y, ac_len)
        print(angle_offsets)
    # end for each layer of triangles

    # make an outline for cutting, use cut_tip and cut_bottom to control it
    cut_vertices = []
    for r in rows: # start at 0,0 and go clockwise, adding each A point in the column
        cut_vertices.append(r[0].pt_a.pts())
    if cut_tip:
        path = rows[-1][0]
        ab_mid = path.pt_a.midpoint(path.pt_b)
        rot = mpl.transforms.Affine2D().rotate_deg_around(ab_mid.x, ab_mid.y, 180.0) 
        cut_vertices.append(path.transformed(rot).pt_c.pts())  

        for n in range(polygon_sides): # add B points of the top (smallest) row
            cut_vertices.append(rows[-1][n].pt_b.pts())
    else: # determine the tip point then set up scores 
        # triangle to tip is QRS, with the tip at Q, with an angle 
        # of rho (rotation_rho) and an isoceles triangle where
        # R and S are two adjacent row Bs.      
        rs_dist = rows[-1][0].pt_b.lengthTo(rows[-1][1].pt_b)
        r_ang = (180.0 - rotation_rho) / 2.0 # isoceles
        qr_dist = law_sines(rs_dist, rotation_rho, r_ang)
        angoff = atan_deg(rows[-1][0].pt_b.pts(), rows[-1][1].pt_b.pts())
        pt_q = rows[-1][0].pt_b.pointFrom(qr_dist, r_ang + angoff)      
        ax.plot(pt_q.x, pt_q.y, 'rx')
        cut_vertices.append(pt_q.pts())
        cut_vertices.append(rows[-1][-1].pt_b.pts())
        row = []
        for n in range(polygon_sides-1): # add B to tip
            x = [rows[-1][n].pt_b.x, pt_q.x]          
            y = [rows[-1][n].pt_b.y, pt_q.y]           
            ax.plot(x, y, 'k')
    
    for i in range(N): # back down the column using the C points on this side
        cut_vertices.append(rows[-(i+1)][-1].pt_c.pts())
    if cut_bottom_func is None:
        for n in range(polygon_sides): # along the wide bottom until back to start
            cut_vertices.append(rows[0][-(n+1)].pt_a.pts())
    cut_path = Path(cut_vertices)
    patch = patches.PathPatch(cut_path, facecolor='k', alpha=0.05, edgecolor='k')
    ax.add_patch(patch)

    # add all the trangles to the plot
    for row in rows:
        for i, r in enumerate(row):        
            patch = patches.PathPatch(r, facecolor=color[i], alpha=0.75, edgecolor='k')
            ax.add_patch(patch)

    plt.axis('off')
    plt.box(False)
    ax.set_aspect(1), ax.autoscale()
    plt.savefig(name + ".svg")
    if show_plot: plt.title(name), plt.show()


make_plot(prefix='strcp', show_plot=True, polygon_sides=3, 
            rotation_rho=20, spirality_sigma=20, 
            N=6, curve = 0.8,
            glue_tab = False,
            cut_tip = False, angle_offsets = None)

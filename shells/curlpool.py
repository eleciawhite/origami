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
import logging

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
    return degrees(atan2(x,y))

def law_sines(length, ang_denom, ang_mult):
    val = length*sin(radians(ang_mult)) / sin(radians(ang_denom))
    return abs(val)

class StraightPath(mplpath.Path): # This is just so I can access these with a and c like I do with CurvedTriangle rows.
    def __init__(self, pt_a, pt_c):
        self.pt_a = pt_a
        self.pt_c = pt_c
        path_codes = [Path.MOVETO, Path.LINETO]
        path_vertices = [pt_a.pts(), pt_c.pts()]
        super(StraightPath, self).__init__(vertices = path_vertices,
                            codes = path_codes)


class CurvedTriangle(mplpath.Path):
    # CurvedTriangle class encapsulates the mpl.Path class 
    # so we can still use vertices as the triangle endpoints
    # while also having curved legs
    def __init__(self, vertices, curve=0, acb_straight=True):
        self.curve = curve
        self.setPointsFromTriangleVertices(vertices)
        self.acb_straight = acb_straight
        if (curve==0):
            path_vertices = vertices
            path_codes = [
                Path.MOVETO,
                Path.LINETO,
                Path.LINETO,
                Path.LINETO          
            ] 
        elif (acb_straight):
            path_codes = [
                Path.MOVETO, # A
                Path.CURVE3, # Draw a quadratic Bezier curve from the current position, with the given control point, to the given end point.
                Path.CURVE3, # B endpoint
                Path.LINETO, # C
                Path.LINETO # A
            ] 
 
            #controlpoint is in the direction of C
            midpoint_ab = self.pt_a.midpoint(self.pt_b)
            controlpoint_ab = midpoint_ab.meetpoint(self.pt_c, curve).pts()
            controlpoint_acb = self.pt_c.pts() 

            path_vertices = [
                vertices[0], # A
                controlpoint_ab,# Control point
                vertices[1], # B
                vertices[2], # C
                vertices[0], # A (back to)   
            ]
            
        else: # acb is curved as well
            path_codes = [
                Path.MOVETO, # A
                Path.CURVE3, # Draw a quadratic Bezier curve from the current position, with the given control point, to the given end point.
                Path.CURVE3, # B endpoint
                Path.CURVE4, # C Control point for Bezier
                Path.CURVE4, # C2 Control point for Bezier                
                Path.CURVE3, # endpoint
            ] 
 
            #controlpoint is in the direction of C
            midpoint_ab = self.pt_a.midpoint(self.pt_b)
            controlpoint_ab = midpoint_ab.meetpoint(self.pt_c, curve).pts()
            controlpoint_acb = self.pt_c.pts() 

            path_vertices = [
                vertices[0], # A
                controlpoint_ab,# Control point
                vertices[1], # B
                vertices[2], # C
                controlpoint_acb, # C
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
        v = self._vertices
        if self.curve == 0:
            triangle_vertices = [v[0], v[1], v[2]]     
        else: # whether acb_straight is true or not:
            triangle_vertices = [v[0], v[2], v[3]]
        return triangle_vertices

    def getTriangleVerticesBySearching(self):
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
        logging.info("a {:2.2f} {:2.2f} b {:2.2f} {:2.2f} c {:2.2f} {:2.2f}".format(
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

def longer_bottom(rows, length):
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

def put_plot_on_fig(ax, rows, cut_vertices, cutline_path):
    cut_path = Path(cut_vertices)
    patch = patches.PathPatch(cut_path, facecolor='k', alpha=0.05, edgecolor='k')
    ax.add_patch(patch)
    patch = patches.PathPatch(cutline_path, alpha=0.75, edgecolor='k')
    ax.add_patch(patch)

    # add all the trangles to the plot
    for row in rows:
        for i, r in enumerate(row):        
            patch = patches.PathPatch(r, alpha=0.75, edgecolor='k')
            ax.add_patch(patch)
    ax.set_aspect(1), ax.autoscale()


def make_plot(prefix='wp', show_plot=True, 
            polygon_sides=3, rotation_rho=10, spirality_sigma=20, 
            N=10, curve = 0, glue_tab = False,
            cut_tip = True, cut_bottom_func=None,
            plot_function=put_plot_on_fig):

    fig, ax = plt.subplots()
    name = '{}_poly{}_rho{}_sig{}_cur{}_N{}'.format(prefix,
        polygon_sides, int(rotation_rho), int(spirality_sigma), 
        int(curve*100), N)
    logging.info(name)
    
    # Check variable validity
    max_rho = 180.0 / polygon_sides
    max_sigma = 90.0 - max_rho
    if not (0.0 <= rotation_rho and rotation_rho <= max_rho):
        logging.error(name + ": rotation_rho out of range")
        return
    if not (0.0 <= spirality_sigma and spirality_sigma <= max_sigma):
        logging.error(name + ": spirality_sigma out of range")
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

    original_angle_offsets = [rotation_rho*x  for x in list(range(polygon_sides))]
    angle_offsets = [rotation_rho*x  for x in list(range(polygon_sides))]
    
    ac_len = 10.0
    row_origin = Point(0.0, 0.0)
    rows = []
    triangles = []
    for layer in range(N):
        # create a basic triangle of ac_len with angles given
        path = make_basic_triangle_path(row_origin, ac_len, basic, curve)       
        start = row_origin
        row = []

        for n in range(polygon_sides):
            r = mpl.transforms.Affine2D().rotate_deg_around(
                path.pt_a.x, path.pt_a.y, 
                -angle_offsets[n])
            path = path.transformed(r)
                
            # put triangle in position at the angle_offset and position
            row.append(path)

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
    # end for each layer of triangles

    # make an outline for cutting, use cut_tip and cut_bottom to control it
    cut_vertices = []
    for r in rows: # start at 0,0 and go clockwise, adding each A point in the column
        cut_vertices.append(r[0].pt_a.pts())

    c0 = row_origin
    cut_vertices.append(c0.pts())  

    if cut_tip:
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
        cut_vertices.append(pt_q.pts())
        cut_vertices.append(rows[-1][-1].pt_b.pts())

        # score topline
        vertices = [(c0.x,c0.y)]
        codes = [ # front load codes
            Path.MOVETO,
        ]
        for n in range(polygon_sides): # add B to tip and B to B
            vertices.append((rows[-1][n].pt_b.x, rows[-1][n].pt_b.y))
            codes.append(Path.LINETO)
            vertices.append((pt_q.x, pt_q.y))
            codes.append(Path.MOVETO)
            vertices.append((rows[-1][n].pt_b.x, rows[-1][n].pt_b.y))
            codes.append(Path.LINETO)
        # also make line from first B to edge
        cutline_path = mplpath.Path(vertices=vertices, codes=codes)

    for i in range(N): # back down the column using the C points on this side
        cut_vertices.append(rows[-(i+1)][-1].pt_c.pts())

    if cut_bottom_func is None:
        for n in range(polygon_sides): # along the wide bottom until back to start
            cut_vertices.append(rows[0][-(n+1)].pt_a.pts())
    else:
        row_path_scores, new_cut_verts = cut_bottom_func(rows[0:2], rows[0][0].pt_a.lengthTo(rows[-1][0].pt_a))
        new_cut_verts.reverse()
        cut_vertices.extend(new_cut_verts)
        rows.insert(0, row_path_scores)

    plot_function(ax, rows, cut_vertices, cutline_path)
    plt.axis('off')
    plt.box(False)
    plt.savefig(name + ".svg")
    if show_plot: plt.title(name), plt.show()



def put_curves_on_fig(ax, rows, cut_vertices, cutline_path, close_poly=False):
    cut_path = Path(cut_vertices)
    patch = patches.PathPatch(cut_path, facecolor='k', alpha=0.05, edgecolor='w')
    ax.add_patch(patch)
    # ignore cutline path

    if close_poly:
        last_code = Path.CLOSEPOLY
    else:
        last_code = Path.MOVETO

    new_row = []
    for row in rows:
        if len(row) == 3:
            path_codes = [
                Path.MOVETO, # A
                Path.CURVE4, # C Control point for Bezier
                Path.CURVE4, # C2 Control point for Bezier                
                Path.CURVE4, # C3 endpoint
                last_code
            ] 
            path_vertices = [
                row[0].pt_a.pts(),
                row[0].pt_c.pts(),
                row[1].pt_c.pts(),
                row[2].pt_c.pts(),
                row[0].pt_a.pts(),
            ]
            curve = mplpath.Path(vertices = path_vertices,
                           codes = path_codes)
            patch = patches.PathPatch(curve, alpha=0.5, edgecolor='k')
            ax.add_patch(patch)

        else:
            logger.error("This polygon can't be an alicorn, try poly=3")
            return

        # now for top line
        row = rows[-1]
        path_codes = [
            Path.MOVETO, # special
            Path.CURVE4, # B Control point for Bezier
            Path.CURVE4, # B2 Control point for Bezier                
            Path.CURVE4, # B3 endpoint
            last_code
        ] 
        path_vertices = [
            cut_vertices[len(rows)],
            row[0].pt_b.pts(),
            row[1].pt_b.pts(),
            row[2].pt_b.pts(),
            cut_vertices[len(rows)],
        ]
        curve = mplpath.Path(vertices = path_vertices,
                       codes = path_codes)
        patch = patches.PathPatch(curve, alpha=0.5, edgecolor='k')
        ax.add_patch(patch)
    ax.set_aspect(1), ax.autoscale()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    make_plot(prefix='curopen', show_plot=True, polygon_sides=3, 
                rotation_rho=10, spirality_sigma=30, 
                N=8, curve=1.0, cut_bottom_func=None,
                glue_tab = False,
                cut_tip = False, plot_function=put_curves_on_fig)
    make_plot(prefix='curopen', show_plot=True, polygon_sides=3, 
                rotation_rho=10, spirality_sigma=20, 
                N=6, curve=1.0, cut_bottom_func=None,
                glue_tab = False,
                cut_tip = False, plot_function=put_curves_on_fig)

#import pdb; pdb.set_trace()

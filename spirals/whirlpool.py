# Generate a whirlpool (or screw shell) from triangles
# This method is based in the one decribed in Spirals 
# by Tomoko Fuse for Ammonites.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
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

class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def lengthTo(self, p):
        x2 = (self.x-p.x)**2
        y2 = (self.y-p.y)**2
        return sqrt(x2 + y2)

    def pts(self):
        return [self.x, self.y]
        
    def negative(self):
        return point(self.x, -self.y)
    
    def pointFrom(self, length, angle):
        x = self.x + length*sin(radians(angle))
        y = self.y + length*cos(radians(angle))
        return point(x, y)

def atan_deg(pt1, pt2):
    x = pt2[0] - pt1[0]
    y = pt2[1] - pt1[1]
    print("atan %f %f => %f"%(x, y, degrees(atan2(x,y))))
    return degrees(atan2(x,y))

def law_sines(length, ang_denom, ang_mult):
    val = length*sin(radians(ang_mult)) / sin(radians(ang_denom))
    return abs(val)

def update_angle_offset(angle_offset, rho):
    for i in range(len(angle_offset)):
        if angle_offset[i] > 0.0001: # epsilon
            angle_offset[i] = rho
    return angle_offset
       
def make_basic_triangle_vertices(origin, ac_len, basic):
    a = point(origin[0], origin[1])
    c = a.pointFrom(ac_len, 0.0)
    ab_len = law_sines(ac_len, basic.beta, basic.gamma)
    b = a.pointFrom(ab_len, basic.alpha)
    vertices = [(a.x, a.y), (b.x, b.y), (c.x, c.y)]
    return vertices


def make_plot(prefix='wp', show_plot=True, polygon_sides=3, rotation_rho=10, spirality_sigma=20, 
            N=10, glue_tab = False,
            cut_tip = True, angle_offsets = None):

    fig, ax = plt.subplots()
    name = '{}_poly{}_rho{}_sig{}_N{}'.format(prefix,
        polygon_sides, int(rotation_rho), int(spirality_sigma), N)
    
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
        angle_offsets = [rotation_rho  for x in list(range(polygon_sides))]
        angle_offsets[0]=0.0
    
    ac_len = [10] * polygon_sides
    row_origin = [0.0, 0.0]
    rows = []
    triangles = []
    for i in range(N):
        # create a basic triangle of ac_len with angles given
        vertices = make_basic_triangle_vertices(row_origin, ac_len[0], basic)       
        print(vertices)
        color = ["red", "green", "blue", "orange", "yellow", "cyan"]
        start = row_origin
        path = Path(vertices)
        row = []
#        import pdb; pdb.set_trace()

        y_translation =0.0
        x_translation =0.0

        for n in range(polygon_sides):
            # put triangle in position at the angle_offset and position
            r = mpl.transforms.Affine2D().rotate_deg_around(
                path.vertices[0][0], path.vertices[0][1], 
                -angle_offsets[n])
            t = mpl.transforms.Affine2D().translate(x_translation, y_translation)  
            tra = r + t 
            path = path.transformed(tra)
            
            row.append(path)
            
            print(color[n])
            print(path)
            patch = patches.PathPatch(path, facecolor=color[n])
            ax.add_patch(patch)
            
            x_translation = path.vertices[2][0] - path.vertices[0][0]
            y_translation = path.vertices[2][1] - path.vertices[0][1]
            new_ac_len = distance(path.vertices[0], path.vertices[2])
            print("translation %d, %f %f %f"%(n, x_translation, y_translation, new_ac_len))

            #setup next point
            vertices = make_basic_triangle_vertices(path.vertices[2], ac_len[n], basic)       




        # end poly for
        rows.append(row)

        totalSoFar = 0.0
        for i in range(len(angle_offsets)):
            if i > 0:
                # getting the atan from flat... not the right way, need from previous
                angle_offsets[i] = atan_deg(row[i-1].vertices[1], row[i].vertices[1]) - totalSoFar
                totalSoFar += angle_offsets[i]
                ac_len[i] = distance(row[i-1].vertices[1], row[i].vertices[1]) # triangle1.b to triangle2.b

        print(angle_offsets, ac_len)
        ac_len[0] = ac_len[-1]
        row_origin = [row[0].vertices[1][0], row[0].vertices[1][1] - ac_len[0]]

        # Move row_origin
        # calculate a_g_len
    # end layers for

    print("row {}".format(len(rows)))
    print("tri {}".format(len(triangles)))

#    plt.axis('off')
#    plt.box(False)
    
    ax.grid('on')
    ax.set_aspect(1), 
    ax.autoscale()
    plt.savefig(name + ".svg")
    if show_plot: plt.title(name), plt.show()




make_plot(prefix='wp', show_plot=True, polygon_sides=4, 
            rotation_rho=10, spirality_sigma=40, 
            N=3, glue_tab = False,
            cut_tip = True, angle_offsets = None)

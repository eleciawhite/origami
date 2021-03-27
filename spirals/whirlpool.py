# Generate a whirlpool (or screw shell) from triangles
# This method is based in the one decribed in Spirals 
# by Tomoko Fuse for Whirlpool Spirals.

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
    c = a.pointFrom(ac_len, 0.0)  # FIXME, is this right?
    ab_len = law_sines(ac_len, basic.beta, basic.gamma)
    b = a.pointFrom(ab_len, basic.alpha)
    vertices = [(a.x, a.y), (b.x, b.y), (c.x, c.y)]
    return vertices

def make_next_triangle(origin, c, basic):
    a = point(origin[0], origin[1])
    c = point(c[0], c[1])
    ac_len = a.lengthTo(c)
    angle_offset = atan_deg(origin, [c.x, c.y])
    ab_len = law_sines(ac_len, basic.beta, basic.gamma)
    b = a.pointFrom(ab_len, basic.alpha + angle_offset)
    vertices = [(a.x, a.y), (b.x, b.y), (c.x, c.y)]
    print("make next triangle")
    print(vertices)
    ac_len = a.lengthTo(c)
    print(angle_offset,ac_len, ab_len)
    return vertices, ac_len


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
        original_angle_offsets = [rotation_rho*x  for x in list(range(polygon_sides))]
        angle_offsets = [rotation_rho*x  for x in list(range(polygon_sides))]
    
    ac_len = 10.0
    row_origin = [0.0, 0.0]
    rows = []
    triangles = []
    for layer in range(N):
        # create a basic triangle of ac_len with angles given
        vertices = make_basic_triangle_vertices(row_origin, ac_len, basic)       
        print(vertices)
        color = ["red", "green", "blue", "orange", "yellow", "cyan"]
        start = row_origin
        row = []

        y_translation = 0.0
        x_translation = 0.0

        for n in range(polygon_sides):
            path = Path(vertices)
            r = mpl.transforms.Affine2D().rotate_deg_around(
                path.vertices[0][0], path.vertices[0][1], 
                -angle_offsets[n])
            t = mpl.transforms.Affine2D().translate(x_translation, y_translation)  
            tra = r + t 
            path = path.transformed(tra)
                

            # put triangle in position at the angle_offset and position
            row.append(path)
            print(color[n])
            print(path)
            patch = patches.PathPatch(path, facecolor=color[n])
            ax.add_patch(patch)

            next_vertices = make_basic_triangle_vertices(origin = path.vertices[2], ac_len=ac_len, basic=basic)  
            vertices = next_vertices


        # end poly for
        rows.append(row) # big matrix of paths so we can make a cut path

        # Calculate angle offsets then move row_origin
        ac_len = distance(row[0].vertices[1], row[1].vertices[1])
        angoff = atan_deg(row[0].vertices[1], row[1].vertices[1]) - original_angle_offsets[1]

        for n in range(polygon_sides):
            angle_offsets[n] = original_angle_offsets[n] + angoff
        b = point(row[0].vertices[1][0],row[0].vertices[1][1])
        a = b.pointFrom(-ac_len, angoff)

        row_origin = [a.x, a.y]
        print(row_origin, ac_len)
        print(angle_offsets)
    # end layers for

    ax.grid('on')
    ax.set_aspect(1), 
    ax.autoscale()
    plt.savefig(name + ".svg")
    if show_plot: plt.title(name), plt.show()


make_plot(prefix='wp', show_plot=True, polygon_sides=6, 
            rotation_rho=10, spirality_sigma=20, 
            N=14, glue_tab = False,
            cut_tip = True, angle_offsets = None)

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

def law_sines(length, ang_denom, ang_mult):
    val = length*sin(radians(ang_mult)) / sin(radians(ang_denom))
    return abs(val)


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

    #FIXME: Check validity

    # standard whirlpool
    if angle_offsets is None:
        angle_offsets = [rotation_rho  for x in list(range(polygon_sides))]

    a_c_len = 10.0
    y_translation=a_c_len
    row_origin = point(0.0, 0.0)
    rows = []
    triangles = []
    for i in range(N):
        # create a basic triangle of ag_len with angles given
        a = row_origin
        c = a.pointFrom(a_c_len, 0.0)
        a_b_len = law_sines(a_c_len, basic.beta, basic.gamma)
        b = a.pointFrom(a_b_len, basic.alpha)

        print(a_b_len, a_c_len)
        vertices = [(a.x, a.y), (b.x, b.y), (c.x, c.y)]
        print(vertices)
        color = ["red", "green", "blue"]
        start = row_origin
        path = Path(vertices)
        row = []
#        import pdb; pdb.set_trace()
        for n in range(polygon_sides):
            # put triangle in position at the angle_offset and position
            row.append(path)
            polygon = patches.Polygon(vertices, color=color[n], alpha=0.10) 
            print(color[n])
            print(path)
            patch = patches.PathPatch(path, facecolor=color[n])
            ax.add_patch(patch)
            r = mpl.transforms.Affine2D().rotate_deg(-angle_offsets[n])
            t = mpl.transforms.Affine2D().translate(0.0, y_translation)          
            tra = r + t 
            path = path.transformed(tra)
        # end poly for
        rows.append(row)
        y_translation = a_c_len
        a_c_len *= .95
        row_origin = point(b.x, b.y-a_c_len)


        # Move row_origin
        # calculate a_g_len
    # end layers for

    print("row {}".format(len(rows)))
    print("tri {}".format(len(triangles)))

#    plt.axis('off')
#    plt.box(False)
    
    ax.set_aspect(1), 
    ax.autoscale()
    plt.savefig(name + ".svg")
    if show_plot: plt.title(name), plt.show()




make_plot(prefix='wp', show_plot=True, polygon_sides=3, rotation_rho=10, spirality_sigma=20, 
            N=3, glue_tab = False,
            cut_tip = True, angle_offsets = None)


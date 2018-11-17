from geometric_operations import*
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import numpy as np


fig = plt.figure()
ax = Axes3D(fig)
ax.set_autoscale_on(False)

ReflectSrf,SrcPts,TgtPts = import_geo()


def from_srf_to_plt_pts(geo_pts):
    plt_pts = np.array(geo_pts)
    plt_pts = plt_pts.transpose()
    x,y,z = plt_pts[0],plt_pts[1],plt_pts[2]
    return [list(zip(x, y, z))]

def from_pts_to_plt_pts(geo_pts):
    plt_pts = np.array(geo_pts)
    plt_pts = plt_pts.transpose()
    x,y,z = plt_pts[0],plt_pts[1],plt_pts[2]
    return x,y,z

s0,s1,s2 = from_pts_to_plt_pts(SrcPts)
r0,r1,r2 = from_pts_to_plt_pts(TgtPts)

ax.scatter3D(s0,s1,s2)
ax.scatter3D(r0,r1,r2, c='r')


for srf_pts in ReflectSrf:
    verts = from_srf_to_plt_pts(srf_pts)

    face = Poly3DCollection(verts,linewidths=1)
    face.set_alpha(0.2)
    face.set_facecolor("C0")
    ax.add_collection3d(face)

    ax.add_collection3d(Line3DCollection(verts, colors='k', linewidths=0.5, linestyles='-'))


# initial zoom

ax.set_xlim([-10, 10])
ax.set_ylim([-10, 10])
ax.set_zlim([-10, 10])

# fix aspect ratio

ax.set_aspect('equal')

plt.show()

print(plt.colors[0])
import numpy as np

#import polylines geometry

def import_geo():

    # IMPORT REFLECTIVE SURFACES (VERTICES)
    pls_pts = []
    with open('refl_srf.txt') as imp:
        content = imp.readlines()
        content = [x.strip() for x in content]

        for line in content:
            pl_pts = []

            str_pts = line.split('/')
            for str_pt in str_pts:
                pt = [float(coord) for coord in str_pt.split(',')]
                pl_pts.append(pt)

            pls_pts.append(pl_pts)
            #pls_pts = np.array(pls_pts)

    # IMPORT SOURCE POINTS
    src_pts = []
    with open('src_pts.txt') as imp:
        content = imp.readlines()
        content = [x.strip() for x in content]

        for line in content:
            src_pts.append([float(coord) for coord in line.split(',')])

    # IMPORT SOURCE POINTS
    tgt_pts = []
    with open('tgt_pts.txt') as imp:
        content = imp.readlines()
        content = [x.strip() for x in content]

        for line in content:
            tgt_pts.append([float(coord) for coord in line.split(',')])

    return pls_pts,src_pts,tgt_pts

##########################################################

# intersection function
def line_srf_intersection(p0, p1, pl_pts, epsilon=1e-6):
    p0 = np.array(p0, dtype=np.float32)
    p1 = np.array(p1, dtype=np.float32)
    pl_pts = np.array(pl_pts, dtype=np.float32)
    ###############   INTERSECTION  ###################

    p_co = pl_pts[0]

    s_pl_pts = np.roll(pl_pts,-1,0) #shift array
    edges_vec = s_pl_pts - pl_pts
    p_no = np.cross(edges_vec[0],edges_vec[1])


    u = p1 - p0
    dot = np.dot(p_no, u)

    unit_p_no = p_no/np.linalg.norm(p_no)
    t0 = np.dot((p0 - p_co),unit_p_no)
    t1 = np.dot((p1 - p_co),unit_p_no)


    if (abs(dot) > epsilon) and (t0*t1 <= 1e-4): #parallel condition + segment plane intersection

        ####################### FIND INTERSECTION #####################

        w = p0 - p_co
        fac = - np.dot(p_no, w) / dot
        u = u * fac
        int_pt = p0 + u

        ####################### INCLUSION TEST #####################

        vp = int_pt - pl_pts
        cp = np.cross(edges_vec,vp)

        dp = [True if np.dot(p_no, val) > 0 else False for val in cp]
        test = all(dp)

        if test:
            return int_pt.tolist()
            # The intersection point is outside the polyline
            return None
    else:
        # The segment is parallel to plane
        return None


def mirror_point(pl_pts, src_pt):
    pl_pts = np.array(pl_pts, dtype=np.float32)
    src_pt = np.array(src_pt, dtype=np.float32)


    p_co = pl_pts[0]

    s_pl_pts = np.roll(pl_pts,-1,0) #shift array
    edges_vec = s_pl_pts - pl_pts

    p_no = np.cross(edges_vec[0],edges_vec[1])

    unit_p_no = p_no/np.linalg.norm(p_no)
    dist = np.dot((src_pt - p_co),unit_p_no) # distance from the plane to point P in the direction of the normal N.
    m_src_pt = src_pt - (2*dist*unit_p_no) #translate P by 2 times that distance D in the direction opposite of normal N.
    return m_src_pt.tolist()


def polyline_length(pl_pts):

    pl_pts = np.array(pl_pts, dtype=np.float32)
    s_pl_pts = np.roll(pl_pts,-1,0) #shift array
    edges_vec = s_pl_pts - pl_pts

    length = np.linalg.norm(edges_vec,axis = 1).sum()

    return length


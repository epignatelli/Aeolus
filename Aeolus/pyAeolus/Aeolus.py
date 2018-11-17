from geometric_operations import*
import numpy as np
import math



n = [1,2]
Compute = True
r = 1


################## IMPORT GEOMETRIES ##################


ReflectSrf,SrcPts,TgtPts = import_geo()

# ReflectSrf = np.array(ReflectSrf, dtype=np.float32)
# SrcPts = np.array(SrcPts, dtype=np.float32)
# TgtPts = np.array(TgtPts, dtype=np.float32)



#line_srf_intersection(p0, p1, pl_pts, epsilon=1e-6):
#mirror_point(pl_pts, src_pt):

def graftlist(List):
    MainList = []
    Void = []
    MainList.append(Void)

    GraftList = []
    for i in range (len(MainList)):
        for j in List:
            Sub = []
            Sub.append(j)
            GraftList.append(Sub)
    return (GraftList)
SrcPtsGraft = graftlist(SrcPts)

ObjList = []
ObjList.append(SrcPtsGraft)


def RecursiveMirror(SrcPtsGraft,gens):
    Macro = []
    for i in range (len(SrcPts)):
        List = []
        for j in range (len(SrcPtsGraft[0])):
            for k in range(len(ReflectSrf)):
                List.append(mirror_point(ReflectSrf[k],SrcPtsGraft[i][j]))
        Macro.append(List)
    if gens != 0:
        ObjList.append(Macro)
    if gens > 0:
        RecursiveMirror(Macro,gens-1)
    return(ObjList)

Nmax = max(n)
mSrcN_full = RecursiveMirror(SrcPtsGraft, Nmax )

###########################################################################################################




# REMOVE FROM MIRRORED SOURCE POINTS LIST ALL DUPLICATES

def PointsConversion(coordinate):
    Converted = []
    for i in range (len(mSrcN_full)):
        Csub1 = []
        for j in range (len(SrcPts)):
            Csub2 =[]
            for k in range (len(mSrcN_full[i][j])):
                Csub2.append(round(mSrcN_full[i][j][k][coordinate],2))
            Csub1.append(Csub2)
        Converted.append(Csub1)
    return(Converted)

mSrcN_x = PointsConversion(0)
mSrcN_y = PointsConversion(1)
mSrcN_z = PointsConversion(2)



def RecursiveCull(mSrcN_full,gens,empty):
    if Nmax >= 2:
        mSrcN = []
        for j in range (len(SrcPts)):
            SubM1 = []
            for k in range (len(mSrcN_full[gens][0])):
                if gens >= 2:
                    if (    (round(mSrcN_full[gens][j][k][0],2)  in (mSrcN_x[(gens-2)][j])) and \
                            (round(mSrcN_full[gens][j][k][1],2)  in (mSrcN_y[(gens-2)][j])) and \
                            (round(mSrcN_full[gens][j][k][2],2)  in (mSrcN_z[(gens-2)][j]))):
                        SubM1.append(None)

                    else:
                        SubM1.append(mSrcN_full[gens][j][k])
            mSrcN.append(SubM1)
        empty.insert(0,mSrcN) #Ordine n
        if gens > 2:
            RecursiveCull(mSrcN_full,gens-1,empty)
        return(empty)
    elif Nmax == 1:
        empty.append(mSrcN_full[0])
        empty.append(mSrcN_full[1])
        return(empty)
    else:
        empty.append(mSrcN_full[0])
        return(empty)



empty = []
mSrcN = (RecursiveCull(mSrcN_full,Nmax,empty))
if Nmax >=2:
    mSrcN.insert(0,mSrcN_full[1])
    mSrcN.insert(0,mSrcN_full[0])


#################################################################################
######################## FIND INTERSECTION PTS AT ORDER N #######################
#################################################################################
def CodeExecution (n):
    #1 FAKE RAYS ORDER N
    fRays = []
    for i in range(len(TgtPts)):
        fRay_Sub = []
        for j in range(len(SrcPts)):
            fRay_Sub2 = []
            for k in range(len(mSrcN[n][0])):
                if mSrcN[n][j][k] != None:
                    fRay_Sub2.append([TgtPts[i],mSrcN[n][j][k]]) ######################################### create list line
                else:
                    fRay_Sub2.append(None)
            fRay_Sub.append(fRay_Sub2)
        fRays.append(fRay_Sub)


    #2 INTERSECTION ORDER N
    ReflectSrf_t = []
    for i in range (int(len(ReflectSrf)**(n)/len(ReflectSrf))):
        for Srf in ReflectSrf:
            ReflectSrf_t.append(Srf) #per n = 3 appende 36 volte la lista di 6 per ramo di src


    Intersection = []
    for i in range (len(TgtPts)):
        sub1 = []
        for j in range (len(SrcPts)):
            sub2 = []
            for w in range(len(ReflectSrf_t)):
                if fRays[i][j][w] != None:
                    Int = line_srf_intersection(fRays[i][j][w][0], fRays[i][j][w][1], ReflectSrf_t[w])
                else:
                    Int = None



                if Int is not None:
                    sub2.append(Int)
                else:
                    sub2.append(None)
            sub1.append(sub2)
        Intersection.append(sub1)


    #################################################################################
    #################### FIND INTERSECTION PTS FROM ORDER N-1 #######################
    #################################################################################


    #RECURSION ( A N-1 OGNI 6 INTERSEZIONI CORRISPONDE UN IMMAGINE, A N-2 OGNI 36 INT CORRISPONDE UN IMMAGINE)

    def RecursiveIntersection (IntPts, gens, IntList):

        if n != 1 :
            fRayN = []
            for i in range (len(TgtPts)):
                sub1 = []
                for j in range (len(SrcPts)):
                    sub2 = []
                    for k in range (len(mSrcN[gens-1][0])):
                        h = k * int((len(Intersection[0][0]))/(len(mSrcN[gens-1][0])))
                        for x in range (int((len(Intersection[0][0]))/(len(mSrcN[gens-1][0])))):
                            if (IntPts [i][j][x + h]) and (mSrcN[gens-1][j][k]) != None:
                                sub2.append([IntPts[i][j][x + h], mSrcN[gens-1][j][k]]) ################################################# create list line
                            else:
                                sub2.append(None)
                    sub1.append(sub2)
                fRayN.append(sub1)

            ReflectSrf_p = []
            for i in range (((int((len(mSrcN[gens-1][0]))/(len(ReflectSrf)))))):
                for Srf in ReflectSrf:
                    for j in range (int((len(IntPts[0][0]))/(len(mSrcN[gens-1][0])))):
                        ReflectSrf_p.append(Srf)

            Pt = []
            for i in range (len(TgtPts)):
                sub1 = []
                for j in range (len(SrcPts)):
                    sub2 = []
                    for k in range(len(ReflectSrf_p)):
                        if fRayN[i][j][k] is not None:
                            Int = line_srf_intersection(fRayN[i][j][k][0],fRayN[i][j][k][1],ReflectSrf_p[k])
                        else:
                            Int = None


                        if Int is not None:
                            sub2.append(Int)
                        else:
                            sub2.append(None)
                    sub1.append(sub2)
                Pt.append(sub1)
            IntList.append(Pt)

        if gens == n:
            IntList.insert(0,Intersection)
        if gens > 2:
            RecursiveIntersection (Pt, gens-1, IntList)
            #aggiunge tre punti: il primo è la funzione, il secondo è intersection, il terzo è frutto della ricorsione
        return(IntList)

    IntList = []
    RecInt = RecursiveIntersection(Intersection, n, IntList)



    #################################################################################
    ################################ DRAW POLYRAYS ##################################
    #################################################################################


    RList = []
    for i in range (len(TgtPts)):
        Rsub1 = []
        for j in range (len(SrcPts)):
            Rsub2 = []
            for k in range (len(ReflectSrf)**n):
                Rsub3 = []
                for w in range (len(RecInt)):
                    Rsub3.append(RecInt[w][i][j][k])
                Rsub2.append(Rsub3)
            Rsub1.append(Rsub2)
        RList.append(Rsub1)



    for i in range (len(TgtPts)):
        for j in range (len(SrcPts)):
            for k in range (len(RList[0][0])):
                    RList[i][j][k].insert(0,TgtPts[i])
                    RList[i][j][k].append(SrcPts[j])

    polylines = []
    for i in range (len(TgtPts)):
        Plsub1 = []
        for j in range (len(SrcPts)):
            Plsub2 = []
            for k in range (len(RList[0][0])):
                if (None in RList[i][j][k]) == True :
                    Plsub2.append(None)
                else:
                    Plsub2.append(RList[i][j][k]) ############################# Plsub2.append(rs.AddPolyline(RList[i][j][k]))
            Plsub1.append(Plsub2)
        polylines.append(Plsub1) # the list contains a list of vertices



    #########################################cull polylines list for obstacles

    #1 FIND SEGMENTS
    SegmentsList = []
    for i in range (len(TgtPts)):
        SLsub1 = []
        for j in range (len(SrcPts)):
            SLsub2 = []
            for k in range (len(polylines[0][0])):
                if polylines[i][j][k] != None:
                    V_list = polylines[i][j][k]
                    SLsub2.append([[V_list[ind],V_list[ind+1]] for ind in range(len(V_list)) if ind+1 < len(V_list)])  ### SLsub2.append(rs.ExplodeCurves(polylines[i][j][k]))
                else:
                    SLsub2.append(None)
            SLsub1.append(SLsub2)
        SegmentsList.append(SLsub1)


    #2 FIND INTERSECTION COUNT LIST

    SegmentIntlist = []
    for i in range (len(TgtPts)):
        SILsub1 = []
        for j in range (len(SrcPts)):
            SILsub2 = []
            for k in range (len(polylines[0][0])):
                SILsub3 = []
                for w in range (n+1):
                    for x in range (len(ReflectSrf)):
                        if SegmentsList[i][j][k] is not None:
                            Int = line_srf_intersection(SegmentsList[i][j][k][w][0],SegmentsList[i][j][k][w][1],ReflectSrf[x]) # rs.CurveBrepIntersect(SegmentsList[i][j][k][w],ReflectSrf[x])
                        else:
                            Int = None

                        if Int is not None:
                            SILsub3.append(Int)
                        else:
                            SILsub3.append(None)
                SILsub2.append(len(SILsub3) - SILsub3.count(None))
            SILsub1.append(SILsub2)
        SegmentIntlist.append(SILsub1)



    #3 BUILD NEW POLYLINES WITH NEW CONDITION

    polyrays = []
    for i in range (len(TgtPts)):
        Prsub1 = []
        for j in range (len(SrcPts)):
            Prsub2 = []
            for k in range (len(RList[0][0])):
                if (SegmentIntlist[i][j][k]) > (2+2*(n-1)) or (None in RList[i][j][k]) == True:
                    Prsub2.append(None)
                else:
                    Prsub2.append(RList[i][j][k]) ############ add polyline
            Prsub1.append(Prsub2)
        polyrays.append(Prsub1)



    #################################################################################

    time = []
    SPL = []
    for i in range(len(TgtPts)):
        time1 = []
        SPL1 = []
        for j in range(len(SrcPts)):
            time2 = []
            SPL2 = []
            for h in range(len(RList[0][0])):
                if polyrays[i][j][h] != None:
                    time2.append((polyline_length(polyrays[i][j][h]))/343)
                    SPL2.append((111-(20*math.log10(polyline_length(polyrays[i][j][h])-1))-11)*(r**n))
                else:
                    time2.append(None)
                    SPL2.append(None)
            time1.append(time2)
            SPL1.append(SPL2)
        time.append(time1)
        SPL.append(SPL1)
    return (SPL,polyrays)


if Compute == True:
    FINAL = []
    for i in range (len(n)):
        FINAL.append(CodeExecution(n[i]))

    SPL = []
    RAYS = []

    for i in range (len(n)):
        SPL.append(FINAL[i][0])
        RAYS.append(FINAL[i][1])

    a = SPL
    b = RAYS



from geometric_operations import*
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection



fig = plt.figure()
ax = Axes3D(fig)
ax.set_autoscale_on(False)



def from_geo_pts_to_plt_pts(geo_pts):
    plt_pts = np.array(geo_pts)
    plt_pts = plt_pts.transpose()
    x,y,z = plt_pts[0],plt_pts[1],plt_pts[2]
    return [list(zip(x, y, z))]

def from_pts_to_plt_pts(geo_pts):
    plt_pts = np.array(geo_pts)
    plt_pts = plt_pts.transpose()
    x,y,z = plt_pts[0],plt_pts[1],plt_pts[2]
    return x,y,z


# DRAW SOURCES AND TARGETS
s0,s1,s2 = from_pts_to_plt_pts(SrcPts)
r0,r1,r2 = from_pts_to_plt_pts(TgtPts)

ax.scatter3D(s0,s1,s2)
ax.scatter3D(r0,r1,r2, c='r')

# DRAW SURFACES
for srf_pts in ReflectSrf:
    verts = from_geo_pts_to_plt_pts(srf_pts)

    face = Poly3DCollection(verts,linewidths=1)
    face.set_alpha(0.2)
    face.set_facecolor("C0")
    ax.add_collection3d(face)

    ax.add_collection3d(Line3DCollection(verts, colors='k', linewidths=0.5, linestyles='-'))


ray_colors = ['b','g','r','y','k']
# DRAW REFLECTION PATHS
for i in range(len(RAYS)): #n
    for j in range(len(RAYS[i])): #tgt
        for k in range(len(RAYS[i][j])): #src
            for l in range(len(RAYS[i][j][k])): #pts_list
                if RAYS[i][j][k][l] != None:
                    verts = from_geo_pts_to_plt_pts(RAYS[i][j][k][l])

                    ax.add_collection3d(Line3DCollection(verts, colors=ray_colors[i], linewidths=0.5, linestyles='-'))

# initial zoom
dim = 5
ax.set_xlim([-dim, dim])
ax.set_ylim([-dim, dim])
ax.set_zlim([-dim, dim])

# fix aspect ratio

ax.set_aspect('equal')

plt.show()
import math

def distance(pt1, pt2):
    dist = math.sqrt((pt2[0] - pt1[0])**2 + (pt2[1] - pt1[1])**2)
    #print("distance: ", dist)
    return dist

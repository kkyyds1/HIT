import os
import sys
from itertools import product
import ipdb

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(parent_dir)

def define_LRH(H, R, V, I, N, hoist_length, max_tank, min_tank, max_hoist_num, H_Interval):
    LH = {}
    RH = {}

    for r in R:
        for i in range(I[r], N[r]):
            LH[r, i] = max_hoist_num
            RH[r, i] = 1
            for hindex, hinterval in enumerate(H_Interval):
                if V[r, i] in hinterval and V[r, i + 1] in hinterval:
                    if LH[r, i] > hindex + 1:
                        LH[r, i] = hindex + 1
                    if RH[r, i] < hindex + 1:
                        RH[r, i] = hindex + 1
            if RH[r, i] < LH[r, i]:
                RH[r, i] = LH[r, i]
    return LH, RH

def limit_to_range(value, C, TB, lower_bound, upper_bound, RI):
    if RI:
        if TB > 0:
            value = value + C[value] - 1 + TB
        else:
            value = value + TB
    else:
        if TB > 0:
            value = value + C[value] - 1
        else:
            value = value 
            
    return max(lower_bound, min(upper_bound, value))

def is_intersection(V1, V2, C, TB):
    if TB > 0:
        if V1 + C[V1] - 1 +TB >= V2:
            return True
    else:
        if V1 + TB <= V2 + C[V2] - 1:
            return True
    return False

def define_zeta(H, R, N, V, C, D, F, M, I, UP, DOWN, hoist_length, W, RIUJ, H_Interval, Gear, Segments, HoistLaunchDuration, HoistTerminateDuration):
    zeta = {}
    beta = hoist_length
    for r, i, u, j in RIUJ:
        for g, h in product(H, H):
            theta = g - h
            TB = theta * beta

            try:            
                if V[r, i] not in H_Interval[h - 1] or V[r, i + 1] not in H_Interval[h - 1] or \
                        V[u, j] not in H_Interval[g - 1] or V[u, j + 1] not in H_Interval[g - 1]:
                    continue
            except:
                ipdb.set_trace()

            if (h in Gear or g in Gear):
                continue

            for seg in Segments:
                if V[r, i] in seg and V[u, j] in seg:
                    break
            else:
                continue
            
            if theta == 0:
                zeta[r, i, u, j, theta] = D[r, i] + F[V[r, i + 1], V[u, j]]
                continue
            
            RITB = limit_to_range(V[r, i], C, TB, min(W), max(W), True)
            RITB1 = limit_to_range(V[r, i + 1], C, TB, min(W), max(W), True)
            UJTB = limit_to_range(V[u, j], C, TB, min(W), max(W), False)
            UJTB1 = limit_to_range(V[u, j + 1], C, TB, min(W), max(W), False)
            
            # a, d
            if (theta < 0 and V[r, i] > V[r, i + 1] and is_intersection(V[r, i + 1], V[u, j], C, TB)) or \
            (theta > 0 and V[r, i] < V[r, i + 1] and is_intersection(V[r, i + 1], V[u, j], C, TB)) or \
            (theta > 0 and V[r, i] > V[r, i + 1] and is_intersection(V[r, i + 1], V[u, j], C, TB)) or \
            (theta < 0 and V[r, i] < V[r, i + 1] and is_intersection(V[r, i + 1], V[u, j], C, TB)):
                # zeta[r, i, u, j, theta] = D[r, i] + F[V[r, i + 1] + TB, V[u, j]]
                zeta[r, i, u, j, theta] = D[r, i] + abs(RITB1 - UJTB) + (HoistLaunchDuration + HoistTerminateDuration) + 3
            
            # b, g, h
            elif (theta < 0 and V[r, i] > V[r, i + 1] and V[u, j] < V[u, j + 1] and is_intersection(V[r, i + 1], V[u, j + 1], C, TB) and not is_intersection(V[r, i + 1], V[u, j], C, TB)) or \
                (theta > 0 and V[r, i] < V[r, i + 1] and V[u, j] > V[u, j + 1] and not is_intersection(V[r, i + 1], V[u, j], C, TB) and not is_intersection(V[r, i + 1], V[u, j], C, TB)) or \
                (theta > 0 and V[r, i] > V[r, i + 1] and V[u, j] > V[u, j + 1] and is_intersection(V[r, i + 1], V[u, j], C, TB) and is_intersection(V[r, i + 1], V[u, j + 1], C, TB) and UP[u, j] <= DOWN[r, i]) or \
                (theta < 0 and V[r, i] < V[r, i + 1] and V[u, j] < V[u, j + 1] and is_intersection(V[r, i], V[u, j], C, TB) and is_intersection(V[r, i + 1], V[u, j + 1], C, TB) and UP[u, j] <= DOWN[r, i]) or \
                (theta > 0 and V[r, i] > V[r, i + 1] and V[u, j] > V[u, j + 1] and not is_intersection(V[r, i], V[u, j], C, TB) and is_intersection(V[r, i + 1], V[u, j + 1], C, TB)) or \
                (theta < 0 and V[r, i] < V[r, i + 1] and V[u, j] < V[u, j + 1] and not is_intersection(V[r, i], V[u, j], C, TB) and is_intersection(V[r, i + 1], V[u, j + 1], C, TB)):
                
                # zeta[r, i, u, j, theta] = D[r, i] - F[V[r, i + 1] + TB, V[u, j]]
                zeta[r, i, u, j, theta] = D[r, i] - abs(RITB1 - UJTB) - (HoistLaunchDuration + HoistTerminateDuration) - UP[u, j]
                if V[r, i + 1] != V[u, j + 1]:
                    zeta[r, i, u, j, theta] += HoistLaunchDuration + 3

            # c, j
            elif (theta < 0 and max(V[u, j], V[u, j + 1]) <= min(V[r, i + 1], V[r, i]) + TB) or \
                (theta > 0 and min(V[u, j], V[u, j + 1]) >= max(V[r, i + 1], V[r, i]) + TB):

                zeta[r, i, u, j, theta] = -M

            # e, f
            elif (theta < 0 and V[r, i] < V[r, i + 1] and V[u, j] < V[u, j + 1] and is_intersection(V[r, i], V[u, j], C, TB) and not is_intersection(V[r, i + 1], V[u, j + 1], C, TB)) or \
                (theta > 0 and V[r, i] > V[r, i + 1] and V[u, j] > V[u, j + 1] and is_intersection(V[r, i], V[u, j], C, TB) and not is_intersection(V[r, i + 1], V[u, j + 1], C, TB)) or \
                (theta > 0 and V[r, i] > V[r, i + 1] and V[u, j] > V[u, j + 1] and is_intersection(V[r, i], V[u, j], C, TB) and not is_intersection(V[r, i + 1], V[u, j], C, TB) and is_intersection(V[r, i + 1], V[u, j + 1], C, TB)) and UP[u, j] >= DOWN[r, i] or \
                (theta < 0 and V[r, i] < V[r, i + 1] and V[u, j] < V[u, j + 1] and is_intersection(V[r, i], V[u, j], C, TB) and not is_intersection(V[r, i + 1], V[u, j], C, TB) and is_intersection(V[r, i + 1], V[u, j + 1], C, TB)) and UP[u, j] >= DOWN[r, i] or \
                (theta < 0 and V[r, i] < V[r, i + 1] and V[u, j] > V[u, j + 1] and is_intersection(V[r, i], V[u, j], C, TB) and is_intersection(V[r, i], V[u, j + 1], C, TB) and not is_intersection(V[r, i + 1], V[u, j], C, TB)) or \
                (theta < 0 and V[r, i] < V[r, i + 1] and V[u, j] > V[u, j + 1] and is_intersection(V[r, i], V[u, j], C, TB) and not is_intersection(V[r, i], V[u, j + 1], C, TB) and not is_intersection(V[r, i + 1], V[u, j], C, TB)) or \
                (theta > 0 and V[r, i] > V[r, i + 1] and V[u, j] < V[u, j + 1] and is_intersection(V[r, i], V[u, j], C, TB) and is_intersection(V[r, i], V[u, j + 1], C, TB) and not is_intersection(V[r, i + 1], V[u, j], C, TB)) or \
                (theta > 0 and V[r, i] > V[r, i + 1] and V[u, j] < V[u, j + 1] and is_intersection(V[r, i], V[u, j], C, TB) and not is_intersection(V[r, i], V[u, j + 1], C, TB) and not is_intersection(V[r, i + 1], V[u, j], C, TB)):
                
                # zeta[r, i, u, j, theta] = UP[r, i] + F[V[r, i] + TB, V[u, j]]
                zeta[r, i, u, j, theta] = UP[r, i] + abs(RITB - UJTB) + (HoistLaunchDuration + HoistTerminateDuration) + 3

            # i
            elif (theta > 0 and V[r, i] > V[r, i + 1] and V[u, j] > V[u, j + 1] and is_intersection(V[r, i], V[u, j + 1], C, TB) and not is_intersection(V[r, i], V[u, j], C, TB) and not is_intersection(V[r, i + 1], V[u, j + 1], C, TB)) or \
                (theta < 0 and V[r, i] < V[r, i + 1] and V[u, j] < V[u, j + 1] and is_intersection(V[r, i], V[u, j + 1], C, TB) and not is_intersection(V[r, i], V[u, j], C, TB) and not is_intersection(V[r, i + 1], V[u, j + 1], C, TB)):
                
                
                zeta[r, i, u, j, theta] = UP[r, i] - abs(RITB - UJTB) + (HoistLaunchDuration + HoistTerminateDuration) - UP[u, j]
                if V[r, i + 1] != V[u, j + 1]:
                    zeta[r, i, u, j, theta] += HoistLaunchDuration + 3
            
            else:
                ipdb.set_trace()
    return zeta
import numpy as np
from math import radians, sin, cos, sqrt, atan2
import random

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance

coords = {
    "Jodhpur": (26.2389, 73.0243),"Udaipur": (24.5854, 73.7125),"Jaisalmer": (26.9157, 70.9083),"Mount Abu": (24.5937, 72.7156),
    "Ajmer": (26.4499, 74.6399),"Jaipur": (26.9124, 75.7873),"Pushkar": (26.4877, 74.5511),
    "Bikaner": (28.0229, 73.3119),
    "Chittorgarh": (24.8887, 74.6269),
    "Ranthambore": (26.0173, 76.5026),
    "Alwar": (27.5667, 76.6250),
    "Bharatpur": (27.2173, 77.4901),
    "Bundi": (25.4305, 75.6499),
    "Kumbhalgarh": (25.1478, 73.5982),
    "Neemrana": (27.9885, 76.3844),
    "Kota": (25.2138, 75.8648),
    "Shekhawati": (27.6000, 75.3000),
    "Mandawa": (28.0566, 75.1413),
    "Sikar": (27.6094, 75.1399),
    "Ranakpur": (25.1105, 73.4763),
    "Churu": (28.3042, 74.9670), 
    "Barmer": (25.7500, 71.4000) 
}

N = len(coords)
location_names = list(coords.keys())
D = np.zeros((N, N))

for i in range(N):
    for j in range(i + 1, N):
        lat1, lon1 = coords[location_names[i]]
        lat2, lon2 = coords[location_names[j]]
        dist = haversine(lat1, lon1, lat2, lon2)
        D[i][j] = dist
        D[j][i] = dist

def cost_tour(tour, D):
    cost = 0
    for i in range(len(tour) - 1):
        cost += D[tour[i], tour[i + 1]]
    cost += D[tour[-1], tour[0]]
    return cost

def sim_ann(D, iter_max=500000, Tm=1000):
    N = len(D)
    s = np.random.permutation(N)
    s_init = np.copy(s)
    ds = cost_tour(s, D)
    d = [ds]

    for i in range(1, iter_max + 1):
        id1, id2 = sorted(random.sample(range(N), 2))
        s_next = np.copy(s)
        s_next[id1:id2 + 1] = s_next[id1:id2 + 1][::-1]
        ds_next = cost_tour(s_next, D)
        E = ds - ds_next
        T = Tm / i
        if E > 0 or random.random() < 1 / (1 + np.exp(-E / T)):
            s = s_next
            ds = ds_next
        d.append(ds)
    
    return s, d

opt_tour, tour_costs = sim_ann(D)
opt_tour_names = [location_names[i] for i in opt_tour]

print("Optimal Tour:", opt_tour_names)
print("Tour Distance (Cost):", tour_costs[-1])

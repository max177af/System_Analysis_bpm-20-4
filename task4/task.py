import numpy as np

def task():
    totals, products = set(), set()
    for i in range(1, 7):
        for j in range(1, 7):
            totals.add(i + j)
            products.add(i * j)
    
    totals, products = sorted(totals), sorted(products)
    totals_l = {s: totals.index(s) for s in totals}
    products_l = {p: products.index(p) for p in products}
    counts = np.zeros((len(totals), len(products)))
    for i in range(1, 7):
        for j in range(1, 7):
            counts[totals_l[i + j], products_l[i * j]] += 1
    
    pbs = counts / 36
    e_AB = -np.sum(pbs * np.log2(pbs, where=np.abs(pbs) > 0.0001))
    pbs_A = np.sum(pbs, axis=1)
    e_A = -np.sum(pbs_A * np.log2(pbs_A, where=np.abs(pbs_A) > 0.0001))
    pbs_B = np.sum(pbs, axis=0)
    e_B = -np.sum(pbs_B * np.log2(pbs_B, where=np.abs(pbs_B) > 0.0001))
    e_A_B = e_AB - e_A  
    inf_AB = e_B - e_A_B   
   
    names = ["H(AB)", "H(A)", "H(B)", "HA(B)","INF(AB)"]
    values = [e_AB, e_A, e_B, e_A_B, inf_AB]

    return {ind:val for (ind, val) in zip(names, values)}

print(task())

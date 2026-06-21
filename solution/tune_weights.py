import json
import os
import random

from .import config as c

def g_t(n=10):
    d=os.path.join(c.r_d,"solution","weight_trials")
    os.makedirs(d,exist_ok=True)
    m=[]

    for i in range(n):
        w = {
            "skl": round(random.uniform(0.01, 0.15), 2),
            "prd": round(random.uniform(0.30, 0.50), 2),
            "exp": round(random.uniform(0.20, 0.45), 2),
            "beh": round(random.uniform(0.10, 0.25), 2),
            "loc": round(random.uniform(0.00, 0.10), 2),
            "not": 0.0
        }
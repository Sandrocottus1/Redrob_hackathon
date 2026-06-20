import argparse
import time
import json
import pandas as pd
from . import pipeline as p
from . import config as c

def m():
    a=argparse.ArgumentParser()
    a.add_argument("--out", type=str, default=None)
    a.add_argument("--model" ,type=str, default=c.d_m)
    a.add_argument("--retrieval_k", type=int,default=c.r_k)
    a.add_argument("--rerank_pool_k",type=int,default=c.r_p_k)
    g=a.parse_args()

    r_i=int(time.time())#unix like timestamp to make filenames unique
    o_f=g.out if g.out else f"sub_{r_i}.csv"#decinding output file

    p_f=f"prms_{r_i}.json"

    c.d_m=g.model
    d_p={
        "r_i":r_i, "o_f":o_f,"mod":g.model,
        "r_k":g.retrieval_k,"rp_k":g.rerank_pool_k,
        "d_w":c.d_w,"b_w":c.b_w,"f_w":c.f_w
    }
    with open(p_f,'w') as f:
        json.dump(d_p,f,indent=2)

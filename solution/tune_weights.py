import json
import os
import random

from .import config as c

def g_t(n=10):#for generating n=10 weight trials
    d=os.path.join(c.r_d,"solution","weight_trials")#creating outut directory
    os.makedirs(d,exist_ok=True)
    m=[]

    for i in range(n):
        w = {#generating n random wiehgts
            "skl": round(random.uniform(0.01, 0.15), 2),#skill score
            "prd": round(random.uniform(0.30, 0.50), 2),#production score
            "exp": round(random.uniform(0.20, 0.45), 2),#expeirence score
            "beh": round(random.uniform(0.10, 0.25), 2),#behavioral score
            "loc": round(random.uniform(0.00, 0.10), 2),#location score
            "not": 0.0
        }


        s=sum(w.values())
        w={k:round(v/s,3) for k,v in w.items()}#score normalization

        t={"id":i,"w":w}
        p=os.path.join(d,f"t_{i}.json")

        with open(p,'w') as f:
            json.dump(t,f,indent=2)
        m.append(p)#saving path in manifest

    #creating manifest file
    with open(os.path.join(d,"m.json"),'w')as f:
        json.dump(m,f,indent=2)

if __name__=="__main__":
    g_t()
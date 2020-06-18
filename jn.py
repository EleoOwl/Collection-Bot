import os
import json

def NewDir(name):
    
    if not os.path.exists(name):
        os.makedirs(name)


def  StrToJson(str, file):
    
    d = json.loads(str)
    with open(file, 'w') as f:
      json.dump(d,f, ensure_ascii=False, indent=2)

def  ObjToJson(ob, file): 
    
    with open(file, 'w') as f:
      json.dump(ob,f, ensure_ascii=False, indent=2)

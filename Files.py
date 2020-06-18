def inF(a, name):
    with open(name, "r") as f:
      for line in f:
          if a==int(line):
            return True
          
      return False

def addF(a,name):
    f = open(name, "a")
    f.writelines(str(a)+"\n")
    f.close()

def AddFn(a,name):
    f = open(name, "a")
    f.writelines(str(a))
    f.close()

def WriteF(name):
    f = open(name, "r")
    for line in f:
         print(line)

def Create(name):
    f=open(name,"x")
    f.close()


def ToStr(name):
     f = open(name, "r")
     for line in f:
         return(line)

def strArr(name):
    a={}
    f = open(name, "r")
    for line in f:
        a.add(line)
    return a
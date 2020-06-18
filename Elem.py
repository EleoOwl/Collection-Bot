class Elem(object):
   def __init__(self, num, name, desc, image):
        self.name = name 
        self.name=num
        self.desc=desc
        self.image=image
   
   def toJstr(self):
       return(
           "{\""+str(self.name)+":"+"\""+str(self.desk)+"\",\""+str(self.image)+"\"}"
           )





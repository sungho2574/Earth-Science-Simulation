
from vpython import *





class Setting ():
    
    
    def __init__ (self):
        self.speedd()

    
    def set_speed (self, s):
        print(s.value)
    
    def speedd (self):
        MIN = 5
        MAX = 1000
        VAL = 100
        
        slider(min=MIN, max=MAX, value=VAL, length=220, bind=self.set_speed, right=15)
        #wtext('\n\n')


testing = Setting()







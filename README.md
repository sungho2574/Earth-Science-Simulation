# Earth Science Simulation
This project is based on Korean Earth Science Curriculum.
 
 `rotation-of-common-mass-center.py` : The two bodies orbit around a center of common mass. You can simulate **eclipses** and **radial velocity** which is the key point of *Exploration of extraterrestrial planets.*
 
 `kepler-law-tv-rv.py` : There are five planets that follow Kepler's law. You can check the **tangential velocity** and **radial velocity** when looking at another planet from one planet.
 
 
 ## How to Use
 Modify the code as below. The code works best in GlowScript.
 
 * [GlowScript](https://glowscript.org/)
```Python
GlowScript 3.2 VPython

# for vsc
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
#from vpython import *
#from vpython.no_notebook import stop_server
#print_anchor = scene.caption_anchor
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 

...

# for vsc
# stop_server()
```

 * Visual Studio Code or etc
```Python
#GlowScript 3.2 VPython

# for vsc
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
from vpython import *
from vpython.no_notebook import stop_server
print_anchor = scene.caption_anchor
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 

...

# for vsc
stop_server()
```

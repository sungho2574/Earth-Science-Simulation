#GlowScript 3.2 VPython



from numpy import datetime_data
from vpython import *
from vpython.no_notebook import stop_server


exit = False

def B(b):
    #stop_server()
    global exit
    exit = True
    print(exit)
    return

button( bind=B, text='Click me!' )

G = 6.7e-11

sun = sphere(pos=vec(0, 0, 0), radius=2e10, mass=2e30, color=color.red)



PLANET_NUM = 1
planets = []

for i in range(PLANET_NUM):
    planets.append(sphere(pos=vec((random()+i+1)*1e11, 0, 0), radius=0.5e10, mass=1e30, p=vec(0, 0, random()*-1e4), color=color.white, make_trail = True))



dt = 1e5
while True:
    rate(500)

    for p in planets:    
        r = sun.pos - p.pos 
        F = G * sun.mass * p.mass * r.hat / mag2(r)

        p.p += F*dt
        p.pos += (p.p/p.mass) * dt


    if (exit == True):
        #stop_server()
        break

# label
# ===============================================================================
start_checked  = 0
arrive_checked = 0

def set_start ():
    global chb_start
    global start_checked

    checked = []
    for c in chb_start:
        if c.checked:
            checked.append(True)
        
        else:
            checked.append(False)
    
    checked[start_checked] = False

    for i, c in enumerate(checked):
        chb_start[i].checked = c
        
        if c:
            start_checked = i

def set_arrive ():
    global chb_arrive
    global arrive_checked

    checked = []
    for c in chb_arrive:
        if c.checked:
            checked.append(True)
        
        else:
            checked.append(False)
    
    checked[arrive_checked] = False

    for i, c in enumerate(checked):
        chb_arrive[i].checked = c
        
        if c:
            arrive_checked = i

scene.append_to_caption('start:\t\t')

chb_start = []
for i in range(5):
    chb_start.append(radio(text='{:}        '.format(i+1), checked=False, bind=set_start))

chb_start[0].checked = True
scene.append_to_caption('\n\n')


scene.append_to_caption('arrive:\t\t')

chb_arrive = []
for i in range(5):
    chb_arrive.append(radio(text='{:}        '.format(i+1), checked=False, bind=set_arrive))

chb_arrive[0].checked = True
scene.append_to_caption('\n\n')



button(text='Apply', bind=ex)

scene.append_to_caption('\n\n')



start_planet = 1
end_planet = 1


def rt_v ():
    s = planets[start_checked].p / planets[start_checked].mass
    e = planets[start_checked].p / planets[arrive_checked].mass

    v = e - s       # relative velocity

    axis = planets[arrive_checked].pos - planets[start_checked].pos

    radial_v     = dot(v, axis.norm())
    tangential_v = v - radial_v*axis.norm()

    return radial_v, tangential_v
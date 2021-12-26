#GlowScript 3.2 VPython

from vpython import *
from vpython.no_notebook import stop_server

print_anchor = scene.caption_anchor


scene.width  = 1000
scene.height = 400
scene.title = "<b>tangential v & radial v\n\n</b>"

G = 6.7e-11



# sun / planets
sun   = sphere(pos=vec(0, 0, 0), radius=2e10, m=2e30, color=color.red)

PLANET_NUM = 5
planets = []

x = [1e11, 1.8e11, 3.4e11, 4.1e11, 5.5e11]

r = [0.6e10, 0.5e10, 0.7e10, 1.5e10, 0.7e10]

m = [1e30, 5e30, 10e30, 1e10, 10e10]

v = [3e4, 2e4, 1.4e4, 1.6e4, 1.7e4]

for i in range(PLANET_NUM):
    planets.append(sphere(pos=vec(x[i], 0, 0), radius=r[i], m=m[i], p=vec(0, 0, -v[i])*m[i], color=color.white, make_trail = True))    



# arrow
radial_arrow = arrow(pos=vec(0, 0, 0), axis=vec(0, 0, 0), shaftwidth=0.02e11, headwidth=2.5e10, headlength=4e10, color=color.yellow)




# Exit
# ===============================================================================
exit = False

def ex(b):
    global exit
    exit = True
    print(exit)
    return

button(text='Exit', pos=scene.title_anchor, bind=ex)




# Run / Pause
# ===============================================================================
running = True

def run(b):
    global running
    
    running = not running
    
    if running:
        b.text = "Pause"
    
    else: 
        b.text = "Run"

button(text="Pause", pos=scene.title_anchor, bind=run)



# ===============================================================================
#                                   setting
# ===============================================================================
def put_text (text):
    wtext(pos=print_anchor, text=text)




# speed
# ===============================================================================
MIN = 5
MAX = 200
VAL = 10
speed = VAL

put_text('\nspeed: ')

def set_speed (s):
    global speed
    speed = s.value

slider(pos=print_anchor, min=MIN, max=MAX, value=VAL, length=220, bind=set_speed, right=15)

put_text('\n\n')




# label
# ===============================================================================
start_checked = 0
end_checked   = 0

start_planet = 0
end_planet   = 0

def set_aim (r):
    global start_checked
    global end_checked

    id = int(r.text) - 1

    if r.name == 'start':
        start_checked = id
    
    else:
        end_checked = id

def apply (b):
    global start_planet
    global end_planet

    # apply when the button pushed
    start_planet = start_checked
    end_planet   = end_checked
 
    global time
    time = 0
    
    g1.delete()
    g2.delete()



# start
put_text('start:\t\t')

start_radios = []
for i in range(PLANET_NUM):
    start_radios.append(radio(pos=print_anchor, text='{:}        '.format(i+1), checked=False, bind=set_aim, name='start'))

put_text('\n\n')


# end
put_text('end:\t\t\t')

end_radios = []
for i in range(PLANET_NUM):
    end_radios.append(radio(pos=print_anchor, text='{:}        '.format(i+1), checked=False, bind=set_aim, name='end'))

start_radios[0].checked = True
end_radios[0].checked   = True


button(pos=print_anchor, text='Apply', bind=apply)
put_text('\n\n\n')




# graph
# ===============================================================================
def rt_v ():
    s = planets[start_planet].p / planets[start_planet].m
    e = planets[end_planet].p / planets[end_planet].m
    r_axis = planets[end_planet].pos - planets[start_planet].pos        # radial velocity basis axis

    v = e - s                                               # relative velocity
    
    radial_v = dot(v, r_axis.norm())

    t_axis = vec(-r_axis.z, 0, r_axis.x)                    # tangential velocity basis axis (ccw)
    tangential_v = v - radial_v*r_axis.norm()          
    tangential_v = dot(tangential_v, t_axis.norm())         # caculate t_v on t_axis

    return tangential_v, radial_v

time = 0

f1 = graph(width=600, height=200, title='tangential velocity')
g1 = gcurve(graph=f1, color=color.red)

f2 = graph(width=600, height=200, title='radial velocity')
g2 = gcurve(graph=f2, color=color.blue)




# ===============================================================================
#                                     main
# ===============================================================================
dt = 1e5
while True:
    rate(speed)

    if running:
        for p in planets:
            r = sun.pos - p.pos 
            F = G * sun.m * p.m * r.hat / mag2(r)

            p.p += F*dt
            p.pos += (p.p/p.m) * dt
        

        # arrow
        radial_arrow.pos  = planets[start_planet].pos
        radial_arrow.axis = planets[end_planet].pos - planets[start_planet].pos


        # graph
        tv, rv = rt_v()
        
        g1.plot(time, tv)
        g2.plot(time, rv)
        
        time += 1

    if (exit == True):
        break

stop_server()
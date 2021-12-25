#GlowScript 3.2 VPython

from vpython import *
from vpython.no_notebook import stop_server

scene.width  = 800
scene.height = 400
scene.title  = "<b>revolution</b>\n\n"

G = 6.7e-11



# star / planet
star   = sphere(pos=vec(-1e11, 0, 0),  radius=2e10, color=color.yellow, make_trail=True)
planet = sphere(pos=vec(1.5e11, 0, 0), radius=1e10, color=color.white,  make_trail=True)

star.mass   = 2e30
planet.mass = 1e30

star.p   = vec(0, 0, -1e4) * star.mass
planet.p = -star.p



# visual effect
star_to_planet = label(pos=vec(1e11, 3e11, 0), text="별-행성 거리: ",   height=15,              visible=False)
cent_to_star   = label(pos=star.pos,           text="중심-별 거리: ",   height=15, yoffset=100, visible=False)
cent_to_planet = label(pos=planet.pos,         text="중심-행성 거리: ", height=15, yoffset=100, visible=False)

star_v   = label(pos=star.pos,   text="속력: ", height=15, yoffset=70, visible=False)
planet_v = label(pos=planet.pos, text="속력: ", height=15, yoffset=70, visible=False)

light = local_light(pos=star.pos, color=star.color)
center = sphere(pos=vec(-0.16e11, 0, 0), radius=0.3e10, color=color.yellow)



# arrow
star_v_arrow   = attach_arrow(star,   "p", scale=1e7/star.mass/2,   shaftwidth=0.3e10, headwidth=0.6e10, headlength=0.6e10, color=color.green)
planet_v_arrow = attach_arrow(planet, "p", scale=1e7/planet.mass/2, shaftwidth=0.3e10, headwidth=0.6e10, headlength=0.6e10, color=color.green)

star_v_arrow.stop()
planet_v_arrow.stop()

star_rv_arrow   = arrow(pos=vec(0, 0, 0), axis=vec(0, 0, 0), visible=False)
planet_rv_arrow = arrow(pos=vec(0, 0, 0), axis=vec(0, 0, 0), visible=False)

star_v0 = arrow(pos=vec(0, 0, 0), axis=vec(0, 0, 0), color=color.red, visible=False)

SCALE = 4e10
x_axis = arrow(pos=vec(0, 0, 0), axis=vec(SCALE, 0, 0),  color=color.white, visible=False)
y_axis = arrow(pos=vec(0, 0, 0), axis=vec(0, SCALE, 0),  color=color.white, visible=False)
z_axis = arrow(pos=vec(0, 0, 0), axis=vec(0, 0, -SCALE), color=color.red,   visible=False)



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
    global star_v0
    
    global star_to_planet 
    global cent_to_star   
    global cent_to_planet         
    global star_v
    global planet_v
    
    global star_v_arrow
    global planet_v_arrow
    global star_rv_arrow
    global planet_rv_arrow
    
    running = not running
    
    if running:
        b.text = "Pause"
        star_v0.visible = False
        
        # label
        if chk_label.checked:
            star_to_planet.visible = True
            cent_to_star.visible   = True
            cent_to_planet.visible = True
            star_v.visible         = True
            planet_v.visible       = True
        
        # v arrow
        if chk_v.checked:
            star_v_arrow.start()
            planet_v_arrow.start()
        
        # rv arrow
        if chk_rv.checked:
            star_rv_arrow.visible   = True
            planet_rv_arrow.visible = True
    
    else: 
        b.text = "Run"

button(text="Pause", pos=scene.title_anchor, bind=run)




# Apply
# ===============================================================================
def set_v (v, ang):
    x = v * cos(radians(ang-90))
    z = v * sin(radians(ang-90))
    
    return vec(x, 0, z)

def apply (b):
    global running
    global star_to_planet 
    global cent_to_star   
    global cent_to_planet         
    global star_v
    global planet_v
    
    global star_v_arrow
    global planet_v_arrow
    global star_rv_arrow
    global planet_rv_arrow
    
    
    # erase prior star system
    star.clear_trail()
    planet.clear_trail()
    
    star_to_planet.visible = False
    cent_to_star.visible   = False
    cent_to_planet.visible = False
    star_v.visible         = False
    planet_v.visible       = False
    
    star_v_arrow.visible    = False
    planet_v_arrow.visible  = False
    star_rv_arrow.visible   = False
    planet_rv_arrow.visible = False
    
    star_v_arrow.stop()
    planet_v_arrow.stop()

    g1.delete()
    g2.delete()


    # set new star system
    dist = sld_dist.value
    star.pos   = vec(-dist*2/5, 0, 0)
    planet.pos = vec( dist*3/5, 0, 0)

    star.radius   = sld_star_r.value
    planet.radius = sld_planet_r.value

    star.mass   = sld_star_m.value
    planet.mass = sld_planet_m.value
    
    center.pos = vec(star.pos.x  +  dist * planet.mass / (star.mass + planet.mass), 0, 0)
    light.pos = star.pos
    
    
    # set v
    star.p   = set_v(sld_star_v.value, sld_star_ang.value)     * star.mass
    planet.p = set_v(sld_planet_v.value, sld_planet_ang.value) * planet.mass
        
    
    # apply v arrow
    SCALE = 1e7/2
    if not running:
        star_v0.visible = True
        star_v0.pos     = star.pos
        star_v0.axis    = vec(x, 0, z) * SCALE

button(text="Apply", pos=scene.title_anchor, bind=apply)




# setting
# ===============================================================================
scene.append_to_caption('<b>setting</b>\n\n')



# speed
# ===============================================================================
MIN = 5
MAX = 1000
VAL = 100
speed = VAL

scene.append_to_caption('speed: ')

def set_speed (s):
    global speed
    speed = s.value

slider(min=MIN, max=MAX, value=VAL, length=220, bind=set_speed, right=15)

scene.append_to_caption('\n\n')




# label
# ===============================================================================
DEFAULT = False

def set_label(r):
    global star_to_planet 
    global cent_to_star   
    global cent_to_planet         
    global star_v   
    global planet_v
    
    if r.checked:
        star_to_planet.visible = True
        cent_to_star.visible   = True
        cent_to_planet.visible = True
        star_v.visible         = True
        planet_v.visible       = True

    else:
        star_to_planet.visible = False
        cent_to_star.visible   = False
        cent_to_planet.visible = False
        star_v.visible         = False
        planet_v.visible       = False

chk_label = checkbox(text='label', checked=DEFAULT, bind=set_label)

scene.append_to_caption('\n\n')




# velocity arrow
# ===============================================================================
DEFAULT = False

def set_v_arrow(r):
    global star_v_arrow
    global planet_v_arrow

    if r.checked:
        star_v_arrow.start()
        planet_v_arrow.start()

    else:
        star_v_arrow.stop()
        planet_v_arrow.stop()
    
chk_v = checkbox(text='velocity arrow', checked=DEFAULT, bind=set_v_arrow)

scene.append_to_caption('\n\n')




# radial velocity arrow
# ===============================================================================
DEFAULT = False
SCALE = 1e7/2

def draw_raial_v (ball, arrow):
    arrow.pos = ball.pos
    arrow.axis = vec(0, 0, ball.p.z/ball.mass) * SCALE

    if (arrow.axis.z > 0):
        arrow.color = color.blue
    
    else:
        arrow.color = color.red

def set_rv_arrow(r):
    global star_rv_arrow
    global planet_rv_arrow

    if r.checked:
        star_rv_arrow.visible   = True
        planet_rv_arrow.visible = True

    else:
        star_rv_arrow.visible  = False
        planet_rv_arrow.visible = False

def set_rv_arrow_size (r):
    global SCALE

    if r.checked:
        SCALE = 1e8/2
    
    else:
        SCALE = 1e7/2

chk_rv = checkbox(text='radial velocity arrow      ', checked=DEFAULT, bind=set_rv_arrow)

checkbox(text='bigger', checked=DEFAULT, bind=set_rv_arrow_size)

scene.append_to_caption('\n\n')




# coordinate axis
# ===============================================================================
DEFAULT = False

def set_coor_axis (r):
    if r.checked:
        x_axis.visible = True
        y_axis.visible = True
        z_axis.visible = True
    
    else:
        x_axis.visible = False
        y_axis.visible = False
        z_axis.visible = False

checkbox(text='coordinate axis', checked=DEFAULT, bind=set_coor_axis)

scene.append_to_caption('\n\n\n')




# star and planet
# ===============================================================================
scene.append_to_caption('<b>new star system</b>\n\n')



# distance between the two planets
# ===============================================================================
MIN  = 1e11
MAX  = 4e11
STEP = 0.1e11
VAL  = 2.5e11

scene.append_to_caption('distance: ')

def set_dist (s):
    wt_dist.text = '{:e}'.format(s.value/1000)

sld_dist = slider(min=MIN, max=MAX, step=STEP, value=VAL, length=220, bind=set_dist, right=15)
wt_dist = wtext(text='{:e}'.format(sld_dist.value/1000))
scene.append_to_caption(' km')

scene.append_to_caption('\n\n')




# v
# ===============================================================================
MIN = 0.5e4
MAX = 3e4
VAL1 = 1e4
VAL2 = 1e4 * 2


scene.append_to_caption('star:\t\tv\t= ')

def set_star_v (s):
    wt_star_v.text = '{:e}'.format(s.value/1000*3600)

sld_star_v = slider(min=MIN, max=MAX, value=VAL1, length=220, bind=set_star_v, right=15)
wt_star_v = wtext(text='{:e}'.format(sld_star_v.value/1000*3600))
scene.append_to_caption(' km/h')


scene.append_to_caption('\t\t')
scene.append_to_caption('planet:\t\tv\t= ')


def set_planet_v (s):
    wt_planet_v.text = '{:e}'.format(s.value/1000*3600)

sld_planet_v = slider(min=MIN, max=MAX, value=VAL2, length=220, bind=set_planet_v, right=15, disabled=True)
wt_planet_v = wtext(text='{:e}'.format(sld_planet_v.value/1000*3600))
scene.append_to_caption(' km/h')

scene.append_to_caption('\n\n')




# ang
# ===============================================================================
MIN  = 0
MAX  = 360
STEP = 1
VAL1 = 0
VAL2 = 180

scene.append_to_caption('\t\tang\t= ')

def set_star_ang (s):
    wt_star_ang.text = '{:03.0f}'.format(s.value)

sld_star_ang = slider(min=MIN, max=MAX, step=STEP, value=VAL1, length=220, bind=set_star_ang, right=15)
wt_star_ang = wtext(text='{:03.0f}'.format(sld_star_ang.value))
scene.append_to_caption(' degree')


scene.append_to_caption('\t\t')
scene.append_to_caption('\t\t\t\t\tang\t= ')


def set_planet_ang (s):
    wt_planet_ang.text = '{:03.0f}'.format(s.value)

sld_planet_ang = slider(min=MIN, max=MAX, step=STEP, value=VAL2, length=220, bind=set_planet_ang, right=15, disabled=True)
wt_planet_ang = wtext(text='{:03.0f}'.format(sld_planet_ang.value))
scene.append_to_caption(' degree')

scene.append_to_caption('\n\n')




# m
# ===============================================================================
MIN  = 0.5e30
MAX  = 4e30
STEP = 0.1e30
VAL1 = 2e30
VAL2 = 1e30

scene.append_to_caption('\t\tm\t= ')

def set_star_m (s):
    wt_star_m.text = '{:e}'.format(s.value/1000)

sld_star_m = slider(min=MIN, max=MAX, step=STEP, value=VAL1, length=220, bind=set_star_m, right=15)
wt_star_m = wtext(text='{:e}'.format(sld_star_m.value/1000))
scene.append_to_caption(' Ton')


scene.append_to_caption('\t\t')
scene.append_to_caption('\t\t\tm\t= ')


def set_planet_m (s):
    wt_planet_m.text = '{:e}'.format(s.value/1000)

sld_planet_m = slider(min=MIN, max=MAX, step=STEP, value=VAL2, length=220, bind=set_planet_m, right=15)
wt_planet_m = wtext(text='{:e}'.format(sld_planet_m.value/1000))
scene.append_to_caption(' Ton')

scene.append_to_caption('\n\n')




# r
# ===============================================================================
MIN  = 0.5e10
MAX  = 4e10
STEP = 0.1e10
VAL1 = 2e10
VAL2 = 1e10

scene.append_to_caption('\t\tr\t= ')

def set_star_r (s):
    wt_star_r.text = '{:e}'.format(s.value/1000)

sld_star_r = slider(min=MIN, max=MAX, step=STEP, value=VAL1, length=220, bind=set_star_r, right=15)
wt_star_r = wtext(text='{:e}'.format(sld_star_r.value/1000))
scene.append_to_caption(' km')


scene.append_to_caption('\t\t')
scene.append_to_caption('\t\t\t\tr\t= ')


def set_planet_r (s):
    wt_planet_r.text = '{:e}'.format(s.value/1000)

sld_planet_r = slider(min=MIN, max=MAX, step=STEP, value=VAL2, length=220, bind=set_planet_r, right=15)
wt_planet_r = wtext(text='{:e}'.format(sld_planet_r.value/1000))
scene.append_to_caption(' km')

scene.append_to_caption('\n\n\n')




# graph
# ===============================================================================
def eclipse ():
    global star
    global planet

    x1 = star.pos.x
    x2 = planet.pos.x
    
    z1 = star.pos.z
    z2 = planet.pos.z
    
    r1 = star.radius
    r2 = planet.radius

    d = abs(x1-x2)


    # calculate the shadow area
    if (z1 > z2):                   # the planet is behind the star
        S = 0

    else:
        if (r1 + r2  <  d):         # not covered
            S = 0
        
        elif (r1 + r2  >  d):       # whole covered
            S = pi * r2**2
        
        else:                       # partly covered
            theta1 = acos((r1**2 + d**2 - r2**2) / (2*r1*d))
            theta2 = acos((r2**2 + d**2 - r1**2) / (2*r2*d))

            S = 1/2 * (r1**2 * (theta1 - sin(theta1*2)) + r2**2 * (theta2 - sin(theta2*2)))

    return pi * r1**2 - S


time = 0

f1 = graph(width=600, height=200, title='radial velocity', ymax=1.5e4, ymin=-1.5e4)
g1 = gcurve(graph=f1, color=color.red)

f2 = graph(width=600, height=200, title='eclipse', ymin=0)
g2 = gcurve(graph=f2, color=color.blue)




# ===============================================================================
#                                     main
# ===============================================================================
dt = 1e5
while True:
    rate(speed)
    
    if running:
        # move
        r = planet.pos - star.pos
        F = G * star.mass * planet.mass * r.hat / mag2(r)

        star.p   = star.p   + F*dt
        planet.p = planet.p - F*dt
    
        star.pos   = star.pos   + (star.p/star.mass)     * dt
        planet.pos = planet.pos + (planet.p/planet.mass) * dt
        
        light.pos = star.pos
        
        
        # label
        s_to_p = star.pos   - planet.pos
        c_to_s = center.pos - star.pos
        c_to_p = center.pos - planet.pos

        star_to_planet.text = '별-행성 거리: {:e}'.format(s_to_p.mag)
        cent_to_star.text   = '중심-별 거리: {:e}'.format(c_to_s.mag)
        cent_to_planet.text = '중심-행성 거리: {:e}'.format(c_to_p.mag)
        
        star_v.text   = '속력: {:e}'.format(mag(star.p/star.mass))
        planet_v.text = '속력: {:e}'.format(mag(planet.p/planet.mass))

        cent_to_star.pos   = star.pos
        cent_to_planet.pos = planet.pos

        star_v.pos   = star.pos
        planet_v.pos = planet.pos
        
        
        # arrow
        draw_raial_v(star,   star_rv_arrow)
        draw_raial_v(planet, planet_rv_arrow)        
        
        
        # graph
        radial_v = star.p.z / star.mass
        
        g1.plot(time, radial_v)
        g2.plot(time, eclipse())
        
        time += 1

    
    # for vsc
    if (exit == True):
        break


#stop_server()











#GlowScript 3.2 VPython

from vpython import *
from vpython.no_notebook import stop_server

scene.width  = 1000
scene.height = 400

kpc = 3e+16         # 1 kpc  =  3.085e+16 km


# sun / planets


class Ball:
    def __init__(self, orbit_r, init_theta, rot_v, color):         # (, km, degree(azimuth), )
        self.orbit_r  = orbit_r
        self.set_w(rot_v, orbit_r)
        
        self.theta    = radians(init_theta-90)
        self.init_pos = self.theta_to_pos()
        self.ball     = sphere(pos=self.init_pos, radius=0.05*kpc, color=color, make_trail = True)
    
    def cut (self, f):
        k = 1
        while True:
            if (int(f * 10**k) != 0):
                break
    
            k += 1
    
        big = f * 10**k

        f = f - (big - int(big)) / 10**k

        return f

    def set_w (self, rot_v, orbit_r):
        s = self.cut(rot_v, orbit_r)
        self.w  = vec(0, -s, 0)
    
    def theta_to_pos (self):
        return vec(self.orbit_r*cos(self.theta), 0, self.orbit_r*sin(self.theta))

    def update(self):
        self.theta += self.w.mag
        self.ball.pos = self.theta_to_pos()

sun   = sphere(pos=vec(0, 0, 0), radius=0.2*kpc, color=color.yellow)

red_ball = Ball(1*kpc,   0, 200, color.red)
blu_ball = Ball(1*kpc, 150, 200, color.blue)



# arrow
r_arrow = arrow(pos=vec(0, 0, 0), axis=vec(0, 0, 0), shaftwidth=0.01*kpc, headwidth=0.03*kpc, headlength=0.03*kpc, color=color.white)
t_arrow = arrow(pos=vec(0, 0, 0), axis=vec(0, 0, 0), shaftwidth=0.01*kpc, headwidth=0.03*kpc, headlength=0.03*kpc, color=color.white)

rel_v_arrow = arrow(pos=vec(0, 0, 0), axis=vec(0, 0, 0), shaftwidth=0.01*kpc, headwidth=0.07*kpc, headlength=0.05*kpc, color=color.yellow)



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




# speed
# ===============================================================================
MIN = 5
MAX = 20000
VAL = 10
speed = VAL

scene.append_to_caption('\nspeed: ')

def set_speed (s):
    global speed
    speed = s.value

slider(min=MIN, max=MAX, value=VAL, length=220, bind=set_speed, right=15)
scene.append_to_caption('\n\n')




# orbit radius
# ===============================================================================
def set_t(s):
    return

scene.append_to_caption('<b>Red</b>:\t\t')
scene.append_to_caption('orbit radius:\t')
red_orbit_r = winput(text='1', number=1, bind=set_t)
scene.append_to_caption(' kpc')

scene.append_to_caption('\t\t\t<b>Blue</b>:\t\t')
scene.append_to_caption('orbit radius:\t')
blu_orbit_r = winput(text='1', number=1, bind=set_t)
scene.append_to_caption(' kpc')
scene.append_to_caption('\n\n')




# initial position
# ===============================================================================
scene.append_to_caption('\t\tinitial position:\t')
red_init_theta = winput(text='0', number=0, bind=set_t)
scene.append_to_caption(' degree')

scene.append_to_caption('\t\t\t\t\tinitial position:\t')
blu_init_theta = winput(text='150', number=150, bind=set_t)
scene.append_to_caption(' degree')
scene.append_to_caption('\n\n')




# rotation v
# ===============================================================================
scene.append_to_caption('\t\trotation v:\t\t')
red_rotation_v = winput(text='200', number=200, bind=set_t)
scene.append_to_caption(' km/s')

scene.append_to_caption('\t\t\t\t\t\ttrotation v:\t')
blu_rotation_v = winput(text='200', number=200, bind=set_t)
scene.append_to_caption(' km/s')




# Apply
# ===============================================================================
def apply (b):
    global red_ball
    global blu_ball
    
    red_ball.theta = radians(red_init_theta.number-90)
    blu_ball.theta = radians(blu_init_theta.number-90)

    red_ball.orbit_r = red_orbit_r.number * kpc
    blu_ball.orbit_r = blu_orbit_r.number * kpc
    
    #red_ball.w = w = vec(0, - red_rotation_v.number / red_ball.orbit_r, 0)
    #red_ball.w = w = vec(0, - blu_rotation_v.number / blu_ball.orbit_r, 0)
    
    red_ball.set_w(red_rotation_v.number, red_ball.orbit_r)
    blu_ball.set_w(blu_rotation_v.number, blu_ball.orbit_r)
    
    red_ball.update()
    blu_ball.update()
    
    red_ball.ball.clear_trail()
    blu_ball.ball.clear_trail()
    
    g1.delete()
    g2.delete()

scene.append_to_caption('\t\t\t')
button(text="Apply", bind=apply)
scene.append_to_caption('\n\n')




# graph
# ===============================================================================
def rt_v ():
    s = cross(red_ball.w, red_ball.ball.pos - sun.pos)
    e = cross(blu_ball.w, blu_ball.ball.pos - sun.pos)
    r_axis = blu_ball.ball.pos - red_ball.ball.pos          # radial velocity basis axis

    v = e - s                                               # relative velocity
    radial_v = dot(v, r_axis.norm())
    
    t_axis = vec(-r_axis.z, 0, r_axis.x)                    # tangential velocity basis axis (ccw)
    tangential_v = v - radial_v*r_axis.norm()          
    tangential_v = dot(tangential_v, t_axis.norm())         # caculate t_v on t_axis
    
    
    # arrow
    r_arrow.pos  = red_ball.ball.pos
    r_arrow.axis = blu_ball.ball.pos - red_ball.ball.pos
    
    t_arrow.pos  = blu_ball.ball.pos
    t_arrow.axis = t_axis / 3
    
    rel_v_arrow.pos  = blu_ball.ball.pos
    rel_v_arrow.axis  = v

    return tangential_v, radial_v

time = 0

#f1 = graph(width=600, height=200, title='tangential velocity', ymin=-9e7, ymax=0)
f1 = graph(width=600, height=200, title='tangential velocity')
g1 = gcurve(graph=f1, color=color.red)

f2 = graph(width=600, height=200, title='radial velocity', ymin=-1, ymax=1)
g2 = gcurve(graph=f2, color=color.blue)





# ===============================================================================
#                                     main
# ===============================================================================

w = vec(0, -0.6e-14, 0)


dt = 1e5
while True:
    rate(speed)

    if running:
        red_ball.update()
        blu_ball.update()
        
        
        # graph
        tv, rv = rt_v()
        
        g1.plot(time, tv)
        g2.plot(time, rv)
        
        time += 1


    if (exit == True):
        break

stop_server()





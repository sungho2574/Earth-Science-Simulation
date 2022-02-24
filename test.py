#GlowScript 3.2 VPython



# for vsc
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
from vpython import *
from vpython.no_notebook import stop_server
print_anchor = scene.title_anchor
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 



scene.width  = 800
scene.height = 400
scene.title  = "<b>revolution</b>\n\n"

G = 6.7e-11

ON  = True
OFF = False

SCALE = 1e7/2           # use in star_v, star_rv initial, star_v0 etc





class LabelBunch ():
    
    def __init__(self):
        self.star_to_planet = label(pos=vec(1e11, 3e11, 0), text="별-행성 거리: ",   height=15,              visible=False)
        self.cent_to_star   = label(pos=star.pos,           text="중심-별 거리: ",   height=15, yoffset=100, visible=False)
        self.cent_to_planet = label(pos=planet.pos,         text="중심-행성 거리: ", height=15, yoffset=100, visible=False)

        self.star_v   = label(pos=star.pos,   text="속력: ", height=15, yoffset=70, visible=False)
        self.planet_v = label(pos=planet.pos, text="속력: ", height=15, yoffset=70, visible=False)



    def on_off (self, on_off):
        self.star_to_planet.visible = on_off
        self.cent_to_star.visible   = on_off
        self.cent_to_planet.visible = on_off
        self.star_v.visible         = on_off
        self.planet_v.visible       = on_off



    def update (self):
        global star, planet, center

        s_to_p = star.pos   - planet.pos
        c_to_s = center.pos - star.pos
        c_to_p = center.pos - planet.pos

        self.star_to_planet.text = '별-행성 거리: {:e}'.format(s_to_p.mag)
        self.cent_to_star.text   = '중심-별 거리: {:e}'.format(c_to_s.mag)
        self.cent_to_planet.text = '중심-행성 거리: {:e}'.format(c_to_p.mag)
        
        self.star_v.text   = '속력: {:e}'.format(mag(star.p/star.mass))
        self.planet_v.text = '속력: {:e}'.format(mag(planet.p/planet.mass))

        self.cent_to_star.pos   = star.pos
        self.cent_to_planet.pos = planet.pos

        self.star_v.pos   = star.pos
        self.planet_v.pos = planet.pos
   




class ArrowBunch ():

    def __init__(self):
        self.RV_SCALE = SCALE
        AX_SCALE = 4e10

        SW   = 0.5e10
        HEAD = 1.0e10
            
        self.star_v   = attach_arrow(star,   "p", scale=SCALE/star.mass,   shaftwidth=SW, headwidth=HEAD, headlength=HEAD, color=color.green)
        self.planet_v = attach_arrow(planet, "p", scale=SCALE/planet.mass, shaftwidth=SW, headwidth=HEAD, headlength=HEAD, color=color.green)

        self.star_rv   = arrow(pos=vec(0, 0, 0), axis=vec(0, 0, 0), shaftwidth=SW, headwidth=HEAD, headlength=HEAD, visible=False)
        self.planet_rv = arrow(pos=vec(0, 0, 0), axis=vec(0, 0, 0), shaftwidth=SW, headwidth=HEAD, headlength=HEAD, visible=False)
        
        self.star_rv_big   = arrow(pos=vec(0, 0, 0), axis=vec(0, 0, 0), visible=False)
        self.planet_rv_big = arrow(pos=vec(0, 0, 0), axis=vec(0, 0, 0), visible=False)

        self.star_v0   = arrow(pos=vec(0, 0, 0), axis=vec(0, 0, 0), color=color.red, visible=False)
        self.planet_v0 = arrow(pos=vec(0, 0, 0), axis=vec(0, 0, 0), color=color.red, visible=False)

        self.x_axis = arrow(pos=vec(0, 0, 0), axis=vec(AX_SCALE, 0, 0),  color=color.white, visible=False)
        self.y_axis = arrow(pos=vec(0, 0, 0), axis=vec(0, AX_SCALE, 0),  color=color.white, visible=False)
        self.z_axis = arrow(pos=vec(0, 0, 0), axis=vec(0, 0, -AX_SCALE), color=color.red,   visible=False)



    def v_switch (self, on_off):
        if on_off:
            self.star_v.start()
            self.planet_v.start()
        
        else:
            self.star_v.stop()
            self.planet_v.stop()
    


    def rv_switch (self, on_off):
        self.star_rv.visible   = on_off
        self.planet_rv.visible = on_off
    


    def rv_big_switch (self, on_off):
        self.star_rv_big.visible   = on_off
        self.planet_rv_big.visible = on_off



    def update (self):
        global star, planet

        self.draw_raial_v(star,   self.star_rv)
        self.draw_raial_v(planet, self.planet_rv)        
        
        self.draw_raial_v(star,   self.star_rv_big)
        self.draw_raial_v(planet, self.planet_rv_big)    



    def draw_raial_v (self, ball, arrow):
        arrow.pos = ball.pos
        arrow.axis = vec(0, 0, ball.p.z/ball.mass) * self.RV_SCALE

        if (arrow.axis.z > 0):
            arrow.color = color.blue
        
        else:
            arrow.color = color.red
        
    
        














def put_text (text):
    wtext(pos=print_anchor, text=text)










class Setting ():
    
    def __init__(self):
        self.speed = 100
        put_text('\n\n\n<b>setting</b>\n\n')
        

        

        self.speed_bar()
        self.label()
        self.velocity_arrow()
        self.radial_velocity_arrow()
        self.coordinate_axis()



    # speed
    # ===============================================================================
    



    def set_speed (self, s):
        self.speed = s.value

    def speed_bar (self):
        MIN = 5
        MAX = 1000
        VAL = 100
       

        put_text('speed: ')
        slider(pos=print_anchor, min=MIN, max=MAX, value=VAL, length=220, bind=self.set_speed, right=15)
        put_text('\n\n')



    # label
    # ===============================================================================
    def label (self):
        DEFAULT = False

        self.chk_label = checkbox(pos=print_anchor, text='label', checked=DEFAULT, bind=self.set_label)
        put_text('\n\n')



    def set_label(self, r):
        global lb
        
        if r.checked:
            lb.on_off(ON)

        else:
            lb.on_off(OFF)
    


    # velocity arrow
    # ===============================================================================
    def velocity_arrow (self):
        DEFAULT = False
            
        self.chk_v = checkbox(pos=print_anchor, text='velocity arrow', checked=DEFAULT, bind=self.set_v_arrow)
        put_text('\n\n')



    def set_v_arrow(self, r):
        global arr

        if r.checked:
            arr.v_switch(ON)

        else:
            arr.v_switch(OFF)



    # radial velocity arrow
    # ===============================================================================
    def radial_velocity_arrow (self):
        DEFAULT = False

        self.chk_rv     = checkbox(pos=print_anchor, text='radial velocity arrow      ', checked=DEFAULT, bind=self.set_rv_arrow)
        self.chk_rv_big = checkbox(pos=print_anchor, text='bigger',                      checked=DEFAULT, bind=self.set_rv_arrow_size)
        put_text('\n\n')
    


    def set_rv_arrow(self, r):
        global arr

        if r.checked:
            arr.rv_switch(ON)

        else:
            arr.rv_switch(OFF)



    def set_rv_arrow_size (self, r):
        global arr
        size = 7

        if r.checked:
            arr.rv_switch(OFF)
            arr.rv_big_switch(ON)
            arr.RV_SCALE *= size
        
        else:
            arr.rv_switch(ON)
            arr.rv_big_switch(OFF)
            arr.RV_SCALE /= size



    # coordinate axis
    # ===============================================================================
    def coordinate_axis (self):
        DEFAULT = False

        checkbox(pos=print_anchor, text='coordinate axis', checked=DEFAULT, bind=self.set_coor_axis)
        put_text('\n\n\n')



    def set_coor_axis (r):
        if r.checked:
            arr.x_axis.visible = True
            arr.y_axis.visible = True
            arr.z_axis.visible = True
        
        else:
            arr.x_axis.visible = False
            arr.y_axis.visible = False
            arr.z_axis.visible = False






class InitSetting ():
    
    def __init__(self):
        put_text('<b>new star system</b>\n\n')
        self.sld_dist = 0
        self.distance()
        self.v()
        self.ang()
        self.m()
        self.r()
        
    

    def connect_sld_text (self, sld, wt):
        sld.conn_text = wt

    def set_sld_text (self, s):
        s.conn_text.text = self.self.sld_text(s)
        
    def set_ang_text (self, s):
        s.conn_text.text = self.ang_text(s)

    def sld_text (self, s):
        return '{:e}'.format(s.value * s.ratio)

    def ang_text (self, s):
        return '{:03.0f}'.format(s.value * s.ratio)



    # distance between the two planets
    # ===============================================================================
    def distance (self):
        MIN  = 1e11
        MAX  = 4e11
        STEP = 0.1e11
        VAL  = 2.5e11

        put_text('distance: ')
        self.sld_dist = slider(pos=print_anchor, min=MIN, max=MAX, step=STEP, value=VAL, length=220, bind=self.set_sld_text, right=15, ratio=1/1000)
        self.wt_dist = wtext(pos=print_anchor, text=self.sld_text(self.sld_dist))
        self.connect_sld_text(self.sld_dist, self.wt_dist)
        put_text(' km\n\n')



    # v
    # ===============================================================================
    def v (self):
        MIN = 0.5e4
        MAX = 3e4
        VAL1 = 1e4
        VAL2 = 1e4 * 2

        put_text('star:\t\tv\t= ')
        self.sld_star_v = slider(pos=print_anchor, min=MIN, max=MAX, value=VAL1, length=220, bind=self.set_sld_text, right=15, ratio=1/1000*3600)
        self.wt_star_v = wtext(pos=print_anchor, text=self.sld_text(self.sld_star_v))
        self.connect_sld_text(self.sld_star_v, self.wt_star_v)
        put_text(' km/h\t\t')


        put_text('planet:\t\tv\t= ')
        self.sld_planet_v = slider(pos=print_anchor, min=MIN, max=MAX, value=VAL2, length=220, bind=self.set_sld_text, right=15, ratio=1/1000*3600)
        self.wt_planet_v = wtext(pos=print_anchor, text=self.sld_text(self.sld_planet_v))
        self.connect_sld_text(self.sld_planet_v, self.wt_planet_v)
        put_text(' km/h\n\n')



    # ang
    # ===============================================================================
    def ang (self):
        MIN  = 0
        MAX  = 360
        STEP = 1
        VAL1 = 0
        VAL2 = 180

        put_text('\t\tang\t= ')
        self.sld_star_ang = slider(pos=print_anchor, min=MIN, max=MAX, step=STEP, value=VAL1, length=220, bind=self.set_ang_text, right=15, ratio=1)
        self.wt_star_ang = wtext(pos=print_anchor, text=self.ang_text(self.sld_star_ang))
        self.connect_sld_text(self.sld_star_ang, self.wt_star_ang)
        put_text(' degree\t\t\t\t\t\t\t')


        put_text('ang\t= ')
        self.sld_planet_ang = slider(pos=print_anchor, min=MIN, max=MAX, step=STEP, value=VAL2, length=220, bind=self.set_ang_text, right=15, ratio=1)
        self.wt_planet_ang = wtext(pos=print_anchor, text=self.ang_text(self.sld_planet_ang))
        self.connect_sld_text(self.sld_planet_ang, self.wt_planet_ang)
        put_text(' degree\n\n')



    # m
    # ===============================================================================
    def m (self):
        MIN  = 0.5e30
        MAX  = 4e30
        STEP = 0.1e30
        VAL1 = 2e30
        VAL2 = 1e30

        put_text('\t\tm\t= ')
        self.sld_star_m = slider(pos=print_anchor, min=MIN, max=MAX, step=STEP, value=VAL1, length=220, bind=self.set_sld_text, right=15, ratio=1/1000)
        self.wt_star_m = wtext(pos=print_anchor, text=self.sld_text(self.sld_star_m))
        self.connect_sld_text(self.sld_star_m, self.wt_star_m)
        put_text(' Ton\t\t\t\t\t')


        put_text('m\t= ')
        self.sld_planet_m = slider(pos=print_anchor, min=MIN, max=MAX, step=STEP, value=VAL2, length=220, bind=self.set_sld_text, right=15, ratio=1/1000)
        self.wt_planet_m = wtext(pos=print_anchor, text=self.sld_text(self.sld_planet_m))
        self.connect_sld_text(self.sld_planet_m, self.wt_planet_m)
        put_text(' Ton\n\n')



    # r
    # ===============================================================================
    def r (self):
        MIN  = 0.5e10
        MAX  = 4e10
        STEP = 0.1e10
        VAL1 = 2e10
        VAL2 = 1e10

        put_text('\t\tr\t= ')
        self.sld_star_r = slider(pos=print_anchor, min=MIN, max=MAX, step=STEP, value=VAL1, length=220, bind=self.set_sld_text, right=15, ratio=1/1000)
        self.wt_star_r = wtext(pos=print_anchor, text=self.sld_text(self.sld_star_r))
        self.connect_sld_text(self.sld_star_r, self.wt_star_r)
        put_text(' km\t\t\t\t\t\t')


        put_text('r\t= ')
        self.sld_planet_r = slider(pos=print_anchor, min=MIN, max=MAX, step=STEP, value=VAL2, length=220, bind=self.set_sld_text, right=15, ratio=1/1000)
        self.wt_planet_r = wtext(pos=print_anchor, text=self.sld_text(self.sld_planet_r))
        self.connect_sld_text(self.sld_planet_r, self.wt_planet_r)
        put_text(' km\n\n\n')
    


class GUI ():
    
    def __init__ (self):
        self.setting = Setting()
        self.init_setting = InitSetting()
        
        # Exit
        self.exit = False
        button(text='Exit', pos=scene.title_anchor, bind=self.ex)


        # Run / Pause
        self.running = True
        button(text="Pause", pos=scene.title_anchor, bind=self.run)
        
        
        # Apply
        button(text="Apply", pos=scene.title_anchor, bind=self.apply)
    
    
    def apply (self, b):
        global star, planet
        global center, light
        global lb, arr
        print(3)
        
        # erase prior star system
        star.clear_trail()
        planet.clear_trail()
        
        lb.on_off(OFF)
        arr.v_switch(OFF)
        arr.rv_switch(OFF)
        arr.rv_big_switch(OFF)

        gra.reset()


        # set new star system
        print(self.init_setting.sld_dist)
        dist = self.init_setting.sld_dist.value
        star.pos   = vec(-dist*2/5, 0, 0)
        planet.pos = vec( dist*3/5, 0, 0)

        star.radius   = self.init_setting.sld_star_r.value
        planet.radius = self.init_setting.sld_planet_r.value

        star.mass   = self.init_setting.sld_star_m.value
        planet.mass = self.init_setting.sld_planet_m.value
        
        center_x = star.pos.x  +  dist * planet.mass / (star.mass + planet.mass)
        center.pos = vec(center_x, 0, 0)
        light.pos = star.pos
        
        print(5)
        
        # set v
        star_v   = self.set_v(self.init_setting.sld_star_v.value, self.init_setting.sld_star_ang.value)
        planet_v = self.set_v(self.init_setting.sld_planet_v.value, self.init_setting.sld_planet_ang.value)

        star.p   = star_v   * star.mass
        planet.p = planet_v * planet.mass
        
        
        # apply v arrow
        if not self.running:
            arr.star_v0.visible = True
            arr.star_v0.pos     = star.pos
            arr.star_v0.axis    = star_v * SCALE

            arr.planet_v0.visible = True
            arr.planet_v0.pos     = planet.pos
            arr.planet_v0.axis    = planet_v * SCALE
        
        print(2)
        # hold on until "Run"
        while not self.running:
            pass                    
        
        
        # ready to start
        arr.star_v0.visible   = False
        arr.planet_v0.visible = False
        
        # label
        if self.setting.chk_label.checked:
            lb.on_off(ON)
        
        # v arrow
        if self.setting.chk_v.checked:
            arr.v_switch(ON)
        
        # rv arrow
        if self.setting.chk_rv.checked:
            arr.rv_switch(ON)
        
        # big rv arrow
        if self.setting.chk_rv_big.checked:
            arr.rv_switch(OFF)
            arr.rv_big_switch(ON)
            
        print(1)
    
    def ex (self,b):
        self.exit = True



    def run(self, b):
        self.running = not self.running
        
        if self.running:
            b.text = "Pause"
        
        else: 
            b.text = "Run"






    def set_v (v, ang):
        x = v * cos(radians(ang-90))
        z = v * sin(radians(ang-90))
        
        return vec(x, 0, z)
       


    
class Graph ():

    def __init__(self):
        self.time = 0

        self.f1 = graph(width=600, height=200, title='radial velocity', ymax=1.5e4, ymin=-1.5e4)
        self.g1 = gcurve(graph=self.f1, color=color.red)

        self.f2 = graph(width=600, height=200, title='eclipse', ymin=0)
        self.g2 = gcurve(graph=self.f2, color=color.blue)


    def plot (self):
        global star, planet

        radial_v = star.p.z / star.mass
        
        self.g1.plot(self.time, radial_v)
        self.g2.plot(self.time, self.eclipse())

        self.time += 1


    def eclipse (self):
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

        return (pi * r1**2) - S
    


    def reset (self):
        self.g1.delete()
        self.g2.delete()






class Simulator ():

    def __init__(self):
        pass
    
    
    
    def run (self):
        while True:
            rate(gui.setting.speed)
            
            if gui.running:
                self.move()
                lb.update()
                arr.update()
                gra.plot()

            
            # for vsc
            if (gui.exit == True):
                break
    
    
    
    def move (self):
        global star, planet, light

        dt = 1e5

        r = planet.pos - star.pos
        F = G * star.mass * planet.mass * r.hat / mag2(r)

        star.p   = star.p   + F*dt
        planet.p = planet.p - F*dt
    
        star.pos   = star.pos   + (star.p/star.mass)     * dt
        planet.pos = planet.pos + (planet.p/planet.mass) * dt
        
        light.pos = star.pos    
    
    
    
    
    
    
if __name__ == "__main__":


    put_text('asdfsdfd')
    # star / planet
    star   = sphere(pos=vec(-1e11, 0, 0),  mass=2e30, radius=2e10, color=color.yellow, make_trail=True)
    planet = sphere(pos=vec(1.5e11, 0, 0), mass=1e30, radius=1e10, color=color.white,  make_trail=True)

    star.p   = vec(0, 0, -1e4) * star.mass
    planet.p = -star.p
    

    # visual effect
    lb = LabelBunch()

    light = local_light(pos=star.pos, color=star.color)
    center = sphere(pos=vec(-0.16e11, 0, 0), radius=0.3e10, color=color.yellow)


    # arrow
    arr = ArrowBunch()
    arr.v_switch(OFF)


    # graph
    gra = Graph()

    #s = Setting()
    #s2 = InitSetting()
    gui = GUI()

    
    
   

    # main
    simulator = Simulator()
    simulator.run()

    















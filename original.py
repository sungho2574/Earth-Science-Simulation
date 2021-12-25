from vpython import *
from vpython.no_notebook import stop_server

exit = False
g = gcurve(x=200, y=200)
def B(b):
    #stop_server()
    global exit
    exit = True
    print(exit)
    return

button( bind=B, text='Click me!' )

G = 6.7e-11

giant = sphere(pos=vector(-1e11, 0, 0), radius=2e10, color=color.red, make_trail = True, interval=10)

giant.mass = 2e30
giant.p = vector(0, 0, -1e4) * giant.mass

dwarf = sphere(pos=vector(1.5e11, 0, 0), radius=1e10, color=color.yellow, make_trail = True, interval=10)

dwarf.mass = 1e30
dwarf.p = -giant.p

dt = 1e5
while True:
    rate(20)

    r = dwarf.pos - giant.pos
    F = G * giant.mass * dwarf.mass * r.hat / mag2(r)

    giant.p = giant.p + F*dt
    dwarf.p = dwarf.p - F*dt

    giant.pos = giant.pos + (giant.p/giant.mass) * dt
    dwarf.pos = dwarf.pos + (dwarf.p/dwarf.mass) * dt

    print(exit)

    if (exit == True):
        #stop_server()
        break


stop_server()


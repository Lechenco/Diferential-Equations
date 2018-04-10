#Skydiving problem

import numpy
import matplotlib.pyplot


g = 9.81    # m / s2
drag_coeficciente = .7
effective_area =  1.14592 # m2  calculated considering a 120 Kg mass
mass = 120.     # Kg
p0 = 101325.     # Pa
t0 = 288.15     # K
R = 8.31447     # J /mol
L = .0065       # j / mol.K
M = 0.0289644   # Kg / mol

h = .000005    # s
end_time = 5. * 60   # s
num_steps = int(end_time / h)
time = h * numpy.array(range(num_steps +1))


def skydiving():
    
    x = numpy.zeros([num_steps + 1])
    v = numpy.zeros([num_steps + 1])
    drag = numpy.zeros([num_steps + 1])
    
    x[0] = 36402.6 # m
    v[0] = 0        # m /s2
    drag[0] = 0     # N
    
    for step in range(num_steps):
        x[step + 1] = x[step] + h * v[step]
        v[step + 1] = v[step] + h * (drag[step] - g)
        t = t0 - x[step] / 150
        p = p0 * (1 - L * x[step] / t0)**(g * M /(R * L))
        pho = p * M / (R * t)
        drag[step + 1] = 0.5 * drag_coeficciente * pho * effective_area * v[step]**2 / mass
    return x, v, drag

x, v, drag = skydiving()

def plot():
    axes_x = matplotlib.pyplot.subplot(311)
    axes_v = matplotlib.pyplot.subplot(312)
    axes_drag = matplotlib.pyplot.subplot(313)
    
    axes_x.plot(time, x)
    axes_x.set_xlabel("Position x")
    axes_v.plot(time, v)
    axes_v.set_xlabel("Velocity v")
    axes_drag.plot(time, drag)
    axes_drag.set_xlabel("Drag force")

plot()
print(abs(min([i for i in v])))
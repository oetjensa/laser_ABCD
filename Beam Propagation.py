import numpy as np
import matplotlib.pyplot as plt
import ABCD_utensils as gb

step = 1
length = 1000

lam, w_0, M2, z_0, rad1, theta = gb.read_param()
lenses = gb.read_lenses()
mirrors = gb.mirrors

z_r = (np.pi*w_0**2) / (lam*M2)   # value will be given

q1 = gb.rth_to_q(rad1,theta, lam, M2)



'''
Start Propagation and plot the results
'''

Optics, position = gb.Optics(step, length, lenses)


# Computer beam parameter over stepwise Optics list
ABCD, distance, beam_radius, beam_angle, radius_inv = gb.Gauss_beam(q1,Optics, lam, M2, rad1, theta, position)


gb.plot(ABCD, distance, beam_radius, radius_inv, lenses, mirrors, save = False)

print('Maximum beam radius: ',max(beam_radius))

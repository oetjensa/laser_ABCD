import numpy as np
import matplotlib.pyplot as plt

path = 'path_to_files'
# might be necessary to run the folowing:
#import sys 
#import os
#sys.path.append(os.path.abspath(path))

import ABCD_utensils as gb

# following four lines are only for nicer plots, not necessary
#import seaborn as sns
#from pandas.plotting import register_matplotlib_converters
#register_matplotlib_converters()
#sns.set_style("darkgrid")


step = 1
# set the total length of the path (in mm)
length = 17000 # 17 m

# read in laser parameter, position of lenses
lam, w_0, M2, z_0, rad1, theta = gb.read_param(path)
lenses = gb.read_lenses(path)
mirrors = np.array([])

z_r = (np.pi*w_0**2) / (lam*M2)   # value will be given

q1 = gb.rth_to_q(rad1,theta, lam, M2)



'''
Start Propagation and plot the results
'''

Optics, position = gb.Optics(step, length, lenses)


# Computer beam parameter over stepwise Optics list
ABCD, distance, beam_radius, beam_angle, radius_inv = gb.Gauss_beam(q1,Optics, lam, M2, rad1, theta, position)


gb.plot(ABCD, distance, beam_radius, radius_inv, lenses, mirrors, length, save = False)

# make sure beam radius does not exceed lens/mirror radius
print('Maximum beam radius: ',max(beam_radius))

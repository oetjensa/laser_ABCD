#!/usr/bin/env python
# coding: utf-8


import numpy as np 
import matplotlib.pyplot as plt

def read_param(path):

    f = open(path+'Input_param.txt', 'r')
    f.readline()
    f.readline()

    lam = float(f.readline().split()[1])
    w_0 = float(f.readline().split()[1])
    M2  = float(f.readline().split()[1])
    z_0 = float(f.readline().split()[1])
    rad1 = float(f.readline().split()[1])
    theta = float(f.readline().split()[1])
    f.close()
    print('lambda = ', lam)
    print('w_0 = ', w_0)
    print('M2 = ', M2)
    print('z_0 = ', z_0)
    print('rad1 = ', rad1)
    print('theta = ', theta)
    return lam, w_0, M2, z_0, rad1, theta

def read_lenses(path):
    #result = defaultdict(list)
    result = {}
    with open(path+"Lenses_param.txt","r") as text:
        text.readline()
        for line in text:
            if len(line) < 2:
                break
            key, value = line.split()
            result[float(key)] = float(value)
    print('Lenses at: ')
    for lens in result:
        print("Position : {} , f = {}".format(lens,result[lens]))
    return result

#mirrors = np.array([300,500,700,800,900])


def space(dist, position): # propagate beam through air 
    A = 1
    B = dist
    C = 0
    D = 1
    matrix = np.array([[A, B], [C, D]]) 
    position.append(dist)
    return matrix, position

def thinlens(f, position):  #!! Thinlens without distance, need to have space before that
    A = 1
    B = 0
    C = -1/f
    D = 1
    matrix = np.array([[A, B], [C, D]])
    position.append(0)
    return matrix, position

## from laser/Laroux
def q_to_rth(q, lam, M2):
    qinv = 1 / q
    #curv = z - z_0 + z_r**2/(z-z_0)
    curv = 1 / qinv.real
    radius = np.sqrt(-(lam * M2 / qinv.imag) / np.pi)
    angle = np.arctan(radius / curv)
    return radius, angle

def rth_to_q(radius, angle, lam, M2):
    curv = radius / np.tan(angle)
    qinv = 1 / curv - 1j * lam * M2 / (np.pi * radius**2)
    return 1 / qinv

####

def beam_prop(qin, prop_matrix):
    A = prop_matrix[0, 0]
    B = prop_matrix[0, 1]
    C = prop_matrix[1, 0]
    D = prop_matrix[1, 1]   
    qn = (A*qin + B) / (C*qin + D)
    #radius = q_to_rth(qn)[0]
    #angle = q_to_rth(qn)[1]

    return qn #, radius, angle


def Gauss_beam(q1, matrices, lam, M2, rad1, theta, position):
    ABCD = []
    multi = [matrices[0]]  ## this is the unity matrix
    #print(multi)
    q_param =[q1]   # maybe have it calculated here??
    radius = q_to_rth(q1, lam , M2)[0]   ### multiply with unity, to obtain original values for radius, theta
    angle = q_to_rth(q1, lam , M2)[1]
    ABCD.append(( radius, angle, q1))  ### solution matrix appends first values from starting point, nothing has happened yet
   # print(ABCD) # should display original values ?! CHECK
    for i in range(len(matrices)-1):
        dotted = np.dot(matrices[i+1], multi[i])   # matrix multiplication with the following one
        #print(dotted)
        multi.append(dotted)
        #print(beam_prop(q_param[i], dotted))
        qn = beam_prop(q1, dotted)
        #qn = beam_prop(q_param[i], matrices[i+1])
        radius = q_to_rth(qn, lam , M2)[0]
        angle = q_to_rth(qn, lam , M2)[1]
        q_param.append(qn)
        ABCD.append((radius, angle, qn))
        #print(multi)
        
    # store parameter in lists
    distance = [position[0]]
    beam_radius = [rad1]
    radius_inv = [-1*rad1]
    beam_angle = [theta]

    for i in range(len(position)-1):
        distance.append(distance[i]+position[i+1]) 
        beam_radius.append(ABCD[i+1][0])
        beam_angle.append(ABCD[i+1][1])
        radius_inv.append(-1*ABCD[i+1][0])
        
    return ABCD, distance, beam_radius, beam_angle, radius_inv

def Optics(step, length, lenses):
    # Initialize lists and parameter
    total_distance = 0.0
    position = []  # this list gets created via the thinlens and space functions
    Optics = [space(0, position)[0]]

    # Create Optics list stepwise over whole distance and all Optics
    while total_distance < length:
        #print(total_distance)
        dist = total_distance + step
        if dist in lenses.keys():
            Optics.append(space(step, position)[0])
            Optics.append(thinlens(int(lenses[dist]), position)[0])
        else:
            Optics.append(space(step, position)[0])
        total_distance = dist
    return Optics, position

# Plotting
# Beam radius

def plot(ABCD, distance, radius, radius_inv, lenses, mirrors,length, save = False):
    # store parameter in lists
    plt.rcParams.update({'font.size': 20})
    fig, ax = plt.subplots(figsize=(20,10), num=1, clear=True, dpi =150)
    fig.suptitle('ABCD Propagation', fontsize=20)
    ax.plot(distance, radius, color = 'blue')  
    ax.plot(distance, radius_inv, color = 'blue')
    ax.fill_between(distance, radius, radius_inv, color = 'lightblue')
    ax.set_ylabel('Beam radius [mm]')
    ax.set_xlabel('Position [m]')
    ax.set_xticks(np.arange(0,length,1000))
    ax.set_xticklabels(np.arange(0,length,1000)/1000)

    # Lenses
    for pos in lenses.keys():
        ax.axvline(x = pos, ymin=-12.7, ymax=12.7, color = 'green', linestyle = 'dashed')
        ax.text(pos - 50, 10.5, 'f='+str(lenses[pos]), color = 'green')

    #Mirrors
    '''
    to visually add the position of mirrors to the plot
    the position needs to be added in mirrors
    '''
    for pos in mirrors:
        ax.axvline(x=pos, ymin=-12.7,ymax=12.7, color = 'silver', linewidth = 1)

    ax.set_ylim(-15,15)
    plt.tight_layout()
    if save == True:
        plt.savefig('ABCD_propagation_plot.pdf')

    plt.show() 

"""
  This script collects the data from forward and backward switchings process and computed the absolute free energy as function of the pressure

  Usage:
    python integrate.py
"""

from numpy import *
import scipy.constants as sc
from scipy.integrate import cumtrapz

N_sim = 10 
#kB = sc.value('Boltzmann constant in eV/K') 
bars2eVAngs3=6.241509074e-7

t_sc = array([1000,2000,5000]) #10000,20000,50000,100000,200000,500000,1000000]) 

for l in range(len(t_sc)):

    V_for = zeros(t_sc[l]+1)
    V_back = zeros(t_sc[l]+1)

    # free energy reference value at T=2200 K and 0.0 GPa.
    G0 = -5.327091 

    for j in range(0,N_sim): 
        # Load potential energy and lambda.

        # Forward integration.
        fileforward = "t_switch"+str(t_sc[l])+"/forward_as_"+str(j+1)+".dat"
        V_f, P_f = loadtxt(fileforward, unpack=True)

        # Backward integration.
        filebackward = "t_switch"+str(t_sc[l])+"/backward_as_"+str(j+1)+".dat"
        V_b, P_b = loadtxt(filebackward, unpack=True)

        for i in range(len(V_for)):
            V_for[i] += V_f[i]
            V_back[i] += V_b[i]  

    V_for = V_for/N_sim
    V_back = V_back/N_sim

    # Compute work done using cummulative integrals [Eq.(21) in the paper].
    W_mech_f = cumtrapz(V_for,P_f,initial=0)
    W_mech_b = cumtrapz(V_back[::-1],P_b[::-1],initial=0)
    W_mech = (W_mech_f+W_mech_b) / 2
    #Q_diss = absolute((W_mech_f-W_mech_b)/2)
    # Compute free energy [Eq.(44) in the paper] and save results.
    P = P_f
    G = G0 + W_mech * bars2eVAngs3
    #G_f = G0 + W_mech_f * bars2eVAngs3
    #G_b = G0 + W_mech_b * bars2eVAngs3

    fileout = "gibbs_energy_liquid_tsc"+str(t_sc[l])+".dat"

    savetxt(fileout,transpose([P,G]),header='P [bars] G [eV/atom]', fmt='%6.6f %.6f')


#savetxt('gibbs_energy_solid.dat', transpose([P,G,G_f,G_b,Q_diss]),
#        header='P [bars] G [eV/atom] G_forward G_backward Qdiss', fmt='%6.6f %.6f %.6f %.6f %6f')

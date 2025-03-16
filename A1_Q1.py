import numpy as np
import matplotlib.pyplot as plt
EI_h2o_ker = 1.25   # [kg/kg] Water vapor emission index for kerosene
EI_h2o_h2 = 8.94    # [kg/kg] Water vapor emission index for hydrogen
epsilon = 0.622     # [-] Ratio of molar mass of water vapor to air
LHV_ker = 43.2e6    # [J/kg] Lower heating value for kerosene
LHV_H2 = 120e6      # [J/kg] Lower heating value for hydrogen
cp_air = 1004       # [J/(kg K)] Specific heat of air at constant pressure cP 1004 J/kg/K

el_a = [-0.58002206 * 10**4, 1.3914993, -0.48640239 * 10**-1, 0.41764768 * 10**-4, -0.14452093 * 10**-7, 0]
ei_a = [-0.56745359 * 10**4, 6.3925247, -0.96778430 * 10**-2, 0.62215701 * 10**-6, 0.20747825 * 10**-8, -0.94840240 * 10**-12]
el_b = 6.5459673
ei_b = 4.1635019

""" 
###### Q1.a ######
"""


def p_sat_vap(a, b, T_range=[215, 255], dT = 1, singleT = 0):
    if singleT != 0:
        T = singleT
        e = np.exp(b * np.log(T) + sum(a[i + 1] * T ** i for i in range(-1, 5)))
    else:
        T = np.arange(T_range[0], T_range[-1] + dT, dT)
        T = np.asarray(T, dtype=float)
        e = np.exp(b * np.log(T) + sum(a[i+1] * T ** i for i in range(-1,5)))
    return e, T
ep_l , T = p_sat_vap(el_a, el_b)
ep_i , T = p_sat_vap(ei_a, ei_b)
ep_l225 = p_sat_vap(el_a, el_b, singleT=225)[0]
ep_l230 = p_sat_vap(el_a, el_b, singleT=230)[0]
ep_i225 = p_sat_vap(ei_a, ei_b, singleT=225)[0]
ep_i230 = p_sat_vap(ei_a, ei_b, singleT=230)[0]
print(f'Sat Vap Pressure 225K: ice = {ep_i225}, liquid = {ep_l225}\n'
      f'Sat Vap Pressure 230K: ice = {ep_i230}, liquid = {ep_l230}')

""" 
###### Q1.b ######
"""
eta1 = 0.3      # [-] Engine Efficiency
rh1 = 1.1       # [-] Rel Humidity
p1 = 220*100    # [Pa]
T1 = 225        # [K]
T_range225 = np.array([T1, T[-1]])

def rh_corr_ph2o(rh, T, ice = False):
    if ice:
        es = p_sat_vap(ei_a,ei_b,singleT=T)[0]
    else:
        es = p_sat_vap(el_a,el_b,singleT=T)[0]
    ep = es * rh
    return ep
def mixing_slope(p, eta, ker=True):
    if ker:
        G = cp_air * p * EI_h2o_ker / (epsilon * (1 - eta) * LHV_ker)
    else:
        G = cp_air * p * EI_h2o_h2 / (epsilon * (1 - eta) * LHV_H2)
    print(f"G is equal to: {G}")
    return G
def mixing_intercept(T, G, rh, ice=False):
    ep = rh_corr_ph2o(rh, T, ice)
    b = ep - T * G
    print(f"b is equal to: {b} \n ep is equal to: {ep}")
    return b
G1 = mixing_slope(p1, eta1)
b1 = mixing_intercept(T1, G1, rh1, True)
p1_plot = T_range225 * G1 + b1

""" 
###### Q1.c ######
"""
eta2 = 0.4
T2 = T1
rh2 = rh1
p2 = p1

G2 = mixing_slope(p1, eta2)
b2 = mixing_intercept(T2, G2, rh2, True)
p2_plot = T_range225 * G2 + b2

""" 
###### Q1.d ######
"""
eta3 = eta1
T3 = T1
p3 = p1
rh3 = rh1

G3 = mixing_slope(p3, eta3, False)
b3 = mixing_intercept(T3, G3, rh1, True)
p3_plot = T_range225 * G3 + b3

""" 
###### Q1.f ######
"""
p4 = 250*100  # [Pa]
T4 = 230  # [K]
rh4 = 0.6
T_range230 = np.array([T4, T[-1]])

G4_1 = mixing_slope(p4, eta1)
G4_2 = mixing_slope(p4, eta2)
G4_3 = mixing_slope(p4, eta1, False)

b4_1 = mixing_intercept(T4, G4_1, rh4)
b4_2 = mixing_intercept(T4, G4_2, rh4)
b4_3 = mixing_intercept(T4, G4_3, rh4)

p4_1_plot = T_range230 * G4_1 + b4_1
p4_2_plot = T_range230 * G4_2 + b4_2
p4_3_plot = T_range230 * G4_3 + b4_3

""" 
###### PLOTTING ######
"""
fig, axs = plt.subplots(1, 2, figsize=(12, 8))  # Create 1 row, 2 columns

axs[0].plot(T, ep_l, label="Water Sat. ($e_\\ell$)", color="black", linestyle=(0, (5, 7)))
axs[0].plot(T, ep_i, label="Ice Sat. ($e_i$)", color="black", linestyle='solid')
axs[0].plot(T_range225, p1_plot, label='Mixing Line: $\\eta = 0.3$, Ker')
axs[0].plot(T_range225, p2_plot, label='Mixing Line: $\\eta = 0.4$, Ker')
axs[0].plot(T_range225, p3_plot, label='Mixing Line: $\\eta = 0.3$, $H_2$')
axs[0].plot(T_range225[0], p3_plot[0], 'ro')
axs[0].axvline(235.15, label='$T = 38$ [C]', color='red', linestyle=(0, (1, 7)), linewidth=1.4)
axs[0].axvline(225, label='$T = 225$ [K', color='black', linestyle=(0, (1, 7)), linewidth=1.4)

axs[0].set_xlabel("Temperature [K]")
axs[0].set_ylabel("Saturation Vapor Pressure [Pa]")
axs[0].set_title("Contrail Formation (p = 220 hPa, T = 225 K, rhi = 110%)")
axs[0].legend(loc="upper left")
axs[0].grid(True, which="both", linestyle="--", linewidth=0.5)

axs[1].plot(T, ep_l, label="Water Sat. ($e_\\ell$)", color="black", linestyle=(0, (5, 7)))
axs[1].plot(T, ep_i, label="Ice Sat.($e_i$)", color="black", linestyle='solid')
axs[1].plot(T_range230, p4_1_plot, label='Mixing Line: $\\eta = 0.3$, Ker')
axs[1].plot(T_range230, p4_2_plot, label='Mixing Line: $\\eta = 0.4$, Ker')
axs[1].plot(T_range230, p4_3_plot, label='Mixing Line: $\\eta = 0.3$, $H_2$')
axs[1].plot(T_range230[0], p4_3_plot[0], 'ro')
axs[1].axvline(235.15, label='$T = 38$ [C]', color='red', linestyle=(0, (1, 7)), linewidth=1.4)
axs[1].axvline(230, label='$T = 225$ [K', color='black', linestyle=(0, (1, 7)), linewidth=1.4)

axs[1].set_xlabel("Temperature [K]")
axs[1].set_ylabel("Saturation Vapor Pressure [Pa]")
axs[1].set_title("Contrail Formation (p = 250 hPa, T = 230 K, rh = 60%)")
axs[1].legend(loc="upper left")
axs[1].grid(True, which="both", linestyle="--", linewidth=0.5)
plt.show()
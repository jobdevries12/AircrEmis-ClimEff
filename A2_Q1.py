import numpy as np
import matplotlib.pyplot as plt
cair = 2.69E+19  # molecules/cm3
T = 298  # K
p = 101300  # [Pa]
k_B = 1.38E-23  # Boltzmann constant
N_A = 6.02E23  # Avogadro's constant
R = 8.314  # Gas constant

k_HO2_HO2 = 6.10E-12                  # molecules/cm3/s
k_OH_NO2 = 9.00E-12                   # molecules/cm3/s
k_CO_OH = 1.57E-13 + cair * 3.54E-33  # molecules/cm3/s
k_HO2_NO = 3.3E-12 * np.exp(270 / T)  # molecules/cm3/s
P_HOx = 1.2E-3 * 10**-9               # mol/mol/s

CO_mr = 4500* 10**-9   # [mol/mol] mixing ratio CO
n_V = p / (R * T)
print(p / k_B / T, n_V*N_A)
CO_conc_ho2 = CO_mr * p / k_B / T / 100**3  # molecules/cm3 n/V = p / (k_B T) ideal gas law
NO2NO_rat = 7  # [-] NO2 to NO ratio
print(CO_conc_ho2)
def HO2_calc(NO_range, NO2NO=NO2NO_rat, CO=CO_conc_ho2, PLOT=False):
    x1 = 2 * k_HO2_HO2
    x2 = k_OH_NO2 / k_CO_OH / CO * NO2NO
    a = x1 * (1 + x2 * NO_range)
    x3 = k_HO2_NO * k_OH_NO2 / k_CO_OH / CO * NO2NO
    b = x3 * NO_range ** 2
    c = - P_HOx * p / k_B / T / 100**3
    print (x1, x2, x3)
    D = b ** 2 - 4 * a * c
    conc_ho2 = (-b + np.sqrt(D)) / (2 * a)
    #print(a,b,c,D)
    print(c)
    print(conc_ho2)

    P_O3 = k_HO2_NO * conc_ho2 * NO_range
    if PLOT:
        fig, ax = plt.subplots(1, 2, figsize=(12, 5))  # Create 2 subplots in 1 row

        # First subplot: [HO2] vs [NO]
        ax[0].plot(NO_range, conc_ho2, label=r'$[HO_2]$ concentration', color='b')
        ax[0].set_xscale('log')  # Logarithmic scale for NO
        ax[0].set_xlabel(r'$[NO]$ (molecules/cm$^3$)')
        ax[0].set_ylabel(r'$[HO_2]$ (molecules/cm$^3$)')
        ax[0].set_title(r'Dependence of $[HO_2]$ on $[NO]$')
        ax[0].grid(True, which="both", linestyle="--", linewidth=0.5)
        ax[0].legend()

        # Second subplot: [O3] Production vs [NO]
        ax[1].plot(NO_range, P_O3, label=r'$O_3$ Production', color='r')
        ax[1].set_xscale('log')  # Logarithmic scale for NO
        ax[1].set_xlabel(r'$[NO]$ (molecules/cm$^3$)')
        ax[1].set_ylabel(r'$[O_3]$ Production (molecules/cm$^3$/s)')
        ax[1].set_title(r'Dependence of $[O_3]$ Production on $[NO]$')
        ax[1].grid(True, which="both", linestyle="--", linewidth=0.5)
        ax[1].legend()

        plt.tight_layout()  # Adjust layout for better spacing
        plt.show()
    return conc_ho2

NO_r =  np.logspace(-1, np.log10(6E10), 1000)
conc_ho2 = HO2_calc(NO_r, PLOT=1)
import xarray as xr
import pandas as pd

M_NO2 = 46.0055  # g/mol
M_NO = 30.01  # g/mol
M_O3 = 48  # g/mol
M_N = N_A / 1E12 / np.array([M_NO, M_NO2, M_O3])

DEBY109 = pd.read_csv("airbase_DEBY109_NO.csv")
DEBY109_NO2 = pd.read_csv("airbase_DEBY109_NO2.csv")
DEBY109_O3 = pd.read_csv("airbase_DEBY109_O3.csv")

DEBY109['NO2'] = DEBY109_NO2['NO2 (µg/m3)']
DEBY109['O3'] = DEBY109_O3['O3 (µg/m3)']
DEBY109 = DEBY109.rename(columns={'NO (µg/m3)': 'NO'}).dropna()
print(DEBY109)
print(DEBY109.loc[[151,225,226]].head(3))
DEBY109[['NO', 'NO2', 'O3']] *= M_N
print(DEBY109)
print(DEBY109.loc[DEBY109['NO'] > 2e14].head(3))
NL00131 = pd.read_csv("airbase_NL00131_NO.csv")
NL00131_NO2 = pd.read_csv("airbase_NL00131_NO2.csv")
NL00131_O3 = pd.read_csv("airbase_NL00131_O3.csv")
NL00131['NO2'] = NL00131_NO2['NO2 (µg/m3)']
NL00131['O3'] = NL00131_O3['O3 (µg/m3)']
NL00131 = NL00131.rename(columns={'NO (µg/m3)': 'NO'}).dropna()
NL00131[['NO', 'NO2', 'O3']] *= M_N

NL00418 = pd.read_csv("airbase_NL00418_NO.csv")
NL00418_NO2 = pd.read_csv("airbase_NL00418_NO2.csv")
NL00418_O3 = pd.read_csv("airbase_NL00418_O3.csv")
NL00418['NO2'] = NL00418_NO2['NO2 (µg/m3)']
NL00418['O3'] = NL00418_O3['O3 (µg/m3)']
NL00418 = NL00418.rename(columns={'NO (µg/m3)': 'NO'}).dropna()
NL00418[['NO', 'NO2', 'O3']] *= M_N

# Function to create scatter plots
def plot_NOx_vs_O3(data, title, ax):
    ax.scatter(data['NO'], data['O3'], color='blue', label='NO', marker=".", alpha=0.3)
    ax.scatter(data['NO2'], data['O3'], color='red', label='NO2', marker=".", alpha=0.3)
    ax.set_xlabel('$NO_x$ (molecules/cm³)')
    ax.set_xscale('log')
    #ax.set_xlim([6e12, 7e12])
    ax.set_ylabel('$O_3$ (molecules/cm³)')
    #ax.set_ylim([0, 7e15])
    #ax.set_yscale('log')
    ax.set_title(title)
    ax.legend()
    ax.grid(True, linestyle="--", linewidth=0.5)

# Create figure and subplots
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Plot each dataset in a separate subplot
plot_NOx_vs_O3(DEBY109, "DEBY109", axes[0])
plot_NOx_vs_O3(NL00131, "NL00131", axes[1])
plot_NOx_vs_O3(NL00418, "NL00418", axes[2])

# Adjust layout and show plot
plt.tight_layout()
plt.show()
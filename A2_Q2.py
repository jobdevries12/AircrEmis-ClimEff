
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file_path = "yearmean_RD1_2019_zm.csv"  
df = pd.read_csv(file_path)

# Constants
R = 8.314  
N_A = 6.022e23  

'''
Question 1a
calculating the ozone concentration based on the provided data.
Plot zonal mean ozone mixing ratio and ozone concentrations
'''



# molar air density (n = P / (R * T)) in mol/m³
df["rho_m"] = df["plev"] / (R * df["tm1"])

# ozone mixing ratio to concentration (molecules/cm³)
df["C_O3"] = df["O3"] * df["rho_m"] * N_A / 1e6  # Convert to cm³

# zonal mean (mean over all longitudes, for each latitude and pressure level)
df_mean_z = df.groupby(["lat", "plev"]).mean(numeric_only=True).reset_index()

# For contour plotting
latitudes = np.sort(df_mean_z["lat"].unique())
pressures = np.sort(df_mean_z["plev"].unique())[::-1]  # Invert for proper pressure axis
o3_mixing_ratio = df_mean_z.pivot(index="plev", columns="lat", values="O3")
o3_concentration = df_mean_z.pivot(index="plev", columns="lat", values="C_O3")

# Plotting
fig, axes = plt.subplots(1, 2, figsize=(12, 6), sharey=True)

# Plot Ozone Mixing Ratio
c1 = axes[0].pcolormesh(latitudes, pressures, o3_mixing_ratio, shading='auto', cmap="viridis")
axes[0].set_xlabel("Latitude")
axes[0].set_ylabel("Pressure (Pa)")
axes[0].set_title("(a) Zonal Mean Ozone Mixing Ratio")
fig.colorbar(c1, ax=axes[0], label="O3 Mixing Ratio (kg/kg)")

# Plot Ozone Concentration
c2 = axes[1].pcolormesh(latitudes, pressures, o3_concentration, shading='auto', cmap="plasma")
axes[1].set_xlabel("Latitude")
axes[1].set_title("(b) Zonal Mean Ozone Concentration")
fig.colorbar(c2, ax=axes[1], label="O3 Concentration (molecules/cm³)")

plt.gca().invert_yaxis()  # Invert y-axis to have lower pressures at the top
plt.tight_layout()
plt.show()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Constants
R = 8.314  # Universal gas constant (J/(mol·K))


def load_data(file_path):
    """Load ozone dataset from CSV file"""
    df = pd.read_csv(file_path)
    df["pressure_Pa"] = df["plev"]
    return df


def calculate_ozone_concentration(df):
    """Calculate ozone concentration using the ideal gas law."""
    df["ozone_concentration"] = (df["plev"] * df["O3"]) / (R * df["tm1"] )
    df["ozone_concentration"] = df["ozone_concentration"] / 1e6
    return df


def plot_ozone(df):
    """Plot ozone mixing ratio and ozone concentration using filled contours."""

    # Aggregate duplicate entries by averaging
    df = df.groupby(["plev", "lat"], as_index=False).mean()

    # Create grid for contour plots
    latitudes = np.unique(df["lat"])
    pressures = np.unique(df["plev"])

    # Reshape data using pivot_table (handles duplicates safely)
    O3_grid = df.pivot_table(index="plev", columns="lat", values="O3").values
    ozone_conc_grid = df.pivot_table(index="plev", columns="lat", values="ozone_concentration").values

    # Plot Ozone Mixing Ratio
    plt.figure(figsize=(8, 6))
    plt.contourf(latitudes, pressures, O3_grid, levels=50, cmap="viridis")
    plt.yscale("log")
    plt.colorbar(label="O3 Mixing Ratio (mol/mol)")
    plt.xlabel("Latitude")
    plt.ylabel("Pressure (Pa)")
    plt.title("Zonal Mean Ozone Mixing Ratio")
    plt.gca().invert_yaxis()
    plt.show()

    # Plot Ozone Concentration
    plt.figure(figsize=(8, 6))
    plt.contourf(latitudes, pressures, ozone_conc_grid, levels=50, cmap="plasma")
    plt.yscale("log")
    plt.colorbar(label="O3 Concentration (mol/m³)")
    plt.ylim(100)
    plt.xlabel("Latitude")
    plt.ylabel("Pressure (Pa)")
    plt.title("Zonal Mean Ozone Concentration")
    plt.gca().invert_yaxis()
    plt.show()



def main():
    """Main function to execute the data processing and visualization."""
    file_path = r"C:\Users\johar\Documents\GitHub\AircrEmis-ClimEff\yearmean_RD1_2019_zm.csv"
    df = load_data(file_path)
    df = calculate_ozone_concentration(df)
    plot_ozone(df)


if __name__ == "__main__":
    main()
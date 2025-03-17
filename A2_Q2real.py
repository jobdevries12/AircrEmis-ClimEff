import numpy as np
import matplotlib.pyplot as plt

#Constands
O3_0 = 0


# steady-state ozone equation
def steady_state_ozone(NO, NO2, alpha=10):
    return -0.5 * (NO - O3_0 + alpha) + 0.5 * np.sqrt((NO - O3_0 + alpha) ** 2 + 4 * alpha * (NO2 + O3_0))

#  NOx range and conditions
NOx_values = np.linspace(0, 700, 700)
O3_case1 = steady_state_ozone(NOx_values, np.zeros_like(NOx_values))  # Initial NO only
O3_case2 = steady_state_ozone(np.zeros_like(NOx_values), NOx_values)  # Initial NO2 only
O3_case3 = steady_state_ozone(NOx_values / 2, NOx_values / 2)  # Equal NO and NO2

# Plotting
plt.figure(figsize=(8, 6))
plt.plot(NOx_values, O3_case1, label='Initial NO only', color='blue')
plt.plot(NOx_values, O3_case2, label='Initial NO2 only', color='red')
plt.plot(NOx_values, O3_case3, label='Equal NO & NO2', color='green')

plt.xlabel("NOx Mixing Ratio (nmol/mol)")
plt.ylabel("Steady-State O3 Mixing Ratio (nmol/mol)")
plt.title("Steady-State Ozone Mixing Ratio for Different Initial NOx Mixing Ratios")
plt.legend()
plt.grid()
plt.show()



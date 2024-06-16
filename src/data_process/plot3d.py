import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Read the CSV data
data = pd.read_csv('../../debug_tests/Nov_No17IdVg.csv')

# Extract unique Sub_V values
unique_sub_v = data['Sub_V'].unique()

# Plot Drain_I vs Gate_V for each Drain_V value and group by Sub_V
plt.figure()
for sub_v in unique_sub_v:
    subset_sub_v = data[data['Sub_V'] == sub_v]
    unique_drain_v = subset_sub_v['Drain_V'].unique()
    for drain_v in unique_drain_v:
        subset_drain_v = subset_sub_v[subset_sub_v['Drain_V'] == drain_v]
        plt.plot(subset_drain_v['Gate_V'], subset_drain_v['Drain_I'], label=f'Sub_V={sub_v}, Drain_V={drain_v:.2f}')
plt.xlabel('Gate_V (V)')
plt.ylabel('Drain_I (A)')
plt.title('Drain_I vs Gate_V for different Drain_V values and Sub_V values')
plt.legend()
plt.grid(True)
plt.show()

# 3D plot for each unique Sub_V
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for sub_v in unique_sub_v:
    subset_sub_v = data[data['Sub_V'] == sub_v]
    unique_drain_v = subset_sub_v['Drain_V'].unique()
    for drain_v in unique_drain_v:
        subset_drain_v = subset_sub_v[subset_sub_v['Drain_V'] == drain_v]
        ax.plot(subset_drain_v['Gate_V'], subset_drain_v['Drain_I'], subset_drain_v['Drain_V'], label=f'Sub_V={sub_v:.2f}, Drain_V={drain_v:.2f}')

ax.set_xlabel('Gate_V (V)')
ax.set_ylabel('Drain_I (A)')
ax.set_zlabel('Drain_V (V)')
ax.set_title('3D Plot of Drain_I vs Gate_V and Drain_V with Sub_V')
ax.legend()
plt.show()
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter

# Load the data
data = pd.read_csv('../../debug_tests/data/Jan_No16VgVdVsub.csv', comment='#')

# Extract unique values for the sweeps
sub_v_values = data['Sub_V'].unique()
drain_v_values = data['Drain_V'].unique()

# Create a 3D plot
fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111, projection='3d')

# Create a color map
colors = plt.cm.viridis(np.linspace(0, 1, len(drain_v_values)))

for j, sub_v in enumerate(sub_v_values):
    sub_v_data = data[data['Sub_V'] == sub_v]
    for _, drain_v in enumerate(drain_v_values):
        drain_v_data = sub_v_data[sub_v_data['Drain_V'] == drain_v]
        ax.plot(drain_v_data['Gate_V'], [sub_v] * len(drain_v_data), drain_v_data['Drain_I'], color=colors[j])

ax.view_init(elev=20, azim=135)
ax.zaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax.zaxis.get_major_formatter().set_powerlimits((0, 0))
ax.set_xlabel('Gate_V')
ax.set_ylabel('Sub_V')
ax.set_zlabel('Drain_I')

ax.set_title('3D Plot of Drain_I vs Gate_V and Sub_V for different Drain_V values')

plt.show()
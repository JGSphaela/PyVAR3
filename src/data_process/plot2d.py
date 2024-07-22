import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import pandas as pd
import numpy as np

data = pd.read_csv('../../debug_tests/data/Nov_No2VgVdVsub2.csv', comment='#')

gate_v_values = data['Gate_V'].unique()
sub_v_values = data['Sub_V'].unique()
drain_v_values = data['Drain_V'].unique()
drain_v_data = []

colors = plt.cm.viridis(np.linspace(0, 1, len(sub_v_values)))
fig, ax = plt.subplots()
# plt.rcParams['text.usetex'] = True

for i, drain_v in enumerate(drain_v_values):
    drain_v_data.append(data[data['Drain_V'] == drain_v])

drain_v_data_split = drain_v_data[30]

for j, sub_v in enumerate(sub_v_values):
    sub_v_data = drain_v_data_split[drain_v_data_split['Sub_V'] == sub_v]
    ax.plot(sub_v_data['Gate_V'], sub_v_data['Drain_I'], color=colors[j])

ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax.yaxis.get_major_formatter().set_powerlimits((0, 0))
ax.set_xlabel(r'$V_{gate}$ [V]')
ax.set_ylabel('Idrain [A]')

ax.set_title(f'Vsub-Idrain for each Vgate when Vdarin = {drain_v_values[30]} V')
plt.show()

# print(gate_v_data)

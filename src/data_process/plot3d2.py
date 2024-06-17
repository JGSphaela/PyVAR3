import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go

# Load the data
data = pd.read_csv('../../debug_tests/Nov_No17IdVg.csv')

# Extract unique values for the sweeps
sub_v_values = data['Sub_V'].unique()
drain_v_values = data['Drain_V'].unique()

# Create a figure
fig = go.Figure()

colors = plt.cm.viridis(np.linspace(0, 1, len(sub_v_values)))

# Add traces for each plane (Sub_V)
for j, sub_v in enumerate(sub_v_values):
    sub_v_data = data[data['Sub_V'] == sub_v]
    for i, drain_v in enumerate(drain_v_values):
        drain_v_data = sub_v_data[sub_v_data['Drain_V'] == drain_v]
        fig.add_trace(go.Scatter3d(
            x=drain_v_data['Gate_V'],
            y=[sub_v] * len(drain_v_data),
            z=drain_v_data['Gate_I'],
            mode='lines',
            line=dict(color=f'rgba({colors[i][0] * 255},{colors[i][1] * 255},{colors[i][2] * 255},1)'),
            name=f"Drain_V={drain_v}"
        ))

# Set labels
fig.update_layout(
    scene=dict(
        xaxis_title='Gate_V',
        yaxis_title='Sub_V',
        zaxis_title='Drain_I'
    ),
    title='3D Plot of Drain_I vs Gate_V and Sub_V for different Drain_V values'
)

# Show the figure
fig.show()

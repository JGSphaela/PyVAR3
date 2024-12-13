import pandas as pd
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv('../../debug_tests/data/teg14_300K_sum.csv', comment='#')

# Extract unique values for the sweeps
sub_v_values = data['Sub_V'].unique()
drain_v_values = data['Drain_V'].unique()

# Create a figure
fig = go.Figure()

# Define the columns for different I values
# i_values = ['Drain_I', 'Gate_I', 'Source_I', 'Sub_I']
i_values = [col for col in data.columns if "_I" in col]
print(i_values)

# Create a color map
colors = plt.cm.viridis(np.linspace(0, 1, len(sub_v_values)))

# Add traces for each I value but set visibility to False initially
for i_val in i_values:
    for j, sub_v in enumerate(sub_v_values):
        sub_v_data = data[data['Sub_V'] == sub_v]
        for i, drain_v in enumerate(drain_v_values):
            drain_v_data = sub_v_data[sub_v_data['Drain_V'] == drain_v]
            fig.add_trace(go.Scatter3d(
                x=drain_v_data['Gate_V'],
                y=[sub_v] * len(drain_v_data),
                z=drain_v_data[i_val],
                mode='lines',
                name=f'{i_val} (Drain_V={drain_v})',
                line=dict(color=f'rgba({colors[j][0] * 255},{colors[j][1] * 255},{colors[j][2] * 255},1)'),
                visible=(i_val == 'Drain_I'),
                hovertemplate=f'Gate_V: %{{x}}<br>Sub_V: %{{y}}<br>{i_val}: %{{z}}<br>Drain_V: {drain_v}<extra></extra>'
            ))

# Create buttons for dropdown
buttons = []
for i_val in i_values:
    visible = [i_val == trace.name.split(' ')[0] for trace in fig.data]
    buttons.append(dict(label=i_val,
                        method='update',
                        args=[{'visible': visible},
                              {'title': f'3D Plot of {i_val} vs Gate_V and Sub_V for different Drain_V values',
                               'scene': {
                                   'xaxis': {'title': 'Gate_V'},
                                   'yaxis': {'title': 'Sub_V'},
                                   'zaxis': {'title': i_val}
                               }}]))

# Add buttons to switch between linear and logarithmic scale for the z-axis
log_button = dict(label='Log Z',
                  method='relayout',
                  args=[{'scene.zaxis.type': 'log'}])

linear_button = dict(label='Linear Z',
                     method='relayout',
                     args=[{'scene.zaxis.type': 'linear'}])

# Update layout with dropdown
fig.update_layout(
    updatemenus=[
        dict(
            buttons=buttons,
            direction="down",
            showactive=True,
            # x=0.17,
            xanchor="left",
            # y=1.15,
            yanchor="top"
        ),
        dict(
            buttons=[linear_button,log_button],
            direction="down",
            showactive=True,
            # x=0.57,
            xanchor="right",
            # y=1.15,
            yanchor="top"
        )
    ],
    scene=dict(
        xaxis=dict(title='Gate_V'),
        yaxis=dict(title='Sub_V'),
        zaxis=dict(title='Drain_I')  # Default z-axis title, will change with dropdown
    ),
    title='3D Plot of Drain_I vs Gate_V and Sub_V for different Drain_V values'
)

# Show the figure
fig.show()
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView
import plotly.io as pio

def create_plot():
    # Load the data
    data = pd.read_csv('your_data.csv')

    # Extract unique values for the sweeps
    sub_v_values = data['Sub_V'].unique()
    drain_v_values = data['Drain_V'].unique()

    # Create a figure
    fig = go.Figure()

    # Define the columns for different I values
    i_values = ['Drain_I', 'Gate_I', 'Source_I', 'Sub_I']

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
                                  {'title': f'3D Plot of {i_val} vs Gate_V and Sub_V for different Drain_V values'}]))

    # Update layout with dropdown
    fig.update_layout(
        updatemenus=[dict(active=0, buttons=buttons)],
        scene=dict(
            xaxis_title='Gate_V',
            yaxis_title='Sub_V',
            zaxis_title='Drain_I'  # Default z-axis title, will change with dropdown
        ),
        title='3D Plot of Drain_I vs Gate_V and Sub_V for different Drain_V values'
    )

    return fig

class PlotlyViewer(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Plotly 3D Plot in PyQt6")
        self.setGeometry(100, 100, 1200, 800)

        layout = QVBoxLayout()
        self.browser = QWebEngineView()

        # Create the plot and convert to HTML
        fig = create_plot()
        html = pio.to_html(fig, full_html=False)

        self.browser.setHtml(html)

        layout.addWidget(self.browser)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
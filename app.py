import pandas as pd
import dash
from dash import dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.subplots as sp
import plotly.graph_objs as go

df = pd.read_csv('correlationGDP.csv')
states = ['{}{}'.format(i, j) for i in ['Ef', 'Ep', 'U', 'N'] for j in ['Ef', 'Ep', 'U', 'N'] if i != j]
ages = [a for a in set(df.age_group) if a != '16-65']
ages.sort()
ages.append('16-65')

# Create a Dash app instance
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Correlations of cyclical components'),
    dcc.Dropdown(
        id='state-dropdown',
        options=[{'label': i, 'value': i} for i in states],
        value=states[0]
    ),
    dcc.Graph(id='time-series-plot'),
    html.Div([  # Container for the legends and text
        html.Div(id='legend1-container', style={'display': 'inline-block', 'width':'15%'}),
        html.Div(id='legend2-container', style={'display': 'inline-block', 'width':'15%'}),
        html.Div(style={'display': 'inline-block', 'width':'10%'}),
        html.Div(id='text-container', style={'display': 'inline-block', 'width' : '60%', 'left-margin':'20px'})
    ])
])


@app.callback(
    Output('time-series-plot', 'figure'),
    [Input('state-dropdown', 'value')]
)
def update_time_series(state):
    x = ages
    filtered_df = df[['age_group'] + [i for i in df.columns if state in i]]

    num_subplots = 9  # Number of subplots
    rows = 1  # Number of rows for subplots
    cols = num_subplots  # Number of columns for subplots

    fig = sp.make_subplots(rows=rows, cols=cols, shared_xaxes=True, shared_yaxes=True)

    # Loop over the subplots and plot the data
    l = -5
    for col in range(1, num_subplots + 1):
        l += 1
        if l <= 0:
            y = [filtered_df[filtered_df['age_group'] == i]['{}_corr_lag{}'.format(state, -1 * l)].values[0] for i in x]
            p = [filtered_df[filtered_df['age_group'] == i]['{}_p_lag{}'.format(state, -1 * l)].values[0] for i in x]
            # blue for positive correlation
            blue_colors = ['#67a9cf' if p_i > 0.1 else
                           '#3690c0' if p_i > 0.05 else
                           '#02818a' if p_i > 0.01 else
                           '#016c59' for p_i in p]
            # red for negative correlation
            red_colors = ['#ef8a62' if p_i > 0.1 else
                          '#e24a33' if p_i > 0.05 else
                          '#d91e05' if p_i > 0.01 else
                          '#b10026' for p_i in p]
            colors = [red_colors[i] if y[i] < 0 else blue_colors[i] for i in range(len(y))]
        else:
            y = [filtered_df[filtered_df['age_group'] == i]['{}_corr_lead{}'.format(state, l)].values[0] for i in x]
            p = [filtered_df[filtered_df['age_group'] == i]['{}_p_lead{}'.format(state, l)].values[0] for i in x]
            blue_colors = ['#67a9cf' if p_i > 0.1 else
                           '#3690c0' if p_i > 0.05 else
                           '#02818a' if p_i > 0.01 else
                           '#016c59' for p_i in p]
            # red for negative correlation
            red_colors = ['#ef8a62' if p_i > 0.1 else
                          '#e24a33' if p_i > 0.05 else
                          '#d91e05' if p_i > 0.01 else
                          '#b10026' for p_i in p]
            colors = [red_colors[i] if y[i] < 0 else blue_colors[i] for i in range(len(y))]
        # Create a horizontal bar chart and add it to the subplot
        fig.add_trace(go.Bar(y=x, x=y, orientation='h', marker=dict(color=colors), name=f'Lag {l}' if l <= 0 else f'Lead {l}'),
                      row=1, col=col)
        fig.update_xaxes(range=[-1, 1], row=1, col=col, title=l)
             
        # Add a shape to mark x=0
        fig.add_shape(type="line", x0=0, x1=0, y0='16-20', y1='16-65', line=dict(color="black", width=1), xref=f'x{col}', yref=f'y{col}')
        # Add a shape to mark x=-0.5
        fig.add_shape(type="line", x0=-0.5, x1=-0.5, y0='16-20', y1='16-65', line=dict(color="black", width=.3, dash='dash'), xref=f'x{col}', yref=f'y{col}')
        # Add a shape to mark x=0.5
        fig.add_shape(type="line", x0=0.5, x1=0.5, y0='16-20', y1='16-65', line=dict(color="black", width=.3, dash='dash'), xref=f'x{col}', yref=f'y{col}')

    fig.update_layout(
        title=f'Correlations of the cycle components of the {state} instantaneous transition rate and the cycle component of the real GDP by Age Group',
        barmode='group',  # 'group' for grouped bars, 'stack' for stacked bars
        yaxis=dict(title='age groups'),
        xaxis=dict(range=[-1, 1]),
        plot_bgcolor='rgb(255, 255, 255)',
        showlegend=False  # Hide the legend
    )

    fig.update_xaxes(showline=True, linewidth=2, linecolor='black')
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black')

    return fig


color_legend_1 = [
    ('#67a9cf', 'p >= 0.1'),
    ('#3690c0', 'p < 0.1'),
    ('#02818a','p < 0.05'),
    ('#016c59', 'p < 0.01')
]

color_legend_2 = [
    ('#ef8a62', 'p >= 0.1'),
    ('#e24a33', 'p < 0.1'),
    ('#d91e05','p < 0.05'),
    ('#b10026', 'p < 0.01')
]


@app.callback(
    Output('legend1-container', 'children'),
    [Input('state-dropdown', 'value')]
)
def update_legend1(state):
    legend_content = html.Div([html.Span('pos. corr.', style={'font-weight': 'bold'})])
    
    for color, label in color_legend_1:
        legend_content.children.append(
            html.Div(label, style={'background-color': color, 'margin': '5px'})
        )
    
    return legend_content

# Callback for the second legend
@app.callback(
    Output('legend2-container', 'children'),
    [Input('state-dropdown', 'value')]
)
def update_legend2(state):
    legend_content = html.Div([html.Span('neg. corr.', style={'font-weight': 'bold'})])
    
    for color, label in color_legend_2:
        legend_content.children.append(
            html.Div(label, style={'background-color': color, 'margin': '5px'})
        )
    
    return legend_content

annotation = """The cyclical components were calculated by applying an HP filter on logs of quarterly average data. \n 
             Correlation was calculated between the cycilcal component of the current transition rate and the cyclical
             component of real GDP shifted by x months."""

@app.callback(
    Output('text-container', 'children'),
    [Input('state-dropdown', 'value')]
)
def update_text_container(state):
    return annotation

if __name__ == '__main__':
    app.run_server(debug=False)

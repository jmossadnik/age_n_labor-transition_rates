import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

# Load and process the data
df = pd.read_csv('cont_STL.csv')
df['date'] = pd.to_datetime(df[['year', 'month']].assign(day=12))
filtered_df = df[df.age_group != ">=65"]
age_group_labels = sorted(set(filtered_df.age_group))

# Define fixed colors for each age group
age_group_colors = {
    '16-19':'#00876c',
    '16-64':'#000000',
    '20-24':'#51a573',
    '25-29':'#88c27b',
    '30-34':'#c2dd85',
    '35-39':'#fff795',
    '40-44':'#fdcb6e',
    '45-49':'#f69e56',
    '50-54':'#e96f4e',
    '55-64':'#d43d51'
}

# Create the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Time Series Visualization"),
    
    html.Label("Select Flow Variable:"),
    dcc.Dropdown(
        id="flow-variable",
        options=[{"label": flow, "value": flow} for flow in [
            "EfEp", "EfU", "EfN", "EpEf", "EpU", "EpN",
            "UEf", "UEp", "UN", "NEf", "NEp", "NU"
        ]],
        value="EfEp"
    ),
    
    html.Label("Select Age Groups:"),
    dcc.Dropdown(
        id="age-group",
        options=[{"label": ag, "value": ag} for ag in age_group_labels],
        value=age_group_labels,
        multi=True
    ),
    
    dcc.Graph(id="line-chart")
])

# Define the callback function to update the line chart
@app.callback(
    dash.dependencies.Output("line-chart", "figure"),
    dash.dependencies.Input("flow-variable", "value"),
    dash.dependencies.Input("age-group", "value")
)
def update_line_chart(flow_variable, selected_age_groups):
    filtered_data = filtered_df[filtered_df.age_group.isin(selected_age_groups)]
    fig = px.line(
        filtered_data,
        x="date",
        y=flow_variable,
        color="age_group",
        color_discrete_map=age_group_colors,  # Use the fixed colors
        title="Time Series",
        labels={"date": "Date", flow_variable: "Flow Variable"}
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(port=8057)

# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX launch data into pandas dataframe (replace with your actual file path)
df = pd.read_csv("spacex_launch_data.csv")

# Calculate max and min payload
max_payload = df['Payload Mass (kg)'].max()
min_payload = df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

    # Task 1: Add a dropdown list to enable Launch Site selection
    dcc.Dropdown(id='site-dropdown',
                 options=[
                    {'label': 'All Sites', 'value': 'ALL'},
                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                 ],
                 value='ALL',
                 placeholder="Select Launch Site",
                 searchable=True
                ),
    html.Br(),

    # Task 2: Add a pie chart to show the total successful launches count for all sites
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),
    # Task 3: Add a slider to select payload range
    dcc.RangeSlider(id='payload-slider',
                    min=min_payload, max=max_payload, step=1000,
                    marks={i: str(i) for i in range(int(min_payload), int(max_payload), 5000)},
                    value=[min_payload, max_payload]),

    # Task 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# Task 2: Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output('success-pie-chart', 'figure'),
              Input('site-dropdown', 'value'))
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        fig = px.pie(df, values='class', names='Launch Site', title='Total Success Launches By Site')
    else:
        filtered_df = df[df['Launch Site'] == selected_site]
        fig = px.pie(filtered_df, values='class', names='class', title=f'Total Launches for site {selected_site}')
    return fig

# Task 4: Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output('success-payload-scatter-chart', 'figure'),
              [Input('site-dropdown', 'value'),
               Input("payload-slider", "value")])
def update_scatter_chart(selected_site, payload_range):
    if selected_site == 'ALL':
        filtered_df = df[(df['Payload Mass (kg)'] >= payload_range[0]) & (df['Payload Mass (kg)'] <= payload_range[1])]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                         title=f'All sites - payload mass between {payload_range[0]:,}kg and {payload_range[1]:,}kg')
    else:
        filtered_df = df[(df['Launch Site'] == selected_site) &
                         (df['Payload Mass (kg)'] >= payload_range[0]) & (df['Payload Mass (kg)'] <= payload_range[1])]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                         title=f'Site {selected_site} - payload mass between {payload_range[0]:,}kg and {payload_range[1]:,}kg')
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

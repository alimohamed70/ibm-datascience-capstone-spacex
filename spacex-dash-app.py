# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the data
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# App
app = dash.Dash(__name__)

# Layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    dcc.Dropdown(
        id='site-dropdown',
        options=[{'label': 'All Sites', 'value': 'ALL'}] +
                [{'label': s, 'value': s} for s in sorted(spacex_df['Launch Site'].unique())],
        value='ALL',
        placeholder='Select a Launch Site here',
        searchable=True
    ),
    html.Br(),

    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),
    dcc.RangeSlider(
        id='payload-slider',
        min=0, max=10000, step=1000,
        value=[min_payload, max_payload],
        marks={0: '0', 2500: '2.5k', 5000: '5k', 7500: '7.5k', 10000: '10k'}
    ),

    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2: Pie chart callback
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        return px.pie(spacex_df, values='class', names='Launch Site',
                      title='Total Successful Launches by Site')
    df_site = spacex_df[spacex_df['Launch Site'] == entered_site].copy()
    df_site['Outcome'] = df_site['class'].map({1: 'Success', 0: 'Failure'})
    return px.pie(df_site, names='Outcome',
                  title=f'Total Success vs Failure for site {entered_site}')

# TASK 4: Scatter plot callback (Payload vs Class, colored by Booster Version Category)
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    Input('site-dropdown', 'value'),
    Input('payload-slider', 'value')
)
def update_scatter(selected_site, payload_range):
    low, high = payload_range
    dff = spacex_df[spacex_df['Payload Mass (kg)'].between(low, high)]
    if selected_site != 'ALL':
        dff = dff[dff['Launch Site'] == selected_site]
        title = f'Correlation between Payload and Success for {selected_site}'
    else:
        title = 'Correlation between Payload and Success for All Sites'
    fig = px.scatter(
        dff,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        hover_data=['Launch Site'],
        title=title
    )
    fig.update_yaxes(title='Class (0 = Failure, 1 = Success)', range=[-0.1, 1.1])
    fig.update_xaxes(title='Payload Mass (kg)')
    return fig

# Run
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)

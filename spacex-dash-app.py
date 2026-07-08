import pandas as pd
import dash
from dash import html, dcc, Input, Output
import plotly.express as px


spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# TASK 1: 
launch_sites = spacex_df['Launch Site'].unique().tolist()
dropdown_options = [{'label': 'All Sites', 'value': 'ALL'}] + \
                   [{'label': site, 'value': site} for site in launch_sites]


app = dash.Dash(__name__)


app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

    # TASK 1: 
    dcc.Dropdown(id='site-dropdown',
                 options=dropdown_options,
                 value='ALL',
                 placeholder="Select a Launch Site here",
                 searchable=True),

    html.Br(),

    # TASK 2: 
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),

    # TASK 3: 
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
        value=[min_payload, max_payload]
    ),

    # TASK 4: 
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2: 
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        
        fig = px.pie(spacex_df,
                     values='Class',
                     names='Launch Site',
                     title='Total Success Launches by Site')
        return fig
    else:
        
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        
        counts = filtered_df['Class'].value_counts().reset_index()
        counts.columns = ['Class', 'count']
        
        counts['Outcome'] = counts['Class'].map({0: 'Failure', 1: 'Success'})
        fig = px.pie(counts,
                     values='count',
                     names='Outcome',
                     title=f'Success vs. Failure for site {entered_site}')
        return fig

# TASK 4: 
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def get_scatter_chart(entered_site, payload_range):
    
    low, high = payload_range
    mask = (spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)
    filtered_df = spacex_df[mask]

    
    if entered_site == 'ALL':
        title = 'Correlation between Payload and Success for All Sites'
        data = filtered_df
    else:
        data = filtered_df[filtered_df['Launch Site'] == entered_site]
        title = f'Correlation between Payload and Success for site {entered_site}'

    
    fig = px.scatter(data,
                     x='Payload Mass (kg)',
                     y='Class',
                     color='Booster Version Category',
                     title=title)
    return fig


if __name__ == '__main__':
    app.run()

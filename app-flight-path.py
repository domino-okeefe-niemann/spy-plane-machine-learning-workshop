#import packages for creating app
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import json
import pandas as pd
import numpy as np
import os   
import plotly.graph_objects as go

# external JavaScript files
external_scripts = [
    'https://www.google-analytics.com/analytics.js',
    {'src': 'https://cdn.polyfill.io/v2/polyfill.min.js'},
    {
        'src': 'https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.10/lodash.core.js',
        'integrity': 'sha256-Qqd/EfdABZUcAxjOkMi8eGEivtdTkh3b65xCZL4qAQA=',
        'crossorigin': 'anonymous'
    }
]

# external CSS stylesheets
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]

app = dash.Dash(__name__,
                external_scripts=external_scripts,
                external_stylesheets=external_stylesheets)

app.scripts.config.serve_locally = True

################################################################
# Configure path for dependencies. This is required for Domino.
#Learn more about Dash on Domino https://blog.dominodatalab.com/building-domino-web-app-dash/

app.config.update({
    'routes_pathname_prefix': '',
    'requests_pathname_prefix': '/{}/{}/r/notebookSession/{}/'.format(
        os.environ.get("DOMINO_PROJECT_OWNER"),
        os.environ.get("DOMINO_PROJECT_NAME"),
        os.environ.get("DOMINO_RUN_ID"))
})

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

#read in data
spy_candidates = pd.read_csv("/mnt/data/new_flight_spy_candidates.csv")
flight_paths = pd.read_csv("/mnt/data/flight_path_data.csv")

#format data for dropdown menu (i.e. plane IDs)
plane_ids = spy_candidates['adshex'].unique()
opts = [{'label' : i, 'value' : i} for i in plane_ids]

#set variable for spy probability
spy_probs = spy_candidates['spy_prob']

mapbox_token = os.environ['mapbox_token']

#plot first flight path
plane1 = flight_paths[flight_paths['adshex'] == plane_ids[0]]

#get center lat and longitude
center_lat = (min(plane1['latitude']) + max(plane1['latitude']))/2
center_lon = (min(plane1['longitude']) + max(plane1['longitude']))/2

#get data points
lat = plane1['latitude']
lon = plane1['longitude']

#create scatter plot
scatter = go.Scattermapbox(lat=lat, lon=lon,
                        mode='markers',
                        marker=go.scattermapbox.Marker(
                        size=7))

#create layout of map
layout = go.Layout(autosize=True,
                    mapbox=go.layout.Mapbox(
                        accesstoken=mapbox_token,
                        bearing=0,
                        center=go.layout.mapbox.Center(
                            lat=center_lat,
                            lon=center_lon
                        ),
                        pitch=0,
                        zoom=6    
                    ),
                )

fig = go.Figure(data = [scatter], layout = layout)

#creat app layout
app.layout = html.Div([
        #title
        html.Div([
            html.H1('Surveillance Plane Identification')
            ],
            style = {'padding' : '30px' , 
                'backgroundColor' : '#F9FAFC'}),
        # dropdown menu
        html.Div([
            html.Label("Choose a plane below:", style={
                                            'margin-right': '2em', 
                                            'fontSize' : '14px',
                                            }),
            dcc.Dropdown(id = 'opt', 
                         options = opts,
                         value = opts[0]['value'],
                         style = {
                            'width':'40%',
                            'verticalAlign':"middle",
                            'fontSize' : '14px'
                         }
                        )], 
            style = {'display':'flex',
                    'align-items':'center',
                    'margin-top':'2em'},
        ),

     #probability output
        html.P(),
        html.Div([
            html.P("Calculated probability of this being a surveillance plane:", 
                   style={'fontSize':'14px', 'fontStyle':'oblique'}),
            html.P(id='result', style = {'fontSize':'30px', 'text-align':'center'})
            ], 
            style = {'display':'flex'}, 
           className="col-sm card card-body bg-light row"),
        #scatter map plot
        html.Div([
        dcc.Graph(id = 'graph', figure=fig)
        ])
])

#create the callback for updating the app figure
@app.callback([Output('graph', 'figure'),
               Output('result', 'children')],
              [Input('opt', 'value')])
#function for updating the app figure
def update_figures(X):
    plane = flight_paths[flight_paths['adshex'] == X]
    lat = plane['latitude']
    lon = plane['longitude']
    center_lat = (min(plane['latitude']) + max(plane['latitude']))/2
    center_lon = (min(plane['longitude']) + max(plane['longitude']))/2

    scatter = go.Scattermapbox(lat=lat, lon=lon,
                            mode='markers',
                            marker=go.scattermapbox.Marker(
                            size=7))

    layout = go.Layout(autosize=True,
                    mapbox=go.layout.Mapbox(
                        accesstoken=mapbox_token,
                        bearing=0,
                        center=go.layout.mapbox.Center(
                            lat=center_lat,
                            lon=center_lon
                        ),
                        pitch=0,
                        zoom=5    
                    ),
                )
    
    fig = go.Figure(data = [scatter], layout = layout)
    
    #update probability
    spy_prob = round(float(spy_probs[spy_candidates['adshex'] == X]), 3)
    prob = '{}'.format(spy_prob)
    return fig, prob

#run app
if __name__ == '__main__':
    app.run_server(host='0.0.0.0',port=8888, debug=True) # Domino hosts all apps at 0.0.0.0:8888
    #app.run_server(host='0.0.0.0',port=8887, debug = True) # for live editing

#import packages for creating app
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import os
import pandas as pd
import numpy as np
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
                external_stylesheets=external_stylesheets, serve_locally = False)

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

#read in data
feds_data = pd.read_csv('/mnt/data/feds_data.csv')
spy_candidates = pd.read_csv("/mnt/data/spy_candidates.csv")

#format data for dropdown menu (i.e. plane IDs)
planes = spy_candidates['adshex']
opts = [{'label' : i, 'value' : i} for i in planes]

#set variable for spy probability
spy_probs = spy_candidates['spy_prob']

#seperate out the steer1 data
x1 = feds_data['steer1']
counts1, _ = np.histogram(feds_data['steer1'], bins= 25)

#create histogram for steer 1 data
hist_1 = go.Histogram(
    x = x1,
    xbins=dict(start=np.min(x1), size= (np.max(x1)-np.min(x1))/25, end=np.max(x1)),
    showlegend = False
)

#data and histrogram for steer 2 variable
x2 = feds_data['steer2']
counts2, _ = np.histogram(feds_data['steer2'], bins= 25)

hist_2 = go.Histogram(
    x = x2,
    xbins=dict(start=np.min(x2), size= (np.max(x2)-np.min(x2))/25, end=np.max(x2)),
    showlegend = False
)

#data and histrogram for squawk code variable
x3 = feds_data['squawk_1']
counts3, _ = np.histogram(feds_data['squawk_1'], bins= 25)

hist_3 = go.Histogram(
    x = x3,
    xbins=dict(start=np.min(x2), size= (np.max(x3)-np.min(x3))/25, end=np.max(x3)),
    showlegend = False
)


#setup up graph layout
layout = go.Layout(
    xaxis_title_text='Value', # xaxis label
    yaxis_title_text='Count', # yaxis label
)

#create figures
fig1 = go.Figure(data = [hist_1], layout = layout)
fig2 = go.Figure(data = [hist_2], layout = layout)
fig3 = go.Figure(data = [hist_3], layout = layout)

#create the app layout itself
app.layout = html.Div([
        html.Div([
            html.H1('Surveillance Plane Identification')
            ],
            style = {'padding' : '30px' , 
                'backgroundColor' : '#F9FAFC'}),
        # dropdown
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
    
    #steer plots
    html.P(),
    html.Button('Tell me why!', id='button', style={'fontSize':'14px'}),
    html.P(),
    html.Div(id='button_container', 
        children=[
        html.Div(
                [
                html.Div(
                    [
                        html.H3('Steer 1'),
                        dcc.Graph(id = 'plot1', figure=fig1)
                    ], 
                    className="col-sm"
                ),

                html.Div(
                    [
                        html.H3('Steer 2'),
                        dcc.Graph(id = 'plot2', figure=fig2)
                    ], 
                    className="col-sm"),

                html.Div(
                    [
                        html.H3('Squawk Code'),
                        dcc.Graph(id = 'plot3', figure=fig3)
                    ], 
                    className="col-sm")

                ], 
                className="row",
                style = {'display':'flex', 'flex-wrap':'wrap'})
        ]),
    ], 
    className='container')


@app.callback(
    dash.dependencies.Output('button_container', 'style'),
    [dash.dependencies.Input('button', 'n_clicks')],
    )
def button_toggle(n_clicks):
    if n_clicks:
        pass
    else:
        n_clicks=0
    if n_clicks % 2 == 0:
        return {'display': 'none'}
    else:
        return {'display': 'block'}


#create the callback for updating the app figure
@app.callback([Output('plot1', 'figure'),
               Output('plot2', 'figure'),
               Output('plot3', 'figure'),
               Output('result', 'children')],
              [Input('opt', 'value')])
#function for updating the app figure
def update_figures(X):
    scatter_1 = go.Scatter(
        x = [float(spy_candidates.loc[spy_candidates['adshex'] == X,'steer1'])],
        y = [max(counts1)],
        name = X,
        mode='markers',
        marker=dict(size=[20],
                color=['green'])   
    )
    scatter_2 = go.Scatter(
        x = [float(spy_candidates.loc[spy_candidates['adshex'] == X,'steer2'])],
        y = [max(counts2)],
        name = X,
        mode='markers',
        marker=dict(size=[20],
                color=['green'])   
    )
    scatter_3 = go.Scatter(
        x = [float(spy_candidates.loc[spy_candidates['adshex'] == X,'squawk_1'])],
        y = [max(counts3) + 5],
        name = X,
        mode='markers',
        marker=dict(size=[20],
                color=['green'])   
    )
    fig1 = go.Figure(data = [hist_1, scatter_1], layout = layout)
    fig2 = go.Figure(data = [hist_2, scatter_2], layout = layout)
    fig3 = go.Figure(data = [hist_3, scatter_3], layout = layout)
    
    legend=go.layout.Legend(
        x=0,
        y=1.2,
        traceorder="normal",
        font=dict(
            family="sans-serif",
            size=12,
            color="black"
        ),
        bgcolor="LightSteelBlue",
        bordercolor="Black",
        borderwidth=2
        )
    fig1.update_layout(legend = legend)
    fig2.update_layout(legend = legend)
    fig3.update_layout(legend = legend)
    
    spy_prob = round(float(spy_probs[spy_candidates['adshex'] == X]), 3)
    prob = '{}'.format(spy_prob)
    
    return fig1, fig2, fig3, prob


if __name__ == '__main__':
    app.run_server(host='0.0.0.0',port=8888) # Domino hosts all apps at 0.0.0.0:8888
    #app.run_server(host='0.0.0.0',port=8887, debug = True) # for live testing
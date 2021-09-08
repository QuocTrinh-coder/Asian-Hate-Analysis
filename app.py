
import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go 
from dash.dependencies import Input, Output
import numpy as np
from flask import Flask
import flask
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import os
import psycopg2
import datetime


from dash import dash_table
from flask import Flask
import logging
from flask import render_template


from flask import Flask
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)
server = app.server

colors = {
    'background': '#FFFFFF',
    'text': '#000000'}

#data section
df = pd.read_csv("ALL_TWEET_SENTIMENT.csv")
df33= pd.read_csv("ALL_TWEET_SENTIMENT.csv")
df2 = pd.read_csv("Unemployment.csv")
#df = df.groupby(['state', 'incident_type', 'fy_declared'])
#df.set_index()
# print(df)
df['Count of China Virus'] = df['Text'].str.count('China Virus')
df['Count of fuckchina'] = df['Text'].str.count('fuckchina')
df['Count of Chinacoronavirus'] = df['Text'].str.count('Chinacoronavirus')
df['Count of China Corona Virus'] = df['Text'].str.count('China Corona Virus')
df['Count of Go Back to China'] = df['Text'].str.count('Go Back to China')
df['Count of chinaliedpeopledied'] = df['Text'].str.count('chinaliedpeopledied')
df['Count of Asian Virus'] = df['Text'].str.count('Asian Virus')
df['Count of Wuhan Virus'] = df['Text'].str.count('Wuhan Virus')
df['Count of Chinese Virus'] = df['Text'].str.count('Chinese Virus')
df['Count of Bat Eater'] = df['Text'].str.count('Bat Eater')
df['Count of nukechina'] = df['Text'].str.count('nukechina')
#app layout section







app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    
    html.H1("Racist Tweet Growth Rate Since Covid Hit", 
            style={'textAlign': 'center',
                   'color': colors['text']}),
        dcc.Dropdown(id = "selected_keyword",
                options=[
                    {"label": x, "value": x} for x in sorted(df33['key word'].unique())],
                 multi=False,
                value= "China Virus"
                 ), 
    html.Div(id ='output_container'),
    html.Br(),    
    dcc.Graph(id = 'my_tweet_map', figure={}),
    dcc.Graph(id = 'my_unemployment_map', figure={})
])

@app.callback(
     [Output(component_id='my_tweet_map', component_property='figure'),
       Output(component_id='my_unemployment_map', component_property='figure')],
    [Input(component_id='selected_keyword', component_property='value')])
def update_graph(option_selected):
    df2 = pd.read_csv("Unemployment.csv")

    df2['Datetime'] = pd.to_datetime(df2['Datetime'], errors='coerce')

    df2.index = df2['Datetime']
    df2 = df2.resample('M').sum().reset_index()
    df2['Datetime'] = pd.to_datetime(df2['Datetime'], utc = True)
    dftrump = pd.read_csv("Trump Hate Tweets - Sheet1.csv")
    dftrump['Text'] = dftrump['Details: ']
    dftrump['Count of China Virus'] = dftrump['Text'].str.count('China Virus')
    dftrump['Count of fuckchina'] = dftrump['Text'].str.count('fuckchina')
    dftrump['Count of Chinacoronavirus'] = dftrump['Text'].str.count('Chinacoronavirus')
    dftrump['Count of China Corona Virus'] = dftrump['Text'].str.count('China Corona Virus')
    dftrump['Count of Go Back to China'] = dftrump['Text'].str.count('Go Back to China')
    dftrump['Count of chinaliedpeopledied'] = dftrump['Text'].str.count('chinaliedpeopledied')
    dftrump['Count of Asian Virus'] = dftrump['Text'].str.count('Asian Virus')
    dftrump['Count of Wuhan Virus'] = dftrump['Text'].str.count('Wuhan Virus')
    dftrump['Count of Chinese Virus'] = dftrump['Text'].str.count('Chinese Virus')
    dftrump['Count of Bat Eater'] = dftrump['Text'].str.count('Bat Eater')
    dftrump['Count of nukechina'] = dftrump['Text'].str.count('nukechina')
    dftrump['Date:'] = pd.to_datetime(dftrump['Date:'], errors='coerce')
    dftrump.index = dftrump['Date:']
    dftrump = dftrump.resample('M').sum().reset_index()
    dftrump['Datetime'] = dftrump['Date:']
    dff = df.copy()
    dftrump = dftrump.copy()
    dff['Datetime'] = pd.to_datetime(dff['Datetime'], errors='coerce')
    dff = dff.set_index("Datetime")
    dff = dff.resample('M').sum()
    dff = dff.reset_index()
    y = str(option_selected)
    dff = dff[['Datetime','Count of {}'.format(y) ]]
    
    dftrump = dftrump[['Datetime','Count of {}'.format(y) ]]
    dftrump['Datetime'] = pd.to_datetime(dftrump['Datetime'], utc = True)
    dff['Datetime'] = pd.to_datetime(dff['Datetime'], utc = True)
    merged = dftrump.merge(dff, how='outer', on='Datetime')
    
    result = pd.merge(merged, df2, how= 'outer', on=["Datetime"])

    fig = px.line(result, x="Datetime", y=result['Count of {}'.format(y)+'_y'], title = "Covid Cases Increases by Date in Different States")
    fig.add_scatter(x=result['Datetime'], y=result['Count of {}'.format(y)+'_x'])
    fig.add_scatter(x=result['Datetime'], y=result['Unemployment_Rate'])
    

    fig2 = px.line(df2, x="Datetime", y= 'Unemployment_Rate', title = "Covid Cases Increases by Date in Different States")
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black')
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black')

    return fig, fig2 #the return obj will be the output and if there are many output, it will go in order ( 1 obj => 1st output)


if __name__ == '__main__':
    app.run_server(debug=True,use_reloader=False, port = 9001)


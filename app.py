
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
# df2 = pd.read_csv("unemployment.csv")
key_words=["China Virus",
'Wuhan Virus',
'Chinacoronavirus',
'China Corona Virus',
'Asian Virus',
'fuckchina',
'Go Back to China',
'chinaliedpeopledied',
'Chinese Virus',
'Bat Eater',
'nukechina'  ]

dfkeywords= pd.DataFrame(key_words,columns=['key_words'])


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


def normalize(df):
    result = df.copy()
    for feature_name in df.columns:
        max_value = df[feature_name].max()
        min_value = df[feature_name].min()
        result[feature_name] = (df[feature_name] - min_value) / (max_value - min_value)
    return result




app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[

    html.H1("Racist Tweet Growth Rate Since Covid Hit",
            style={'textAlign': 'center',
                   'color': colors['text']}),
        dcc.Dropdown(id = "selected_keyword",
                options=[
                    {"label": x, "value": x} for x in sorted(dfkeywords['key_words'].unique())],
                 multi=False,
                value= "China Virus"
                 ),
    html.Div(id ='output_container'),
    html.Br(),
    dcc.Graph(id = 'my_tweet_map', figure={}),
    dcc.Graph(id = 'my_unemployment_map', figure={}),
    dcc.Graph(id = 'my_stack_bargraph', figure={}),
    dcc.Graph(id = 'my_covid_graph', figure = {})
])

@app.callback(
[Output(component_id='my_tweet_map', component_property='figure'),
       Output(component_id='my_unemployment_map', component_property='figure'),
       Output(component_id='my_stack_bargraph', component_property='figure'),
       Output(component_id='my_covid_graph', component_property='figure')],
    [Input(component_id='selected_keyword', component_property='value')])
def update_graph(option_selected):
    # df2 =df2.copy()
    # df2['Datetime'] = pd.to_datetime(df2['Datetime'], errors='coerce')
    #
    # df2.index = df2['Datetime']
    # df2 = df2.resample('M').sum().reset_index()
    # df2['Datetime'] = pd.to_datetime(df2['Datetime'], utc = True)

    dftweet = df.copy()
    dftweet['Datetime'] = pd.to_datetime(dftweet['Datetime'], errors='coerce')
    s = pd.to_datetime(dftweet['Datetime'])
    df33 = s.groupby(s.dt.floor('d')).size().reset_index(name='count')
    df33['Datetime'] = pd.to_datetime(df33['Datetime'], errors='coerce')


    dftrump = pd.read_csv("Trump Hate Tweets - Sheet1.csv")
    dftrump['Date:'] = pd.to_datetime(dftrump['Date:'], errors='coerce')
    ss = pd.to_datetime(dftrump['Date:'])
    dff = ss.groupby(ss.dt.floor('d')).size().reset_index(name='count')
    dff["Datetime"] = dff["Date:"]
    dff= dff[['Datetime', 'count']]
    dff['Datetime'] = pd.to_datetime(dff['Datetime'], errors='coerce')
    dff['Datetime'] = pd.to_datetime(dff['Datetime'], utc = True)
    df33['Datetime'] = pd.to_datetime(df33['Datetime'], utc = True)

    mergedd = df33.merge(dff, how='right', on='Datetime')
    dfcovid = pd.read_csv('covid_cases_US.csv')

    # merged = normalize(merged)
    dffn = normalize(df33)
    dftrumpn = normalize(mergedd)
    # df2n = normalize(df2)
    tweet = pd.read_csv("ALL_TWEET_SENTIMENT.csv",parse_dates=['Datetime'])
    tweet = tweet.set_index('Datetime')

    result = tweet.reset_index().groupby(                                        \
              [pd.Grouper(key='Datetime', freq='1d'), 'analysis'] \
            ).count().unstack(fill_value=0).stack().reset_index()
    result=result[pd.to_numeric(result['Text'], errors='coerce').notnull()]
    resulty = result[['Datetime', 'Text', ]]

    covid = pd.read_csv('Covid_data.csv')
    covid['submission_date'] = pd.to_datetime(covid['submission_date'], errors='coerce')

    covid.index = covid['submission_date']
    covid = covid.resample('d').sum().reset_index()
    covid['submission_date'] = pd.to_datetime(covid['submission_date'], utc = True)
    covid = covid[['submission_date', 'new_case']]
    covid=covid[pd.to_numeric(covid['new_case'], errors='coerce').notnull()]
    covid['new_case'] = covid['new_case'].astype(float)

    # result['Text'] = result['Text'].astype(float)
    resultn = normalize(resulty)

    fig = px.line(result, x= 'Datetime', y=resultn['Text'],color='analysis', title = "Covid Cases Increases by Date in Different States")
    fig.add_scatter(x=mergedd['Datetime'], y=dftrumpn['count_y'])
#     fig.add_scatter(x=df2['Datetime'], y=df2n['Unemployment_Rate'])


    #fig= px.line(covid, x= "Date", y=covid['positiveIncrease'],title = "Tweet Mention of China Virus")
    # fig.add_scatter(x=covid['submission_date'], y=covidn['new_case'])
    #Unemployment Rate
    fig2 = px.bar(result, x="Datetime", y="index", color="key word", title="Count of Racial Slurs Used on Twitter")
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black')
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black')



    tweet = pd.read_csv("ALL_TWEET_SENTIMENT.csv")
    tweet = tweet[tweet['key word'].map(tweet['key word'].value_counts()) > 900]

    tweet['Datetime'] = pd.to_datetime(tweet['Datetime'], errors='coerce')
    tweet['Datetime'] = pd.to_datetime(tweet['Datetime'], utc = True)
    tweet = tweet[['Datetime', 'key word']]
    # tweet = tweet.set_index('Datetime')

    result = tweet.reset_index().groupby(                                        \
                  [pd.Grouper(key='Datetime', freq='1w'), 'key word'] \
                ).count().unstack(fill_value=0).stack().reset_index()
    # result=result[pd.to_numeric(result['new_case'], errors='coerce').notnull()]
    fig3 = px.bar(result, x="Datetime", y="index", color="key word", title="Count of Racial Slurs Used on Twitter")
    #Need Data for Covid graph
    covid_data = pd.read_csv("Covid_data.csv")

    covid_data.index = covid_data['submission_date']
    covid_data = covid_data.resample('d').sum().reset_index()
    covid_data['submission_date'] = pd.to_datetime(covid_data['submission_date'], utc = True)
    covid_data = covid_data[['submission_date', 'new_case']]
    covid_data=covid_data[pd.to_numeric(covid_data['new_case'], errors='coerce').notnull()]
    covid_data['new_case'] = covid_data['new_case'].astype(float)


    result = covid_data.reset_index().groupby(                                        \
            [pd.Grouper(key='submission_case', freq='1w'), 'key word'] \
            ).count().unstack(fill_value=0).stack().reset_index()
    fig4 = px.line(result, x = "submission_date", y = "new_case", title = "Graph of New Covid Cases")
    fig3 = px.bar(result, x="Datetime", y="index", color="key word", title="Count of Racial Slurs Used on Twitter")

    return fig, fig2, fig3, fig4  #the return obj will be the output and if there are many output, it will go in order ( 1 obj => 1st output)


if __name__ == '__main__':
    app.run_server(debug=True,use_reloader=False, port = 9001)


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

import dash_bootstrap_components as dbc
from dash import dash_table
from flask import Flask
import logging
from flask import render_template


from flask import Flask
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server,  external_stylesheets=[dbc.themes.GRID])
server = app.server

#data section
df = pd.read_csv("ALL_TWEET_SENTIMENT.csv")
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


#app layout section


def normalize(df):
    result = df.copy()
    for feature_name in df.columns:
        max_value = df[feature_name].max()
        min_value = df[feature_name].min()
        result[feature_name] = (df[feature_name] - min_value) / (max_value - min_value)
    return result


colors = {
    'background': '#FFFFFF',
    'text': '#808080'}

#data section
df = pd.read_csv("ALL_TWEET_SENTIMENT.csv")
df33= pd.read_csv("ALL_TWEET_SENTIMENT.csv")

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




app.layout = html.Div(
        html.Div(style={'backgroundColor': colors['background'], 'color': colors['text'], 'height':'100vh', 'width':'100%', 'height':'100%', 'top':'0px', 'left':'0px'},
                 children=[
                    html.Div(className='four columns div-user-controls',
                             children=[

                                 html.H1('How has covid-19, Trump, and unemployment rates impacted anti-Asian sentiment on Twitter?',style={'textAlign': 'center', 'color': 'black'}),
        html.H4("Amidst a global pandemic, the number of reported Asian-related crimes have spiked. Derogatory terms such as “China-Virus” sponsored by former President Donald Trump have sparked xenophobia and racism towards the Asian Community. His actions have given life to new disgustingly blatantly racist slurs. In combination with fears of COVID-19 and growing unemployment around the country, China has been pinned by many for their misfortune. The Asian-American community however has been subject to racial discrimination and violence, with news surfacing all around the country, from an elderly Asian woman attacked in San Francisco, California, forced to defend herself with a wooden plank, to the deadly spa shootings in Atlanta Georgia. Violence against the Asian-American community is rising.", style={'textAlign': 'center',  'fontSize': 14}),
        html.H4("Our mission is to bring to light the ongoing rise in Anti-Asian sentiment in society and factors relating to its growth, by studying the correlation between national COVID-19 case surges, unemployment, Trump’s use of Asian derogatory terms, and racist tweets on Twitter. ", style={'textAlign': 'center',  'fontSize': 14})  ,
        html.H4("We stand in solidarity with the Asian-American Community.", style={'textAlign': 'center',  'fontSize': 14}),
                                 html.Div(
                                     className='dropdown_items',
                                     children=[    dcc.Dropdown(id = "selected_keyword",
                options=[
                    {"label": x, "value": x} for x in sorted(df33['key word'].unique())],
                 multi=False,
                value= "China Virus"
                 ),
                                         dbc.Row([
                                             dbc.Col(dcc.Graph(id="my_tweet_map"),md=12),


                                         ])
                                     ],
                                     style={'color': '#1E1E1E'})
                                ]
                             ),
                    html.Div(className='eight columns div-for-charts bg-grey',
                             children=[
                                 dbc.Row([
                                 dbc.Col(dcc.Graph(id="my_covid_map"),md=6),
                                dbc.Col(dcc.Graph(id="unemployment_graph"),md=6)
                                 ])
                             ]), dbc.Row([
                                dbc.Col(md=3),
                                dbc.Col(dcc.Graph(id="stack_bargraph"),md=12)


                                 ]), dbc.Row([
                                dbc.Col(md=3),



                                 ])

                                                   ])
)



@app.callback(
     Output(component_id='my_tweet_map', component_property='figure'),
       Output(component_id='stack_bargraph', component_property='figure'),
      Output(component_id='my_covid_map', component_property='figure'),
      Output(component_id='unemployment_graph', component_property='figure'),
    [Input(component_id='selected_keyword', component_property='value')])
def update_graph(option_selected):
    df2 = pd.read_csv("Unemployment.csv")
    df2['Datetime'] = pd.to_datetime(df2['Datetime'], errors='coerce')
    #
    df2.index = df2['Datetime']
    df2 = df2.resample('M').sum().reset_index()
    df2['Datetime'] = pd.to_datetime(df2['Datetime'], utc = True)
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
    df2n = normalize(df2)
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
    covid = covid[['submission_date', 'new_death']]
    covid=covid[pd.to_numeric(covid['new_death'], errors='coerce').notnull()]
    covid['new_death'] = covid['new_death'].astype(float)
    covidn = normalize(covid)
    # result['Text'] = result['Text'].astype(float)
    resultn = normalize(resulty)
    fig = px.line(result, x= 'Datetime', y=resultn['Text'],color='analysis', title = "Trump and Twitter Tweets with Anti-Asian Vocabularly Over Time ",
    labels = {'x':"This is a graph comparing Trump’s use of Anti-Asian rhetoric on Twitter, to the overall trends of posts on Twitter that use Anti-Asian slurs. Negative Tweets refer to tweets that are hateful towards the Asian Community. Positive Tweets refer to Tweets that are in opposition to Asian hate or are in support of ending Asian hate. Neutral refers to tweets that are neither positive nor negative. Select lines in the key to make the corresponding line disappear from the graph. The data from Trump’s tweets were scraped from https://www.thetrumparchive.com/. The overall tweets were scraped from Twitter’s database using a Twitter developer account.\n *All values were normalized on the y-axis for viewing purposes*",
              'y':'Magnitude'})
    fig.add_scatter(x=mergedd['Datetime'], y=dftrumpn['count_y'],   name='Anti-Asian Trump Tweets',)
    fig4 = px.line(x=df2['Datetime'], y=df2['Unemployment_Rate'], title = "Unemployment Rate",
    labels = {'x':"This is a graph comparing the relationship between unemployment in the US and Anti-Asian tweets.\n Select the line in the key to make the corresponding line disappear from the graph.\n The National unemployment data used in the graph was gathered from https://www.bls.gov/. The Anti-Asian Tweets were scraped using a Twitter developer account from Twitter’s database.",
              'y':'National Unemployment Rate'})


    #fig= px.line(covid, x= "Date", y=covid['positiveIncrease'],title = "Tweet Mention of China Virus")
#     fig.add_scatter(x=covid['submission_date'], y=covidn['new_death'])
    fig3 = px.line(covid, x='submission_date', y=covid['new_death'], title= "New Covid Cases Nationally",
    labels = {'x':"This is a graph comparing the rise in national COVID-19 cases and Anti-Asian tweets on Twitter.  Select the line in the key to make the corresponding line disappear from the graph. The data of national COVID-19 cases were gathered from the CDC at: https://data.cdc.gov/Case-Surveillance/United-States-COVID-19-Cases-and-Deaths-by-State-o/9mfq-cb36. The Anti-Asian Tweets were scraped from Twitter’s database using a Twitter developer account.",
              'y':'Number of New COVID-19 Deaths'})
    fig3.add_scatter(x=df33['Datetime'], y=df33['count'],   name='Anti-Asian Tweets',)



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
    fig2 = px.bar(result, x="Datetime", y="index", color="key word", title="Count of Racial Slurs Used on Twitter",
    labels = {'x':"This is a graph representing the number of times a specific derogatory term was used each week along side a timeline of when Trump used Anti-Asian Rhetoric on Twitter. Select any of the keywords in the key to make the corresponding bar disappear from the graph. Data of specific derogatory terms directed towards Asians were scraped from Twitter’s database. The dates of Trump’s Tweets were scraped from https://www.thetrumparchive.com/.",
              'y':'Number of Tweets'})
    fig2.add_scatter(x=mergedd['Datetime'], y=dftrumpn['count_y'], mode='markers')

    # fig2 = px.line(df2, x="Datetime", y= 'Unemployment_Rate', title = "Covid Cases Increases by Date in Different States")
    return fig, fig2, fig3, fig4  #the return obj will be the output and if there are many output, it will go in order ( 1 obj => 1st output)


if __name__ == '__main__':
    app.run_server(debug=True,use_reloader=False, port = 9001)

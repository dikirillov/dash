import dash
import numpy as np
from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
from urllib.request import urlopen
import json
import plotly.express as px
from itertools import cycle, islice

dash.register_page(__name__)

df = pd.read_csv("crimedata.csv")
df = df.fillna(0)

murders_count = pd.melt(df[["communityName", "state", "murders"]], id_vars=["communityName", "state"], var_name="MurdersCnt", value_name="Perc")
murders_count = murders_count[murders_count["Perc"] != 0].reset_index()

murders_per_pop = pd.melt(df[["communityName", "state", "murdPerPop"]], id_vars=["communityName", "state"], var_name="MurdersCnt", value_name="Perc")
murders_per_pop = murders_per_pop[murders_per_pop["Perc"] != 0].reset_index()


fig_mur_1 = px.bar(data_frame=murders_count, x="communityName", y="Perc", log_y=True)
fig_mur_2 = px.bar(data_frame=murders_per_pop, x="communityName", y="Perc", log_y=True)
fig_mur_1.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

layout = html.Div(children=[
    html.Div([
        html.Div([
            dcc.Markdown('Select State'),
            dcc.Dropdown(murders_count.state.unique(), murders_count.state[0], id='state_1_dropdown'),
        ]),
    ], style={'columnCount': 1, 'align': 'center'}),

    html.Div([
        html.Div([
            dcc.Markdown('Murders distribution'),
            dcc.Graph(
                id='Murders_1_bar',
                figure=fig_mur_1,
            ),
        ]),
        html.Div([
            dcc.Markdown('Murders per population distribution'),
            dcc.Graph(
                id='Murders_2_bar',
                figure=fig_mur_2,
            ),
        ]),
    ], style={'columnCount': 1, 'align': 'center'})
])

@callback(
    Output("Murders_1_bar", 'figure'),
    Input("state_1_dropdown", "value")
)
def update_pue_1(state):
    fig_mur_1 = px.bar(data_frame=murders_count[(murders_count.state == state)], x="communityName", y="Perc", log_y=True, color=np.log(murders_count[(murders_count.state == state)].Perc))
    fig_mur_1.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig_mur_1.update_xaxes(categoryorder="total ascending")
    return fig_mur_1

@callback(
    Output("Murders_2_bar", 'figure'),
    Input("state_1_dropdown", "value")
)
def update_pue_2(state):
    fig_mur_2 = px.bar(data_frame=murders_per_pop[(murders_per_pop.state == state)], x="communityName", y="Perc", log_y=True, color=np.log(murders_per_pop[(murders_per_pop.state == state)].Perc))
    fig_mur_2.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig_mur_2.update_xaxes(categoryorder="total ascending")
    return fig_mur_2

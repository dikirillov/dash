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

df["total_crimes_per_people"] = df["murdPerPop"] + \
                                df["rapesPerPop"] + \
                                df["robbbPerPop"] + \
                                df["assaultPerPop"] + \
                                df["burglPerPop"] + \
                                df["larcPerPop"] + \
                                df["autoTheftPerPop"] + \
                                df["arsonsPerPop"]
crimes_count = pd.melt(df[["state", "total_crimes_per_people", "racepctblack", "PctUnemployed"]], id_vars=["state", "PctUnemployed", "racepctblack"], var_name="CrimesStat", value_name="Perc")
violant_crimes_count = pd.melt(df[["state", "ViolentCrimesPerPop", "racepctblack", "PctUnemployed"]], id_vars=["state", "PctUnemployed", "racepctblack"], var_name="CrimesStat", value_name="Perc")
non_violent_crimes_count = pd.melt(df[["state", "nonViolPerPop", "racepctblack", "PctUnemployed"]], id_vars=["state", "PctUnemployed", "racepctblack"], var_name="CrimesStat", value_name="Perc")

fig_mur_1 = px.histogram(data_frame=crimes_count, x="racepctblack", y="Perc", log_y=True, histfunc='avg', text_auto="y")
fig_mur_1.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

fig_mur_2 = px.histogram(data_frame=crimes_count, x="PctUnemployed", y="Perc", log_y=True, histfunc='avg', text_auto="y")
fig_mur_2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

layout = html.Div(children=[
    html.Div([
        html.Div([
            dcc.Markdown('Select State'),
            dcc.Dropdown(crimes_count.state.unique(), crimes_count.state[0], id='state_1_dropdown'),
            dcc.Markdown('Select gravity of crime'),
            dcc.Dropdown(["all", "violent", "non violent"], 'all', id='crime_1_dropdown'),
            dcc.Markdown('Log mode'),
            dcc.Dropdown(["on", "off"], 'on', id='log_1_dropdown'),
        ]),
    ], style={'columnCount': 1, 'align': 'center'}),

    html.Div([
        html.Div([
            dcc.Markdown('Crimes distribution by black per population'),
            dcc.Graph(
                id='Distr_1_bar',
                figure=fig_mur_1,
            ),
        ]),
        html.Div([
            dcc.Markdown('Crimes distribution by unemployed per population'),
            dcc.Graph(
                id='Distr_2_bar',
                figure=fig_mur_2,
            ),
        ]),
    ], style={'columnCount': 1, 'align': 'center'})
])

@callback(
    Output("Distr_1_bar", 'figure'),
    Input("state_1_dropdown", "value"),
    Input("crime_1_dropdown", "value"),
    Input("log_1_dropdown", "value")
)
def update_pue_1(state, type, mode):
    log_mode = (mode == 'on')
    cur_df = pd.DataFrame
    if type == "all":
        cur_df = crimes_count[(crimes_count.state == state)]
    elif type == "violent":
        cur_df = violant_crimes_count[(violant_crimes_count.state == state)]
    else:
        cur_df = non_violent_crimes_count[(non_violent_crimes_count.state == state)]
    fig_mur_1 = px.histogram(data_frame=cur_df, x="racepctblack", y="Perc", log_y=log_mode, histfunc='avg', text_auto="y")
    fig_mur_1.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig_mur_1.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                      marker_line_width=1.5, opacity=0.6)
    return fig_mur_1


@callback(
    Output("Distr_2_bar", 'figure'),
    Input("state_1_dropdown", "value"),
    Input("crime_1_dropdown", "value"),
    Input("log_1_dropdown", "value")
)
def update_pue_1(state, type, mode):
    log_mode = (mode == 'on')
    cur_df = pd.DataFrame
    if type == "all":
        cur_df = crimes_count[(crimes_count.state == state)]
    elif type == "violent":
        cur_df = violant_crimes_count[(violant_crimes_count.state == state)]
    else:
        cur_df = non_violent_crimes_count[(non_violent_crimes_count.state == state)]
    fig_mur_2 = px.histogram(data_frame=cur_df, x="PctUnemployed", y="Perc", log_y=log_mode, histfunc='avg', text_auto="y")
    fig_mur_2.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig_mur_2.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                      marker_line_width=1.5, opacity=0.6)
    return fig_mur_2

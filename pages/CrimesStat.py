import dash
from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px

dash.register_page(__name__)

df = pd.read_csv("crimedata.csv")
df = df.fillna(0)

crime_data = pd.melt(df[["communityName", "state", "murders", "rapes", "robberies", "assaults", "burglaries", "larcenies", "autoTheft", "arsons"]], id_vars=["communityName", "state"], var_name="CrimeType", value_name="Perc")
thefts_data = pd.melt(df[["communityName", "state", "robberies", "burglaries", "larcenies", "autoTheft",]], id_vars=["communityName", "state"], var_name="TheftType", value_name="Perc")


fig_1 = px.pie(data_frame=crime_data, values="Perc", names="CrimeType", hole=.4, hover_name="CrimeType")
fig_1.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

fig_2 = px.pie(data_frame=thefts_data, values="Perc", names="TheftType", hole=.4, hover_name="TheftType")
fig_2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

layout = html.Div(children=[
    html.Div([
        html.Div([
            dcc.Markdown('Select State'),
            dcc.Dropdown(crime_data.state.unique(), crime_data.state[0], id='state_1_dropdown'),
            dcc.Markdown('Select community'),
            dcc.Dropdown(crime_data.communityName.unique(), crime_data.communityName[0], id='community_stat_dropdown'),
        ]),
    ], style={'columnCount': 1, 'align': 'center'}),

    html.Div([
        html.Div([
            dcc.Markdown('Crime distribution'),
            dcc.Graph(
                id='Crime_1_pie',
                figure=fig_1,
            ),
        ]),
        html.Div([
            dcc.Markdown('Thefts distribution'),
            dcc.Graph(
                id='Theft_1_pie',
                figure=fig_2,
            ),
        ]),
    ], style={'columnCount': 1, 'align': 'center'})
])

@callback(
    Output("community_stat_dropdown", 'options'),
    Input("state_1_dropdown", "value")
)
def update_counties_1(val):
    res = crime_data[crime_data.state == val].communityName.unique()
    return res

@callback(
    Output("Crime_1_pie", 'figure'),
    Input("community_stat_dropdown", "value"),
    Input("state_1_dropdown", "value")
)
def update_pue_1(community, state):
    fig_1 = px.pie(data_frame=crime_data[(crime_data.communityName == community) & (crime_data.state == state)], values="Perc", names="CrimeType", hole=.4, hover_name="CrimeType")
    fig_1.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig_1


@callback(
    Output("Theft_1_pie", 'figure'),
    Input("community_stat_dropdown", "value"),
    Input("state_1_dropdown", "value")
)
def update_pue_1(community, state):
    fig_1 = px.pie(data_frame=thefts_data[(thefts_data.communityName == community) & (thefts_data.state == state)], values="Perc", names="TheftType", hole=.4, hover_name="TheftType")
    fig_1.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig_1

import json

import dash_bootstrap_components as dbc
import numpy as np
from dash import callback_context
from dash.dependencies import Output, Input, MATCH, ALL, State
from dash.exceptions import PreventUpdate
from plotly import graph_objs as go

from utils import rgb_to_rgba
from WebApp import WebApp
from config import AppConfig
from models import AnalyzedInterventions


@WebApp.callback(
    Output({'id': 'dd-parties-div', 'loc': MATCH}, 'children'),
    Input({'type': 'dd-party', 'loc': MATCH, 'ref': ALL}, 'n_clicks'),
    prevent_initial_call=True
)
def update_party_dropdown(_):
    fired_prop_id = callback_context.triggered[0]['prop_id']
    selected_party = fired_prop_id.split('.')[0]
    data = json.loads(selected_party)
    actual_party = data['ref']

    dropdown_menu = dbc.DropdownMenu(
        [
            dbc.DropdownMenuItem(
                party,
                key=party,
                id={
                    'type': 'dd-party',
                    'loc': data['loc'],
                    'ref': party
                }
            ) for party in AppConfig.PARTY_ABBREVS if party != actual_party
        ],
        label=actual_party,
        addon_type='prepend',
        color=f'{actual_party}',
        className='select-dropdown',
        id={
            'id': 'dd-parties',
            'loc': data['loc'],
        }
    )

    return dropdown_menu


@WebApp.callback(
    Output({'id': 'monthly-data', 'loc': MATCH}, 'figure'),
    Output({'id': 'monthly-data', 'loc': MATCH}, 'style'),
    Output({'id': 'select-data', 'loc': MATCH}, 'style'),
    Output({'id': 'warning', 'loc': MATCH}, 'style'),
    Input({'id': 'dd-topics', 'loc': MATCH}, 'value'),
    Input({'id': 'dd-parties', 'loc': MATCH}, 'label'),
    State({'id': 'monthly-data', 'loc': MATCH}, 'figure'),
)
def update_monthly_graph(topics, actual_party, figure):
    if topics and actual_party in AppConfig.PARTY_ABBREVS:
        party_scatter_start = len(AppConfig.TOPIC_NAMES) * list(AppConfig.PARTY_ABBREVS).index(actual_party)
        figure['layout']['xaxis']['rangeslider']['yaxis'].pop('_template', None)

        fig = go.Figure(figure)
        fig.update_traces(visible=False)

        for idx in topics:
            fig.data[idx + party_scatter_start].visible = True

        return fig, dict(display='block'), dict(display='none'), dict(display='none')

    return figure, dict(display='none'), dict(display='block'), dict(display='block')
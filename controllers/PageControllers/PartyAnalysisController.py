import json

import dash_bootstrap_components as dbc
import numpy as np
from dash import callback_context
from dash.dependencies import Output, Input, MATCH, ALL, State
from dash.exceptions import PreventUpdate
from plotly import graph_objs as go

from controllers import rgb_to_rgba
from WebApp import WebApp
from config import AppConfig
from models import AnalyzedInterventions


def build_topic_chart():
	data = AnalyzedInterventions.topic_distribution_per_party()
	figure = go.Figure()

	for party_id in AppConfig.PARTY_CONFIG:
		figure.add_trace(
			go.Bar(
				x=list(AppConfig.TOPIC_NAMES.keys()),
				y=data.loc[data.index == party_id].values.squeeze(),
				name=party_id,
				marker_color=AppConfig.PARTY_CONFIG[party_id]['color'],
				hovertemplate='Porcentaje de tiempo: %{y:.2f}<br>',
			)
		)

	figure.layout.update(
		template='lux',
		barmode='group',
		showlegend=False,
		xaxis_title='Temas',
		yaxis_title='Porcentaje de tiempo',
	)

	return figure


def build_woman_vs_man_chart():
	data = AnalyzedInterventions.topic_distribution_per_sex()
	figure = go.Figure()

	for sex_id in AppConfig.SEX_CONFIG:
		figure.add_trace(
			go.Bar(
				x=list(AppConfig.TOPIC_NAMES.keys()),
				y=data.loc[data.index == sex_id].values.squeeze(),
				name=AppConfig.SEX_CONFIG[sex_id]['name'],
				marker_color=AppConfig.SEX_CONFIG[sex_id]['color'],
				hovertemplate='Porcentaje de tiempo: %{y:.2f}<br>'
			)
		)

	figure.layout.update(
		template='lux',
		barmode='group',
		legend=dict(
			yanchor="top",
			y=0.99,
			xanchor="left",
			x=0.01
		),
		xaxis_title='Temas',
		yaxis_title='Porcentaje de tiempo',
	)

	return figure


def build_topic_chart_duration():
	data = AnalyzedInterventions.max_time_per_topic()
	figure = go.Figure(
		go.Bar(
			x=list(AppConfig.TOPIC_NAMES.keys()),
			y=list(np.diag(data[[f'topic_{i}_time' for i in range(0, AppConfig.N_TOPICS)]])),
			marker_color=list(AppConfig.TOPIC_NAMES.values()),
			customdata=list(zip(data['fecha'], data['diputado'].apply(str.title), data['organizacion'])),
			hovertemplate=
			'<b>Tema: %{x}</b><br><br>' +
			'Fecha: %{customdata[0]|%d-%m-%y}<br>' +
			'Diputado: %{customdata[1]}<br>' +
			'Partido: %{customdata[2]}<br>' +
			'Duración: %{y:.0f} min <br>' +
			'<extra></extra>'
		)
	)

	figure.layout.update(
		template='lux',
		barmode='group',
		xaxis_title='Temas',
		yaxis_title='Minutos estimados',
	)

	return figure


def topic_scores_per_month():
	monthy_topic_scores_per_party = AnalyzedInterventions.monthly_topics()
	figure = go.Figure()

	for party_id in monthy_topic_scores_per_party:
		for topic_idx, topic_name in enumerate(AppConfig.TOPIC_NAMES):
			figure.add_trace(
				go.Scatter(
					x=monthy_topic_scores_per_party[party_id].index,
					y=monthy_topic_scores_per_party[party_id][f'topic_{topic_idx}'],
					text=monthy_topic_scores_per_party[party_id].index,
					line=dict(color=AppConfig.TOPIC_NAMES[topic_name]),
					hovertemplate=
					f'<b>{topic_name}</b><br>' +
					'Media de minutos: %{y:.3f}<br>'
					'<extra></extra>',
				)
			)

	figure.update_traces(
		mode='lines+markers',
		showlegend=False,
		visible=False,
	)

	figure.layout.update(
		template='lux',
		hovermode="x",
		xaxis=dict(
			rangeslider=dict(visible=True),
		),
		yaxis=dict(
			side='right',
			zeroline=False,
		),
		yaxis_title='Minutos',
		height=1000,
		margin=dict(
			t=50,
			b=20
		),
	)

	return figure


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
			) for party in AppConfig.PARTY_CONFIG if party != actual_party
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
	if topics and actual_party in AppConfig.PARTY_CONFIG:
		party_scatter_start = len(AppConfig.TOPIC_NAMES) * list(AppConfig.PARTY_CONFIG).index(actual_party)
		figure['layout']['xaxis']['rangeslider']['yaxis'].pop('_template', None)

		fig = go.Figure(figure)
		fig.update_traces(visible=False)

		for idx in topics:
			fig.data[idx + party_scatter_start].visible = True

		fig.layout.update(
			plot_bgcolor=rgb_to_rgba(AppConfig.PARTY_CONFIG[actual_party]['color'], 0.05)
		)

		return fig, dict(display='block'), dict(display='none'), dict(display='none')

	return figure, dict(display='none'), dict(display='block'), dict(display='block')
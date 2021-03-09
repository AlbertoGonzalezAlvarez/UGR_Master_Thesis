import json

import dash_bootstrap_components as dbc
import numpy as np
from dash import callback_context
from dash.dependencies import Output, Input, MATCH, ALL, State
from dash.exceptions import PreventUpdate
from plotly import graph_objs as go

from Utils import rgb_to_rgba
from WebApp import WebApp
from Config import AppConfig
from Models import AnalyzedInterventions


def build_topic_chart():
	data = AnalyzedInterventions.get_topic_distribution_per_party()

	figures = [
		go.Bar(
			x=data['topic'].unique(),
			y=data.loc[data['organizacion'] == party]['score'],
		    name=party,
			marker_color=AppConfig.PARTY_COLORS[party],
		    hovertemplate='Porcentaje de tiempo: %{y:.2f}<br>') for party in data['organizacion'].unique()
	]

	layout = dict(
		template='lux',
		barmode='group',
		showlegend=False,
		xaxis_title='Temas',
		yaxis_title='Porcentaje de tiempo',
	)

	return go.Figure(figures, layout)


def build_woman_vs_man_chart():
	data = AnalyzedInterventions.get_topic_distribution_per_sex()

	figures = [
		go.Bar(
			x=AppConfig.TOPIC_NAMES,
			y=data.loc[data['sexo'] == sex_id]['score'],
			name=AppConfig.SEX_NAMES[sex_id],
			marker_color=AppConfig.SEX_COLORS[sex_id],
			hovertemplate='Porcentaje de tiempo: %{y:.2f}<br>'
		) for sex_id in data['sexo'].unique()
	]

	layout = dict(
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

	return go.Figure(figures, layout)


def build_topic_chart_duration():
	data = AnalyzedInterventions.get_max_time_per_topic()

	figure = go.Bar(
		x=data['predominant_topic'],
		y=data['score'],
		marker_color=AppConfig.TOPIC_COLORS,
		customdata=list(zip(data['fecha'], data['diputado'].str.replace('-', ' ').apply(str.title), data['organizacion'])),
		hovertemplate=
		'<b>Tema: %{x}</b><br><br>' +
		'Fecha: %{customdata[0]|%d-%m-%y}<br>' +
		'Diputado: %{customdata[1]}<br>' +
		'Partido: %{customdata[2]}<br>' +
		'Duración: %{y:.0f} min <br>' +
		'<extra></extra>'
	)

	layout = dict(
		template='lux',
		barmode='group',
		xaxis_title='Temas',
		yaxis_title='Minutos estimados',
	)

	return go.Figure(figure, layout)


def topic_scores_per_month():
	data = AnalyzedInterventions.get_monthly_evolution_topics()

	dates = data['fecha'].unique()
	figures = []

	for party in AppConfig.PARTY_ABBREVS:
		for topic_idx, topic_name in enumerate(AppConfig.TOPIC_NAMES):
				figures.append(
					go.Scatter(
						x=dates,
						y=data.loc[data['organizacion'] == party][topic_name],
						text=dates,
						visible=False,
						mode='lines+markers',
						line=dict(color=AppConfig.TOPIC_COLORS[topic_idx]),
						hovertemplate=
						f'<b>{topic_name}</b><br>' +
						'Media de minutos: %{y:.3f}<br>'
						'<extra></extra>',
					)
				)


	layout= dict(
		showlegend=False,
		template='lux',
		hovermode='x',
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

	return go.Figure(figures, layout)


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
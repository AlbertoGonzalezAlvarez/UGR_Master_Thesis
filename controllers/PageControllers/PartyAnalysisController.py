import json

import dash_bootstrap_components as dbc
import numpy as np
from dash import callback_context
from dash.dependencies import Output, Input, MATCH, ALL, State
from plotly import graph_objs as go

import controllers
from WebApp import WebApp
from config.AppConfig import PARTY_CONFIG, TOPIC_NAMES, SEX_CONFIG, N_TOPICS
from models.AnalyzedInterventions import topic_distribution_per_party, topic_distribution_per_sex, max_time_per_topic, \
	monthly_topics


def build_topic_chart():
	data = topic_distribution_per_party()
	figure = go.Figure()

	for party_id in PARTY_CONFIG:
		figure.add_trace(
			go.Bar(
				x=list(TOPIC_NAMES.keys()),
				y=data.loc[data.index == party_id].values.squeeze(),
				name=party_id,
				marker_color=PARTY_CONFIG[party_id]['color'],
				hovertemplate='Porcentaje de tiempo: %{y:.2f}<br>',
			)
		)

	figure.layout.update(
		template='lux',
		barmode='group',
		showlegend=False,
		xaxis_title='' if controllers.MainController.is_mobile_device else 'Temas',
		yaxis_title='' if controllers.MainController.is_mobile_device else 'Porcentaje de tiempo',
	)

	return figure


def build_woman_vs_man_chart():
	data = topic_distribution_per_sex()
	figure = go.Figure()

	for sex_id in SEX_CONFIG:
		figure.add_trace(
			go.Bar(
				x=list(TOPIC_NAMES.keys()),
				y=data.loc[data.index == sex_id].values.squeeze(),
				name=SEX_CONFIG[sex_id]['name'],
				marker_color=SEX_CONFIG[sex_id]['color'],
				showlegend=False if controllers.MainController.is_mobile_device else True,
				hovertemplate='Porcentaje de tiempo: %{y:.2f}<br>'
			)
		)

	figure.layout.update(
		template='lux',
		barmode='group',
		xaxis_title='' if controllers.MainController.is_mobile_device else 'Temas',
		yaxis_title='' if controllers.MainController.is_mobile_device else 'Porcentaje de tiempo',
	)

	return figure


def build_topic_chart_duration():
	data = max_time_per_topic()
	figure = go.Figure(
		go.Bar(
			x=list(TOPIC_NAMES.keys()),
			y=list(np.diag(data[[f'topic_{i}_time' for i in range(0, N_TOPICS)]])),
			marker_color=list(TOPIC_NAMES.values()),
			customdata=list(zip( data['fecha'], data['diputado'].apply(str.title), data['organizacion'])),
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
		xaxis_title='' if controllers.MainController.is_mobile_device else 'Temas',
		yaxis_title='' if controllers.MainController.is_mobile_device else 'Minutos estimados',
	)

	return figure


def topic_scores_per_month():
	monthy_topic_scores_per_party = monthly_topics()
	figure = go.Figure()

	for party_id in monthy_topic_scores_per_party:
		for topic_idx, topic_name in enumerate(TOPIC_NAMES):
			figure.add_trace(
				go.Scatter(
					x=monthy_topic_scores_per_party[party_id].index,
					y=monthy_topic_scores_per_party[party_id][f'topic_{topic_idx}'],
					text=monthy_topic_scores_per_party[party_id].index,
					line=dict(color=TOPIC_NAMES[topic_name]),
				)
			)

	figure.update_traces(
		mode='lines+markers',
		showlegend=False,
		visible=False,
		hovertemplate=
		'Mes: %{x}<br>' +
		'Media de minutos: %{y:.3f}<br>'
		'<extra></extra>',
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
	State({'id': 'monthly-data', 'loc': MATCH}, 'figure'),
	prevent_initial_call=True
)
def update_party_dropdown(_, figure_status):
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
			) for party in PARTY_CONFIG if party != actual_party
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
	if topics and actual_party in PARTY_CONFIG:
		party_scatter_start = len(TOPIC_NAMES) * list(PARTY_CONFIG).index(actual_party)

		for idx in range(len(figure['data'])):
			figure['data'][idx]['visible'] = False

		for topic_idx in topics:
			idx = topic_idx + party_scatter_start
			figure['data'][idx]['visible'] = True

		figure['layout'].update(
			plot_bgcolor=controllers.rgb_to_rgba(PARTY_CONFIG[actual_party]['color'], 0.1)
		)

		return figure, dict(display='block'), dict(display='none'), dict(display='none')

	return figure, dict(display='none'), dict(display='block'), dict(display='block')
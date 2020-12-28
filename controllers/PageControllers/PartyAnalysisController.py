from plotly import graph_objs as go
import numpy as np
import pandas as pd
import controllers
from config.AppConfig import PARTY_CONFIG, TOPIC_NAMES, PLOT_BASE_CONFIG, SEX_CONFIG, N_TOPICS
from models.AnalyzedInterventions import topic_distribution_per_party, topic_distribution_per_sex, max_time_per_topic, \
	monthly_topics
import plotly.express as px

def build_topic_chart():
	data = topic_distribution_per_party()
	figure = go.Figure(data=[
		go.Bar(
			x=TOPIC_NAMES,
			y=data.loc[data.index == party_id].values.squeeze(),
			name=party_id,
			marker_color=PARTY_CONFIG[party_id]['color'],
			showlegend=False if controllers.MainController.is_mobile_device else True,
			hovertemplate='Porcentaje de tiempo: %{y:.2f}<br>'
		) for party_id in PARTY_CONFIG],
		layout=dict(
			barmode='group',
			margin=dict(l=0, r=40, t=40),
			xaxis_title='' if controllers.MainController.is_mobile_device else 'Temas',
			yaxis_title='' if controllers.MainController.is_mobile_device else 'Porcentaje de tiempo',
			**PLOT_BASE_CONFIG
		)
	)

	return figure


def build_woman_vs_man_chart():
	data = topic_distribution_per_sex()
	figure = go.Figure(data=[
		go.Bar(
			x=TOPIC_NAMES,
			y=data.loc[data.index == sex_id].values.squeeze(),
			name=SEX_CONFIG[sex_id]['name'],
			marker_color=SEX_CONFIG[sex_id]['color'],
			showlegend=False if controllers.MainController.is_mobile_device else True,
			hovertemplate='Porcentaje de tiempo: %{y:.2f}<br>'
		) for sex_id in SEX_CONFIG],
		layout=dict(
			barmode='group',
			margin=dict(l=0, r=40, t=40),
			xaxis_title='' if controllers.MainController.is_mobile_device else 'Temas',
			yaxis_title='' if controllers.MainController.is_mobile_device else 'Porcentaje de tiempo',
			**PLOT_BASE_CONFIG
		)
	)

	return figure


def build_topic_chart_duration():
	data = max_time_per_topic()
	figure = go.Figure(go.Bar(
			x=data['predominant_topic'],
			y=list(np.diag(data[[f'topic_{i}_time' for i in range(0, N_TOPICS)]])),
			marker_color=controllers.COLORS,
			customdata=list(zip(
				data['fecha'], data['diputado'].apply(controllers.camel_case_deputy_name), data['organizacion'])),
			hoverinfo='skip',
			hovertemplate=
			'<b>Tema: %{x}</b><br><br>' +

			'Fecha: %{customdata[0]|%d-%m-%y}<br>' +
			'Diputado: %{customdata[1]}<br>' +
			'Partido: %{customdata[2]}<br>' +
			'Duración: %{y:.0f} min <br>' +
			'<extra></extra>'
		),
		layout=dict(
			barmode='group',
			hoverlabel_align='left',
			margin=dict(l=0, r=40, t=40),
			xaxis_title='' if controllers.MainController.is_mobile_device else 'Temas',
			yaxis_title='' if controllers.MainController.is_mobile_device else 'Minutos estimados',
			**PLOT_BASE_CONFIG
		)
	)

	return figure


def build_topic_scores_per_month():
	monthy_topic_scores_per_party = monthly_topics(pd.DataFrame.mean)
	figure = go.Figure()

	for party_id in monthy_topic_scores_per_party:
		for topic_idx in range(N_TOPICS):
			figure.add_trace(
				go.Scatter(
					x=monthy_topic_scores_per_party[party_id]['fecha'].to_list(),
					y=monthy_topic_scores_per_party[party_id][f'topic_{topic_idx}'].to_list(),
					text=monthy_topic_scores_per_party[party_id]['fecha'].to_list(),
					name=TOPIC_NAMES[topic_idx],
					yaxis=f'y',
					visible=False,
					line=dict(color=px.colors.qualitative.Bold[topic_idx % len(px.colors.qualitative.Bold)]),
					hovertemplate=
					"Mes: %{x}<br>" +
					"Media de minutos: %{y:.3f}<br>"
				)
			)

	figure.update_traces(
		hoverinfo="name+x+text+y",
		line={"width": 1},
		marker={"size": 10},
		mode="lines+markers",
		showlegend=False
	)

	buttons = [dict(
		label='Seleccinar partido',
		method="update",
		args=[{"visible": [False] * N_TOPICS * len(PARTY_CONFIG)}]
	)]

	start_index = 0
	party_index = 0

	for party in PARTY_CONFIG:
		visible = [False] * N_TOPICS * len(PARTY_CONFIG)
		end_index = N_TOPICS * (party_index + 1)
		visible[start_index:end_index] = [True] * N_TOPICS

		buttons.append(
			dict(
				label=party,
				method="update",
				args=[{"visible": visible.copy()}]
			)
		)
		party_index += 1
		start_index = end_index

	figure.layout.update(
		updatemenus=[
			dict(
				active=0,
				buttons=buttons,
				showactive=True,
			)
		],
	)

	# Update axes
	figure.layout.update(
		xaxis=dict(
			autorange=True,
			tickformat='%m-%Y',
			rangeslider=dict(
				autorange=True,
			),
			type="date"
		),
		yaxis=dict(
			anchor="x",
			autorange=True,
			domain=[0, 1],
			mirror=True,
			showline=True,
			side="right",
			tickfont={"color": "#673ab7"},
			tickmode="auto",
			titlefont={"color": "#673ab7"},
			type="linear",
			zeroline=False
		),
	)

	# Update layout
	figure.layout.update(
		dragmode="zoom",
		hovermode="x",
		yaxis_title="Minutos",
		legend=dict(traceorder="reversed"),
		height=1000,
		margin=dict(
			t=100,
			b=100
		),
	)

	return figure
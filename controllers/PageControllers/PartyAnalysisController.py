from plotly import graph_objs as go
import numpy as np
import controllers
from config.AppConfig import PARTY_CONFIG, TOPIC_NAMES, PLOT_BASE_CONFIG, SEX_CONFIG, N_TOPICS
from models.AnalyzedInterventions import topic_distribution_per_party, topic_distribution_per_sex, max_time_per_topic


def build_topic_chart():
	data = topic_distribution_per_party()
	figure = go.Figure(data=[
		go.Bar(
			x=TOPIC_NAMES,
			y=data.loc[data.index == PARTY_CONFIG[party_id]['gp_name']].values.squeeze(),
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
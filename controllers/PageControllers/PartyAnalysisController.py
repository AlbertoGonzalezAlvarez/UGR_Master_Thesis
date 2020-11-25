from plotly import graph_objs as go

import controllers
from config.AppConfig import PARTY_CONFIG, TOPIC_NAMES, PLOT_BASE_CONFIG
from models.AnalyzedInterventions import topic_distribution_per_party


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
		layout={
			'barmode': 'group',
			'margin': dict(l=0, r=40, t=40),
			'xaxis_title': '' if controllers.MainController.is_mobile_device else 'Temas',
			'yaxis_title': '' if controllers.MainController.is_mobile_device else 'Porcentaje de tiempo',
			**PLOT_BASE_CONFIG
		}
	)

	return figure


def build_woman_vs_man_chart():
	return go.Figure()


def build_topic_chart_duration():
	return go.Figure()
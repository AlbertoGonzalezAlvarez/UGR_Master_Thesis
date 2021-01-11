import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

import controllers
from WebApplication import is_mobile_device
from config.AppConfig import PARTY_CONFIG
from models import AnalyzedInterventions

parties_info = AnalyzedInterventions.get_parties_info()
party_charts = (
	{
		'id': 'topic-chart',
		'title': 'Temas hablados por partido',
		'info': ''' En la siguiente gráfica se puede ver el porcentaje de tiempo que 
					dedican los partidos a los diferentes temas que se tratan. ''',
		'figure': controllers.PartyAnalysisController.build_topic_chart()
	},
	{
		'id': 'topic-chart-woman-vs-man',
		'title': 'Temas hablados por sexo',
		'info': ''' A continuación mostraremos si hay diferencias entre los temas que hablan las 
					mujeres y los hombres independientemente del partido. Están incluidas las 
					intervenciones de personas invitadas al parlamento. ''',
		'figure': controllers.PartyAnalysisController.build_woman_vs_man_chart()
	},
	{
		'id': 'topic-chart-duration',
		'title': 'Discurso más largo de cada tema',
		'info': [
			'Duración estimada', html.Strong('*'), ' del discurso más largo en cada uno de los temas. También ',
			'se puede idenfitificar el partido y el diputado que lo realizó.', html.Br(), html.Br(),
					
			html.I([html.Strong('*'), 'teniendo en cuenta una velocidad de 140 palabras por minuto'])
		],
		'figure': controllers.PartyAnalysisController.build_topic_chart_duration()
	}
)

party_info_card_content = [
	[
		dbc.CardHeader(children=[
			dbc.CardLink(href='#', className='d-flex', children=[
				html.I(className='far fa-minus-square mr-2 align-self-center', id={
					'type': 'collapse-icon',
					'ref': party
				}),
				html.Span(PARTY_CONFIG[party]["extended_name"]),
				dbc.Badge(party, style={'color': '#fff', 'backgroundColor': PARTY_CONFIG[party]['color']},
							className='align-self-center ml-auto')
			],
			id={
				'type': 'collapse-button',
				'ref': party
			}),
		]),
		dbc.Collapse(
			dbc.CardBody(
				[
					html.H5('Información', className='card-title'),
					html.P(id=f'{party}-card-info', className='card-text', children=
						[
							f'- Interevenciones realizadas: {parties_info["n_interventions"][party]}',
							html.Br(),
							f'- Realizadas por mujeres: {parties_info["n_women_interventions"][party]:.2f}%',
							html.Br(),
							f'- Número de diputados: {parties_info["n_deputies"][party]}',
							html.Br(),
							f'- Mujeres diputadas: {parties_info["n_women_deputies"][party]:.2f}%',
						]
					),
				]
			),
			id={
				'type': 'collapsible-item',
				'ref': party
			},
			is_open=not is_mobile_device,
		)
	] for party in PARTY_CONFIG
]

party_info_cards_row = \
	dbc.Row(className='mb-4 justify-content-center', children=
		[
			dbc.Col(className='col-lg-3 col-12 mb-3 mb-lg-0', children=[
				dbc.Card(card_content, color='light')
			]) for card_content in party_info_card_content
		],
	)

party_charts_row = \
	dbc.Row(className='justify-content-center', children=
		[
			dbc.Col(className='col-lg-3 col-12 mb-3 mb-lg-0 d-flex flex-column', children=[
				dbc.Card(outline=True, className='h-100', children=
					[
						dbc.CardHeader(children=
							[
								html.I(className='fas fa-info-circle mr-2'),
								html.Span(chart['title']),
							],
						),
						dbc.CardBody(className='d-flex flex-column', children=
							[
								html.H5('Información', className='card-title'),
								html.P(children=chart['info'], className="card-text"),
								dcc.Graph(id=chart['id'], className='mt-auto', figure=chart['figure']),
							]
						)
					]
				),
			]) for chart in party_charts
		]
	)

layout = party_info_cards_row, party_charts_row
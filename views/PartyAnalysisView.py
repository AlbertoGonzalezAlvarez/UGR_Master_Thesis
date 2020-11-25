import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc

import controllers
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
		'title': 'Tiempo dedicado a cada tema',
		'info': ''' A continuación se muestra el porcentaje de tiempo que han dedicado los 
					parlamentarios en cada una de sus intervenciones a los temas presentados 
					independientemente del partido al que pertenezcan. ''',
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
							f'- Interevenciones realizadas: {parties_info["n_interventions"][PARTY_CONFIG[party]["gp_name"]]}',
							html.Br(),
							f'- Realizadas por mujeres: {parties_info["n_women_interventions"][PARTY_CONFIG[party]["gp_name"]]:.2f}%',
							html.Br(),
							f'- Número de diputados: {parties_info["n_deputies"][PARTY_CONFIG[party]["gp_name"]]}',
							html.Br(),
							f'- Mujeres diputadas: {parties_info["n_women_deputies"][PARTY_CONFIG[party]["gp_name"]]:.2f}%',
						]
					),
				]
			),
			id={
				'type': 'collapsible-item',
				'ref': party
			},
			is_open=not controllers.MainController.is_mobile_device,
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
								dcc.Graph(id=chart['id'], className='mt-auto', figure=chart['figure'])
							]
						)
					]
				),
			]) for chart in party_charts
		]
	)

layout = party_info_cards_row, party_charts_row
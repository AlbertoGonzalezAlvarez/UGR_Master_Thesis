import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

import controllers
from config import PARTY_CONFIG, TOPIC_NAMES
from models import AnalyzedInterventions

parties_info = AnalyzedInterventions.get_parties_info()
party_charts = [
	{
		'id': 'topic-chart',
		'title': 'Temas hablados por partido',
		'info': ''' En la siguiente gráfica se puede ver el porcentaje de tiempo que 
					dedican los partidos a los diferentes temas que se tratan. ''',
		'figure': controllers.build_topic_chart()
	},
	{
		'id': 'topic-chart-woman-vs-man',
		'title': 'Temas hablados por sexo',
		'info': ''' A continuación mostraremos si hay diferencias entre los temas que hablan las 
					mujeres y los hombres independientemente del partido. Están incluidas las 
					intervenciones de personas invitadas al parlamento. ''',
		'figure': controllers.build_woman_vs_man_chart()
	},
	{
		'id': 'topic-chart-duration',
		'title': 'Discurso más largo de cada tema',
		'info': [
			'Duración estimada', html.Strong('*'), ' del discurso más largo en cada uno de los temas. También ',
			'se puede idenfitificar el partido y el diputado que lo realizó.', html.Br(), html.Br(),
					
			html.I([html.Strong('*'), 'teniendo en cuenta una velocidad de 140 palabras por minuto'])
		],
		'figure': controllers.build_topic_chart_duration()
	}
]


def buil_card_content(default_collapsed):
	return [[
		dbc.CardHeader(children=[
			html.A(className='text-decoration-none d-flex', href=f'#collapsible-item-{party}-{default_collapsed}', role='button', children=[
				html.I(className='far mr-2 align-self-center'),
				html.Span(f'{PARTY_CONFIG[party]["extended_name"]}'),
				dbc.Badge(party, className=f'align-self-center ml-auto {party}')
			], **{'data-toggle': 'collapse', 'aria-expanded': default_collapsed, 'aria-controls': f'collapsible-item-{party}-{default_collapsed}'}),
		]),
		html.Div(id=f'collapsible-item-{party}-{default_collapsed}', className=f'collapse {"show" if default_collapsed else ""}', children=
		dbc.CardBody([
			html.P(id=f'{party}-card-info', className='card-text', children=dcc.Markdown(
				f'''
					A continuación, se recogen algunos datos relevantes relacionados con el {PARTY_CONFIG[party]["gp_name"]}.  

					\- Interevenciones realizadas: {parties_info["n_interventions"][party]}  
					\- Realizadas por mujeres: {parties_info["n_women_interventions"][party]:.2f}%  
					\- Número de diputados: {parties_info["n_deputies"][party]}  
					\- Mujeres diputadas: {parties_info["n_women_deputies"][party]:.2f}%
				'''
			))
		]
		))
	] for party in PARTY_CONFIG]

party_info_cards_row = \
	dbc.Row(className='mt-4 mb-4 justify-content-center', children=
		[
			dbc.Col(className='col-12 mb-2 d-block d-lg-none',
			        children=dbc.Card(card, color='light')) for card in buil_card_content(default_collapsed=False)
		] +
		[
			dbc.Col(className='col-4 d-none d-lg-block',
			        children=dbc.Card(card, color='light')) for card in buil_card_content(default_collapsed=True)
		]
	)

party_charts_row = \
	dbc.Row(className='justify-content-center mb-4', children=
		[
			dbc.Col(className='col-lg-4 col-12 mb-3 mb-lg-0 d-flex flex-column', children=[
				dbc.Card(outline=True, className='h-100', children=[
						dbc.CardHeader(children=[
								html.I(className='fas fa-info-circle mr-2'),
								html.Span(chart['title']),
							],
						),
						dbc.CardBody(className='d-flex flex-column', children=[
								html.H5('Información', className='card-title'),
								html.P(children=chart['info'], className="card-text"),
								dcc.Graph(id=chart['id'], figure=chart['figure']),
							]
						)
					]
				),
			]) for chart in party_charts
		]
	)

party_evolution = dbc.Row(className='justify-content-center mb-4', children=
				[
					dbc.Col(children=
						dbc.Card(className='text-left', children=
							dbc.CardBody(
								[
									html.H4('Serie de tiempo dedicado a cada tema', className='card-title'),
									html.P(
										'Analizamos los temas de los que han hablado los diferentes partidos a lo largo de la legislatura '
										'para poder estudiar el porcentaje de intervenciones dedicados a cada uno de ellos.'),
									dbc.Col(
										id='evolution-mobile-warning',
										className='col-12 d-lg-none d-block text-center',
										children=[
											html.I(
												className='fas fa-exclamation-triangle fa-3x text-warning mt-3 mb-3',
											),
											html.H4(
												children='Por favor, visualice la evolución en un dispositivo mayor',
											),
										]
									),
									dbc.Row([
										dbc.Col(
											dbc.InputGroup(
												[
													html.Div(
														dbc.DropdownMenu(
															[
																dbc.DropdownMenuItem(
																	party,
																	key=party,
																	id={
																		'type': 'dd-party',
																		'loc': 'left',
																		'ref': party
																	},
																) for party in PARTY_CONFIG
															],
															label='Partido',
															addon_type='prepend',
															className='select-dropdown',
															id={
																'id': 'dd-parties',
																'loc': 'left',
															}
														),
													className='d-flex',
													id={'id': 'dd-parties-div', 'loc': 'left'}
													),
													dcc.Dropdown(
														options=[
															{
																'label': topic,
															    'value': idx,
																'title': controllers.filter_special_characters(topic)
															} for idx, topic in enumerate(TOPIC_NAMES)
														],
													multi=True,
													id={'id': 'dd-topics', 'loc': 'left'},
													placeholder='Seleccionar temas',
													value=None
													),
												]
											),
										className='border-right'
										),
										dbc.Col(
											dbc.InputGroup(
												[
													html.Div(
														dbc.DropdownMenu(
															[
																dbc.DropdownMenuItem(
																	party,
																	key=party,
																	id={
																		'type': 'dd-party',
																		'loc': 'right',
																		'ref': party
																	},
																) for party in PARTY_CONFIG
															],
															label='Partido',
															addon_type='prepend',
															className='select-dropdown',
															id={
																'id': 'dd-parties',
																'loc': 'right',
															}
														),
														className='d-flex',
														id={'id': 'dd-parties-div', 'loc': 'right'}
													),
													dcc.Dropdown(
														options=[
															{
																'label': topic,
															    'value': idx,
																'title': controllers.filter_special_characters(topic)
															 } for idx, topic in enumerate(TOPIC_NAMES)
														],
														multi=True,
														id={'id': 'dd-topics', 'loc': 'right'},
														placeholder='Seleccionar temas',
														value=None
													),
												]
											),
										),
									],
									className='pt-3 d-lg-flex d-none',
									id='evolution-selectors'),
									dbc.Row(id='evolution-figures', className='d-lg-flex d-none', children=[
										dbc.Col(
											lg=6,
											width=12,
											className='border-right text-center',
											children=[
												html.I(
													className='fas fa-exclamation-triangle fa-3x text-warning mt-3 mb-3',
													id={'id': 'warning', 'loc': 'left'},
												),
												html.H4(
													id={'id': 'select-data', 'loc': 'left'},
													children='Selecciona al menos un tema y un partido',
													style=dict(display='block')
												),
												dcc.Graph(
													id={'id': 'monthly-data', 'loc': 'left'},
													figure=controllers.topic_scores_per_month(),
													style=dict(display='None')
												),
											]
										),
										dbc.Col(
											lg=6,
											width=12,
											className='text-center',
											children=[
												html.I(
													className='fas fa-exclamation-triangle fa-3x text-warning mt-3 mb-3',
													id={'id': 'warning', 'loc': 'right'},
												),
												html.H4(
													id={'id': 'select-data', 'loc': 'right'},
													children='Selecciona al menos un tema y un partido',
													style=dict(display='block')
												),
												dcc.Graph(
													id={'id': 'monthly-data', 'loc': 'right'},
													figure=controllers.topic_scores_per_month(),
													style=dict(display='None')
												)
											]
										)
									]),
								]
							)
						)
					)
				]
			)

layout = party_info_cards_row, party_charts_row, party_evolution
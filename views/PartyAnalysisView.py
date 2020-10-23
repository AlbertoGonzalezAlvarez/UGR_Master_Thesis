import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc

from config.AppConfig import PARTY_CONFIG
from models import AnalyzedInterventions

parties_info = AnalyzedInterventions.get_parties_info()

party_info_card_content = [
	[
		dbc.CardHeader(children=[
			dbc.CardLink(id=f'{party}-party-collapse-button', href='#', className='d-flex', children=[
				html.I(id=f'{party}-collapse-icon'),
				html.Span(PARTY_CONFIG[party]["extended_name"]),
				dbc.Badge(party, style={'color': '#fff', 'backgroundColor': PARTY_CONFIG[party]['color']},
						  className='align-self-center ml-auto')
			]),
	]	),
		dbc.Collapse(
			dbc.CardBody(
				[
					html.H5('Información general', className='card-title'),
					html.P(id=f'{party}-card-info', className='card-text', children=
						[
							f'- Interevenciones realizadas: {parties_info["n_interventions"][PARTY_CONFIG[party]["gp_name"]]}',
							html.Br(),
							f'- Realizadas por mujeres: {parties_info["n_women_interventions"][PARTY_CONFIG[party]["gp_name"]]}%',
							html.Br(),
							f'- Número de diputados: {parties_info["n_deputies"][PARTY_CONFIG[party]["gp_name"]]}',
							html.Br(),
							f'- Mujeres diputadas: {parties_info["n_women_deputies"][PARTY_CONFIG[party]["gp_name"]]}%',
						]
					),
				]
			),
			id=f'{party}-party-collapse',
			is_open=True,
		)
	] for party in PARTY_CONFIG
]

psoe_info_card_content = None
pp_info_card_content = None
iu_info_card_content = None

party_cards_content = {
	'pp': psoe_info_card_content,
	'psoe': pp_info_card_content,
	'iu': iu_info_card_content
}

party_info_cards = \
	dbc.Row(className="mb-4 justify-content-center", children=
		[
			dbc.Col(className='col-lg-3 col-12 mb-3 mb-lg-0', children=[
				dbc.Card(card_content, color="light")
			]) for card_content in party_info_card_content
		],
	)

layout = party_info_cards
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

import utils
from config import PARTY_ABBREVS, TOPIC_NAMES
from views import builders

party_charts = [
    {
        'id': 'topic-chart',
        'title': 'Temas hablados por partido',
        'info': ''' En la siguiente gráfica se puede ver el porcentaje de tiempo que 
                    dedican los partidos a los diferentes temas que se tratan. ''',
        'figure': builders.PartyAnalysis.build_topic_distribution_chart()
    },
    {
        'id': 'topic-chart-woman-vs-man',
        'title': 'Temas hablados por sexo',
        'info': ''' A continuación mostraremos si hay diferencias entre los temas que hablan las 
                    mujeres y los hombres independientemente del partido. Están incluidas las 
                    intervenciones de personas invitadas al parlamento. ''',
        'figure': builders.PartyAnalysis.build_woman_vs_man_chart()
    },
    {
        'id': 'topic-chart-duration',
        'title': 'Discurso más largo de cada tema',
        'info':
            '''
                Duración estimada* del discurso más largo de cada uno de los temas. También se 
                puede idenfitificar el partido y el diputado que lo realizó.

                *\* teniendo en cuenta una velocidad de 140 palabras por minuto.*
            ''',
        'figure': builders.PartyAnalysis.build_topic_duration_chart()
    }
]

party_info_cards_row = dbc.Row(
    className='mt-4 mb-4 justify-content-center',
    children=[
                 dbc.Col(width=12, className='d-block d-lg-none mb-2', children=dbc.Card(card, color='light'))
                 for card in builders.PartyAnalysis.build_party_info_cards(default_collapsed=False)
             ] + [
                 dbc.Col(width=4, className='d-none d-lg-block', children=dbc.Card(card, color='light'))
                 for card in builders.PartyAnalysis.build_party_info_cards(default_collapsed=True)
             ]
)

party_charts_row = dbc.Row(className='justify-content-center mb-4', children=[
    dbc.Col(width=12, lg=4, className='mb-3 mb-lg-0 d-flex flex-column', children=[
        dbc.Card(outline=True, className='h-100', children=[
            dbc.CardHeader(children=[
                html.I(className='fas fa-info-circle mr-2'),
                html.Span(chart['title']),
            ]),
            dbc.CardBody(className='d-flex flex-column', children=[
                html.H5('Información', className='card-title'),
                html.P(children=dcc.Markdown(chart['info']), className="card-text"),
                dbc.Spinner(color="success", children=dcc.Graph(id=chart['id'], figure=chart['figure'])),
            ])
        ]),
    ]) for chart in party_charts
])

party_evolution = dbc.Row(className='justify-content-center mb-4', children=[
    dbc.Col(children=dbc.Card(className='text-left', children=
    dbc.CardBody([
        html.H4('Serie de tiempo dedicado a cada tema', className='card-title'),
        html.P(
            '''Analizamos los temas de los que han hablado los diferentes partidos a lo largo de la legislatura
               para poder estudiar el porcentaje de intervenciones dedicados a cada uno de ellos.'''
        ),
        dbc.Col(id='evolution-mobile-warning', width=12, className='d-lg-none d-block text-center', children=[
            html.I(className='fas fa-exclamation-triangle fa-3x text-warning mt-3 mb-3'),
            html.H4(children='Por favor, visualice la evolución en un dispositivo mayor')
        ]),
        dbc.Row(className='pt-3 d-lg-flex d-none', children=[
            dbc.Col(className='border-right', children=dbc.InputGroup([
                html.Div(
                    id={'id': 'dd-parties-div', 'loc': 'left'},
                    className='d-flex',
                    children=dbc.DropdownMenu(
                        id={'id': 'dd-parties', 'loc': 'left'},
                        label='Partido',
                        addon_type='prepend',
                        className='select-dropdown',
                        children=[
                            dbc.DropdownMenuItem(
                                party,
                                key=party,
                                id={
                                    'type': 'dd-party',
                                    'loc': 'left',
                                    'ref': party
                                }
                            ) for party in PARTY_ABBREVS],
                    ),
                ),
                dcc.Dropdown(
                    id={'id': 'dd-topics', 'loc': 'left'},
                    placeholder='Seleccionar temas',
                    multi=True,
                    value=None,
                    options=[
                        {'label': topic, 'value': idx, 'title': utils.filter_special_characters(topic)}
                        for idx, topic in enumerate(TOPIC_NAMES)
                    ]
                )
            ])),
            dbc.Col(dbc.InputGroup([
                html.Div(
                    id={'id': 'dd-parties-div', 'loc': 'right'},
                    className='d-flex',
                    children=dbc.DropdownMenu(
                        id={'id': 'dd-parties', 'loc': 'right'},
                        label='Partido',
                        addon_type='prepend',
                        className='select-dropdown',
                        children=[
                            dbc.DropdownMenuItem(
                                party,
                                key=party,
                                id={'type': 'dd-party', 'loc': 'right', 'ref': party}) for party in PARTY_ABBREVS
                        ]
                    )
                ),
                dcc.Dropdown(
                    multi=True,
                    id={'id': 'dd-topics', 'loc': 'right'},
                    placeholder='Seleccionar temas',
                    value=None,
                    options=[{'label': topic, 'value': idx, 'title': utils.filter_special_characters(topic)}
                             for idx, topic in enumerate(TOPIC_NAMES)],
                ),
            ])),
        ]),
        dbc.Row(id='evolution-figures', className='d-lg-flex d-none', children=[
            dbc.Col(
                lg=6,
                width=12,
                className='border-right text-center',
                children=[
                    html.I(
                        id={'id': 'warning', 'loc': 'left'},
                        className='fas fa-exclamation-triangle fa-3x text-warning mt-3 mb-3',
                    ),
                    html.H4(
                        id={'id': 'select-data', 'loc': 'left'},
                        children='Selecciona al menos un tema y un partido',
                        style=dict(display='block')
                    ),
                    dbc.Spinner(color="success", children=
                        dcc.Graph(
                            id={'id': 'monthly-data', 'loc': 'left'},
                            style=dict(display='None'),
                            figure=builders.PartyAnalysis.build_topic_distribution_per_month(),
                        )
                    ),
                ]
            ),
            dbc.Col(
                lg=6,
                width=12,
                className='text-center',
                children=[
                    html.I(
                        id={'id': 'warning', 'loc': 'right'},
                        className='fas fa-exclamation-triangle fa-3x text-warning mt-3 mb-3',
                    ),
                    html.H4(
                        id={'id': 'select-data', 'loc': 'right'},
                        children='Selecciona al menos un tema y un partido',
                        style=dict(display='block')
                    ),
                    dbc.Spinner(color="success", children=
                        dcc.Graph(
                            id={'id': 'monthly-data', 'loc': 'right'},
                            style=dict(display='None'),

                            figure=builders.PartyAnalysis.build_topic_distribution_per_month(),
                        )
                    )
                ]
            )
        ]),
    ])))
])

layout = party_info_cards_row, party_charts_row, party_evolution

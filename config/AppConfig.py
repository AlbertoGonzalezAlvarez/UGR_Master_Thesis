APP_LOGO = "https://cdn2.iconfinder.com/data/icons/circle-icons-1/64/bar-chart-512.png"
STYLESHEETS = [
	'https://use.fontawesome.com/releases/v5.8.1/css/all.css'
]

APP_TITLE = 'Anali.sys'
STATIC_DATA = './assets'
USER_ANGENT_REGEX = '(?i)adnroid|fennec|iemobile|iphone|opera (?:mini|mobi)|mobile'
INITIAL_LOCATION_ID = 'analisis-lda'

PAGE_ROUTES = (
	{'id': 'analisis-lda', 'route': '/analisis-lda', 'name': 'Análisis de LDA'},
	{'id': 'analisis-partidos', 'route': '/analisis-partidos', 'name': 'Análisis de partidos'},
	{'id': 'analisis-diputados', 'route': '/analisis-diputados', 'name': 'Análisis de diputados'}
)

ORG_CONFIG = {
	'PSOE': {'extended_name': 'Partido Socialista', 'gp_name': 'G.P. SOCIALISTA', 'color': 'rgb(217, 83, 79)', 'is_party': True},
	'PP': {'extended_name': 'Partido Popular', 'gp_name': 'G.P. POPULAR', 'color': 'rgb(31, 155, 207)', 'is_party': True},
	'IU-LV': {'extended_name': 'Izquierda Unida-Los Verdes', 'gp_name': 'G.P. IZQUIERDA UNIDA', 'color': 'rgb(75, 191, 115)', 'is_party': True},
	'NO_PARTY': {'extended_name': 'Invitados', 'gp_name': 'No parlamentario', 'color': 'rgb(182, 182, 4)', 'is_party': False}
}

PARTY_CONFIG = {org_id: ORG_CONFIG[org_id] for org_id in ORG_CONFIG if ORG_CONFIG[org_id]['is_party']}

SEX_CONFIG = {
	'H': {'name': 'Hombre', 'color':  'rgb(57, 153, 255)'},
	'M': {'name': 'Mujer', 'color':  'rgb(255, 57, 102)'},
}

TOPIC_NAMES = (
	'Transportes',
	'Patrimonio',
	'Sanidad',
	'Acceso a la vivienda',
	'Justicia',
	'TV pública',
	'Actividad parlamentaria',
	'Protección social',
	'Agricultura',
	'Cultura',
	'Educación',
	'Crítica parlamentaria',
	'Transparencia',
	'Legislación',
	'Economía'
)

N_TOPICS = len(TOPIC_NAMES)

PLOT_BASE_CONFIG = {
	'font_family': "Nunito Sans",
	'title_font_family': "Nunito Sans",
	'xaxis_tickangle': -45,
}
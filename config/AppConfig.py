import os
import json

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_CONFIG = 'config/config.json'
CUSTOM_STYLES = 'assets/css/custom_styles.css'

PAGE_ROUTES = (
	{'id': 'inicio', 'route': '/inicio', 'name': 'Inicio'},
	{'id': 'analisis-partidos', 'route': '/analisis-partidos', 'name': 'Análisis de partidos'},
	{'id': 'analisis-diputados', 'route': '/analisis-diputados', 'name': 'Análisis de diputados'}
)
INITIAL_PAGE_ID = 'inicio'

with open('./config/config.json', encoding='utf-8') as config_file:
	APP_CONFIG = json.load(config_file)

APP_TITLE = APP_CONFIG['app_config']['app_title']
APP_LOGO = APP_CONFIG['app_config']['logo']
EXTERNAL_STYLESHEETS = APP_CONFIG['app_config']['external_stylesheets']
EXTERNAL_SCRIPTS = APP_CONFIG['app_config']['external_scripts']

TOPIC_NAMES = list(APP_CONFIG['topic_data'].keys())
N_TOPICS = len(TOPIC_NAMES)
TOPIC_TIMES = [f'topic_{i}_time' for i in range(0, N_TOPICS)]
TOPIC_COLORS = list(APP_CONFIG['topic_data'].values())

__ORG_ABBREVS__ = APP_CONFIG['organization_data']['org_abbrevs']
__ORG_IS_PARTY__ = APP_CONFIG['organization_data']['org_is_party']
__EXTENDED_NAMES__ = APP_CONFIG['organization_data']['extended_names']
__GP_NAMES__ = APP_CONFIG['organization_data']['gp_names']
__COLORS__ = APP_CONFIG['organization_data']['colors']

PARTY_ABBREVS = [party for idx, party in enumerate(__ORG_ABBREVS__) if __ORG_IS_PARTY__[idx]]
NO_PARTY_ABBREVS = [party for idx, party in enumerate(__ORG_ABBREVS__) if not __ORG_IS_PARTY__[idx]]

PARTY_COLORS = {party: __COLORS__[idx] for idx, party in enumerate(__ORG_ABBREVS__) if __ORG_IS_PARTY__[idx]}
NO_PARTY_COLORS = {party: __COLORS__[idx] for idx, party in enumerate(__ORG_ABBREVS__) if not __ORG_IS_PARTY__[idx]}

GP_NAMES = {org: __GP_NAMES__[idx] for idx, org in enumerate(__ORG_ABBREVS__)}
ORG_EXTENDED_NAMES = {org: __EXTENDED_NAMES__[idx] for idx, org in enumerate(__ORG_ABBREVS__)}

SEX_ABBREVS = list(APP_CONFIG['sex_data'].keys())
SEX_NAMES = {sex: APP_CONFIG['sex_data'][sex]['name'] for idx, sex in enumerate(SEX_ABBREVS)}
SEX_COLORS = {sex: APP_CONFIG['sex_data'][sex]['color'] for idx, sex in enumerate(SEX_ABBREVS)}
import dash
import copy
from dash.dependencies import Input, Output, State

from config import AppConfig
from config.AppConfig import INITIAL_LOCATION_ID
from controllers.Utils import get_page_route
from views import BaseView, LDAAnalysisView, PartyAnalysisView
from views.BaseView import MENU_NAV_LINKS

WebApp = dash.Dash(
	__name__,
	external_stylesheets=AppConfig.STYLESHEETS,
	suppress_callback_exceptions=True,
	title=AppConfig.APP_TITLE,
	assets_folder=AppConfig.STATIC_DATA
)

WebApp.layout = BaseView.layout

@WebApp.callback(
	[Output('page-content', 'children'), Output('page-nav', 'children')],
	Input('url', 'pathname')
)
def page_to_render(pathname):
	page_nav_links = copy.deepcopy(MENU_NAV_LINKS)

	if pathname == '/' or pathname == '' or pathname == get_page_route(INITIAL_LOCATION_ID):
		page_nav_links[INITIAL_LOCATION_ID].active = True
		return [LDAAnalysisView.layout, list(page_nav_links.values())]

	elif pathname == get_page_route('analisis-partidos'):
		page_nav_links['analisis-partidos'].active = True
		return [PartyAnalysisView.layout, list(page_nav_links.values())]

	return [None, list(MENU_NAV_LINKS.values())]
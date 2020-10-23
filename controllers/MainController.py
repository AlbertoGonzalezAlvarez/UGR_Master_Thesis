import dash
import copy
from dash.dependencies import Input, Output, State

from App import WebApp
from config import AppConfig
from config.AppConfig import INITIAL_LOCATION_ID
from controllers.Utils import get_page_route
from views import BaseView, LDAAnalysisView, PartyAnalysisView, NotFoundView
from views.BaseView import MENU_NAV_LINKS
import controllers.PageControllers.LDAAnalysisController


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

	return [NotFoundView.layout, list(MENU_NAV_LINKS.values())]
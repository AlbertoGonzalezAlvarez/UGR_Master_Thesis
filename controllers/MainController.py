import copy
import re

from dash import callback_context
from dash.dependencies import Input, Output, State, MATCH, ALL, ClientsideFunction
from dash.exceptions import PreventUpdate
from flask import request

from App import WebApp
from config.AppConfig import INITIAL_LOCATION_ID, USER_ANGENT_REGEX
from controllers.Utils import get_page_route
from views import LDAAnalysisView, PartyAnalysisView, NotFoundView
from views.BaseView import MENU_NAV_LINKS


@WebApp.callback(
	Output('page-content', 'children'),
	Output('page-nav', 'children'),
	Input('url', 'pathname'),
)
def page_to_render(pathname):
	page_nav_links = copy.deepcopy(MENU_NAV_LINKS)

	if pathname == '/' or pathname == '' or pathname == get_page_route(INITIAL_LOCATION_ID):
		page_nav_links[INITIAL_LOCATION_ID].active = True
		return LDAAnalysisView.layout, list(page_nav_links.values())

	elif pathname == get_page_route('analisis-partidos'):
		page_nav_links['analisis-partidos'].active = True
		return PartyAnalysisView.layout, list(page_nav_links.values())

	return NotFoundView.layout, list(MENU_NAV_LINKS.values())


@WebApp.callback(
	Output('local_storage', 'data'),
	Input('page-content', 'children'),
	State('local_storage', 'data')
)
def mobile_checking(_, data):
	if 'mobile' in data:
		raise PreventUpdate

	data['mobile'] = len(re.findall(USER_ANGENT_REGEX, request.headers['User_Agent'])) > 0
	return data


WebApp.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='collapse_function'
    ),
	[Output({'type': 'collapsible-item', 'ref': MATCH}, "is_open"),
	Output({'type': 'collapse-icon', 'ref': MATCH}, "className")],
	Input({'type': 'collapse-button', 'ref': MATCH}, "n_clicks"),
)
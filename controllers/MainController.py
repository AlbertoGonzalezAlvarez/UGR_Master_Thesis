import re

from dash.dependencies import Input, Output, State, MATCH, ClientsideFunction
from flask import request

import views
from WebApp import app
from config.AppConfig import INITIAL_LOCATION_ID, USER_ANGENT_REGEX
from controllers.Utils import get_page_route

is_mobile_device = None

@app.callback(
	Output('page-content', 'children'),
	Output('page-nav', 'children'),
	Input('url', 'pathname'),
	State('page-nav', 'children'),
)
def page_to_render(pathname, menu_links):
	is_mobile_device = len(re.findall(USER_ANGENT_REGEX, request.headers['User_Agent'])) > 0

	if pathname == '/' or pathname == '' or pathname == get_page_route(INITIAL_LOCATION_ID):
		layout = views.LDAAnalysisView.layout
		actual_location = INITIAL_LOCATION_ID
	elif pathname == get_page_route('analisis-partidos'):
		layout = views.PartyAnalysisView.layout
		actual_location = 'analisis-partidos'
	else:
		layout = views.NotFoundView.layout
		actual_location = None

	for menu_item in menu_links:
		if menu_item['props']['id'] == actual_location:
			menu_item['props']['active'] = True
		else:
			menu_item['props']['active'] = False

	return layout, menu_links


app.clientside_callback(
	ClientsideFunction(
		namespace='clientside',
		function_name='collapse_function'
	),
	[
		Output({'type': 'collapsible-item', 'ref': MATCH}, "is_open"),
		Output({'type': 'collapse-icon', 'ref': MATCH}, "className")
	],
	Input({'type': 'collapse-button', 'ref': MATCH}, "n_clicks"),
	State({'type': 'collapsible-item', 'ref': MATCH}, "is_open"),
	prevent_initial_call=True
)
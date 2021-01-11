import dash
from dash.dependencies import Input, Output, State, MATCH, ClientsideFunction

from config import AppConfig
from config.AppConfig import INITIAL_LOCATION_ID
from controllers.Utils import get_page_route
from views import BaseView

app = dash.Dash(
	__name__,
	external_stylesheets=AppConfig.STYLESHEETS,
	suppress_callback_exceptions=True,
	update_title=None,
	title=AppConfig.APP_TITLE,
	assets_folder=AppConfig.STATIC_DATA
)

app.layout = BaseView.layout
server = app.server
is_mobile_device = None

@app.callback(
	Output('page-content', 'children'),
	Output('page-nav', 'children'),
	Input('url', 'pathname'),
	State('page-nav', 'children'),
)
def page_to_render(pathname, menu_links):
	if pathname == '/' or pathname == '' or pathname == get_page_route(INITIAL_LOCATION_ID):
		from views import LDAAnalysisView
		layout = LDAAnalysisView.layout
		actual_location = INITIAL_LOCATION_ID
	elif pathname == get_page_route('analisis-partidos'):
		from views import PartyAnalysisView
		layout = PartyAnalysisView.layout
		actual_location = 'analisis-partidos'
	else:
		from views import NotFoundView
		layout = NotFoundView.layout
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

if __name__ == "__main__":
	app.run_server(debug=False)
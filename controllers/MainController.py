import dash
from dash.dependencies import Input, Output, State

from config import AppConfig
from views import BaseView, LDAAnalysisView

WebApp = dash.Dash(
	__name__,
	external_stylesheets=AppConfig.STYLESHEETS,
	suppress_callback_exceptions=True,
	title=AppConfig.APP_TITLE
)

WebApp.layout = BaseView.layout

@WebApp.callback(
	Output('page-content', 'children'),
	Input('url', 'pathname')
)
def page_to_render(pathname):
	if pathname == '/' or pathname == '' or pathname == '/index':
		return LDAAnalysisView.layout

@WebApp.callback(
	[Output(f"link-{i}", "active") for i in range(1, 4)],
	[Input('url', 'pathname')],
	[State(f"link-{i}", "href") for i in range(1, 4)]
)
def set_active_page(pathname, *args):
	return [True if nav_item == pathname else False for nav_item in args]
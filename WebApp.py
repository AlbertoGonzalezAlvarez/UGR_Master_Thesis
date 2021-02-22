from dash import dash

from config import AppConfig
from views import BaseView

WebApp = dash.Dash(
	__name__,
	external_stylesheets=AppConfig.STYLESHEETS,
	suppress_callback_exceptions=True,
	update_title=None,
	title=AppConfig.APP_TITLE,
	meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

WebApp.layout = BaseView.layout
server = WebApp.server

from controllers.MainController import *

if __name__ == "__main__":
	WebApp.run_server(debug=True, port=80)
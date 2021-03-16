from dash import dash

from config import AppConfig
from views import BaseView

WebApp = dash.Dash(
	__name__,
	external_stylesheets=AppConfig.EXTERNAL_STYLESHEETS,
	external_scripts=AppConfig.EXTERNAL_SCRIPTS,
	suppress_callback_exceptions=True,
	update_title=None,
	title=AppConfig.APP_TITLE,
)

WebApp.layout = BaseView.layout
server = WebApp.server

from controllers import *

if __name__ == "__main__":
	WebApp.run_server(debug=False)
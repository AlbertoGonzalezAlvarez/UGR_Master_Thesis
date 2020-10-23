from dash import dash

from config import AppConfig
from views import BaseView

WebApp = dash.Dash(
	__name__,
	external_stylesheets=AppConfig.STYLESHEETS,
	suppress_callback_exceptions=True,
	title=AppConfig.APP_TITLE,
	assets_folder=AppConfig.STATIC_DATA
)

WebApp.layout = BaseView.layout

from controllers.MainController import *

if __name__ == "__main__":
	WebApp.run_server(debug=True)
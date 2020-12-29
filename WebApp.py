from dash import dash

from config import AppConfig
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

from controllers.MainController import *

if __name__ == "__main__":
	app.run_server(debug=False)
from dash import dash

from Config import AppConfig
from Views import BaseView
from waitress import serve

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

from Controllers.MainController import *

if __name__ == "__main__":
	serve(WebApp.server, host='0.0.0.0', port=80, threads=4)
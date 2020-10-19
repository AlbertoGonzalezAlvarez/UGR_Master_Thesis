import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc

from config.AppConfig import APP_LOGO

layout = html.Div(
	[
			html.Meta(name='viewport', content='width=device-width, initial-scale=1'),
			dcc.Store(id='navigator_memory'),
			dbc.Navbar(color="primary", dark=True, expand='lg', children=[
				dbc.Col(children=
					html.A(className='d-inline-flex', href="#", children=
						dbc.Row(align="center", children=[
							dbc.Col(children=html.Img(src=APP_LOGO, height="30px")),
							dbc.NavbarBrand("Anali.sys")
							],
						),
					),
				),
				dbc.NavbarToggler(id="navbar-toggler"),
				dbc.Collapse(id="navbar-collapse", navbar=True, children=
					dbc.Nav(navbar=True, className='ml-auto', children=[
						dbc.NavLink("Ánalisis de LDA", id='link-1', href="/"),
						dbc.NavLink("Análisis de partidos", id='link-2', href="/analisis-partidos"),
						dbc.NavLink("Análisis de diputados", id='link-3', href="/analisis-diputados"),
						]
					),
				)
			]),
			dcc.Location(id='url', refresh=False),
			html.Div(
				id='page-content',
				className='mt-4 text-justify container-fluid'
			),
			html.Div(
				id='after-page-content'
			)
	]
)
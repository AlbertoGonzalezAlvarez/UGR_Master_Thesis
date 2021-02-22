import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from config import APP_LOGO, PAGE_ROUTES

MENU_NAV_LINKS = {}

for page in PAGE_ROUTES:
	MENU_NAV_LINKS[page["id"]] = \
		dbc.NavLink(page['name'], id=page["id"], href=page["route"], active=False)

layout = html.Div(id='main-div', children=
	[
			html.Meta(name='viewport', content='width=device-width, initial-scale=1'),
			dbc.Navbar(color='primary', fixed='top', sticky='fixed', dark=True, expand='lg', children=[
				dbc.Col(children=
					html.A(className='d-inline-flex', href="#", children=
						dbc.Row(align='center', children=[
							dbc.Col(children=html.Img(src=APP_LOGO, height='30px')),
							dbc.NavbarBrand(children='Anali.sys', id='navbar_brand')
							],
						),
					),
				),
				dbc.NavbarToggler(id='navbar-toggler'),
				dbc.Collapse(id='navbar-collapse', navbar=True, children=
					dbc.Nav(id='page-nav', navbar=True, className='ml-auto', children=list(MENU_NAV_LINKS.values()))
				)
			]),
			dcc.Location(id='url', refresh=False),
			html.Div(
				id='page-content',
				className='mt-4 mb-4 text-justify container-fluid'
			),
			html.Footer(className='footer', children=
				html.Div(className='text-center', children=
					[
						'Made with ❤️ by ',
						html.A(href='https://www.linkedin.com/in/alberto-gonzalez-alvarez/', children='Alberto González')
					]
				)
			),
			dcc.Store(id='mobile_device', storage_type='session'),
	]
)
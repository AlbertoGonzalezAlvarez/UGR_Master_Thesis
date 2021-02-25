import dash_html_components as html
import dash_bootstrap_components as dbc

layout = html.Div(className='d-flex flex-row align-items-center', style=dict(minHeight='88vh'), children=
	dbc.Container([
		dbc.Row(className='justify-content-center', children=
			dbc.Col(md=12, className='text-center', children=[
				html.I(className='fas fa-cog fa-9x text-logo animation-rotate'),
				html.Div(className='mb-2 display-4', children='Página en construcción'),
				html.A(href='/', children='Volver al inicio')
			])
		),
	])
)
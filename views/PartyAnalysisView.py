import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc

layout = [
			html.Div(className='justify-content-center row', children=
				html.Div(className='col-6', children=
					[
						html.H1('Análisis de partidos'),
						html.P('En esta sección recogeremos los temas así como las palabras que se usan más en cada uno de ellos.')
					]
				)
			)
		]


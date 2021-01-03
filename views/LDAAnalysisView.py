import dash_html_components as html

import WebApp

layout = [
			html.Div(className='justify-content-center row', children=
				html.Div(className='col-6', children=
					[
						html.H1('Análisis general de temáticas'),
						html.P('En esta sección recogeremos los temas así como las palabras que se usan más en cada uno de ellos.')
					]
				)
			),
			html.Div(className="justify-content-md-center", children=[
				html.Div(className='col-sm-6 mx-auto', children=
					html.Div(
						id='embeded',
						className='embed-responsive embed-responsive-4by3 d-flex justify-content-center align-items-center',
						children=html.Embed(src=WebApp.app.get_asset_url('below_10_above_0.1-model_t15_a051_b001.html'), className='embed-responsive-item')
					)
				)
			])
		]


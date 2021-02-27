import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

header = html.Header(className='bg-green py-5 mb-5', children=
	dbc.Container(className='container-fliud h-100', children=
		dbc.Row(className='h-100 align-items-center', children=
			dbc.Col(lg=12, children=[
				html.H1(className='display-4 text-white mt-5 mb-2', children='¿Qué es Analy.sis?'),
				html.P(className='lead mb-5 text-white', children=
				'''
					Analys.sis es un proyecto que analiza las intervenciones realizadas en el Parlamento de Andalucía 
					entre 2008 y 2012. La finalidad es saber y poner al alcance de la ciudadanía el tiempo 
					que invierten los parlamentarios en diferentes temas que son de interés para la sociedad.
				''')
			])
		)
	)
)
layout = [
	html.Video(id='init-video', autoPlay=True, muted=True, loop=True, src='assets/media/data_science.mp4'),
	dbc.Container([
		dbc.Row(className='justify-content-around', children=[
			dbc.Col(className='mb-5 bg-white-65 p-4', md=8, children=[
				html.H2([html.I(className='fas fa-search mr-2'), '¿Que encontraré en la web?']),
				html.Hr(),
				html.P(
				'''
					En la web podrás encontrar diferentes análisis que he realizado en base a las temáticas extraídas
					con un algoritmo de extracción de temas. Podrás conocer el tiempo que dedica cada partido a cada tema,
					tiempo que dedican los grupos parlamentario a cada tema de forma mensual e incluso datos pormenorizados
					de cada uno de los diputados. 
				'''),
				html.Br(),
				html.P(
				'''
					Este proyecto nace como Trabajo de Final de Máster (TFM) en el que hice estos análisis y decidí buscar
					la manera de que fueran públicos y accesibles para familiarizarme con diferentes tecnologías web útiles para
					la presentación y análisis de resultados.
				'''),
			]),
			dbc.Col(className='mb-5 bg-white-65 p-4 ml-2', md=3, children=[
				html.H2([html.I(className='fas fa-user mr-2'), 'Sobre mi']),
				html.Hr(),
				html.P('Soy Alberto González Álvarez, graduado en Ingeniería Informática en la ULL y máster en Ciencia de Datos en la UGR. '),
				html.P(children=[
					html.I(className='fab fa-github-square mr-2 align-self-center'),
					html.A('GitHub', href='https://github.com/AlberTJ97/analysis')
				]),
				html.P(children=[
					html.I(className='fab fa-linkedin mr-2 align-self-center'),
					html.A('LinkedIn', href='https://www.linkedin.com/in/alberto-gonzalez-alvarez/')
				]),
				html.P(children=[
					html.I(className='fas fa-envelope mr-2 align-self-center'),
					html.A('alberjga97@gmail.com', href='mailto:alberjga97@gmail.com')
				]),
			]),
		]),
		dbc.Row([
			dbc.Col(className='mb-5', md=4, children=[
				dbc.Card(className='bg-white-65', children=[
					dbc.CardImg(src='https://placehold.it/300x200', top=True),
					dbc.CardBody([
						html.H4('Card 1', className='card-title'),
						html.P(className='card-text bg-white-50', children=
							'''
								Lorem ipsum dolor sit amet consectetur adipiscing, elit cursus vel accumsan pulvinar,
								justo malesuada morbi phasellus.
							'''
						),
						dbc.Button('Go somewhere', color='primary'),
					]),
				])
			]),
			dbc.Col(className='mb-5', md=4, children=[
				dbc.Card(className='bg-white-65', children=[
					dbc.CardImg(src='https://placehold.it/300x200', top=True),
					dbc.CardBody([
						html.H4('Card 2', className='card-title'),
						html.P(className='card-text bg-white-50', children=
							'''
								Lorem ipsum dolor sit amet consectetur adipiscing, elit cursus vel accumsan pulvinar,
								justo malesuada morbi phasellus.
							'''
						),
						dbc.Button('Go somewhere', color='primary'),
					]),
				])
			]),
			dbc.Col(className='mb-5', md=4, children=[
				dbc.Card(className='bg-white-65', children=[
					dbc.CardImg(src='https://placehold.it/300x200', top=True),
					dbc.CardBody([
						html.H4('Card 3', className='card-title'),
						html.P(className='card-text bg-white-50', children=
							'''
								Lorem ipsum dolor sit amet consectetur adipiscing, elit cursus vel accumsan pulvinar,
								justo malesuada morbi phasellus.
							''',
						),
						dbc.Button('Go somewhere', color='primary'),
					]),
				])
			]),

		])
	]),
]
import dash_html_components as html
import dash_bootstrap_components as dbc

layout = html.Div(className='d-flex flex-row align-items-center min-vh-100', children=
    dbc.Container(
        dbc.Row(className='justify-content-center', children=
            dbc.Col(md=12, className='text-center', children=[
                html.I(className='fas fa-exclamation-triangle fa-9x text-warning'),
                html.Div(className='mb-1 mt-2 display-4', children='Página no encontrada'),
                html.A(href='/', children='Volver al inicio')
            ])
        )
    )
)
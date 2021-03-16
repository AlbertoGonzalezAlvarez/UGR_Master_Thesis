import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from config import APP_LOGO, PAGE_ROUTES

layout = html.Div(id='main-div', children=
    [
            html.Meta(name='viewport', content='width=device-width, initial-scale=1'),
            dbc.Navbar(color='primary', sticky='top', dark=True, expand='lg', children=[
                dbc.Col(children=
                    html.A(className='d-inline-flex', href="#", children=
                        dbc.Row(align='center', children=[
                            dbc.NavbarBrand(children=html.A(href='/', children=
                                html.Img(id='logo-image', src=APP_LOGO, style=dict(height='35px')))
                            )],
                        ),
                    ),
                ),
                dbc.NavbarToggler(id='navbar-toggler'),
                dbc.Collapse(id='navbar-collapse', navbar=True, children=
                    dbc.Nav(id='page-nav', navbar=True, className='ml-auto', children=[
                        dbc.NavLink(page['name'], id=page['id'], href=page['route'], active=False) for page in PAGE_ROUTES]
                    )
                )
            ]),
            dcc.Location(id='url', refresh=False),
            html.Header(id='page-header'),
            html.Div(
                id='page-content',
                className='text-justify container-fluid'
            ),
            html.Footer(className='footer', children=
                html.Div(className='text-center', children=
                    [
                        'Made with ❤️ by ',
                        html.A(href='https://www.linkedin.com/in/alberto-gonzalez-alvarez/', children='Alberto González')
                    ]
                )
            ),
    ]
)
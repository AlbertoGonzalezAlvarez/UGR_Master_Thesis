from dash.dependencies import Input, Output, State

import views
from WebApplication import WebApp
from config import INITIAL_PAGE_ID
from utils import get_page_route


@WebApp.callback(
    Output('page-content', 'children'),
    Output('page-nav', 'children'),
    Output('page-header', 'children'),
    Input('url', 'pathname'),
    State('page-nav', 'children'),
)
def page_to_render(pathname, menu_links):
    if pathname == '/' or pathname == '' or pathname == get_page_route(INITIAL_PAGE_ID):
        header = views.InitView.header
        layout = views.InitView.layout
        actual_location = 'inicio'
    elif pathname == get_page_route('analisis-partidos'):
        header = None
        layout = views.PartyAnalysisView.layout
        actual_location = 'analisis-partidos'
    elif pathname == get_page_route('analisis-diputados'):
        header = None
        layout = views.WorkingView.layout
        actual_location = 'analisis-diputados'
    else:
        header = None
        layout = views.NotFoundView.layout
        actual_location = None

    for menu_item in menu_links:
        if menu_item['props']['id'] == actual_location:
            menu_item['props']['active'] = True
        else:
            menu_item['props']['active'] = False

    return layout, menu_links, header


@WebApp.callback(
    Output("navbar-collapse", "is_open"),
    Input("navbar-toggler", "n_clicks"),
    Input('url', 'pathname'),
    State("navbar-collapse", "is_open")
)
def toggle_navbar_collapse(n, _, is_open):
    if n:
        return not is_open
    return False
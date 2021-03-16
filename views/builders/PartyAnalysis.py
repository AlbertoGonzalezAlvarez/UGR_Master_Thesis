import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from plotly import graph_objs as go

from config import AppConfig
from models import AnalyzedInterventions


def build_topic_distribution_chart():
    data = AnalyzedInterventions.get_topic_distribution_per_party()

    figures = [
        go.Bar(
            x=data['topic'].unique(),
            y=data.loc[data['organizacion'] == party]['score'] * 100,
            name=party,
            marker_color=AppConfig.PARTY_COLORS[party],
            hovertemplate='Porcentaje de tiempo: %{y:.2f}%<br>') for party in data['organizacion'].unique()
    ]

    layout = dict(
        template='lux',
        barmode='group',
        showlegend=False,
        xaxis_title='Temas',
        yaxis_title='Porcentaje de tiempo',
    )

    return go.Figure(figures, layout)


def build_woman_vs_man_chart():
    data = AnalyzedInterventions.get_topic_distribution_per_sex()

    figures = [
        go.Bar(
            x=AppConfig.TOPIC_NAMES,
            y=data.loc[data['sexo'] == sex_id]['score'] * 100,
            name=AppConfig.SEX_NAMES[sex_id],
            marker_color=AppConfig.SEX_COLORS[sex_id],
            hovertemplate='Porcentaje de tiempo: %{y:.2f}%<br>'
        ) for sex_id in data['sexo'].unique()
    ]

    layout = dict(
        template='lux',
        barmode='group',
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        xaxis_title='Temas',
        yaxis_title='Porcentaje de tiempo',
    )

    return go.Figure(figures, layout)


def build_topic_duration_chart():
    data = AnalyzedInterventions.get_max_time_per_topic()

    figure = go.Bar(
        x=data['predominant_topic'],
        y=data['score'],
        marker_color=AppConfig.TOPIC_COLORS,
        customdata=list(
            zip(data['fecha'], data['diputado'].str.replace('-', ' ').apply(str.title), data['organizacion'])),
        hovertemplate=
        '<b>Tema: %{x}</b><br><br>' +
        'Fecha: %{customdata[0]|%d-%m-%y}<br>' +
        'Diputado: %{customdata[1]}<br>' +
        'Partido: %{customdata[2]}<br>' +
        'Duración: %{y:.0f} min <br>' +
        '<extra></extra>'
    )

    layout = dict(
        template='lux',
        barmode='group',
        xaxis_title='Temas',
        yaxis_title='Minutos estimados',
    )

    return go.Figure(figure, layout)


def build_topic_distribution_per_month():
    data = AnalyzedInterventions.get_monthly_evolution_topics()

    dates = data['fecha'].unique()
    figures = []

    for party in AppConfig.PARTY_ABBREVS:
        for topic_idx, topic_name in enumerate(AppConfig.TOPIC_NAMES):
            figures.append(
                go.Scatter(
                    x=dates,
                    y=data.loc[data['organizacion'] == party][topic_name] * 100,
                    text=dates,
                    visible=False,
                    mode='lines+markers',
                    line=dict(color=AppConfig.TOPIC_COLORS[topic_idx]),
                    hovertemplate=
                    f'<b>{topic_name}</b><br>' +
                    'Media de minutos: %{y:.3f}<br>'
                    '<extra></extra>',
                )
            )

    layout = dict(
        showlegend=False,
        template='lux',
        hovermode='x',
        xaxis=dict(
            rangeslider=dict(visible=True),
        ),
        yaxis=dict(
            side='right',
            zeroline=False,
        ),
        yaxis_title='Minutos',
        height=1000,
        margin=dict(
            t=50,
            b=20
        ),
    )

    return go.Figure(figures, layout)


def build_party_info_cards(default_collapsed):
    intervention_count = AnalyzedInterventions.get_intervention_count()
    woman_interventions = AnalyzedInterventions.get_woman_interventions()
    n_deputies = AnalyzedInterventions.get_n_deputies()
    woman_deputies = AnalyzedInterventions.get_n_woman_deputies()

    return [
        [
            dbc.CardHeader(children=[
                html.A(className='text-decoration-none d-flex', href=f'#collapsible-item-{party}-{default_collapsed}',
                       role='button',
                       children=[
                           html.I(className='far mr-2 align-self-center'),
                           html.Span(f'{AppConfig.ORG_EXTENDED_NAMES[party]}'),
                           dbc.Badge(party, className=f'align-self-center ml-auto {party}')
                       ],
                       **{'data-toggle': 'collapse', 'aria-expanded': default_collapsed,
                          'aria-controls': f'collapsible-item-{party}-{default_collapsed}'}
                       ),
            ]),
            html.Div(
                id=f'collapsible-item-{party}-{default_collapsed}',
                className=f'collapse {"show" if default_collapsed else ""}', children=
                dbc.CardBody([
                    html.P(id=f'{party}-card-info', className='card-text', children=dcc.Markdown(
                        f'''
                            A continuación, se recogen algunos datos relevantes relacionados con el {AppConfig.GP_NAMES[party]}.  

                            \- Interevenciones realizadas: {intervention_count[party]}  
                            \- Realizadas por mujeres: {woman_interventions[party]:.2f}%  
                            \- Número de diputados: {n_deputies[party]}  
                            \- Mujeres diputadas: {woman_deputies[party]:.2f}%
                         '''
                    ))
                ])
            )
        ] for party in AppConfig.PARTY_ABBREVS]

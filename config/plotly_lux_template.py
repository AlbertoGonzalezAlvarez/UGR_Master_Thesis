import plotly.express as px
import plotly.io as pio

pio.templates['lux'] = pio.templates['plotly']
pio.templates['lux'].layout.font.update(family='Nunito Sans')
pio.templates['lux'].layout.plot_bgcolor = None
pio.templates['lux'].layout.paper_bgcolor = 'white'
pio.templates['lux'].layout.margin.update(l=0, r=0, t=40, b=0)
pio.templates['lux'].layout.xaxis.update(
    mirror=True,
    ticks='outside',
    gridcolor='rgba(0, 0, 0, 0.125)',
    linecolor='rgba(0, 0, 0, 0.125)',
    zerolinecolor='rgba(0, 0, 0, 0.125)',
    zeroline=True,
    showgrid=True,
    gridwidth=1,
    zerolinewidth=2,
    tickangle=-45
)
pio.templates['lux'].layout.yaxis.update(
    mirror=True,
    ticks='outside',
    gridcolor='rgba(0, 0, 0, 0.125)',
    linecolor='rgba(0, 0, 0, 0.125)',
    zerolinecolor='rgba(0, 0, 0, 0.125)',
    zeroline=True,
    showgrid=True,
    gridwidth=1,
    zerolinewidth=2,
)
pio.templates['lux'].layout.colorway = px.colors.qualitative.Bold + \
                                       ['#AF0038', '#DDCC77', '#90AD1C'] + \
                                       px.colors.qualitative.Light24

pio.templates['lux'].layout.annotations = [
    dict(
        text='@AlbertoTJ97',
        opacity=0.1,
        font=dict(color='black', size=32),
        bgcolor='white',
        xref='x domain',
        yref='y domain',
        x=0.5,
        y=0.6,
        textangle=-30,
        xanchor='center',
        yanchor='middle',
        showarrow=False,
        name='twitter_username',
    )
]
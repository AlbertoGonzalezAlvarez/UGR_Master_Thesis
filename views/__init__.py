from .BaseView import *
from .templates.plotly_lux_template import *
from .PartyAnalysisView import *
from .LDAAnalysisView import *
from .NotFoundView import *
import plotly.io as pio

pio.templates.default = 'lux'
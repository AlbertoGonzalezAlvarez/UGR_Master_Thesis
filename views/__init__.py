from .BaseView import *
from .templates.plotly_lux_template import *
from .PartyAnalysisView import *
from .NotFoundView import *
from .InitView import *
import plotly.io as pio

pio.templates.default = 'lux'
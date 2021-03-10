from .BaseView import *
from .Templates.plotly_lux_template import *
from .PartyAnalysisView import *
from .NotFoundView import *
from .WorkingView import *
from .InitView import *
import plotly.io as pio

pio.templates.default = 'lux'
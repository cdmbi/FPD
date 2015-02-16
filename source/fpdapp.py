"""
This file demonstrates a bokeh applet, which can be viewed directly
on a bokeh-server. See the README.md file in this directory for
instructions on running.
"""

import os
import logging
logging.basicConfig(level=logging.DEBUG)

import numpy as np
import pandas as pd

from bokeh.plotting import circle, figure
from bokeh.models import Plot, ColumnDataSource, Range1d
from bokeh.properties import Instance, String
from bokeh.server.app import bokeh_app
from bokeh.server.utils.plugins import object_page
from bokeh.models.widgets import HBox, Slider, TextInput, VBoxForm, Select, String, PreText

_data = pd.read_csv(os.path.join('data',
                    'FPD-non-redundant-processed.csv'),
                    delimiter=',')
d = _data.head(n=20).ix[:, ['excitation_new', 'emission_new']].dropna()
data = _data.head(n=20).ix[d.index,['emission_new',
                        'emission_alt',
                        'excitation_new',
                        'excitation_alt',
                        'excitation_color_new',
                        'excitation_color_class',
                        'emission_color_new',
                        'emission_color_class',
                        'chromophore_name',
                        'chromophore_class',
                        'fpid',
                        ]].fillna('')

CHROMOPHORES = sorted(set(data.head(n=20)['chromophore_class'].dropna()))

class FPDApp(HBox):
    extra_generated_classes = [["FPDApp", "FPDApp", "HBox"]]

    pretext = Instance(PreText)
    input_box = Instance(VBoxForm)
    preview = Instance(HBox)
    selector = Instance(Select)
    colname = String(default=CHROMOPHORES[0])
    source = Instance(ColumnDataSource)
    plot = Instance(Plot)

    @classmethod
    def create(cls):
        """
        This function is called once, and is responsible for
        creating all objects (plots, datasources, etc)
        """
        obj = cls()

        obj.source = ColumnDataSource(data=data)

        obj.selector = Select(
                name="variable",
                value='A',
                options=sorted(data.chromophore_class),
                )

        # TODO:: add a select tool
        toolset = "pan,reset,resize,save,wheel_zoom,hover"

        obj.plot = figure(title="A Scatter Plot", tools=toolset)
        obj.plot.circle('excitation_new', 'emission_new',
                source=obj.source,
                plot_width=600, plot_height=600,
                radius=2, fill_alpha=0.6,
                fill_color='excitation_color_new',
                line_color='#000000',
                )

        obj.pretext = PreText(text=str(obj.get_data()[:3]),
                                        width=500)

        obj.input_box = VBoxForm(children=[obj.selector])
        obj.preview = HBox(children=[obj.pretext, obj.plot])
        obj.children.append(obj.input_box)
        obj.children.append(obj.preview)

        return obj

    def setup_events(self):
        super(FPDApp, self).setup_events()
        if self.selector:
            self.selector.on_change('value', self, 'input_change')

    def input_change(self, obj, attrname, old, new):
        """
        This callback is executed whenever the input form changes. It is
        responsible for updating the plot, or anything else you want.
        The signature is:
        Args:
            obj : the object that changed
            attrname : the attr that changed
            old : old value of attr
            new : new value of attr
        """
        if obj == self.selector:
            self.colname = new

        # d = data[data['chromophore_class']==self.colname]
        d = self.get_data()
        self.pretext.text = str(d[:3])
        self.source.data = d.to_dict('list')

    def get_data(self):
        selected = data['chromophore_class'] == self.colname
        return data[selected]

@bokeh_app.route("/bokeh/fpd/")
@object_page("sin")
def make_object():
    app = FPDApp.create()
    return app

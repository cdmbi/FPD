#!/usr/bin/env python
'''Description'''

import sys
import os
import logging
logging.basicConfig(level=logging.DEBUG)

import pandas as pd
import numpy as np

from collections import OrderedDict
from bokeh.plotting import circle, figure
from bokeh.models import Plot, ColumnDataSource, Range1d, HoverTool
from bokeh.properties import Instance
from bokeh.server.app import bokeh_app
from bokeh.server.utils.plugins import object_page
from bokeh.models.widgets import HBox, Slider, TextInput, VBoxForm, Select

data = pd.read_csv(os.path.join('data',
                    'FPD-non-redundant-processed.csv'),
                    delimiter=',')

CHROMOPHORES = sorted(set(data['chromophore_class'].dropna()))

class FPDApp(HBox):
    extra_generated_classes = [["FPDApp", "FPDApp", "HBox"]]

    inputs = Instance(VBoxForm)

    # text = Instance(TextInput)

    excitation = Instance(Slider)
    emission = Instance(Slider)
    chromophore = Instance(Select)

    plot = Instance(Plot)
    source = Instance(ColumnDataSource)

    def __init__(self, *args, **kwargs):
        super(FPDApp, self).__init__(*args, **kwargs)
        self._dfs = {}

    @property
    def df(self):
        return data.head().ix[:, ['excitation_new',
                                    'emission_new',
                                    'excitation_color_new',
                                    'excitation_color_class',
                                    ]].dropna()

    def make_source(self):
        self.source = ColumnDataSource(data=self.df)

    @classmethod
    def create(cls):
        obj = cls()

        obj.make_source()

        obj.excitation = Slider(
                title="Excitation", name="excitation",
                value=1.0, start=-5.0, end=5.0,
                )
        obj.emission = Slider(
                title="Emission", name="emission",
                value=1.0, start=-5.0, end=5.0,
                )
        obj.chromophore = Select(
                name="Chromophore",
                value=CHROMOPHORES[0],
                options=CHROMOPHORES,
                )
        toolset = "pan,reset,resize,save,wheel_zoom,hover"

        p = figure(title="Just a simple plot", tools=toolset)
        p.circle('excitation_new', 'emission_new',
                source=obj.source,
                plot_width=600, plot_height=600,
                radius=2, fill_alpha=0.6,
                fill_color='excitation_color_new',
                line_color='#000000',
                )
        hover = p.select(dict(type=HoverTool))
        hover.tooltips = [
            # ("FPID", "@fpid"),
            # ("Chromophore", "@chromophore"),
            ("Excitation Color Class", "@excitation_color_class"),
            # ("Emission color class", "@emission_color_class"),
            ("Primary excitation", "@excitation_new"),
            # ("Secondary excitation", "@excitation_alt"),
            ("Primary emission", "@emission_new"),
            # ("Secondary emission", "@emission_alt"),
        ]
        # obj.update_data()
        obj.plot = p
        obj.inputs = VBoxForm(
                children=[
                    obj.excitation,
                    obj.emission,
                    obj.chromophore,
                    ]
                )

        obj.children.append(obj.inputs)
        obj.children.append(obj.plot)
        return obj

    # def setup_events(self):
    #     super(FPDApp, self).setup_events()
        # for w in ["offset", "amplitude", "phase", "freq"]:
        #     getattr(self, w).on_change("value",
        #                         self, "input_change")

    # def input_change(self, obj, attrname, old, new):
    #     self.update_data()
        # self.plot.title = self.text.value

    # def update_data(self):
    #     pass

@bokeh_app.route("/bokeh/fpd/")
@object_page("sin")
def make_object():
    app = FPDApp.create()
    return app

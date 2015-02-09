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
from bokeh.properties import Instance, String
from bokeh.server.app import bokeh_app
from bokeh.server.utils.plugins import object_page
from bokeh.models.widgets import HBox, Slider, TextInput, VBoxForm, Select

def get_data(chrom_class):
    data = pd.read_csv(os.path.join('data',
                        'FPD-non-redundant-processed.csv'),
                        delimiter=',')
    d = data.head(n=20).ix[:, ['excitation_new', 'emission_new']].dropna()
    cleaned_data = data.head(n=20).ix[d.index,['emission_new',
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
    selected_data = cleaned_data[
                        cleaned_data['chromophore_class']==chrom_class]
    return selected_data

data = pd.read_csv(os.path.join('data',
                    'FPD-non-redundant-processed.csv'),
                    delimiter=',')

CHROMOPHORES = sorted(set(data.head(n=20)['chromophore_class'].dropna()))

class FPDApp(HBox):
    extra_generated_classes = [["FPDApp", "FPDApp", "HBox"]]

    inputs = Instance(VBoxForm)
    plots = Instance(HBox)

    # text = Instance(TextInput)

    excitation = Instance(Slider)
    emission = Instance(Slider)
    chrom_class_select = Instance(Select)
    chrom_class = String(default='AYG')

    plot = Instance(Plot)
    source = Instance(ColumnDataSource)

    def __init__(self, *args, **kwargs):
        super(FPDApp, self).__init__(*args, **kwargs)


    @classmethod
    def create(cls):
        obj = cls()

        print('---- INSTANTIATE OBJ ----')
        obj.make_inputs()
        obj.make_source()
        obj.make_plots()
        obj.set_children()

        print('---- ALL DONE ---- .')

        return obj


    @property
    def df(self):
        data = get_data(self.chrom_class)
        return data


    def make_inputs(self):
        print('CALL: make_inputs')
        print('Current chromophore class: %s', self.chrom_class)

        self.excitation = Slider(
                title="Excitation", name="excitation",
                value=1.0, start=-5.0, end=5.0,
                )
        self.emission = Slider(
                title="Emission", name="emission",
                value=1.0, start=-5.0, end=5.0,
                )
        self.chrom_class_select = Select(
                name="Chromophore",
                value='AYG',
                options=CHROMOPHORES,
                )


    def make_source(self):
        print('CALL: make_source')
        self.source = ColumnDataSource(data=self.df)
        print('CALL END: make_source')


    def make_plots(self):
        print('CALL: make_plots')
        self.plot = self.scatter_plot()


    def scatter_plot(self):
        print('CALL: scatter_plot')
        toolset = "pan,reset,resize,save,wheel_zoom,hover"

        plot = figure(title="A Scatter Plot", tools=toolset)
        plot.circle('excitation_new', 'emission_new',
                source=self.source,
                plot_width=600, plot_height=600,
                radius=2, fill_alpha=0.6,
                fill_color='excitation_color_new',
                line_color='#000000',
                )
        hover = plot.select(dict(type=HoverTool))
        hover.tooltips = [
            ("FPID ", "@fpid"),
            ("Chromophore name ", "@chromophore_name"),
            ("Excitation color class ", "@excitation_color_class"),
            ("Emission color class ", "@emission_color_class"),
            ("Primary excitation ", "@excitation_new"),
            ("Secondary excitation ", "@excitation_alt"),
            ("Primary emission ", "@emission_new"),
            ("Secondary emission ", "@emission_alt"),
        ]
        return plot

    def set_children(self):
        print('CALL: set_children')
        self.inputs = VBoxForm(children=[
                                self.excitation,
                                self.emission,
                                self.chrom_class_select,
                            ])

        print('set_children part II ----')
        self.plots = HBox(children=[self.plot])
        self.children = [self.inputs, self.plots]

    def setup_events(self):
        print('CALL: setup_events')
        super(FPDApp, self).setup_events()

        if self.chrom_class_select:
            self.chrom_class_select.on_change(
                    'value', self, 'input_change')

    def input_change(self, obj, attrname, old, new):
        print('CALL: input_change')
        if obj == self.chrom_class_select:
            self.chrom_class = new
            print '\n\nChromophore class: %s\n' % \
                    self.chrom_class

        self.make_source()
        # self.make_plots()
        # self.set_children()

@bokeh_app.route("/bokeh/fpd/")
@object_page("fpd")
def make_object():
    app = FPDApp.create()
    return app

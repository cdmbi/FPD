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
from bokeh.models.widgets import HBox, Slider, TextInput, VBox,\
                                    VBoxForm, Select, PreText, DataTable
from bokeh.models.widgets.tables import TableColumn

_data = pd.read_csv(os.path.join('data',
                    'FPD-non-redundant-processed.csv'),
                    delimiter=',')
d = _data.ix[:, ['excitation_new', 'emission_new']].dropna()
data = _data.ix[d.index,['emission_new',
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
                        'uniprot',
                        'pdb_id',
                        'genbank',
                        'mutation',
                        'quantum_yield',
                        'pka',
                        'protein_name',
                        'amino_acid_sequence',
                        ]].fillna('')

CHROMOPHORES = sorted(set(data['chromophore_class']))
xy_margin = 50
max_emission = max(data['emission_new']) + xy_margin
min_emission = min(data['emission_new']) - xy_margin
max_excitation = max(data['excitation_new']) + xy_margin
min_excitation = min(data['excitation_new']) - xy_margin

columns = [
        TableColumn(field='fpid', title='FPID'),
        TableColumn(field='protein_name', title='Protein name'),
        TableColumn(field='excitation_new', title='Excitation'),
        TableColumn(field='emission_new', title='Emission'),
        TableColumn(field='pdb_id', title='PDB ID'),
        TableColumn(field='genbank', title='Genbank ID'),
        TableColumn(field='mutation', title='Mutation'),
        TableColumn(field='quantum_yield', title='Quantum Yield'),
        TableColumn(field='pka', title='pka'),
        TableColumn(field='amino_acid_sequence', title='Sequence'),
        ]

class FPDApp(HBox):
    extra_generated_classes = [["FPDApp", "FPDApp", "HBox"]]

    main_frame = Instance(VBox)
    top_frame = Instance(HBox)
    table_frame = Instance(HBox)
    input_frame = Instance(VBoxForm)
    plot_frame = Instance(HBox)
    data_table = Instance(DataTable)

    # text = Instance(TextInput)

    excitation = Instance(Slider)
    emission = Instance(Slider)
    chrom_class_select = Instance(Select)
    chrom_class = String(default='AYG')

    plot = Instance(Plot)
    source = Instance(ColumnDataSource)
    pretext = Instance(PreText)

    def __init__(self, *args, **kwargs):
        super(FPDApp, self).__init__(*args, **kwargs)


    @classmethod
    def create(cls):
        obj = cls()

        obj.make_inputs()
        obj.source = ColumnDataSource(data=obj.get_data())
        obj.pretext = PreText(text="No items selected.", width=500)
        obj.data_table = DataTable(source=obj.source, columns=columns)
        obj.data_table.width = 1000
        obj.data_table.source = obj.source
        obj.make_plots()
        obj.set_children()

        return obj


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


    def get_data(self):
        selected = data[data['chromophore_class']==self.chrom_class]
        return selected


    def make_source(self):
        self.source.data = self.get_data().to_dict('list')


    def make_plots(self):
        print('CALL: make_plots')
        self.plot = self.scatter_plot()

    @property
    def selected_df(self):
        pandas_df = self.get_data()
        selected = self.source.selected
        if selected:
            pandas_df = pandas_df.iloc[selected, :]
        return pandas_df


    def scatter_plot(self):
        toolset = "pan,reset,resize,save,wheel_zoom,hover,select"

        plot = figure(title="A Scatter Plot", tools=toolset)
        plot.scatter('excitation_new', 'emission_new',
                source=self.source,
                plot_width=600, plot_height=600,
                radius=4, fill_alpha=0.6,
                fill_color='excitation_color_new',
                line_color='#000000',
                )
        plot.x_range = Range1d(start=min_excitation, end=max_excitation)
        plot.y_range = Range1d(start=min_emission, end=max_excitation)
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
        self.input_frame = VBoxForm(children=[
                                self.excitation,
                                self.emission,
                                self.chrom_class_select,
                            ])

        self.plot_frame = HBox(children=[self.plot])
        self.top_frame = HBox(children=[self.plot_frame, self.input_frame])
        self.table_frame = HBox(children=[self.data_table])
        self.main_frame = VBox(children=[self.top_frame, self.table_frame])
        self.children = [self.main_frame]

    def setup_events(self):
        super(FPDApp, self).setup_events()

        if self.source:
            self.source.on_change('selected', self, 'input_change')
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
        self.pretext.text = str(self.selected_df[:2])
        self.data_table.source = self.source

@bokeh_app.route("/bokeh/fpd/")
@object_page("fpd")
def make_object():
    app = FPDApp.create()
    return app

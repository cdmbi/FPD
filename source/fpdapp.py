#!/usr/bin/env python
'''Description'''

import sys
import os
import logging
logging.basicConfig(level=logging.DEBUG)

import pandas as pd
import numpy as np

from collections import OrderedDict
from bokeh.plotting import figure, curdoc
from bokeh.models import Plot, ColumnDataSource, Range1d, HoverTool
from bokeh.properties import Instance, String
from bokeh.server.app import bokeh_app
from bokeh.server.utils.plugins import object_page
from bokeh.models.widgets import (HBox, Slider, TextInput,
                                    VBox, VBoxForm, Select,
                                    PreText, DataTable, Button,
                                )
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
                        'doi',
                        ]].fillna('')

CHROMOPHORES = sorted(set(data['chromophore_class']))
CHROMOPHORES.insert(0, 'All')
xy_margin = 80
max_emission = max(data['emission_new']) + xy_margin
min_emission = min(data['emission_new']) - xy_margin
max_excitation = max(data['excitation_new']) + xy_margin
min_excitation = min(data['excitation_new']) - xy_margin

columns = [
    TableColumn(field='fpid', title='FPID'),
    TableColumn(field='chromophore_name', title='chromophore_name'),
    TableColumn(field='chromophore_class', title='chromophore_class'),
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

    # widget instances
    # TODO:: add a reset button
    min_excitation = Instance(Slider)
    max_excitation = Instance(Slider)
    min_emission = Instance(Slider)
    max_emission = Instance(Slider)
    chrom_class_select = Instance(Select)
    chrom_class = String(default='All')
    data_table = Instance(DataTable)
    button = Instance(Button)

    plot = Instance(Plot)
    source = Instance(ColumnDataSource)
    # pretext = Instance(PreText)


    def __init__(self, *args, **kwargs):
        super(FPDApp, self).__init__(*args, **kwargs)


    @classmethod
    def create(cls):
        obj = cls()

        # create input widgets only once
        obj.min_excitation = Slider(
                title="Min Excitation", name="min_excitation",
                value=min_excitation,
                start=min_excitation,
                end=max_excitation,
                )
        obj.max_excitation = Slider(
                title="Max Excitation", name="max_excitation",
                value=max_excitation,
                start=min_excitation,
                end=max_excitation,
                )
        obj.min_emission = Slider(
                title="Min Emission", name="min_emission",
                value=min_emission,
                start=min_emission,
                end=max_emission,
                )
        obj.max_emission = Slider(
                title="Max Emission", name="max_emission",
                value=max_emission,
                start=min_emission,
                end=max_emission,
                )

        obj.chrom_class_select = Select(
                name="Chromophore",
                value='All',
                options=CHROMOPHORES,
                )

        obj.button = Button(label="reset", type="primary")
        obj.button.on_click(obj.reset_sliders)

        obj.source = ColumnDataSource(data=data)
        obj.data_table = DataTable(source=obj.source, columns=[
            TableColumn(field='fpid', title='FPID'),
            TableColumn(field='chromophore_name', title='chromophore_name'),
            TableColumn(field='chromophore_class', title='chromophore_class'),
            TableColumn(field='protein_name', title='Protein name'),
            TableColumn(field='excitation_new', title='Excitation'),
            TableColumn(field='emission_new', title='Emission'),
            TableColumn(field='pdb_id', title='PDB ID'),
            TableColumn(field='genbank', title='Genbank ID'),
            TableColumn(field='mutation', title='Mutation'),
            TableColumn(field='quantum_yield', title='Quantum Yield'),
            TableColumn(field='pka', title='pka'),
            TableColumn(field='amino_acid_sequence', title='Sequence'),
        ])
        obj.data_table.width = 1200
        # obj.pretext = PreText(text='No selected items', width=400)

        obj.make_plots()
        obj.set_children()

        return obj

    def reset_sliders(self):
        self.min_excitation = Slider(
                title="Min Excitation", name="min_excitation",
                value=self.min_excitation.value,
                start=min_excitation,
                end=max_excitation,
                )
        self.max_excitation = Slider(
                title="Max Excitation", name="max_excitation",
                value=self.max_excitation.value,
                start=min_excitation,
                end=max_excitation,
                )
        self.min_emission = Slider(
                title="Min Emission", name="min_emission",
                value=self.min_emission.value,
                start=min_emission,
                end=max_emission,
                )
        self.max_emission = Slider(
                title="Max Emission", name="max_emission",
                value=self.max_emission.value,
                start=min_emission,
                end=max_emission,
                )


    def get_data(self):
        df = data

        df = df[df['excitation_new']>=self.min_excitation.value]
        df = df[df['excitation_new']<=self.max_excitation.value]
        df = df[df['emission_new']>=self.min_emission.value]
        df = df[df['emission_new']<=self.max_emission.value]

        if self.chrom_class == 'All':  # all chromophore classes
            return df
        else:
            df = df[df['chromophore_class']==self.chrom_class]

        return df


    def make_source(self):
        self.source.data = self.get_data().to_dict('list')


    def make_plots(self):
        # print('CALL: make_plots')
        self.plot = self.scatter_plot()

    @property
    def selected_df(self):
        df = data
        selected = self.source.selected
        if selected:
            df = df.iloc[selected, :]
        return df


    def scatter_plot(self):
        toolset = "pan,reset,resize,save,wheel_zoom,hover,box_select"

        plot = figure(tools=toolset)
        plot.scatter('excitation_new', 'emission_new',
                source=self.source,
                plot_width=500, plot_height=600,
                radius=4, fill_alpha=0.4,
                fill_color='excitation_color_new',
                line_color='#000000',
                ylabel='Emission',
                xlabel='Excitation',
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
                                self.min_excitation,
                                self.max_excitation,
                                self.min_emission,
                                self.max_emission,
                                self.button,
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

        if self.min_excitation:
            self.min_excitation.on_change('value', self, 'input_change')

        if self.max_excitation:
            self.max_excitation.on_change('value', self, 'input_change')

        if self.min_emission:
            self.min_emission.on_change('value', self, 'input_change')

        if self.max_emission:
            self.max_emission.on_change('value', self, 'input_change')

        if self.chrom_class_select:
            self.chrom_class_select.on_change(
                                'value', self, 'input_change')


    def input_change(self, obj, attrname, old, new):
        if obj == self.chrom_class_select:
            self.chrom_class = new

        if obj == self.min_excitation:
            self.min_excitation.value = new
            if self.min_excitation.value > self.max_excitation.value:
                self.min_excitation.value = self.max_excitation.value

        if obj == self.max_excitation:
            self.max_excitation.value = new
            if self.max_excitation.value < self.min_excitation.value:
                self.max_excitation.value = self.min_excitation.value

        if obj == self.min_emission:
            self.min_emission.value = new
            if self.min_emission.value > self.max_emission.value:
                self.min_emission.value = self.max_emission.value

        if obj == self.max_emission:
            self.max_emission.value = new
            if self.max_emission.value < self.min_emission.value:
                self.max_emission.value = self.min_emission.value

        self.make_source()
        # self.pretext.text = str(self.selected_df['doi'])
        # self.data_table.source = self.source
        self.reset_sliders()
        self.make_plots()
        self.set_children()
        curdoc().add(self)

@bokeh_app.route("/bokeh/fpd/")
@object_page("fpd")
def make_object():
    app = FPDApp.create()
    return app

var grid;
var columns = [
    {id: 'fpid', name: 'ID', field: 'fpid'},
    {id: 'emission_new', name: 'Emission', width: 100, field: 'emission_new', sortable: true},
    {id: 'excitation_new', name: 'Excitation', width: 100, field: 'excitation_new', sortable: true},
    {id: 'chromophore_class', name: 'Chromophore class', width: 100, field: 'chromophore_class'},
    {id: 'genbank', name: 'Genbank', width: 100, field: 'genbank'},
    {id: 'pdb_id', name: 'PDB', width: 100, field: 'pdb_id'},
    {id: 'pka', name: 'pka', width: 100, field: 'pka'},
    {id: 'quantum_yield', name: 'Quantum Yield', width: 100, field: 'quantum_yield'},
];

var options = {
    enableCellNavigation: true,
    enableColumnReorder: false
};

var curr_data;

var margin = 80, width = 800, height = 600;
var yslider_min, yslider_max, xslider_min, xslider_max;
var x_field = 'quantum_yield';
var y_field = 'pka';

function draw_circles(data) {

    var yslider_lo = $('#yslider').slider("option", "values")[0];
    var yslider_hi = $('#yslider').slider("option", "values")[1];
    var xslider_lo = $('#xslider').slider("option", "values")[0];
    var xslider_hi = $('#xslider').slider("option", "values")[1];

    function filter_y(d) {
        if (d[y_field] === '') {
            return false;
        } else {
            return (parseFloat(d[y_field]) >= yslider_lo && parseFloat(d[y_field]) <= yslider_hi);
        }
    }

    function filter_x(d) {
        if (d[x_field] === '') {
            return false;
        } else {
            return (parseFloat(d[x_field]) >= xslider_lo && parseFloat(d[x_field]) <= xslider_hi);
        }
    }

    d3.select('svg')
        .selectAll('circle')
        .remove();

    d3.select('svg')
        .selectAll('circle')
            .data(data.filter(function(d) {
                    if ($('#chromclass_sel').val() === 'All') {
                        return filter_y(d) && filter_x(d);
                    } else {
                        return (d.chromophore_class === $('#chromclass_sel').val())
                                    && filter_y(d) && filter_x(d);
                    }}))
            .enter()
            .append('circle')
            .attr('r', 8)

    curr_data = data.filter(function(d) {
            if ($('#chromclass_sel').val() === 'All') {
                return filter_y(d) && filter_x(d);
            } else {
                return (d.chromophore_class === $('#chromclass_sel').val())
                            && filter_y(d) && filter_x(d);
            }
        });

    grid.setData(curr_data);
    grid.invalidate();

    var x_extent = d3.extent(data, function(d) { return parseFloat(d[x_field]) });
    var x_scale = d3.scale.linear()
        .range([margin, width-margin])
        .domain(x_extent);

    var y_extent = d3.extent(data, function(d) { return parseFloat(d[y_field]) });
    var y_scale = d3.scale.linear()
        .range([height-margin, margin])
        .domain(y_extent);

    d3.selectAll('circle')
        .attr('cx', function(d){return x_scale(parseFloat(d[x_field]))})
        .attr('cy', function(d){return y_scale(parseFloat(d[y_field]))})
        .style('fill', function(d){return d.excitation_color_new})
        .style('opacity', 0.5)
        .style('stroke', 'black')
        .style('stroke-width', 1)

    d3.selectAll('circle')
        .on('mouseover', function(d) {
                d3.select(this)
                    .transition()
                    .attr('r', 16)
                    .style('opacity', 1)
                    .style('stroke-width', 2)

                var x_position = parseFloat(d3.select(this).attr('cx')) + 30;
                var y_position = parseFloat(d3.select(this).attr('cy')) - 30;

                d3.select('#tooltip').style('display', 'none');

                d3.select('#tooltip')
                    .style('left', x_position + 'px')
                    .style('top', y_position + 'px')
                    .select('#yvalue')
                    .text(d[y_field])

                d3.select('#tooltip')
                    .select('#xvalue')
                    .text(d[x_field])

                d3.select('#tooltip')
                    .select('#chromclass')
                    .text(d.chromophore_class);

                d3.select('#tooltip')
                    .select('#tooltip-ylabel')
                    .text(y_field +  " ")

                d3.select('#tooltip')
                    .select('#tooltip-xlabel')
                    .text(x_field + " ")

                d3.select('#tooltip')
                    .select('#genbank')
                        .attr('href', 'http://www.ncbi.nlm.nih.gov/nuccore/' + d.genbank)
                        .attr('target', '_blank')
                    .select('#genbank_link')
                        .text(d.genbank)

                d3.select('#tooltip')
                    .select('#uniprot')
                        .attr('href', 'http://www.uniprot.org/uniprot/' + d.uniprot_id)
                        .attr('target', '_blank')
                    .select('#uniprot_link')
                        .text(d.uniprot_id)

                d3.select('#tooltip')
                    .select('#species')
                    .text(d.species);

                d3.select('#tooltip').style('display', 'block');
                });

    d3.selectAll('circle')
        .on('mouseout', function(d) {
                d3.select(this)
                    .transition()
                    .attr('r', 8)
                    .style('opacity', 0.5)
                    .style('stroke-width', 1)
                });
}

function draw(data) {
    "use strict";

    d3.select('#mainplot')
        .append('svg')
            .attr('width', width)
            .attr('height', height);

    draw_circles(data);

    d3.select('svg')
        .on('click', function(d) {
                d3.select('#tooltip').style('display', 'none');
                })

    // add axes

    var x_extent = d3.extent(
            data, function(d) { return parseFloat(d[x_field]) }
            );

    var x_scale = d3.scale.linear()
        .domain(x_extent)
        .range([margin, width-margin]);

    var x_axis = d3.svg.axis()
        .scale(x_scale)

    var y_extent = d3.extent(
            data, function(d) { return parseFloat(d[y_field]) }
            );

    var y_scale = d3.scale.linear()
        .domain(y_extent)
        .range([height-margin, margin]);

    var y_axis = d3.svg.axis()
        .scale(y_scale)
        .orient('left');

    d3.select('svg')
        .append('g')
            .attr('class', 'x axis')
            .attr('transform', 'translate(0,' + (height-margin) + ')')
        .call(x_axis);

    d3.select('svg')
        .append('g')
            .attr('class', 'y axis')
            .attr('transform', 'translate(' + margin + ',0)')
        .call(y_axis);

    // add axis title
    d3.select('.x.axis')
        .append('text')
            .text(x_field)
            .attr('x', (width/2)-margin)
            .attr('y', margin / 1.5);

}

$(document).ready(function() {

    // create some main components
    d3.json("data/FPD-non-redundant-processed.json", function(error, data) {

        var chromophores = [];

        for (var i = 0; i < data.length; i++) {
            var obj = data[i];
            chromophores.push(obj['chromophore_class']);
        }
        chromophores = $.unique(chromophores);
        chromophores.sort();

        d3.select('#chromclass_sel')
            .selectAll('option')
            .data(chromophores)
            .enter()
            .append('option')
            .attr('value', function(d) { return d })
            .text(function(d) { return d})

        grid = new Slick.Grid('#datagrid', data, columns, options);
    });

    // TODO: create a function that will sets up sliders according to x and y variables.

    // need to refactor so that data is not reloaded again here.
    d3.json("data/FPD-non-redundant-processed.json", create_sliders);

    function create_sliders(data) {
        // code for setting up sliders go here.
        yrange_max = d3.max(data, function(d) {
                return parseFloat(d[y_field]);
            });
        yrange_min = d3.min(data, function(d) {
                return parseFloat(d[y_field]);
            });
        xrange_max = d3.max(data, function(d) {
                return parseFloat(d[x_field]);
            });
        xrange_min = d3.min(data, function(d) {
                return parseFloat(d[x_field]);
            });

        $('#yrange').text(y_field + ' ' + yrange_min + '-' + yrange_max);
        $('#xrange').text(x_field + ' ' + xrange_min + '-' + xrange_max);

        $('#yslider').slider({
            range: true,
            min: yrange_min,
            max: yrange_max,
            values: [yrange_min, yrange_max],
            slide: function(event, ui) {
                $('#yrange')
                    .text(y_field + ' ' + ui.values[0] + '-' + ui.values[1]);

                d3.select('#tooltip').classed('hidden', true);
                // TODO: should directly call draw_circles with data as a parameter.
                d3.json("data/FPD-non-redundant-processed.json", draw_circles);
                }
            });

        $('#xslider').slider({
            range: true,
            min: xrange_min,
            max: xrange_max,
            values: [xrange_min, xrange_max],
            slide: function(event, ui) {
                $('#xrange')
                    .text(x_field + ' ' + ui.values[0] + '-' + ui.values[1]);

                d3.select('#tooltip').classed('hidden', true);
                // TODO: should directly call draw_circles with data as a parameter.
                d3.json("data/FPD-non-redundant-processed.json", draw_circles);
                }
            });
    }

    $('#reset-btn').button().click(function(event) {
            window.location.reload(true);
            });


    $('#chromclass_sel').selectmenu().selectmenu("menuWidget").addClass('overflow');
    $('#chromclass_sel').selectmenu("option", "width", 200);
    $('#chromclass_sel').on("selectmenuchange",
            function(event, ui) {
                var chromclass = ui.item.value;
                d3.select('#tooltip').style('display', 'none');
                d3.json("data/FPD-non-redundant-processed.json", draw_circles);
            });

    $('#x_selector')
        .selectmenu()
        .on("selectmenuchange", function(event, ui) {
            x_field = ui.item.value;
            d3.json("data/FPD-non-redundant-processed.json", create_sliders);
            d3.json("data/FPD-non-redundant-processed.json", draw_circles);
        });
    $('#y_selector')
        .selectmenu()
        .on("selectmenuchange", function(event, ui) {
            y_field = ui.item.value;
            d3.json("data/FPD-non-redundant-processed.json", create_sliders);
            d3.json("data/FPD-non-redundant-processed.json", draw_circles);
        });

    d3.json("data/FPD-non-redundant-processed.json", draw);
});

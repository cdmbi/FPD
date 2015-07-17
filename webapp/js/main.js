var data, curr_data, table;

var margin = 80, width = 700, height = 600;
var yslider_min, yslider_max, xslider_min, xslider_max;
var x_field = 'emission_new';
var y_field = 'excitation_new';
var x_extent, x_scale, y_extent, y_scale;
var x_axis, y_axis;

function filter_data() {
    function filter_y(d) {
        if (parseFloat(d[y_field]) + 1 > 0) {
            return true;
        } else {
            return false;
        }
    }

    function filter_x(d) {
        if (parseFloat(d[x_field]) + 1 > 0) {
            return true;
        } else {
            return false;
        }
    }

    curr_data = data.filter(function(d) {
        return filter_y(d) && filter_x(d);
    });

    // grid.setData(curr_data);
    // grid.invalidate();
    console.log(data.length, curr_data.length);
}

function update_sliders_change() {

    var yslider_lo = $('#yslider').slider("option", "values")[0];
    var yslider_hi = $('#yslider').slider("option", "values")[1];
    var xslider_lo = $('#xslider').slider("option", "values")[0];
    var xslider_hi = $('#xslider').slider("option", "values")[1];

    function filter_y(d) {
        if (parseFloat(d[y_field]) + 1 > 0) {
            return (parseFloat(d[y_field]) >= yslider_lo && parseFloat(d[y_field]) <= yslider_hi);
        } else {
            return false;
        }
    }

    function filter_x(d) {
        if (parseFloat(d[x_field]) + 1 > 0) {
            return (parseFloat(d[x_field]) >= xslider_lo && parseFloat(d[x_field]) <= xslider_hi);
        } else {
            return false;
        }
    }

    curr_data = data.filter(function(d) {
        if ($('#chromclass_sel').val() === 'All') {
            return filter_y(d) && filter_x(d);
        } else {
            return (d.chromophore_class === $('#chromclass_sel').val())
                        && filter_y(d) && filter_x(d);
        }
    });

    // grid.setData(curr_data);
    // grid.invalidate();

}
function create_scales() {
    x_extent = d3.extent(curr_data, function(d) { return parseFloat(d[x_field]) });
    x_scale = d3.scale.linear().range([margin, width-margin]).domain(x_extent);

    y_extent = d3.extent(curr_data, function(d) { return parseFloat(d[y_field]) });
    y_scale = d3.scale.linear().range([height-margin, margin]).domain(y_extent);

    x_axis = d3.svg.axis()
        .scale(x_scale)
        .orient("bottom")

    y_axis = d3.svg.axis()
        .scale(y_scale)
        .orient("left");

    d3.select('.x.axis').remove();
    d3.select('.y.axis').remove();
    d3.select('.x.axis').select('text').remove();

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

// function update_scale(data) {
//     x_extent = d3.extent(data, function(d) { return parseFloat(d[x_field]) });
//     x_scale.range([margin, width-margin]).domain(x_extent);
// 
//     y_extent = d3.extent(data, function(d) { return parseFloat(d[y_field]) });
//     y_scale.range([height-margin, margin]).domain(y_extent);
// 
//     d3.select('svg')
//         .transition()
//         .duration(1000)
//         .call(x_axis);
// 
//     d3.select('svg')
//         .transition()
//         .duration(1000)
//         .call(y_axis);
// }

function draw_circles() {

    // remove existing circles
    d3.select('svg')
        .selectAll('circle')
        .remove();

    d3.select('svg')
        .selectAll('circle')
            .data(curr_data)
            .enter()
            .append('circle')
            .attr('r', 8)
            .style('fill', function(d){return d.excitation_color_new})
            .style('opacity', 0.5)
            .style('stroke', 'black')
            .style('stroke-width', 1)
            .attr('cx', function(d){return x_scale(parseFloat(d[x_field]))})
            .attr('cy', function(d){return y_scale(parseFloat(d[y_field]))})

    add_tooltips(curr_data);
}

function draw_circles_transition() {
    // remove existing circles
    d3.select('svg')
        .selectAll('circle')
        .remove();

    console.log('inside draw_circles_transition');
    console.log(x_field, y_field);
    d3.select('svg')
        .selectAll('circle')
            .data(curr_data)
            .enter()
            .append('circle')
            .attr('cx', function(d){return x_scale(parseFloat(d[x_field]))})
            .attr('cy', height-margin)
            .attr('r', 8)
            .style('fill', function(d){return d.excitation_color_new})
            .style('opacity', 0.5)
            .style('stroke', 'black')
            .style('stroke-width', 1)
            .transition()
            .duration(500)
            .attr('cx', function(d){return x_scale(parseFloat(d[x_field]))})
            .attr('cy', function(d){return y_scale(parseFloat(d[y_field]))})

    add_tooltips(curr_data);
}

function add_tooltips() {
    d3.selectAll('circle')
        .on('mouseover', function(d) {
                d3.select(this)
                    .transition()
                    .attr('r', 16)
                    .style('opacity', 1)
                    .style('stroke-width', 2)

                var x_position = parseFloat(d3.select(this).attr('cx'));
                var y_position = parseFloat(d3.select(this).attr('cy'));

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

    d3.select('svg')
        .on('click', function(d) {
                d3.select('#tooltip').style('display', 'none');
                })
}

$(document).ready(function() {

    // create some main components
    d3.json("data/FPD-non-redundant-processed.json", function(error, input_data) {
        data = input_data;

        d3.select('#mainplot')
            .append('svg')
                .attr('width', width)
                .attr('height', height);

        // add data grid for filtered data
        // grid = new Slick.Grid('#datagrid', data, columns, options);


        // filter data
        filter_data(data);

        // create data table
        create_table();

        // create selectors
        create_chrom_selector();
        create_xyselectors();

        // create sliders
        create_sliders();

        // create scales and axes
        create_scales();

        // add a reload button
        $('#reset-btn').button().click(function(event) {
                window.location.reload(true);
            });

        // draw initial circles for excitation vs emission
        d3.select('svg')
            .selectAll('circle')
                .data(curr_data)
                .enter()
                .append('circle')
                .attr('cx', function(d){return x_scale(parseFloat(d[x_field]))})
                .attr('cy', height-margin)
                .attr('r', 8)
                .style('fill', function(d){return d.excitation_color_new})
                .style('opacity', 0.5)
                .style('stroke', 'black')
                .style('stroke-width', 1)
                .transition()
                .duration(500)
                .attr('cx', function(d){return x_scale(parseFloat(d[x_field]))})
                .attr('cy', function(d){return y_scale(parseFloat(d[y_field]))})

        add_tooltips();

    });

    function create_chrom_selector() {
        d3.select('#chromclass_sel')
            .selectAll('option')
            .remove();

        var chromophores = [];

        for (var i = 0; i < curr_data.length; i++) {
            var obj = curr_data[i];
            chromophores.push(obj['chromophore_class']);
        }
        chromophores = $.unique(chromophores);
        chromophores.sort();
        chromophores.splice(0, 0, 'All');

        d3.select('#chromclass_sel')
            .selectAll('option')
            .data(chromophores)
            .enter()
            .append('option')
            .attr('value', function(d) { return d })
            .text(function(d) { return d})

        $('#chromclass_sel').selectmenu().selectmenu("menuWidget").addClass('overflow');
        $('#chromclass_sel').selectmenu("option", "width", 200);
        $('#chromclass_sel').on("selectmenuchange",
                function(event, ui) {
                    var chromclass = ui.item.value;
                    d3.select('#tooltip').style('display', 'none');
                    update_sliders_change(data);
                    draw_circles();
                    table.clear().rows.add(curr_data).draw();
                });
    }

    function create_xyselectors() {
        $('#x_selector')
            .selectmenu()
            .on("selectmenuchange", function(event, ui) {
                x_field = ui.item.value;
                filter_data();
                create_scales();
                create_chrom_selector();
                create_sliders();
                draw_circles_transition();
                table.clear().rows.add(curr_data).draw();
            });

        $('#y_selector')
            .selectmenu()
            .on("selectmenuchange", function(event, ui) {
                y_field = ui.item.value;
                filter_data();
                create_scales();
                create_chrom_selector();
                create_sliders();
                draw_circles_transition();
                table.clear().rows.add(curr_data).draw();
            });
    }

    function create_sliders() {
        // code for setting up sliders go here.
        yrange_max = d3.max(curr_data, function(d) {
                return parseFloat(d[y_field]);
            });
        yrange_min = d3.min(curr_data, function(d) {
                return parseFloat(d[y_field]);
            });
        xrange_max = d3.max(curr_data, function(d) {
                return parseFloat(d[x_field]);
            });
        xrange_min = d3.min(curr_data, function(d) {
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
                update_sliders_change();
                draw_circles();
                table.clear().rows.add(curr_data).draw();
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
                update_sliders_change();
                draw_circles();
                table.clear().rows.add(curr_data).draw();
                }
            });
    }

    function create_table() {
        console.log('num rows:', curr_data.length);
        table = $('#data_table').DataTable({ data: data,
                                   columns: [
                                       {data: 'fpid'},
                                       {data: 'emission_new'},
                                       {data: 'excitation_new'},
                                       {data: 'chromophore_class'},
                                       {data: 'pka'},
                                       {data: 'uniprot_id'},
                                       {data: 'pdb_id'},
                                       {data: 'genbank'},
                                       {data: 'quantum_yield'}
                                   ]});
    }
});

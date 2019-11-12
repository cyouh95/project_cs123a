$(function() {

    // Tab selection
    $('.button').on('click', function() {
        var sel = $(this).data('tab');
        $('.tab, .button').removeClass('active');
        $('#' + sel).addClass('active');
        $(this).addClass('active');
    });

    // Get data
    try {
        create_dendrogram(JSON.parse(data));
    } catch(e) {
        create_dendrogram();
    }

    // Create dendrogram
    function create_dendrogram(data) {
        var width = 800;
        var height = 400;

        var svg = d3.select('#dendrogram')
            .append('svg')
            .attr('width', width)
            .attr('height', height)
            .append('g');

        // Return if error in data
        if (typeof data === 'undefined') {
            svg.append('text')
                .attr('transform', 'translate(' + width / 2 + ', ' + height / 2 + ')')
                .classed('unavailable-text', true)
                .text('Invalid data.');

            svg.append('text')
                .attr('transform', 'translate(' + width / 2 + ', ' + height * 0.65 + ')')
                .classed('unavailable-icon', true)
                .text('\uf080');

            return;
        }

        // Define scale
        var maxDistance = data.distance;

        var xScale = d3.scaleLinear()
            .domain([0, maxDistance])
            .range([width-100, 0]);

        var xAxisGenerator = d3.axisBottom(xScale)
            .tickSize(4);

        // Create the cluster layout
        var cluster = d3.cluster()
            .size([height - 20, width - 100]);

        // Give the data to this cluster layout
        var root = d3.hierarchy(data, function (d) {
            return d.children;
        });
        cluster(root);

        // Add the links between nodes
        svg.selectAll('path')
            .data(root.descendants().slice(1))
            .enter()
            .append('path')
            .attr('d', function (d) {
                return 'M' + xScale(d.data.distance) + ',' + d.x
                    + 'L' + xScale(d.parent.data.distance) + ',' + d.x
                    + ' ' + xScale(d.parent.data.distance) + ',' + d.parent.x;
            })
            .style('fill', 'none')
            .attr('stroke', '#ccc');

        // Create nodes
        var g = svg.selectAll('g')
            .data(root.descendants())
            .enter()
            .append('g')
            .attr('transform', function (d) {
                return 'translate(' + xScale(d.data.distance) + ',' + d.x + ')'
            });

        // Add circles
        g.filter(function(d) { return d.data.distance === 0; })
            .append('circle')
            .attr('r', 7);

        // Add text
        g.append('text')
            .attr('dy', '0.37em')
            .attr('x', function(d) { return d.data.distance === 0 ? 10 : 2; })
            .text(function(d) { return d.data.distance === 0 ? d.data.name : Math.round(d.data.distance * 1000) / 1000; });

        // Add axis
        svg.append('g')
            .classed('axis', true)
            .attr('transform', 'translate(0,' + 370 + ')')
            .call(xAxisGenerator);
    }

});

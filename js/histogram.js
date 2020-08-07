function drawHistogram(binCount, dtype) {

    d3.json('http://localhost:5000/data/' + dtype + '/feature/histogram', function (result) {
        result = result.x;

      d3.select('#piechart-heading').text('Histogram of H1B Petitions');

        console.log(result);
        var margin = {top: 10, right: 30, bottom: 60, left: 100};

        var width = 400 - margin.left - margin.right, height = 400 - margin.top - margin.bottom;


        var svg = d3.select("#piechart")
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform",
                "translate(" + margin.left + "," + (margin.top) + ")");


        console.log('inside make');

        var x = d3.scaleLinear()
            .domain([d3.min(result, function (d) {
                return Number(d)
            }),
                d3.max(result, function (d) {
                    return Number(d)
                })])
            .range([0, width]);

        svg.append("g")
            .attr("transform", "translate(0," + (height - 25) + ")")
            .call(d3.axisBottom(x))
            .selectAll("text")
            .style("text-anchor", "end")
            .attr("dx", "-.7em")
            .attr("dy", ".14em")
            .attr("transform", function (d) {
                return "rotate(-70)"
            });


        svg.append("text")
            .attr("transform", "translate(" + (width / 2) + " ," + (height + margin.bottom) + ")")
            .style("text-anchor", "middle")
            .text('Years')
            .attr("font-family", "Saira Condensed");

        // Add the text label for the Y axis
        svg.append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 0 - margin.left)
            .attr("x", 0 - (height / 2))
            .attr("dy", "1em")
            .style("text-anchor", "middle")
            .text("H1B Petitions")
            .attr("font-family", "Saira Condensed");
        var yaxis = svg.append("g");

        function update(binCount) {

            var histogram = d3.histogram()
                .value(function (d) {
                    return d;
                })
                .domain(x.domain())
                .thresholds(x.ticks(+binCount));
            var bins = histogram(result);

            console.log(bins);
            var y = d3.scaleLinear()
                .range([height - 25, 0]);
            y.domain([d3.min(bins, function (d) {
                return Number(d)
            }), d3.max(bins, function (d) {
                return d.length;
            })]);


            yaxis.transition().duration(1000).call(d3.axisLeft(y));

            // append the bar rectangles to the svg element
            var u = svg.selectAll("rect")
                .data(bins);

            u.enter()
                .append("rect")
                .merge(u)
                .transition().duration(1000)
                .attr("x", 1)
                .attr("transform", function (d) {
                    return "translate(" + x(d.x0) + "," + (y(d.length) - 25) + ")";
                })
                .attr("width", function (d) {
                    return x(d.x1) - x(d.x0);
                })
                .attr("height", function (d) {
                    return height - y(d.length);
                })
                .style("stroke", strokeColor)
                .style("fill", barColor)
                .style("stroke-width", strokeBorder);

            u.exit().remove();

        }
        update(30);
        var data = [0, 15, 30, 50, 70, 85, 100];

        var sliderValue;

        var slider = d3Slider.sliderHorizontal()
            .domain(d3.extent(data))
            .width(400)
            .tickFormat(d3.format('d'))
            .ticks(5)
            .default(30)
            .on('onchange', val => {
                sliderValue = d3.format('d')(val);
                //d3.select("svg").remove();
                update(sliderValue);
            });


        var g = d3.select("#slide2").append("svg")
            .attr("width", 400)
            .attr("height", 100)
            .append("g")
            .style("top", "10px")
            .style("left", "20px")
            .attr("transform", "translate(30,30)");

        console.log('slider should be invoked here');
        g.call(slider);

    });

}

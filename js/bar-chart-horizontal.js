var barChartsvg, barChartPresent, barChartxAxis, barChartyAxis, bhChosenValue;

async function drawHorizontalBarChart(tab, dtype, key, value) {
    console.log(value);
    let response = await fetch('http://localhost:5000/data/' + dtype + '/feature/' + tab + '/employer?' + key + '=' + value+'&syear='+syear+'&eyear='+eyear);
    let result = await response.json();


    var data = dataConversionHorizontal(result);
    console.log(data);
    var label, xlabel;
    if (tab === 'petitions'){
        label = 'Petitions';
        xlabel = 'H1B Petitions';
    }
    else if (tab === 'wages') {
        label = 'Wages';
        xlabel = 'Wages (in x1000$)'
    }



    var margin = {top: 20, right: 30, bottom: 60, left: 150};

    if (tab === 'wages')
        margin.left += 40;
    else
        margin.left += 10;

    var width = 400 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

// set the ranges
    var y = d3.scaleBand()
        .range([height, 0])
        .padding(0.1);

    var x = d3.scaleLinear()
        .range([0, width]);


    if (!barChartPresent) {
        barChartsvg = d3.select("#piechart").append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform",
                "translate(" + margin.left + "," + margin.top + ")");
        barChartxAxis = barChartsvg.append("g")
            .attr("transform", "translate(0," + height + ")");

        barChartyAxis = barChartsvg.append("g");

    }

    data.forEach(function (d) {
        d.COUNT = +d.COUNT;
    });

    x.domain([0, d3.max(data, function (d) {
        return d.COUNT;
    })]);

    barChartxAxis.call(d3.axisBottom(x))
        .selectAll("text")
        .attr("y", 0)
        .attr("x", 9)
        .attr("dy", ".35em")
        .attr("transform", "rotate(45)")
        .style("text-anchor", "start")
        .style("font-family", "sans-serif");

    y.domain(data.map(function (d) {
        return d.EMPLOYER_NAME;
    }));
    barChartyAxis.transition().duration(1000).call(d3.axisLeft(y));


    if (!barChartPresent) {
        barChartsvg.append("g")
            .attr("class", "axis axis--x");

        barChartsvg.append("g")
            .attr("class", "axis axis--y");

        barChartsvg.append("text")
            .attr("transform", "translate(" + (width / 2) + " ," + (height + margin.bottom - 5) + ")")
            .style("text-anchor", "middle")
            .style("font-family", "sans-serif")
            .text(xlabel);

        barChartsvg.append("text")
            .attr("transform", "rotate(-90)")
            .attr("x", 0 - (height / 2 - 10))
            .attr("y", 0 - margin.left - 8)
            .attr("dy", "1.4em")
            .attr("text-anchor", "middle")
            .style("font-family", "Playfair")
            .text('Employers');
        barChartPresent = true;
    }


    var u = barChartsvg.selectAll(".bar")
        .data(data);
    var s = u.enter().append("rect")
        .merge(u)
        .attr("class", "bar")
        .style("fill", barColor)
        .style("stroke", strokeColor)
        .style("stroke-width", strokeBorder)
        //.attr("x", function(d) { return x(d.sales); })
        .attr("width", function (d) {
            return x(d.COUNT);
        })
        .attr("y", function (d) {
            return y(d.EMPLOYER_NAME);
        })
        .attr("height", y.bandwidth());
    s.transition().duration(1000);
    s.on("mouseover", function (d, index) {
        d3.select(this).style("fill", hoverColor);

    })
    .on("mouseout", function (d, index) {
        if(d.EMPLOYER_NAME != bhChosenValue) {
            d3.select(this).style("fill", barColor);
        }

    })
    .on("click", function(d, index){
        bhChosenValue = d.EMPLOYER_NAME;
        console.log(bhChosenValue);
        drawBarChart(tab, dtype,'employer', d.EMPLOYER_NAME);
        drawGeoMap(tab, dtype, 'employer', d.EMPLOYER_NAME);
        d3.selectAll(".bar").style("fill", barColor);
        d3.select(this).style("fill", hoverColor);
    });


    u.exit().remove();
    d3.select('#piechart-heading').text(label + ' vs Employers');

}


function dataConversionHorizontal(arr) {
    var result = [];
    for (var i = 0; i < arr['EMPLOYER_NAME'].length; i++) {
        result.push({'EMPLOYER_NAME': arr['EMPLOYER_NAME'][i], 'COUNT': arr['COUNT'][i]});
    }
    return result;
}
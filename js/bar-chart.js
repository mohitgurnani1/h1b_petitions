var bcg, bcPresent, bcxAxis, bcyAxis, bcChosen;

async function drawBarChart(tab, dtype, key, value) {
    console.log("Inside Bar Chart"+value);
    let response = await fetch('http://localhost:5000/data/' + dtype + '/feature/' + tab + '/job?' + key + '=' + value+'&syear='+syear+'&eyear='+eyear);
    let result = await response.json();

    var data = result;
    console.log(data);
    var label, xlabel;

    if (tab === 'petitions') {
        label = 'Petitions';
        xlabel = 'H1B Petitions';
    }
    else if (tab === 'wages') {
        label = 'Wages';
        xlabel = 'Wages in (x1000)$'
    }

    var margin = {top: 10, right: 30, bottom: 120, left: 50};
    if (tab === 'wages')
        margin.left += 20;

    var width = 400 - margin.left - margin.right, height = 400 - margin.top - margin.bottom;
    var x = d3.scaleBand().padding(0.3), y = d3.scaleLinear();
    x.domain(data['Job Title']);
    y.domain([0, d3.max(data[label])]);

    if (!bcPresent) {
        var svg = d3.select("#barchart")
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom);

        bcg = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");
        bcg.append("g")
            .attr("class", "axis axis--x");

        bcg.append("g")
            .attr("class", "axis axis--y");

        bcg.append("text")
            .attr("transform", "translate(" + (width / 2) + " ," + (height + margin.bottom) + ")")
            .style("text-anchor", "middle")
            .style("font-family", "sans-serif")
            .text("Job Titles");
        var xlabel;
        if (tab === 'petitions')
            xlabel = 'Petitions (in x 1000s)';
        else if (tab === 'wages')
            xlabel = 'Wages (in x 1000$)';

        bcg.append("text")
            .attr("transform", "rotate(-90)")
            .attr("x", 0 - (height / 2))
            .attr("y", 0 - margin.left - 8)
            .attr("dy", "1.4em")
            .attr("text-anchor", "middle")
            .style("font-family", "Playfair")
            .text(xlabel);
        var bounds = svg.node().getBoundingClientRect(),
            width = bounds.width - margin.left - margin.right,
            height = bounds.height - margin.top - margin.bottom;


    }


    x.rangeRound([0, width]);
    y.rangeRound([height, 0]);

    if (!bcPresent) {
        bcxAxis = bcg.select(".axis--x")
            .attr("transform", "translate(0," + height + ")");
        bcyAxis = bcg.select(".axis--y");
        bcPresent = true;
    }

    bcxAxis.call(d3.axisBottom(x))
        .selectAll("text")
        .attr("y", 0)
        .attr("x", 9)
        .attr("dy", ".35em")
        .attr("transform", "rotate(45)")
        .style("text-anchor", "start")
        .style("font-family", "sans-serif");


    bcyAxis.transition().duration(1000).call(d3.axisLeft(y));

    var convertedData = dataConversion(data, label);
    console.log(convertedData);
    var bars = bcg.selectAll(".bar")
        .data(convertedData);

    var s = bars
        .enter().append("rect")
        .merge(bars)
        .attr("class", "bar")
        .attr("x", function (d) {
            //console.log(d);
            return x(d['Job Title']);
        })
        .attr("y", function (d) {
            //console.log(d);
            return y(d[label]);
        })
        .attr("width", x.bandwidth())
        .attr("height", function (d) {
            return height - y(d[label]);
        })
        .style("fill", barColor)
        .style("stroke", strokeColor)
        .style("stroke-width", strokeBorder);

    s.transition().duration(1000);
    s.on("mouseover", function (d, index) {
        d3.select(this).style("fill", hoverColor);
    })
    .on("mouseout", function (d, index) {
            if(d['Job Title'] != bcChosen){
                d3.select(this).style("fill", barColor);
            }
        })
    .on("click", function(d, index){
        console.log(d['Job Title']);
        bcChosen = d['Job Title'];
        drawHorizontalBarChart(tab, dtype,'job', d['Job Title']);
        drawGeoMap(tab, dtype, 'job', d['Job Title']);
        d3.selectAll(".bar").style("fill", barColor);
        d3.select(this).style("fill", hoverColor);
    });
    bars.exit().remove();
    d3.select('#barchart-heading').text(label + ' vs Job Titles');

}


function dataConversion(arr, label) {
    var result = [];
    console.log('inside data conversion');
    console.log(label);
    for (var i = 0; i < arr['Job Title'].length; i++) {
        temp = {};
        temp['Job Title'] = arr['Job Title'][i];
        temp[label] = arr[label][i];
        result.push(temp);
    }
    return result;
}
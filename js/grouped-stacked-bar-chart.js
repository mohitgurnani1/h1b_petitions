function drawGroupedStackedBarChart(tab, dtype, html, feature) {
    var label = 'Petitions Success Ratio';
    var feat;

    if (feature == 'petitions')
        feat = 'Job Titles';
    else
        feat = 'Employers';

    d3.select(html+'-heading').text(label + ' vs '+ feat);

    var margin = {top: 10, right: 30, bottom: 120, left: 50};

    var width = 400 - margin.left - margin.right, height = 400 - margin.top - margin.bottom;
    var svg = d3.select(html)
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");

    
    d3.csv("http://localhost:5000/data/" + dtype + "/feature/" + feature + "/jobstacked?" + Math.floor(Math.random() * 1000), function(data) {
        
        var groups;

        if (feature == 'petitions')
            groups = d3.map(data, function(d){return(d.JOB_TITLE)}).keys();
        else
            groups = d3.map(data, function(d){return(d.EMPLOYER_NAME)}).keys();

        console.log('inside groupstacked with feature'+feature)
        console.log("data: ", data);
        console.log("groups: ", groups);

        var subgroups = data.columns.slice(1);
        console.log("subgroups: ", subgroups);

        // Adding the X axis
        var x = d3.scaleBand()
            .domain(groups)
            .range([0, width])
            .padding([0.2])
        svg.append("g")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x).tickSizeOuter(0))
            .selectAll("text")
            .attr("y", 0)
            .attr("x", 9)
            .attr("dy", ".35em")
            .attr("transform", "rotate(45)")
            .style("text-anchor", "start")
            .style("font-family", "sans-serif");

        // Adding the Y axis
        var y = d3.scaleLinear()
            .domain([0, 100])
            .range([ height, 0 ]);
        svg.append("g")
            .call(d3.axisLeft(y));

        var color = d3.scaleOrdinal()
            .domain(subgroups)
            .range([barColor,'#F1948A'])
        
        var stackedData = d3.stack()
            .keys(subgroups)(data)

        console.log("stackData", stackedData)

        // Show the bars
        svg.append("g")
            .selectAll("g")
            .data(stackedData)
            .enter().append("g")
            .attr("fill", function(d) { return color(d.key); })
            .selectAll("rect")
            .data(function(d) { return d; })
            .enter().append("rect")
            .attr("x", function(d) {
                if(feature  == 'petitions')
                    return x(d.data.JOB_TITLE);
                else
                    return x(d.data.EMPLOYER_NAME);
            })
            .attr("y", function(d) { return y(d[1]); })
            .attr("height", function(d) { return y(d[0]) - y(d[1]); })
            .attr("width", x.bandwidth())
    });

}



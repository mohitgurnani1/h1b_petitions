function drawHorizontalBarChart(tab, dtype) {
    d3.json('http://localhost:5000/data/' + dtype + '/feature/' + tab + '/employer', function (result) {
    var data = dataConversionHorizontal(result);
    console.log(data);
    var label;

    if (tab === 'petitions')
        label = 'Petitions';
    else if(tab === 'wages')
        label = 'Wages';


    d3.select('#piechart-heading').text(label + ' vs Employers');

    var margin = {top: 20, right: 20, bottom: 60, left: 150};

    if(tab === 'wages')
        margin.left += 20;

    var  width = 400 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

    // set the ranges
    var y = d3.scaleBand()
              .range([height, 0])
              .padding(0.1);

    var x = d3.scaleLinear()
              .range([0, width]);

    // append the svg object to the body of the page
    // append a 'group' element to 'svg'
    // moves the 'group' element to the top left margin
    var svg = d3.select("#piechart").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");

      // format the data
      data.forEach(function(d) {
        d.COUNT = +d.COUNT;
      });

      // Scale the range of the data in the domains
      x.domain([0, d3.max(data, function(d){ return d.COUNT; })])
      y.domain(data.map(function(d) { return d.EMPLOYER_NAME; }));
      //y.domain([0, d3.max(data, function(d) { return d.sales; })]);

         svg.append("g")
            .attr("class", "axis axis--x");

        svg.append("g")
            .attr("class", "axis axis--y");

        svg.append("text")
            .attr("transform", "translate(" + (width / 2) + " ," + (height + margin.bottom) + ")")
            .style("text-anchor", "middle")
            .style("font-family", "sans-serif")
            .text(label);


            svg.append("text")
            .attr("transform", "rotate(-90)")
            .attr("x", 0 - (height / 2))
            .attr("y", 0 - margin.left - 8)
            .attr("dy", "1.4em")
            .attr("text-anchor", "middle")
            .style("font-family", "Playfair")
            .text('Employers');


      // append the rectangles for the bar chart
      svg.selectAll(".bar")
          .data(data)
        .enter().append("rect")
          .attr("class", "bar")
          .style("fill", barColor)
          .style("stroke", strokeColor)
          .style("stroke-width", strokeBorder)
      //.attr("x", function(d) { return x(d.sales); })
          .attr("width", function(d) {return x(d.COUNT); } )
          .attr("y", function(d) { return y(d.EMPLOYER_NAME); })
          .attr("height", y.bandwidth())
          .on("mouseenter", mouseoverbar)
          .on("mouseleave", function (d, index) {
                d3.select(this).style("fill", barColor);
            });


      // add the x Axis
      svg.append("g")
          .attr("transform", "translate(0," + height + ")")
          .call(d3.axisBottom(x))
         .selectAll("text")
            .attr("y", 0)
            .attr("x", 9)
            .attr("dy", ".35em")
            .attr("transform", "rotate(45)")
            .style("text-anchor", "start")
            .style("font-family", "sans-serif");

      // add the y Axis
      svg.append("g")
          .call(d3.axisLeft(y));
        });
}




function dataConversionHorizontal(arr) {
    var result = [];
    for(var i = 0; i < arr['EMPLOYER_NAME'].length; i++){
      result.push({'EMPLOYER_NAME':arr['EMPLOYER_NAME'][i], 'COUNT':arr['COUNT'][i]});
    }
    return result;
}
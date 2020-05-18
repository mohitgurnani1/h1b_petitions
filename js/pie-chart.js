function drawPieChart(tab, dtype) {
    d3.json('http://localhost:5000/data/' + dtype + '/feature/' + tab + '/piechart', function (result) {
    var data = dataConversionPie(result)
    d3.select('#piechart-heading').text('Petitions vs Employers');

            // set the dimensions and margins of the graph
    var width = 450
        height = 450

    // The radius of the pieplot is half the width or half the height (smallest one). I subtract a bit of margin.
    var radius = Math.min(width, height) / 2

    // append the svg object to the div called 'my_dataviz'
    var svg = d3.select("#piechart")
      .append("svg")
        .attr("width", width)
        .attr("height", height)
      .append("g")
        .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

    var arc = d3.arc()
          .innerRadius(0)
          .outerRadius(radius - 10);
    var label_arc = d3.arc()
          .innerRadius(radius - 40)
          .outerRadius(radius - 40);

    // create 2 data_set

    // set the color scale
    var color = d3.scaleOrdinal()
      .domain(result['EMPLOYER_NAME'])
      .range(d3.schemeDark2);

    // // A function that create / update the plot for a given variable:
    //
    //   // Compute the position of each group on the pie:
      var pie = d3.pie()
        .value(function(d) {return d.value; })
        .sort(function(a, b) { console.log(a) ; return d3.ascending(a.value, b.value);} ) // This make sure that group order remains the same in the pie chart
      var data_ready = pie(d3.entries(data))

     var g = svg.selectAll(".arc")
      .data(data_ready)
     .enter().append("g")
      .attr("class", "arc");

      g.append("path")
          .attr("d", arc)
          .style("fill", function(d) { return color(d.data.key); });

      g.append("text")
          .attr("transform", function(d) { return "translate(" + label_arc.centroid(d) + ")"; })
          .attr("dy", ".35em")
          .text(function(d) {
              console.log(d.data.key);
              return d.data.key; });
          // map to data
    //   var u = svg.selectAll(".arc")
    //     .data(data_ready).enter()
    //     .append('g')
    //     .attr("class", "arc")
    //     .append("path")
    //     .attr('d', arc
    //     )
    //     .attr('fill', function(d){ return(color(d.data.key)) })
    //     .attr("stroke", "white")
    //     .style("stroke-width", "2px")
    //     .style("opacity", 1)
    //     .append("text")
    //     .attr("transform", function(d) {                    //set the label's origin to the center of the arc
    //              return "translate(" + label_arc.centroid(d) + ")";        //this gives us a pair of coordinates like [50, 50]
    //          })
    //     .attr("text-anchor", "middle")
    // //    .attr("dy", ".35em")
    //     .text(function(d) {
    //          console.log(d.data.key);
    //          return d.data.key; });

    });
}


function dataConversionPie(arr) {
    var result = {};
    for(var i = 0; i < arr['EMPLOYER_NAME'].length; i++){
      result[arr['EMPLOYER_NAME'][i]]=arr['CASE_STATUS'][i];
    } 
    return result;
}
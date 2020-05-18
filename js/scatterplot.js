function drawScatterPlot(gtype, dtype, html){
    d3.json('http://localhost:5000/data/' + dtype + '/feature/' + gtype, function (result) {

    console.log(result);
    var label;
    if (gtype === 'mds')
        label = 'mds';
    else
        label = 'pca';

    d3.select(html+'-heading').text('PCA Scatterplot');

    var margin = {top: 10, right: 30, bottom: 120, left: 50};
    var width = 500 - margin.left - margin.right, height = 500 - margin.top - margin.bottom;

      var svg = d3.select(html)
      .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");

        var x = d3.scaleLinear()
          .domain([d3.min(result.x1) - 1, d3.max(result.x1) + 1])
          .range([ 0, width ]);
        svg.append("g")
           .attr("transform", "translate(0," + (height ) + ")")
          .call(d3.axisBottom(x));
        // Add Y axis
        var y = d3.scaleLinear()
          .domain([d3.min(result.x2) - 1, d3.max(result.x2) + 1])
          .range([ height - 25, 0]);
          svg.append("g")
            .call(d3.axisLeft(y));
        // Add dots

        var tag1 = 'Principal Component 1', tag2 = 'Principal Component 2';
        if(gtype==='mds'){
            tag1 = 'MDS Component 1';
            tag2 = 'MDS Component 2';
        }
            svg.append("text")
           .attr("transform", "translate(" + (width / 2) + " ," + (height + margin.bottom - 20) + ")")
           .style("text-anchor", "middle")
           .text(tag1)
           .attr("font-family", "Saira Condensed");


        svg.append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 0 - margin.left + 10)
            .attr("x",0 - (height / 2))
            .attr("dy", "1em")
            .style("text-anchor", "middle")
            .text(tag2)
            .attr("font-family", "Saira Condensed");

        scatter_data = convert_data_scatterplot(result);
        drawLegendScatterplot(result.cluster, svg);
        color_arr = {0 : "69b3a2", 1: "30B33A", 2:"B32A14", 3:"DE95AD"};


        console.log(scatter_data);
        svg.append("g").selectAll(".dot")
          .data(scatter_data)
          .enter()
          .append("circle")
              .attr("class", "dot")
            .attr("cx", function (d) {return x(d[0]); } )
            .attr("cy", function (d) { return y(d[1]); } )
            .attr("r", 3)
            .style("fill", function(d){ return color_arr[d[2]]; })

});
}
function drawLegendScatterplot(cluster, svg){
    var uniq_Arr = cluster.filter(uniq)
    console.log(uniq_Arr)
    if (uniq_Arr.length > 1)
    {
        var legend = [{"color" : "#69b3a2", "label" : "Cluster 1"}, {"color" : "#30B33A", "label" : "Cluster 2"}, {"color" : "#B32A14", "label" : "Cluster 3"}, {"color" : "#DE95AD", "label" : "Cluster 4"}];
        var margin_legend = 10;

        svg.selectAll("g.legend").data(legend).enter().append("g")
        .attr("class", "legend").attr("transform", function(d,i) {
            return "translate(" + margin_legend + "," + (margin_legend + i*20) + ")";
        }).each(function(d, i) {
            d3.select(this).append("rect").attr("width", 30).attr("height", 15)
            .attr("fill", d.color);
            d3.select(this).append("text").attr("text-anchor", "start")
            .attr("x", 30+10).attr("y", 15/2).attr("dy", "0.35em")
            .text(d.label);
        });
    }

}
var uniq = function onlyUnique(value, index, self) {
    return self.indexOf(value) === index;
}

function convert_data_scatterplot(result) {
  var scatter_data = [];
  for ( var i = 0; i < result.x1.length; i++ ) {
          scatter_data.push([result.x1[i], result.x2[i], result.cluster[i]]);
  }
  return scatter_data;
}

var geoChoosenValue, geosvg, geoPresent, geoLegend, geoyAxis;

function drawGeoMap(tab, dtype, key, value) {
    var width = 500;
    var height = 440;
    var label;

    if (tab === 'petitions')
        label = 'H1B Petitions';
    else if(tab === 'wages')
        label = 'Wages';
    else if(tab === 'petitions-success-ratio')
        label = 'H1B Petitions Success Ratio';

// D3 Projection
    var projection = d3.geoAlbersUsa()
        .translate([width / 2, height / 2])    // translate to center of screen
        .scale([650]);          // scale things down so see entire US

// Define path generator
    var path = d3.geoPath()               // path generator that will convert GeoJSON to SVG paths
        .projection(projection);  // tell path generator to use albersUsa projection

    var color;

    if(tab === 'petitions-success-ratio')
        color = d3.scaleLinear()
        .range(["rgb(84,36,55)", "rgb(217,91,67)", "rgb(69,173,168)"]);
    else
            color = d3.scaleLinear()
        .range(["rgb(84,36,55)", "rgb(217,91,67)", "rgb(69,173,168)", "rgb(213,222,217)" ]);


    var legendText;

    if (tab === 'petitions' && geoPresent)
        legendText = ["H1B Petitions > 1500", "H1B Petitions > 500", "H1B Petitions > 100", "H1B Petitions < 100"];
    else if(tab == 'petitions')
        legendText = ["H1B Petitions > 200000", "H1B Petitions > 90000", "H1B Petitions > 20000", "H1B Petitions < 20000"];
    else if(tab === 'wages')
        legendText = ["Average Wages > 180k$", "Average Wages > 140k$", "Average Wages > 100k$", "Average Wages < 100k$"];
    else if(tab === 'petitions-success-ratio')
        legendText = ["H1B Petitions Success Ratio > 88%", "H1B Petitions Success Ratio > 80%", "H1B Petitions Success Ratio < 80%"];

    if(!geoPresent) {
         geosvg = d3.select("#geomap")
            .append("svg")
            .attr("width", width)
            .attr("height", height);
    }

// Load in my states data!

    var url;
    if(tab === 'petitions-success-ratio')
        url = "http://localhost:5000/data/" + dtype + '/feature/geomap/jobstacked?random='+ Math.floor(Math.random() * 1000);
    else
        url = "http://localhost:5000/data/" + dtype + '/feature/' + tab + "/geomap?"+key+"=" +value+"&syear="+syear+"&eyear="+eyear+"&random="+ Math.floor(Math.random() * 1000);

    d3.csv(url, function (data) {
        if(tab === 'petitions-success-ratio')
            color.domain([0, 1, 2]);
        else
            color.domain([0, 1, 2, 3]); // setting the range of the input data
        console.log('inside geo map');
        d3.json("http://localhost:5000/data/json", function (json) {
            for (var i = 0; i < data.length; i++) {

                var dataState = data[i].state;
                var dataValue = data[i].count;
                for (var j = 0; j < json.features.length; j++) {
                    var jsonState = json.features[j].properties.name;
                    if (dataState == jsonState) {
                        json.features[j].properties.count = dataValue;
                        break;
                    }
                }
            }
            console.log(geosvg);
            console.log(json.features);

            var u = geosvg.selectAll("path")
                .data(json.features);

                u.enter()
                .append("path")
                    .merge(u)
                .attr("d", path)
                .style("stroke", "#fff")
                .style("stroke-width", "1")
                .style("fill", function (d) {
                    var value = d.properties.count;
                    if (value) {
                        return color(value);
                    } else {
                        return "rgb(213,222,217)";
                    }
                }).on("click", function(d){
                     geoChoosenValue = d.properties.name;
                     d3.selectAll("path").style("fill-opacity", "1");
                     d3.select(this).style("fill-opacity", "0.6");
                     drawHorizontalBarChart(tab, dtype,'state', d.properties.name);
                     drawBarChart(tab, dtype, 'state', d.properties.name);
            }).on("mouseenter", function (d) {
                d3.select(this).style("fill-opacity", "0.7");
            })
            .on("mouseleave", function (d) {
                if(geoChoosenValue != d.properties.name){
                    d3.select(this).style("fill-opacity", "1");
                }


            });
            u.exit().remove();

            if(!geoPresent) {
                console.log('inside geoLegend debug');
                 geoPresent = true;
            }

            d3.select(".legend").remove();


                geosvg.selectAll("text")
                    .data(json.features)
                    .enter()
                    .append("svg:text")
                    .text(function (d) {
                        return d.properties.name;
                    })
                    .attr("x", function (d) {
                        return path.centroid(d)[0];
                    })
                    .attr("y", function (d) {
                        return path.centroid(d)[1];
                    })
                    .attr("text-anchor", "middle")
                    .attr('font-size', '6pt');


                var left, width;
              if(tab === 'petitions-success-ratio')
              {
                  left = "190px";
                  width = 300;
              }
              else{
                  left = "270px";
                  width = 200;
              }


                geoLegend = d3.select("#geomap").append("svg")
                    .attr("class", "legend")
                    .attr("width", width)
                    .attr("height", 200)
                    .style("position", "absolute")
                    .style("left", left)
                    .style("top", "405px")
                    .selectAll("g")
                    .data(color.domain())
                    .enter()
                    .append("g")
                    .attr("transform", function (d, i) {
                        return "translate(0," + i * 20 + ")";
                    });

                geoLegend.append("rect")
                    .attr("width", 15)
                    .attr("height", 15)
                    .style("fill", color);

            //console.log(legendText);
            geoLegend.append("text")
                .data(legendText)
                .attr("x", 24)
                .attr("y", 9)
                .attr("dy", ".20em")
                .text(function (d) {
                    return d;
                });
            geoLegend.exit().remove();
           d3.select('#geomap-heading').text(label + ' vs US States');

        });

    });
}
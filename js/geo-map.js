
function drawGeoMap(tab, dtype) {
    var width = 500;
    var height = 440;
    var label;

    if (tab === 'petitions')
        label = 'Petitions';
    else if(tab === 'wages')
        label = 'Wages';

    d3.select('#geomap-heading').text(label + ' vs US States');

// D3 Projection
    var projection = d3.geoAlbersUsa()
        .translate([width / 2, height / 2])    // translate to center of screen
        .scale([650]);          // scale things down so see entire US

// Define path generator
    var path = d3.geoPath()               // path generator that will convert GeoJSON to SVG paths
        .projection(projection);  // tell path generator to use albersUsa projection


// Define linear scale for output
    var color = d3.scaleLinear()
        .range(["rgb(84,36,55)", "rgb(217,91,67)", "rgb(69,173,168)", "rgb(213,222,217)" ]);


    var legendText;

    if (tab === 'petitions')
        legendText = ["H1B Petitions > 200000", "H1B Petitions > 90000", "H1B Petitions > 20000", "H1B Petitions < 20000"];
    else if(tab === 'wages')
        legendText = ["Average Wages > 180k$", "Average Wages > 140k$", "Average Wages > 100k$", "Average Wages < 100k$"];


//Create SVG element and append map to the SVG
    var svg = d3.select("#geomap")
        .append("svg")
        .attr("width", width)
        .attr("height", height);


// Load in my states data!
    d3.csv("http://localhost:5000/data/" + dtype + '/feature/' + tab + "/geomap?" + Math.floor(Math.random() * 1000), function (data) {
        color.domain([0, 1, 2, 3]); // setting the range of the input data

// Load GeoJSON data and merge with states data
        d3.json("http://localhost:5000/data/json", function (json) {

// Loop through each state data value in the .csv file
            for (var i = 0; i < data.length; i++) {

                // Grab State Name
                var dataState = data[i].state;
                // console.log(dataState)
                // Grab data value
                var dataValue = data[i].count;
                // console.log(dataValue)
                // Find the corresponding state inside the GeoJSON
                for (var j = 0; j < json.features.length; j++) {
                    var jsonState = json.features[j].properties.name;
                    if (dataState == jsonState) {
                        json.features[j].properties.count = dataValue;
                        break;
                    }
                }
            }


// Bind the data to the SVG and create one path per GeoJSON feature
            svg.selectAll("path")
                .data(json.features)
                .enter()
                .append("path")
                .attr("d", path)
                .style("stroke", "#fff")
                .style("stroke-width", "1")
                .style("fill", function (d) {
                    var value = d.properties.count;
                    console.log(value)

                    if (value) {
                        //If value exists…
                        // return color(stateByWage[value]);
                        return color(value);
                    } else {
                        //If value is undefined…
                        return "rgb(213,222,217)";
                    }
                });
            svg.selectAll("text")
            .data(json.features)
            .enter()
            .append("svg:text")
            .text(function(d){
                return d.properties.name;
            })
            .attr("x", function(d){
                return path.centroid(d)[0];
            })
            .attr("y", function(d){
                return  path.centroid(d)[1];
            })
            .attr("text-anchor","middle")
            .attr('font-size','6pt');


            var legend = d3.select("#geomap").append("svg")
                .attr("class", "legend")
                .attr("width", 190)
                .attr("height", 200)
                .style("position", "absolute")
                .style("left", "270px")
                .style("top", "400px")
                .selectAll("g")
                .data(color.domain())
                .enter()
                .append("g")
                .attr("transform", function (d, i) {
                    return "translate(0," + i * 20 + ")";
                });

            legend.append("rect")
                .attr("width", 15)
                .attr("height", 15)
                .style("fill", color);

            console.log(legendText);
            legend.append("text")
                .data(legendText)
                .attr("x", 24)
                .attr("y", 9)
                .attr("dy", ".20em")
                .text(function (d) {
                    return d;
                });
        });

    });
}
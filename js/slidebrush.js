var sliderx2, slidersvg, sliderPresent;
function drawSlideBrush() {
    setTimeout(5000);
    console.log('drawing slide brush');
   var  margin2 = {top: 0, right: 20, bottom: 20, left: 30},
        width = 700 - margin2.left - margin2.right,
        height2 = 60 - margin2.top - margin2.bottom;
    //if(!sliderPresent) {
    slidersvg = d3.select("#slide").append("svg")
        .attr("width", "750px")
        .attr("height", "80px");
      //  sliderPresent = true;
    //}
    var parseDate = d3.timeParse("%Y");

    sliderx2 = d3.scaleTime().range([0, width]), y2 = d3.scaleLinear().range([height2, 0]);

    var
        xAxis2 = d3.axisBottom(sliderx2),
        yAxis = d3.axisLeft(y2);

    var brush = d3.brushX()
        .extent([[0, 0], [width, height2]])
        .on("end", brushed);


    var area2 = d3.area()
        .curve(d3.curveMonotoneX)
        .x(function (d) {
            return sliderx2(d.YEAR);
        })
        .y0(height2)
        .y1(function (d) {
            return y2(d.PREVAILING_WAGE);
        });


    var context = slidersvg.append("g")
        .attr("class", "context")
        .attr("transform", "translate(" + margin2.left + "," + margin2.top + ")");

    d3.csv("http://localhost:5000/random?a=695", type, function (error, data) {
        if (error) throw error;

        console.log(data);
        sliderx2.domain(d3.extent(data, function (d) {
            return d.YEAR;
        }));
        y2.domain([0, d3.max(data, function (d) {
            return d.PREVAILING_WAGE;
        })]);



        context.append("path")
            .datum(data)
            .attr("class", "area")
            //.style("fill","red")
            .attr("d", area2);

        context.append("g")
            .attr("class", "axis axis--x")
            .attr("transform", "translate(0," + height2 + ")")
            .call(xAxis2);

        context.append("g")
            .attr("class", "brush")
            .call(brush)
            .call(brush.move, sliderx2.range());

    });

    function brushed() {
        var s = d3.event.selection || sliderx2.range();
        sliderx2.domain(s.map(sliderx2.invert, sliderx2));
        //focus.select(".area").attr("d", area);
        //focus.select(".axis--x").call(xAxis);
        console.log(s);
        console.log(sliderx2);
        syear = s[0];
        eyear = s[1];
        if(syear != 0 || eyear != 650) {
            if(bhChosenValue){
                drawBarChart(tab, dtype, 'employer', bhChosenValue);
                drawGeoMap(tab, dtype, 'employer', bhChosenValue);
                //drawHorizontalBarChart(tab, dtype, null, null);
            }
            else if(bcChosen){
                //drawBarChart(tab, dtype, null, null);
                drawGeoMap(tab, dtype, 'job', bcChosen);
                drawHorizontalBarChart(tab, dtype, 'job', bcChosen);
            }
            else if(geoChoosenValue){
                drawBarChart(tab, dtype, 'state', geoChoosenValue);
                drawHorizontalBarChart(tab, dtype, 'state', geoChoosenValue);
                //drawGeoMap(tab, dtype, null, null);
            }
            else{
                drawBarChart(tab, dtype, null, null);
                drawGeoMap(tab, dtype, null, null);
                drawHorizontalBarChart(tab, dtype, null, null);
            }

        }
    }


    function type(d) {
        d.YEAR = parseDate(d.YEAR);
        d.PREVAILING_WAGE = +d.PREVAILING_WAGE;
        return d;
    }

}
class barchart {

    constructor(tab, dtype){

        if (tab === 'petitions')
            this.label = 'Petitions';
        else if (tab === 'wages')
            this.label = 'Wages';

        d3.select('#barchart-heading').text(this.label + ' vs Job Titles');
        this.margin = {top: 10, right: 30, bottom: 120, left: 50};
        if (tab == 'wages')
            this.margin.left += 20;

        this.width = 400 - this.margin.left - this.margin.right, this.height = 400 - this.margin.top - this.margin.bottom;
        this.svg = d3.select("#barchart")
            .append("svg")
            .attr("width", width + this.margin.left + this.margin.right)
            .attr("height", height + this.margin.top + this.margin.bottom);


        this.g = this.svg.append("g").attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")");

        this.g.append("g")
            .attr("class", "axis axis--x");

        this.g.append("g")
            .attr("class", "axis axis--y");

        this.g.append("text")
            .attr("transform", "translate(" + (width / 2) + " ," + (height + margin.bottom) + ")")
            .style("text-anchor", "middle")
            .style("font-family", "sans-serif")
            .text("Job Titles");

        this.xlabel;
        if (tab === 'petitions')
            this.xlabel = 'Petitions (in x 1000s)';
        else if (tab === 'wages')
            this.xlabel = 'Wages in $';

        this.g.append("text")
            .attr("transform", "rotate(-90)")
            .attr("x", 0 - (height / 2))
            .attr("y", 0 - this.margin.left - 8)
            .attr("dy", "1.4em")
            .attr("text-anchor", "middle")
            .style("font-family", "Playfair")
            .text(this.xlabel);

        this.bounds = this.svg.node().getBoundingClientRect();
        this.width = this.bounds.width - this.margin.left - this.margin.right;
        this.height = this.bounds.height - this.margin.top - this.margin.bottom;
        this.tab = tab;
        this.dtype = dtype;
    }

    async update() {

        let response = await fetch('http://localhost:5000/data/' + this.dtype + '/feature/' + this.tab + '/job');
        let data = await response.json();

        var x = d3.scaleBand().padding(0.3);
        var y = d3.scaleLinear();
        console.log('testing here');
        console.log(this.label);

        x.domain(data['Job Title']);
        y.domain([0, d3.max(data[this.label])]);


        x.rangeRound([0, this.width]);
        y.rangeRound([this.height, 0]);

        this.g.select(".axis--x")
            .attr("transform", "translate(0," + this.height + ")")
            .call(d3.axisBottom(x))
            .selectAll("text")
            .attr("y", 0)
            .attr("x", 9)
            .attr("dy", ".35em")
            .attr("transform", "rotate(45)")
            .style("text-anchor", "start")
            .style("font-family", "sans-serif");


        this.g.select(".axis--y")
            .call(d3.axisLeft(y));
        this.convertedData = this.dataConversion(data, this.label);
        console.log(this.convertedData);

        var bars = this.g.selectAll(".bar")
            .data(this.convertedData);

        bars
            .enter().append("rect")
            .attr("class", "bar")
            .attr("x", function (d) {
                //console.log(d);
                return x(d['Job Title']);
            })
            .attr("y", function (d) {
                console.log(this.label);
                console.log(d[this.label]);
                return y(d[this.label]);
            })
            .attr("width", x.bandwidth())
            .attr("height", function (d) {
                return this.height - y(d[this.label]);
            })
            .style("fill", barColor)
            .style("stroke", strokeColor)
            .style("stroke-width", strokeBorder)
            .on("mouseenter", function (d, index) {
                d3.select(this).style("fill", hoverColor);
            })
            .on("mouseleave", function (d, index) {
                d3.select(this).style("fill", barColor);
            });
        this.bars.exit().remove();
    }

    dataConversion(arr, label) {
        var result = [];
        console.log('inside data conversion');
        console.log(label);
        for (var i = 0; i < arr['Job Title'].length; i++) {
            let temp = {};
            temp['Job Title'] = arr['Job Title'][i];
            temp[label] = arr[label][i];
            result.push(temp);
        }
        return result;
    }

}
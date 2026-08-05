function drawLegend(legendSelector, legendColorScale, scaleType) {

    //  Credit Prof. Rz with minor edits to accomodate to our own project

    // Shrink legend bar by 5 px inwards from sides of SVG
    const offsets = { width: 10,
                    top: 2,
                    bottom: 24 }; 
    // Number of integer 'pixel steps' to draw when showing continuous scales
    const stepSize = 4; 
    // Extend the minmax by 0% in either direction to expose more features by default
    const minMaxExtendPercent = 0;
    
    const legend = d3.select(legendSelector);
    const legendHeight = legend.attr("height");
    const legendBarWidth = legend.attr("width") - (offsets.width * 2);
    const legendMinMax = d3.extent(legendColorScale.domain()); 
                // recover the min and max values from most kinds of numeric scales
    const minMaxExtension = (legendMinMax[1] - legendMinMax[0]) * minMaxExtendPercent;
    const barHeight = legendHeight - offsets.top - offsets.bottom;     
    
    // In this case the "data" are pixels, and we get numbers to use in colorScale
    // Use this to make axis labels
    let barScale = d3.scaleLinear().domain([legendMinMax[0]-minMaxExtension,
                                            legendMinMax[1]+minMaxExtension])
                                .range([0,legendBarWidth]);

    const domainRange = legendMinMax[1] - legendMinMax[0];

    // Determine what scale to divide by to determind number of ticks
    let num;
    if (scaleType == 'gdp') {
        num = 1000000000000;
    } else if (scaleType == 'gini') {
        num = 10;
    } else if (scaleType == 'co2') {
        num = 1000000000;
    };

    // // Determine the number of ticks based on the domain range
    let numTicks = 6;
    if (domainRange / num <= 3) {
        numTicks = 3;
    } else if (domainRange / num <= 18) {
        numTicks = 4;
    }
    else  {
        numTicks = 6;
    };


    let barAxis = d3.axisBottom(barScale)
                        .tickFormat(d3.format(".0s"))
                        .ticks(numTicks);

    // Place for bar slices to live
    let bar = legend.append("g")
                    .attr("class", "legend colorbar")
                    .attr("transform", `translate(${offsets.width},${offsets.top})`)


    // we have a continuous / roundable scale
    //  In an ideal world you might construct a custom gradient mapped to the scale
    //  For this one, we use a hack of making stepped rects
    if (legendColorScale.hasOwnProperty('rangeRound')) {
    // NOTE: The barAxis may round min and max values to make them pretty
    // ** This also means there is a risk of the legend going beyond scale bounds
    // We need to use the barAxis min and max just to be sure the bar is complete
    //    Using barAxis.scale().invert() goes from *axis* pixels to data values easily
    // ** We also need to create patches for the scale if the labels exceed bounds
    //     (floating point comparisons risky for small data ranges,but not a big deal
    //      because patches will be indistinguishable from actual scale bottom)
    // It's likely that scale clamping will actually do this for us elegantly
    // ...but better to be safer and patch the regions anyways
    
    for (let i=0; i<legendBarWidth; i=i+stepSize) {
        
        let center = i+(stepSize/2);
        let dataCenter = barAxis.scale().invert( center );
        
        // below normal scale bounds
        if ( dataCenter < legendMinMax[0] ) { 
        bar.append("rect")
            .attr("x", i)
            .attr("y", 0)
            .attr("width", stepSize)
            .attr("height",barHeight)
            .style("fill", legendColorScale( legendMinMax[0] ) ); 
        }
        // within normal scale bounds
        else if ( dataCenter < legendMinMax[1] ) {
        bar.append("rect")
            .attr("x", i)
            .attr("y", 0)
            .attr("width", stepSize)
            .attr("height",barHeight)
            .style("fill", legendColorScale( dataCenter ) ); 
        }
        // above normal scale bounds
        else {
        bar.append("rect")
            .attr("x", i)
            .attr("y", 0)
            .attr("width", stepSize)
            .attr("height",barHeight)
            .style("fill", legendColorScale( legendMinMax[1] ) ); 
        }
    }
    }
    
    // Finally, draw legend labels
    legend.append("g")
        .attr("class", "legend axis")
        .attr("transform",`translate(${offsets.width},${offsets.top+barHeight+5})`)
        .call(barAxis);
    
}

function updateLegend(legendSelector, legendColorScale, scaleType) {

    // remove existing legend
    d3.select(legendSelector).selectAll("*").remove();

    // create new legend given a color scale
    drawLegend(legendSelector, legendColorScale, scaleType);
}
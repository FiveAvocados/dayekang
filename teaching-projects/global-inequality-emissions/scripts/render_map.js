
// modified from
// https://observablehq.com/@d3/world-map-svg

const Projections = Object.freeze({
    Mercator: () => d3.geoMercator(),
    EqualEarth: () => d3.geoEqualEarth()
});

function renderMap(svg, countryFeatures, scale, projection, pathClass, idName, onClick){
    const width = svg.attr("width");
    const height = svg.attr("height");
    const p = projection().scale(scale).translate([width / 2, height / 1.7]);
    const path = d3.geoPath().projection(p);
    const g = svg.append("g");
    g.selectAll("path")
                    .data(countryFeatures)
                    .join("path")
                    .attr("d", path)
                    .attr("class", pathClass)
                    .attr(idName, d => d.id)
                    .attr("stroke", "black")
                    .attr("stroke-width", "0.5px")
                    .attr("fill", "lightgray")
                    .on("click", (event, d) => {
                        const bb = boundingBox(path, d);
                        if(onClick) onClick(d, bb, svg);
                    });

    return {
        map: g,
        path: path
    };
}

function updateMap(g, yearObj, mapData, numToId, useYearlyExtents, targetClass, fallbackColor){
    let domain = undefined;
    const year = yearObj.value;
    const dataValues = mapData.data;
    const scaler = mapData.scaler;
    const colors = mapData.colors;
    if(useYearlyExtents.value && dataValues.haveDomain(year)){
        domain = dataValues.getDomain(year);
    }else if(dataValues.haveOverallDomain){
        domain = dataValues.overallDomain;
    }

    if (domain){
        // whenever we update the map, we also need to update the 
        // domain for the scaler and the colors, so the legend
        // knows how to draw the tick marks and labels
        scaler.domain(domain);
        scaler.range(domain);
        colors.domain(domain);
        g.selectAll(targetClass)
        .attr("fill", d => {
            const id = numToId[d.id];
            const data = dataValues.data[year][id];
            if(data && data.value) {
                const value = data.value;
                const scaled = scaler(value);
                const color = colors(scaled);
                return color;
            } else {
                return fallbackColor;
            }
        });
    }else{
        g.selectAll(targetClass)
        .attr("fill", fallbackColor);
    }


}

function updateMapStroke(g, selectedCountryId){
    g.selectAll("path")
    .attr("stroke-width", d => {
        if (selectedCountryId.value && d.id === selectedCountryId.value) {
            return "2px";
        } else {
            return "0.5px";
        }
    });

}

// from
// https://stackoverflow.com/questions/44345924/get-bounding-box-of-individual-countries-from-topojson
function boundingBox(path, feature){
    const bounds = path.bounds(feature);
    const id = feature.id;
    const x = bounds[0][0];
    const y = bounds[0][1];
    const width = bounds[1][0] - x;
    const height = bounds[1][1] - y;
    return {
        id: id,
        x: x,
        y: y,
        width: width,
        height: height
    }
}
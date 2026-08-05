function detailBox(
  feature,
  boundingBox,
  svg,
  data,
  minYear,
  maxYear,
  dataNames,
  prevCountryId,
  currentYear
) {
  // first remove all "detail" foreignObjects from svg
  // to make sure there is only one detail box at a time
  svg.selectAll("foreignObject.detail").remove();
  if (feature.id !== prevCountryId.value) {
    prevCountryId.value = feature.id;
    const margins = {
      left: 40,
      right: 20,
      top: 10,
      bottom: 20,
    };
    const width = data.detailBoxWidth || 650;
    const sideBarWidth = data.detailBoxSideBarWidth || 250;
    const chartWidth = width - sideBarWidth;
    const height = data.detailBoxHeight || 260;

    let xTranslation = boundingBox.x + boundingBox.width;
    if (xTranslation > svg.attr("width") / 2) {
      // 643, 242 need special treatment here,
      // they wrap around the edges of the map so
      // their positions causes massive negative x translation
      xTranslation = boundingBox.x - boundingBox.width - width;
      if (feature.id === "643" || feature.id === "242") {
        xTranslation = boundingBox.x - width / 2;
      }
    }
    const detailG = svg
      .append("g")
      .attr("transform", `translate(${xTranslation}, ${boundingBox.y})`);

    // then add a new detail box
    const detail = detailG
      .append("foreignObject")
      .attr("class", "detail")
      .attr("width", width)
      .attr("height", height);

    // make it so the box is opaque
    const body = detail
      .append("xhtml:body")
      .style("background", "white")
      .style("opacity", 1)
      .style("border", "1px solid black")
      .style("padding-left", "5px")
      .style("padding-bottom", "5px")
      .style("border-radius", "5px");

    const bodyDiv = body.append("div");

    const countryCodeNumeric = feature.id;
    const countryName = data.codes.numToName[countryCodeNumeric];
    const countryCodeAlpha3 = data.codes.numToId[countryCodeNumeric];
    let dataName = dataNames.gdp;

    // add a div to the detail box with the country name
    const countryTitle = bodyDiv
      .append("h2")
      .style("padding-left", "8px")
      .text(countryName);

    // add 3 buttons, "GDP", "GINI", and "CO2"
    const buttonsDiv = bodyDiv
      .append("div")
      .style("padding-left", "8px")
      .style("padding-bottom", "8px")
      .attr("class", "buttons");

    const gdpButton = buttonsDiv
      .append("button")
      .attr("class", "lensbutton")
      .text("GDP")
      .style("background-color", "grey")
      .on("click", function () {
        dataName = dataNames.gdp;
        changeColor("gdp");
        drawGraph();
      });

    const giniButton = buttonsDiv
      .append("button")
      .attr("class", "lensbutton")
      .style("background-color", "lightgrey")
      .text("GINI")
      .on("click", async () => changeColor("gini"))
      .on("click", function () {
        dataName = dataNames.gini;
        changeColor("gini");
        drawGraph();
      });

    const co2Button = buttonsDiv
      .append("button")
      .attr("class", "lensbutton")
      .style("background-color", "lightgrey")
      .text("CO2")
      .on("click", function () {
        dataName = dataNames.co2;
        changeColor("co2");
        drawGraph();
      });

    function changeColor(buttonType) {
      if (buttonType == "gdp") {
        gdpButton.style("background-color", "grey");
        giniButton.style("background-color", "lightgrey");
        co2Button.style("background-color", "lightgrey");
      }
      if (buttonType == "gini") {
        gdpButton.style("background-color", "lightgrey");
        giniButton.style("background-color", "grey");
        co2Button.style("background-color", "lightgrey");
      }
      if (buttonType == "co2") {
        gdpButton.style("background-color", "lightgrey");
        giniButton.style("background-color", "lightgrey");
        co2Button.style("background-color", "grey");
      }
    }
    const chartDiv = bodyDiv.append("div").attr("class", "chartcontainer");

    function drawGraph() {
      // first remove any existing svg
      chartDiv.selectAll("svg").remove();

      // modified from
      // https://d3-graph-gallery.com/graph/line_basic.html

      // add svg for line chart
      const lineChart = chartDiv
        .append("svg")
        .attr("width", chartWidth)
        .attr("height", height)
        .style("border-top", "1px solid black")
        .style("border-right", "1px solid black");

      const xScale = d3
        .scaleLinear()
        .domain([minYear, maxYear])
        .range([margins.left, chartWidth - margins.right]);

      const xAxis = d3.axisBottom(xScale).ticks(5).tickFormat(d3.format("d"));

      const rawData = data[dataName].data;

      // gdpData contains keys with years, each year contains
      // keys for alpha3 country codes, each country code
      // has keys for value and code, so we need to search
      // through the data for what we want
      const filteredData = [];
      const filteredDomain = [Infinity, -Infinity];
      for (let year = minYear; year <= maxYear; year++) {
        const yearData = rawData[year];
        if (yearData) {
          const countryData = yearData[countryCodeAlpha3];
          if (countryData && countryData.value) {
            filteredDomain[0] = Math.min(filteredDomain[0], countryData.value);
            filteredDomain[1] = Math.max(filteredDomain[1], countryData.value);
            filteredData.push({
              year: year,
              value: countryData.value,
            });
          }
        }
      }

      console.log(filteredData);

      const yScale = d3
        .scaleLinear()
        .domain(filteredDomain)
        .range([height - margins.bottom, margins.top]);

      // since yAxis contains massive values such as
      // 20,000,000,000,000, need to format it so it's
      // visible on the graph
      const yAxis = d3.axisLeft(yScale).tickFormat(d3.format(".2s"));

      lineChart
        .append("g")
        .attr("transform", `translate(0, ${height - margins.bottom})`)
        .call(xAxis);

      lineChart
        .append("g")
        .attr("transform", `translate(${margins.left}, 0)`)
        .call(yAxis);

      const line = lineChart
        .append("path")
        .datum(filteredData)
        .attr("fill", "none")
        .attr("stroke", "steelblue")
        .attr("stroke-width", 2)
        .attr(
          "d",
          d3
            .line()
            .x((d) => xScale(d.year))
            .y((d) => yScale(d.value))
        );

      // remove all sidebars
      chartDiv.selectAll(".sidebar").remove();

      const sidebar = chartDiv
        .append("div")
        .attr("class", "sidebar")
        .style("width", `${sideBarWidth - 2}px`)
        .style("height", height + "px")
        .style("border", "none")
        .style("border-top", "1px solid black");

      const sectors = data[dataNames.sectors];
      const sectorData = sectors[currentYear.value][countryCodeAlpha3];
      // sectorData is object like { Agriculture: 357820000, Waste: 199340000, ... }
      // create list starting from largest to smallest and add to sidebar
      // though need to check if it undefined first
      if (sectorData) {
        const sectorList = [];
        Object.keys(sectorData).forEach((sector) => {
          sectorList.push({
            sector: sector,
            value: sectorData[sector],
          });
        });
        sectorList.sort((a, b) => b.value - a.value);
        const sectorTitle = sidebar
          .append("h3")
          .text(`Emission Sector Data for Year ${currentYear.value}`)
          .style("padding-left", 5);
        const sectorUl = sidebar.append("ul").attr("class", "sector-list");

        // since numbers might be really large, format them
        sectorUl
          .selectAll("li")
          .data(sectorList)
          .join("li")
          .text((d) => `${d.sector}: ${d3.format(".2s")(d.value)}`);
      } else {
        sidebar
          .append("p")
          .style("padding-left", 5)
          .text(
            `There is no sector data for year ${currentYear.value} in this country.`
          );
      }
    }

    drawGraph();
  } else {
    // we clicked the same country again, so the svg.selectAll
    // line at the top would have already removed the detail box
    // so we deselected the country
    prevCountryId.value = undefined;
  }
}

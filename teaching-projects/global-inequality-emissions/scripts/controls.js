
/**
 * In the given element selected by d3, given an array of tuple in the form [name, callback],
 * create a button for each tuple, with the given name and callback.
 * 
 * The button will also ensure all other buttons in the element have their
 * class set to "dormant" when clicked, while setting its own class to "active".
 * 
 * The button at the initialIndex will be set to "active" initially.
 * 
 * All buttons will also have the class "lensbutton".
 * 
 * The callback will receive the parameters `map` and `data`.
 */
function createLensButtons(element, buttonTuples, initialIndex, map, data) {
    element.selectAll("button")
        .data(buttonTuples)
        .join("button")
        .attr("class", (d, i) => i === initialIndex ? "active lensbutton notmap" : "dormant lensbutton notmap")
        .text(d => d[0])
        .on("click", (event, d) => {
            element.selectAll("button")
                .attr("class", "dormant lensbutton");
            d[1](map, data);
            d3.select(event.target)
                .attr("class", "active lensbutton");
        });
}
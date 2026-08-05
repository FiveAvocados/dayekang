
/**
 * load gdp reads in data from specified file asynchronously,
 * producing an object containing the data for each year and 
 * country, along with extents for the data by year and 
 * overall.
 * 
 * To identify an entry as a valid country, also need an object whose
 * keys are ISO 3166-1 3-letter country codes so that we can check
 * that the country code in the gdp data is valid.
 * 
 * @param {string} gdpFile the name of the file containing the gdp data
 * @param {Object} countryCodes an object whose keys are ISO 3166-1 3-letter country codes
 * @returns {Promise} a promise that resolves to an object containing the data
 */
async function loadGDP(gdpFile, countryCodes) {
    const gdps = await d3.json(gdpFile);

    let overallMini = Infinity;
    let overallMaxi = -Infinity;

    // extents contains the min and max for each year
    // as well as the overall min and max
    const extents = {};

    const minYear = gdps.minYear;
    const maxYear = gdps.maxYear;
    for (let i = minYear; i <= maxYear; i++) {
        const yearData = gdps.data[i];
        Object.keys(yearData).forEach(countryCode => {
            const gdp = yearData[countryCode].value;

            if(gdp && countryCodes[countryCode]){
                if (gdp < overallMini) overallMini = gdp;
                if (gdp > overallMaxi) overallMaxi = gdp;

                // check if we already have an extent data for year
                if (extents[i]){
                    const extent = extents[i];
                    if (gdp < extent.mini) extent.mini = gdp;
                    if (gdp > extent.maxi) extent.maxi = gdp;
                }else {
                    extents[i] = {
                        mini: gdp,
                        maxi: gdp
                    }
                }
            }
        });
    }

    extents.overall = {
        mini: overallMini,
        maxi: overallMaxi
    };

    return {
        minYear: minYear,
        maxYear: maxYear,
        data: gdps.data,
        extents: extents,
        get overallDomain() {
            return [this.extents.overall.mini, this.extents.overall.maxi];
        },
        get haveOverallDomain() {
            return this.extents.overall.mini !== Infinity && this.extents.overall.maxi !== -Infinity;
        },
        getDomain: function(year) {
            const extent = this.extents[year];
            return [extent.mini, extent.maxi];
        },
        haveDomain: function(year) {
            // not all years are guaranteed to have data
            return this.extents[year] !== undefined;
        }
    };
}

/**
 * load gini reads in data from specified file asynchronously,
 * producing an object containing the data for each year and
 * country, along with extents for the data by year and
 * overall.
 * 
 * To identify an entry as a valid country, also need an object whose
 * keys are ISO 3166-1 3-letter country codes so that we can check
 * that the country code in the gini data is valid.
 * 
 * @param {string} giniFile the name of the file containing the gini data
 * @param {Object} countryCodes an object whose keys are ISO 3166-1 3-letter country codes
 * @returns {Promise} a promise that resolves to an object containing the data
 */
async function loadGINI(giniFile, countryCodes) {
    const ginis = await d3.json(giniFile);

    let overallMini = Infinity;
    let overallMaxi = -Infinity;

    // extents contains the min and max for each year
    // as well as the overall min and max
    const extents = {};

    const minYear = ginis.minYear;
    const maxYear = ginis.maxYear;
    for (let i = minYear; i <= maxYear; i++) {
        const yearData = ginis.data[i];
        Object.keys(yearData).forEach(countryCode => {
            const gini = yearData[countryCode].value;
            if(gini && countryCodes[countryCode]){
                if (gini < overallMini) overallMini = gini;
                if (gini > overallMaxi) overallMaxi = gini;

                // check if we already have an extent data for year
                if (extents[i]){
                    const extent = extents[i];
                    if (gini < extent.mini) extent.mini = gini;
                    if (gini > extent.maxi) extent.maxi = gini;
                }else {
                    extents[i] = {
                        mini: gini,
                        maxi: gini
                    }
                }
            }
        });
    }

    extents.overall = {
        mini: overallMini,
        maxi: overallMaxi
    };

    return {
        minYear: minYear,
        maxYear: maxYear,
        data: ginis.data,
        extents: extents,
        get overallDomain() {
            return [this.extents.overall.mini, this.extents.overall.maxi];
        },
        get haveOverallDomain() {
            return this.extents.overall.mini !== Infinity && this.extents.overall.maxi !== -Infinity;
        },
        getDomain: function(year) {
            const extent = this.extents[year];
            return [extent.mini, extent.maxi];
        },
        haveDomain: function(year) {
            // not all years are guaranteed to have data
            return this.extents[year] !== undefined;
        }
    };
}

/**
 * load co2 reads in data from specified file asynchronously,
 * producing an object containing the data for each year and
 * country, along with extents for the data by year and
 * overall.
 * 
 * To identify an entry as a valid country, also need an object whose
 * keys are ISO 3166-1 3-letter country codes so that we can check
 * that the country code in the co2 data is valid.
 * 
 * @param {string} co2File the name of the file containing the co2 data
 * @param {Object} countryCodes an object whose keys are ISO 3166-1 3-letter country codes
 * @returns {Promise} a promise that resolves to an object containing the data
 */
async function loadCO2(co2File, countryCodes) {
    const co2s = await d3.json(co2File);

    let overallMini = Infinity;
    let overallMaxi = -Infinity;

    // extents contains the min and max for each year
    // as well as the overall min and max
    const extents = {};

    const minYear = co2s.minYear;
    const maxYear = co2s.maxYear;
    for (let i = minYear; i <= maxYear; i++) {
        const yearData = co2s.data[i];
        Object.keys(yearData).forEach(countryCode => {
            const co2 = yearData[countryCode].value;
            if(co2 && countryCodes[countryCode]){
                if (co2 < overallMini) overallMini = co2;
                if (co2 > overallMaxi) overallMaxi = co2;

                // check if we already have an extent data for year
                if (extents[i]){
                    const extent = extents[i];
                    if (co2 < extent.mini) extent.mini = co2;
                    if (co2 > extent.maxi) extent.maxi = co2;
                }else {
                    extents[i] = {
                        mini: co2,
                        maxi: co2
                    }
                }
            }
        });
    }

    extents.overall = {
        mini: overallMini,
        maxi: overallMaxi
    };

    return {
        minYear: minYear,
        maxYear: maxYear,
        data: co2s.data,
        extents: extents,
        get overallDomain() {
            return [this.extents.overall.mini, this.extents.overall.maxi];
        },
        get haveOverallDomain() {
            return this.extents.overall.mini !== Infinity && this.extents.overall.maxi !== -Infinity;
        },
        getDomain: function(year) {
            const extent = this.extents[year];
            return [extent.mini, extent.maxi];
        },
        haveDomain: function(year) {
            // not all years are guaranteed to have data
            return this.extents[year] !== undefined;
        }
    };
}

/**
 * loads co2 emissions data split by sector from specified file asynchronously,
 * producing an object containing the data for each year and
 * country
 * 
 * To identify an entry as a valid country, also need an object whose
 * keys are ISO 3166-1 3-letter country codes so that we can check
 * that the country code in the co2 data is valid. *TODO*
 */
async function loadCO2Sectors(co2SectorFile, countryCodes) {
    const co2Sectors = await d3.json(co2SectorFile);

    return co2Sectors;
}

/**
 * load country code data from specified file asynchronously,
 * producing an object containing mapping from ISO 3166-1 3-letter
 * country codes to ISO 3166-1 numeric country codes, as well
 * as the reverse mapping.
 * 
 * @param {string} countryCodesFile the name of the file containing the country code data
 * @returns {Promise} a promise that resolves to an object containing the data
 */
async function loadCountryCodes(countryCodesFile) {
    const codes = await d3.json(countryCodesFile);

    const idToNum = {};
    const numToId = {};
    const numToName = {};

    codes.forEach(code => {
        idToNum[code["alpha-3"]] = code["country-code"];
        numToId[code["country-code"]] = code["alpha-3"];
        numToName[code["country-code"]] = code["name"];
    });

    return {
        idToNum: idToNum,
        numToId: numToId,
        numToName: numToName
    };
}
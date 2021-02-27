# Summary
This repository documents the data processing and analysis code associated with the article **"Exposure Density and Neighborhood Disparities in COVID-19 Infection Risk"** published in *PNAS*.

# Title: Exposure Density and Neighborhood Disparities in COVID-19 Infection Risk

**Authors**: [Boyeong Hong](https://marroninstitute.nyu.edu/people/boyeong-hong)<sup>1</sup>, [Bartosz J. Bonczak](https://marroninstitute.nyu.edu/people/bartosz-bonczak)<sup>1</sup>, [Arpit Gupta](https://www.stern.nyu.edu/faculty/bio/arpit-gupta)<sup>2</sup>, [Lorna E. Thorpe](https://med.nyu.edu/faculty/lorna-e-thorpe)<sup>3</sup> and [Constantine E. Kontokosta](https://marroninstitute.nyu.edu/people/constantine-kontokosta)<sup>1,4,*</sup>

<sup>1</sup>[New York University, Marron Institute of Urban Management, 60 5th Avenue, New York, NY 10011](https://marroninstitute.nyu.edu/)

<sup>2</sup>[New York University, Stern School of Business, 44 West 4th Street, New York, NY 10012](https://www.stern.nyu.edu/)

<sup>3</sup>[New York University, Grossman School of Medicine, 550 First Avenue, New York, NY 10016](https://med.nyu.edu/)

<sup>4</sup>[New York University, Center for Urban Science and Progress, 370 Jay Street, Brooklyn, NY 11201](https://cusp.nyu.edu/)

<sup>*</sup>Correspondence and requests for materials should be addressed to Constantine E. Kontokosta (email: <ckontokosta@nyu.edu>).

![fig](https://github.com/UrbanIntelligenceLab/Exposure-Density-and-Neighborhood-Disparities-in-COVID-19-Infection-Risk/blob/main/exp_dens.png?raw=true)

## Abstract
Although there is increasing awareness of disparities in COVID-19 infection risk among vulnerable communities, the effect of behavioral interventions at the scale of individual neighborhoods has not been fully studied. We develop a new method to quantify neighborhood activity behaviors at high spatial and temporal resolutions and test whether, and to what extent, behavioral responses to social distancing policies vary with socioeconomic and demographic characteristics. We define *exposure density* (*E<sub>x</sub> &rho;*) as a measure of both the localized volume of activity in a defined area and the proportion of activity occurring in distinct land use types. Using detailed neighborhood data for New York City, we quantify neighborhood exposure density using anonymized smartphone geolocation data over a three-month period covering more than 12 million unique devices, and rasterize granular land use information to contextualize observed activity. Next, we analyze disparities in community social distancing by estimating variations in neighborhood activity by land use type before and after a mandated stay-at-home order. Finally, we evaluate the effects of localized demographic, socioeconomic, and built environment density characteristics on infection rates and deaths in order to identify disparities in health outcomes related to exposure risk. Our findings demonstrate distinct behavioral patterns across neighborhoods after the stay-at-home order and that these variations in exposure density had a direct and measurable impact on the risk of infection. Notably, we find that an additional 10\% reduction in exposure density city-wide could have saved between 1,849 and 4,068 lives during the study period, predominantly in lower-income and minority communities.

## Cite
Hong, B., Bonczak, B., Gupta, A., Thorpe, L. E. & Kontokosta, C. E. (in press). Exposure Density and Neighborhood Disparities in COVID-19 Infection Risk. *PNAS*

# Repository Structure
The repository documents the data processing and analysis performed to support the findings of the study reported in the published article. It is structured as follows:

```
.\root
    |--- data                           # placeholder directory intended to contain raw data
        |--- rsterization               # folder containing rasterization data
            |--- us_cities              # lists all of different cities data
                |--- 1_New_York_City    # selected New York City data
                    |--- Boundary       # city boundary shapefile
                    |--- Buildings      # city building footprints shapefile
                    |--- Land Use       # land use information shapefile
                    |--- Streets        # street network shapefile
    |--- figures                        # figures generated for the publication purposes
    |--- scripts                        # contains all scripts used in the study 
```

# Data Description

The study combines geolocated mobility data with detailed land cover and land use information in New York City to estimate neighborhood level exposure density and evaluate it's relationship with local COVID-19 infection rates. All of the data sources used in the paper are listed in the table below.

Dataset | Time range | Resolution (spatial/temporal) | Source | Description | URL
--------|------------|-------------------------------|--------|-------------|----
Mobility data | 2020-02-01∼2020-04-30 | (X,Y)/second | [VenPath, Inc.](https://www.venpath.net/) | More than 127 billion geotagged data points associated with 120 million unique devices every month. | N/A<sup>*</sup>
NYC Primary Land Use Tax Lot Output (PLUTO) | updated 2020-02-24 | Parcel/NaN | [NYC Department of City Planning (DCP)](https://www1.nyc.gov/site/planning/index.page) | Land  use  and  building  type  information  provided. | https://www1.nyc.gov/site/planning/data-maps/open-data/bytes-archive.page?sorts[year]=0
NYC Building Footprints | updated 2020-07-06 | Footprint/NaN | [NYC Department of Information Technology & Telecom-munications (DoITT)](https://www1.nyc.gov/site/doitt/index.page) | Perimeter outlines of more than 1 million buildings in NYC. | https://www1.nyc.gov/site/doitt/residents/gis-2d-data.page
Road Network Data (LION) | updated 2020-04-28 | Street segment/NaN | [NYC Department of Transportation](https://www1.nyc.gov/html/dot/html/home/home.shtml) | Single line street base map with associated information on type, width, accessibility etc. | https://www1.nyc.gov/site/planning/data-maps/open-data/dwn-lion.page
NYC COVID-19 data | 2020-04-01∼2020-06-04 | Zipcode/daily | [NYC Department of Health and Mental Hygiene](https://www1.nyc.gov/site/doh/index.page) | COVID-19  confirmed  cases,  deaths,  and  positivity  rates | https://github.com/nychealth/coronavirus-data
American Community Survey (ACS) | 2018 5-yearestimates | Zipcode/NaN | [U.S. Census Bureau](https://www.census.gov/en.html) | Neighborhood demographic and socioeconomic characteristics. | https://www.census.gov/data/developers/data-sets/acs-5year.2018.html
NYC Hospital locations | updated 2017-09-08 | (X,Y)/NaN | [NYC Health and Hospital Corporation](https://www.nychealthandhospitals.org/) | Hospitals affiliated with the NYC Health and Hospital Corporation and public hospital system. | https://data.cityofnewyork.us/Health/NYC-Health-Hospitals-Facilities-2011/ymhw-9cz9
Nursing home data | updated 2020-05-24 | (X,Y)/NaN | [Centers for Disease Control’s National Healthcare Safety Network](https://www.cdc.gov/nhsn/index.html) | Nursing home information, including the number of beds and occupancy | https://data.cms.gov/stories/s/bkwz-xpvg

### <sup>*</sup>Data Availability Statement
The annonymized geolocated mobile application activity data that support the findings of this study are available from VenPath, Inc. but restrictions apply to the availability of these data, which were used under license for the current study, and are therefore not publicly available. However, data are available from the authors upon
reasonable request and with permission of VenPath, Inc.

# System Specifications
Mobility data were provided via a dedicated AWS S3 service and were managed in accordance with NYU Institutional Review Board approval IRB-FY2018-1645 and stored and accessed in a secured environment at [New York University](https://www.nyu.edu/)’s [High Performance Computing](https://sites.google.com/a/nyu.edu/nyu-hpc/home) (HPC) and [Center for Urban Science and Progress](cusp.nyu.edu) (NYU CUSP) [Research Computing Facility](https://datahub.cusp.nyu.edu/) (RCF), both of which are secure environments with controlled access and restricted connectivity. Raw data were deployed to the NYU HPC Dumbo server, equipped with a Hadoop (2.6.0) Cloudera CDH (5.15) cluster with Yarn with 44 compute nodes and the total of 704 CPU cores (2x8-core per node), 5.6 TB RAM (128 GB per node) and 1.4 PB storage. Initial data processing was conducted using [Apache PySpark](https://spark.apache.org/docs/latest/api/python/index.html) version 2.4. The following analysis performed on the processed data was conducted on RCF's High Memory computing server with total memory of 1TB and Intel(R) Xeon(R) CPU E5-4640 0 @ 2.40GHz (4x8 cores) using predominantly [Python](https://www.python.org/) version 3.7 and [Quantum GIS](https://www.qgis.org/en/site/index.html) version 3.4 Madeira. Each script file relies on a separate set of libraries, which were listed at the beginning of each file, including the library version used for the particular task.

# License

MIT License

Copyright (c) 2021 Urban Intelligence Lab, Hong, Bonczak, Gupta, and Kontokosta

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

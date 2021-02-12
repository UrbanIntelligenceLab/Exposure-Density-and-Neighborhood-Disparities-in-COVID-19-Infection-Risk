# Summary
This repository documents the data processing and analysis perform on the data to support the findings presented in the article **"Exposure Density and Neighborhood Disparities in COVID-19 Infection Risk"** published in *PNAS*.

# Title: Exposure Density and Neighborhood Disparities in COVID-19 Infection Risk

**Authors**: [Boyeong Hong](https://marroninstitute.nyu.edu/people/boyeong-hong)<sup>1</sup>, [Bartosz J. Bonczak](https://marroninstitute.nyu.edu/people/bartosz-bonczak)<sup>1</sup>, [Arpit Gupta](https://www.stern.nyu.edu/faculty/bio/arpit-gupta)<sup>2</sup>, [Lorna E. Thorpe](https://med.nyu.edu/faculty/lorna-e-thorpe)<sup>3</sup> and [Constantine E. Kontokosta](https://marroninstitute.nyu.edu/people/constantine-kontokosta)<sup>1,4,*</sup>

<sup>1</sup>[New York University, Marron Institute of Urban Management, 60 5th Avenue, New York, NY 10011](https://marroninstitute.nyu.edu/)

<sup>2</sup>[New York University, Stern School of Business, 44 West 4th Street, New York, NY 10012](https://www.stern.nyu.edu/)

<sup>3</sup>[New York University, Grossman School of Medicine, 550 First Avenue, New York, NY 10016](https://med.nyu.edu/)

<sup>4</sup>[New York University, Center for Urban Science and Progress, 370 Jay Street, Brooklyn, NY 11201](https://cusp.nyu.edu/)

<sup>*</sup>Correspondence and requests for materials should be addressed to Constantine E. Kontokosta (email: <ckontokosta@nyu.edu>).

![fig](https://github.com/UrbanIntelligenceLab/Exposure-Density-and-Neighborhood-Disparities-in-COVID-19-Infection-Risk/blob/main/figures/exp_dens.png?raw=true)

## Abstract
Although there is increasing awareness of disparities in COVID-19 infection risk among vulnerable communities, the effect of behavioral interventions at the scale of individual neighborhoods has not been fully studied. We develop a new method to quantify neighborhood activity behaviors at high spatial and temporal resolutions and test whether, and to what extent, behavioral responses to social distancing policies vary with socioeconomic and demographic characteristics. We define *exposure density* (*E<sub>x</sub> &rho;*) as a measure of both the localized volume of activity in a defined area and the proportion of activity occurring in distinct land use types. Using detailed neighborhood data for New York City, we quantify neighborhood exposure density using anonymized smartphone geolocation data over a three-month period covering more than 12 million unique devices, and rasterize granular land use information to contextualize observed activity. Next, we analyze disparities in community social distancing by estimating variations in neighborhood activity by land use type before and after a mandated stay-at-home order. Finally, we evaluate the effects of localized demographic, socioeconomic, and built environment density characteristics on infection rates and deaths in order to identify disparities in health outcomes related to exposure risk. Our findings demonstrate distinct behavioral patterns across neighborhoods after the stay-at-home order and that these variations in exposure density had a direct and measurable impact on the risk of infection. Notably, we find that an additional 10\% reduction in exposure density city-wide could have saved between 1,849 and 4,068 lives during the study period, predominantly in lower-income and minority communities.

## Cite
Hong, B., Bonczak, B., Gupta, A., Thorpe, L. E. & Kontokosta, C. E. (in press). Exposure Density and Neighborhood Disparities in COVID-19 Infection Risk. *PNAS*

# Repository Structure
The repository documents the data processing and analysis perform on the data to support the findings of the study reported in the published article. It is structured as follows:

```
.\root
    |--- data                   # placeholder directory intended to contain raw data
    |--- figures                # figures generated for the publication purposes
    |--- scripts                # contains all scripts used in the study 
```

# Data Description

The study combines a large scale, geolocated mobility data with detailed land cover and land use information in New York City to estimate neighborhood level exposure density and evaluate it's relationship with local COVID-19 rates. All of the data sources used in the paper are listed in the table below.

Dataset | Time range | Resolution (spatial/temporal) | Source | Description | URL
--------|------------|-------------------------------|--------|-------------|----
Mobility data | 2020-02-01∼2020-04-30 | (X,Y)/second | [VenPath, Inc.](https://www.venpath.net/) | More than 127 billion geotagged data points associated with 120 million unique devices every month. | N/A<sup>*</sup>
NYC Primary Land UseTax Lot Output (PLUTO) | updated 2020-02-24 | Parcel/NaN | [NYC Department of City Planning](https://www1.nyc.gov/site/planning/index.page) | Land  use  and  building  type  information  provided. | 
NYC Building Footprints | updated 2020-07-06 | Footprint/NaN | NYC Department of Information Technology & Telecom-munications (DoITT) | Perimeter outlines of more than 1 million buildings in NYC. | 
Road Network Data (LION) | updated 2020-04-28 | Street segment/NaN | NYC Department of Transportation | Single line street base map with associated information on type, width, accessibility etc. |   
NYC COVID-19 data | 2020-04-01∼2020-06-04 | Zipcode/daily | NYC Department of Health and Mental Hygiene | COVID-19  confirmed  cases,  deaths,  and  positivity  rates | https://github.com/nychealth/coronavirus-data
American CommunitySurvey (ACS) | 2018 5-yearestimates | Zipcode/NaN | U.S. Census Bureau | Neighborhood demographic and socioeconomic characteristics. | 
NYC Hospital locations | updated 2017-09-08 | (X,Y)/NaN | NYC Health and Hospital Corporation | Hospitals affiliated with the NYC Health and Hospital Corporation and public hospital system. | 
Nursing home data | updated 2020-05-24 | (X,Y)/NaN | Centers for Disease Control’s NationalHealthcare Safety Network | Nursing home information, including the number of beds and occupancy | 

<sup>*</sup>See Data Availability Statement 

### Data Availability Statement
The annonymized geolocated mobile application activity data that support the findings of this study are available from VenPath, Inc. but restrictions apply to the availability of these data, which were used under license for the current study, and so are not publicly available. Data are however available from the authors upon
reasonable request and with permission of VenPath, Inc.

# System Specifications
Mobility data were provided via dedicated AWS S3 service and were managed in accordance with NYU Institutional Review Board approval IRB-FY2018-1645 and stored and accessed in a secured environment at [New York University’s Center for Urban Science and Progress](cusp.nyu.edu) (NYU CUSP) [Research Computing Facility](https://datahub.cusp.nyu.edu/) (RCF), which is equipped with High Performance Computing (HPC) infrastructure, controlled access, and restricted connectivity. Raw data was deployed to Hadoop Cloudera cluster of 20 nodes with 256 GB memory and 2.1 GHz CPU speed each with a total of 1280 cores and 5.1 TB memory. Initial data processing was conducted using [Apache PySpark](https://spark.apache.org/docs/latest/api/python/index.html) version 2.4. The following analysis performed on the processed data was conducted on RCF's High Memory computing server with total memory of 1TB and Intel(R) Xeon(R) CPU E5-4640 0 @ 2.40GHz (4x8 cores) using predominantly [Python](https://www.python.org/) version 3.7 and [Quantum GIS](https://www.qgis.org/en/site/index.html) version 3.4 Madeira. Each script file relies on a separate set of libraries, which were listed at the begining of each of the file, including library version used for the particular task.

# License

MIT License

Copyright (c) 2021 Urban Intelligence Lab

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

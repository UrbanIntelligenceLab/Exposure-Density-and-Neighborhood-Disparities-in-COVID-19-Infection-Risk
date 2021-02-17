#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" 
Author: Bartosz Bonczak
Description:
This PySPark scripts maps geolocated mobility data for valid users
to specific land use type where the activity occured and counts
number of unique users within each land use type aggregated to 250m x 250m 
neighborhoods in New York City.
"""

# imports
from pyspark.sql.session import SparkSession

from pyspark.sql.functions import col, concat, lit, substring, countDistinct, date_format, to_date, upper
from pyspark.sql.types import * # import types

import numpy as np
from math import sin, cos, sqrt, atan2, radians

spark = SparkSession.builder.getOrCreate()

def distance_km(x1, y1, x2, y2):
	# approximate radius of earth in km
	R = 6373.0
	lat1 = radians(y1)
	lon1 = radians(x1)
	lat2 = radians(y2)
	lon2 = radians(x2)
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))
	distance = R * c
	return distance

# Load grid data
land_use = spark.read.parquet('/raster/grid_classification/parquet_grid_data/')
x_raster_step = 0.000009
y_raster_step = 0.000012

# Load venpath data activity
df = spark.read.parquet('<directory-to-mobility-data-on-HDFS>')

df = df.withColumn('ad_id_upper', upper(col('ad_id')))

# define boundaries extent 
llc_lon = -74.2555954656
llc_lat = 40.4961100684
urc_lon = -73.7000071112
urc_lat = 40.9155259862

# subset data based on bounding box
nyc = df.filter((col('ad_id')!='00000000-0000-0000-0000-000000000000') \
	& (col('lon')>=llc_lon) \
	& (col('lon')<=urc_lon) \
	& (col('lat')>=llc_lat) \
	& (col('lat')<=urc_lat) )

# create date column
nyc = nyc.withColumn("date", to_date(col("timestamp")))

# find valid users based on number of days active
ad_id_count = nyc.groupby("ad_id_upper").agg(countDistinct("date").alias('day_count')).withColumnRenamed("ad_id_upper", "id")
ad_id_count_filtered = ad_id_count.filter((col("day_count")>14))

nyc = nyc.join(ad_id_count_filtered, nyc.ad_id_upper == ad_id_count_filtered.id, how='inner')

# cast raster cell indices
nyc = nyc.withColumn("x_raster_cell", ((nyc["lon"]-llc_lon) / x_raster_step).cast('integer'))
nyc = nyc.withColumn("y_raster_cell", ((nyc["lat"]-llc_lat) / y_raster_step).cast('integer'))

# join with land use raster
nyc = nyc.join(land_use, (nyc.x_raster_cell == land_use.x_cell) & (nyc.y_raster_cell == land_use.y_cell), how='left')

# calculate the extent of the bounding box in kilometers
xx = distance_km(llc_lon, np.mean([llc_lat, urc_lat]), urc_lon, np.mean([llc_lat, urc_lat]))
yy = distance_km(np.mean([llc_lon, urc_lon]), llc_lat, np.mean([llc_lon, urc_lon]), urc_lat)

# find number of 500 m cels in x and y dimension
x_grid = xx / 0.25
y_grid = yy / 0.25

# define the x and y step size in geographic coordinates
x_grid_step = (urc_lon - llc_lon)/x_grid
y_grid_step = (urc_lat - llc_lat)/y_grid

# assign cell x, y, coordiantes and index for each ping
nyc = nyc.withColumn("x_250m_cell", ((nyc["lon"]-llc_lon) / x_grid_step).cast('integer'))
nyc = nyc.withColumn("cell_250m_lon", llc_lon+nyc["x_250m_cell"]*x_grid_step+0.5*x_grid_step)

nyc = nyc.withColumn("y_250m_cell", ((nyc["lat"]-llc_lat) / y_grid_step).cast('integer'))
nyc = nyc.withColumn("cell_250m_lat", llc_lat+nyc["y_250m_cell"]*y_grid_step+0.5*y_grid_step)

nyc = nyc.withColumn('cell_index', concat(col("x_250m_cell"), lit(";"), col("y_250m_cell")))

# create hour column
nyc = nyc.withColumn("hour", date_format(col("timestamp").cast("timestamp"), "yyyy-MM-dd HH:00"))

# count cell aggregations and save to file
hourly_counts = nyc.groupby("hour", "cell_index", "class").agg(countDistinct("ad_id_upper"))

hourly_counts.write \
.format("com.databricks.spark.csv") \
.mode("overwrite") \
.save("/user/bjb417/covid/output/nyc/nyc_land_use/nyc_250mGrid_landUse_uniqueDev_hourlyCounts_active14days.csv")

# save 250m x 250m grid information
grid = nyc.select("cell_index", "x_250m_cell", "y_250m_cell", "cell_250m_lon", "cell_250m_lat") \
	.drop_duplicates(subset=['cell_index'])

grid.write \
.format("com.databricks.spark.csv") \
.mode("overwrite") \
.save("/user/bjb417/covid/output/nyc/nyc_land_use/nyc_250mGrid_landUse_active14days.csv")
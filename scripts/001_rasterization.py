#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 
Author: Bartosz Bonczak
Title: 01_rasterization
Description:
This code generates 1m x 1m raster of land cover and land use 
types within the administrative boundaries of New York City.
The output is then used to map mobility data to the particular 
type of activity inferred from the land use type.

It uses the following layers:
- administrative boundary
- street network
- land use information
- building footprints

Each pixel is classified according to the class mapping dictionary 
in ../data/rasterization/us_cities/code_dictionary.csv.

"""

# Imports
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon, Point
import numpy as np
import os
from geocube.api.core import make_geocube
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from math import sin, cos, sqrt, atan2, radians, degrees
from glob import glob
from datetime import datetime
import warnings 
warnings.filterwarnings('ignore', 'GeoSeries.notna', UserWarning)



# calculate xx, yy distance 
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



# calculate street buffer
def buffer(row):
	try:
		return row['geometry'].buffer(pd.to_numeric(row['width'], errors='coerce'))
	except:
		return np.nan



# data loader helper
def data_loader(layer_type):
	layer_file = glob(city_dir+'/{}/*.shp'.format(layer_type))[0]
	layer = gpd.read_file(layer_file)
	layer.dropna(subset=['geometry'], inplace=True)
	layer = layer[layer.geometry.notnull()]
	return layer_file, layer



# boundary processing
def process_boundary(boundary):
	if boundary.crs == {}:
		boundary.crs = crs
	elif boundary.crs == crs:
		pass
	else:
		boundary = boundary.to_crs(crs)
	boundary['code'] = 2

	# evaluate the number of boundary vertices for simplification purposes
	for i, row in boundary.iterrows():
		# It's better to check if multigeometry
		multi = row.geometry.type.startswith("Multi")
		if multi:
			n = 0
			# iterate over all parts of multigeometry
			for part in row.geometry:
				n += len(part.exterior.coords)
		else:
			n = len(row.geometry.exterior.coords)
		n_vertices.append(n)
	return boundary



def process_streets(layer):
	if layer.crs == {}:
		layer.crs = crs_m
	elif layer.crs == crs_m:
		pass
	else:
		layer = layer.to_crs(crs_m)

	lion_dict = {
		'0':'road',
		'1':'other transportation',
		'2':None,
		'3':None,
		'5':'open space',
		'6':'road',
		'7':None,
		'8':None,
		'9':None,
		'A':'sidewalk',
		'W':'sidewalk',
		'C':'road',
		'F':'other transportation'
	}

	layer['road_type'] = layer['FeatureTyp'].map(lion_dict)
	layer['road_type'] = np.where(layer['NonPed']=='V', 'highway', layer['road_type'])
	layer['width'] = layer['StreetWidt']*0.5*0.3048

	layer = layer[['road_type', 'width', 'geometry']]
	layer['geometry'] = layer.apply(buffer, axis=1)
	layer = layer[layer.geometry.notnull()]
	layer = layer.to_crs(crs)
	layer['code'] = layer.road_type.map(codes_dict)
	layer = gpd.clip(layer, boundary_sim.geometry)
	layer = layer[['code','geometry']].append(additions, ignore_index=True)
	return layer



def process_lu(layer, layer_file):
	if layer.crs == {}:
		layer.crs = crs
	elif layer.crs == crs:
		pass
	else:
		try:
			layer = layer.to_crs(crs)
		except ValueError:
			layer.crs = crs
	
	lu_mapping_subset = lu_mapping[lu_mapping['File']==layer_file]
	column_name = lu_mapping_subset['Column'].unique().item()
	column_type = lu_mapping_subset['DataType'].unique().item()
	lu_type_dict =  pd.Series(data=lu_mapping_subset['Label'].values, index=lu_mapping_subset['Type'].astype(column_type, errors='ignore').astype(str)).to_dict()
	
	# map land use type
	layer['lu_type'] = layer[column_name].astype(str).map(lu_type_dict)

	# map land use codes
	layer['code'] = layer.lu_type.map(codes_dict)

	# clean layer data
	layer = layer[layer.geometry.notnull()]

	# trick to solve problems with invalid geometries
	layer['geometry'] = layer.buffer(0)

	# clip layer
	layer = gpd.clip(layer, boundary_sim.geometry)

	# assign empty features in the corners to maintain same extent
	layer = layer[['code','geometry']].append(additions, ignore_index=True)

	return layer

def process_bldg(layer):
	if layer.crs == {}:
		layer.crs = crs
	elif layer.crs == crs:
		pass
	else:
		layer = layer.to_crs(crs)

	# assign bldg code
	layer['code'] = 1

	#check for valid features only
	layer = layer[layer.geometry.notnull()]

	# trick to solve problems with invalid geometries
	layer['geometry'] = layer.buffer(0)
	layer = gpd.clip(layer, boundary_sim.geometry)

	# assign empty features in the corners to maintain same extent
	layer = layer[['code','geometry']].append(additions, ignore_index=True)

	return layer


# create new polygons in the corner of the extent
def generate_additions(boundary):
	additions = gpd.GeoDataFrame(
		[Polygon([[
			boundary.total_bounds[0], boundary.total_bounds[1]],
			[boundary.total_bounds[0]+0.00000001, boundary.total_bounds[1]],
			[boundary.total_bounds[0]+0.00000001, boundary.total_bounds[1]+0.00000001],
			[boundary.total_bounds[0], boundary.total_bounds[1]+0.00000001]]),
		Polygon([[
			boundary.total_bounds[2], boundary.total_bounds[3]],
			[boundary.total_bounds[2]-0.00000001, boundary.total_bounds[3]],
			[boundary.total_bounds[2]-0.00000001, boundary.total_bounds[3]-0.00000001],
			[boundary.total_bounds[2], boundary.total_bounds[3]-0.00000001]])
		], columns=['geometry'])
	return additions



# estimate city extent in kilometers
def estimate_layer_extent(llc_lon, llc_lat, urc_lon, urc_lat):
	# calculate the extent of the bounding box in kilometers
	if urc_lon > 0 + (180-abs(llc_lon)):
		C = 40075 # Earth circumference in km
		c_lat = round(cos(radians(np.mean([llc_lat, urc_lat]))), 10)*C # latitudial circumference at given latitude
		xx = c_lat - distance_km(llc_lon, np.mean([llc_lat, urc_lat]), urc_lon, np.mean([llc_lat, urc_lat]))
	else:
		xx = distance_km(llc_lon, np.mean([llc_lat, urc_lat]), urc_lon, np.mean([llc_lat, urc_lat]))
	yy = distance_km(np.mean([llc_lon, urc_lon]), llc_lat, np.mean([llc_lon, urc_lon]), urc_lat)
	return xx, yy



# calculate step for chosen grid cell size
def grid_cell_step(xx, yy, cell_size):
	# find number of cells in x and y dimension
	x_grid = xx / cell_size
	y_grid = yy / cell_size
	# define the x and y step size in geographic coordinates
	x_grid_step = (urc_lon - llc_lon)/x_grid
	y_grid_step = (urc_lat - llc_lat)/y_grid
	return x_grid_step, y_grid_step



# define rasterization function
def rasterize(layer, layer_type):
	if layer_type == 'Boundary':
		raster = make_geocube(
			vector_data=layer,
			measurements=['code'],
			resolution=(x_grid_step, y_grid_step),
			fill=0   # optional
		)
	else:
		raster = make_geocube(
			vector_data=layer,
			measurements=['code'],
			resolution=(x_grid_step, y_grid_step),
			# fill=999   # optional
		)
	return raster



def array_alignment(array, base_array):
	if array.shape != base_array.shape:
		x_diff = array.shape[0] - base_array.shape[0]
		y_diff = array.shape[1] - base_array.shape[1]
		# evaluate the differences in raster size
		# x dimension
		if (x_diff >= 0):
			x_pad = int(x_diff/2)
		else:
			x_pad = 0
		# y dimension
		if (y_diff >= 0):
			y_pad = int(y_diff/2)
		else:
			y_pad = 0
		# align the arrays accordingly
		array = array[x_pad:base_array.shape[0], y_pad:base_array.shape[1]]
	else:
		pass
	return array




if __name__ == '__main__':

	script_start = datetime.now()
	print('Start the rasterization process on {}'.format(script_start))

	print('Specify global variables...')

	# specify path to data
	mypath = '../data/rasterization/us_cities/'

	# Load land use documentation file and convert to dictionary
	lu_mapping = pd.read_csv('{}/land_use_mapping.csv'.format(mypath))

	# Load land use codes documentation file and convert to dictionary
	codes = pd.read_csv('{}/code_dictionary.csv'.format(mypath))
	codes_dict = pd.Series(data=codes['code'].values, index=codes['land_use_cat']).to_dict()

	# specify preferred CRS
	crs = {'init': 'epsg:4326'}
	crs_m = {'init': 'epsg:3857'}

	# assign cell size in kilometers
	cell_size = 0.001

	number_of_chunks = 200

	city_list = [c for c in glob('{}/*'.format(mypath))]

	print('Start processing city specific data...')
	print('======================================')
	print('')
	# For each city directory
	for city_dir in glob(mypath+'/*'):

		city_start = datetime.now()
		print('Start processing {} on {}'.format(city_dir.split('/')[-1], city_start))

		boundary = None
		n_vertices=[]
		boundary_sim = None
		llc_lon, llc_lat, urc_lon, urc_lat = (None, None, None, None)
		x_grid_step, y_grid_step = (None, None)
		additions = None
		# land_use_raster = None
		base_raster = None
		base_array = None

		# for each layer
		for layer_type in ['Boundary', 'Streets', 'Land Use', 'Buildings']:
			layer_start = datetime.now()

			print('    - start processing {} layer...'.format(layer_type))
			# Load data...
			layer_file, layer = data_loader(layer_type)

			# process each layer and update base raster
			# process boundary, get extent and raster resolution
			if layer_type == 'Boundary':
				layer = process_boundary(layer)
				additions = generate_additions(layer)
				llc_lon, llc_lat, urc_lon, urc_lat = layer.geometry.total_bounds
				xx, yy = estimate_layer_extent(llc_lon, llc_lat, urc_lon, urc_lat)
				x_grid_step, y_grid_step = grid_cell_step(xx, yy, cell_size)

				# # convert data to integers
				base_raster = rasterize(layer, layer_type)
				base_array = np.array(base_raster['code'], dtype='float32')
				print('raster shape = {}'.format(base_array.shape))

				boundary_sim = layer.copy()
				if n_vertices[0]>10000:
					boundary_sim['geometry'] = boundary_sim.simplify(.001, preserve_topology=True)
				else:
					boundary_sim

			# process streets layer and fill in base raster
			elif layer_type == 'Streets':
				layer = process_streets(layer)

				raster = rasterize(layer, layer_type)
				array = np.array(raster['code'], dtype='float32')
				print('raster shape = {}'.format(array.shape))
				array = array_alignment(array, base_array)
				base_array = np.where(np.isnan(array), base_array, array)
				base_raster.code.values = base_array

			# process land use layer and fill in base raster
			elif layer_type == 'Land Use':
				layer = process_lu(layer, layer_file)
				raster = rasterize(layer, layer_type)
				array = np.array(raster['code'], dtype='float32')
				print('raster shape = {}'.format(array.shape))
				array = array_alignment(array, base_array)
				base_array = np.where(np.isnan(array), base_array, array)
				base_raster.code.values = base_array

			# process buildings layer and sum with base layer
			else:
				layer = process_bldg(layer)
				raster = rasterize(layer, layer_type)
				array = np.array(raster['code'], dtype='float32')
				array = np.sum((base_array, array), axis=0)
				print('raster shape = {}'.format(array.shape))
				array = array_alignment(array, base_array)
				base_array = np.where(np.isnan(array), base_array, array)
				base_raster.code.values = base_array

			print('    - finished after {}'.format(datetime.now() - layer_start))
			print('')

		base_raster.code.values = base_array.astype(float)

		raster_path = city_dir+'/raster/'

		os.mkdir(raster_path)

		# Save raster data as parquet files
		grid_data_start = datetime.now()
		print('    - start convert grid data to DF...')

		raster_data_path = city_dir+'/raster/grid_classification/'

		os.mkdir(raster_data_path)

		# generate grid cell locations
		x_coors = pd.DataFrame(base_raster.coords.indexes['x'])
		x_coors.columns = ['lon']
		x_coors.to_csv(raster_data_path + 'x_coors.csv')

		y_coors = pd.DataFrame(base_raster.coords.indexes['y'])
		y_coors.columns = ['lat']
		y_coors.to_csv(raster_data_path + 'y_coors.csv')

		# generate grid specification dataframe
		grid_classification = pd.DataFrame(data={
			'class':base_array.flatten(),
			'lon':x_coors.lon.tolist()*base_array.shape[0],
			'lat':np.array([[y]*base_array.shape[1] for y in y_coors.lat.tolist()]).flatten(),
			'x_cell':x_coors.index.tolist()*base_array.shape[0],
			'y_cell':np.array([[y]*base_array.shape[1] for y in y_coors.index.tolist()]).flatten()
		})

		# save as parquet file with gzip compression
		print('    - start saving grid data to parquet...')
		grid_classification.to_parquet(raster_data_path + 'parquet_grid_data.gz', compression='gzip')

		print('    - finished saving to parquet after {}'.format(datetime.now() - grid_data_start))
		print('')
		print('Done processing {} after {}'.format(city_dir.split('/')[-1], datetime.now()-city_start))
		print('======================================')
		print('')

	print('Script finished after {}'.format(datetime.now()-script_start))

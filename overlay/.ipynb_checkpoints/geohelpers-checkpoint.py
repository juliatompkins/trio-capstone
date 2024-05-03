from osgeo import osr, ogr, gdal
import pyproj
from pyproj import Proj, transform
import geopandas as gpd
import numpy as np
import rasterio
import pandas as pd
import seaborn as sns
import matplotlib as plt
from sklearn.model_selection import train_test_split
from sklearn import svm
import math
import datetime

############################################################################################################################################function which will take in LatLon coordinates of the training data and output an array index, which will co-locate training data points to the training data labels 
def collocate(x,y,td_raster_path):
    # coordinates to get array values for
    points = [(x, y)]
    # open the raster file
    ds = gdal.Open(td_raster_path)
    ds_arr = rasterio.open(td_raster_path).read()
    b,h,l = ds_arr.shape

    # get georeference info
    transform = ds.GetGeoTransform() # (-2493045.0, 30.0, 0.0, 3310005.0, 0.0, -30.0)
    xOrigin = transform[0] # -2493045.0 for new delhi ue
    yOrigin = transform[3] # 3310005.0 for new delhi ue 
    pixelWidth = transform[1] # 30.0 for landsat
    pixelHeight = transform[5] # -30.0 for landsat

    band = ds.GetRasterBand(1) # 1-based index
    data = band.ReadAsArray()
    # loop through the coordinates
    for point in points:
        x = point[0]
        y = point[1]

        xOffset = int((x - xOrigin) / pixelWidth)
        yOffset = int((y - yOrigin) / pixelHeight)
        # get individual pixel values
    return xOffset,yOffset

############################################################################################################################################function which will take in a single row of shapefile df, convert to geographic CRS if necessary, and return its latLon values
def getCoords(shp_path, fid):

    shapefile = ogr.Open(shp_path)
    layer = shapefile.GetLayer(0)
    
    #define projected->geographic point transformer for later use
    inProj = Proj('epsg:3857')
    outProj = Proj('epsg:4326')
    
    convert2Geo = False
    #conditional for whether or not transorming is necessary by determining if projected or geographic CRS
    if (gpd.read_file(shp_path).crs) == "epsg:3857":
        convert2Geo = True 
        
    feature = layer.GetFeature(fid)
    lon = feature['LON']
    lat = feature['LAT']
    #lc_class = feature['class']
    
        #if in projected CRS, transform extents to geographic
    if convert2Geo == True:
        finalLon,finalLat = transform(inProj,outProj,lon, lat)
        lon = finalLon
        lat = finalLat
    else:
        return lon,lat #,lc_class
    return lon, lat #, lc_class
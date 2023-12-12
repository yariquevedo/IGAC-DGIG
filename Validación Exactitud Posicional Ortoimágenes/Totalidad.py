# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Direccion de Gestion de Información Geografica
# Created on: 2023-11-28
# Created by: Kelly Garro
# # Usage: Validacion ORTOIMAGENES
# Description:
# ---------------------------------------------------------------------------
import os
import arcpy
from arcpy import env
from arcpy.sa import *

arcpy.env.overwriteOutput = True

dataset = arcpy.GetParameterAsText(0) #mdt
limite = arcpy.GetParameterAsText(1) #shp limite
salida = arcpy.GetParameterAsText(2) #folder salida

def validar(dataset, limite, salida):

    desc = arcpy.Describe(dataset) #raster
    nombre_reporte = 'Reporte_Porcentaje_Omision_'+str(desc.Name[0:-4])+'.txt'

    arrow = "=============================================="
    espacio= '	'

    background = os.path.join(salida,'background.tif')
    background_shp = os.path.join(salida,'background.shp')
    copy_raster = os.path.join(salida,'raster_2.shp')
    copy_limite = os.path.join(salida,'limite_2.shp')
    omision = os.path.join(salida, 'omision.shp')

    #crear el poligono del extent
    sr = arcpy.SpatialReference(9377)
    arcpy.management.CreateFeatureclass(salida, 'raster_limite.shp', 'POLYGON', spatial_reference = sr)
    xmax = desc.Extent.XMax
    xmin = desc.Extent.XMin
    ymax = desc.Extent.YMax
    ymin = desc.Extent.YMin
    array = arcpy.Array([arcpy.Point(xmin, ymin),
                        arcpy.Point(xmin, ymax),
                        arcpy.Point(xmax, ymax),
                        arcpy.Point(xmax, ymin)
                        ])
    polygon = arcpy.Polygon(array)
    cursor = arcpy.da.InsertCursor(os.path.join(salida, 'raster_limite.shp'), ['SHAPE@'])
    cursor.insertRow([polygon])

    arcpy.management.CopyFeatures(limite, copy_limite, '', '', '') #limite
    attExtract = ExtractByAttributes(dataset, "VALUE = 0") #background tif
    attExtract.save(background)
    arcpy.conversion.RasterToPolygon(background, background_shp, 'NO_SIMPLIFY') #background shp

    arcpy.management.AddField(background_shp, 'AREA_m2','DOUBLE')
    arcpy.management.CalculateGeometryAttributes(background_shp, [["AREA_m2", "AREA"]],"METERS", "SQUARE_METERS") #calcular area  background

    select = arcpy.management.SelectLayerByAttribute(background_shp, 'NEW_SELECTION', "AREA_m2 > 1", 'NON_INVERT') #selecciona sin poligonos basura
    arcpy.management.CopyFeatures(select, os.path.join(salida, "select.shp"), '', '', '', '') #limite
    
    arcpy.analysis.Erase(os.path.join(salida,'raster_limite.shp'),os.path.join(salida, "select.shp"), copy_raster) #limite

    #interseccion para ver el area de omision
    arcpy.analysis.Intersect([copy_limite,copy_raster], omision)
    arcpy.management.AddField(omision, 'AREA_m2','DOUBLE')
    arcpy.management.CalculateGeometryAttributes(omision, [["AREA_m2", "AREA"]],"METERS", "SQUARE_METERS")

    arcpy.management.AddField(copy_limite, 'AREA_m2','DOUBLE')
    arcpy.management.CalculateGeometryAttributes(copy_limite, [["AREA_m2", "AREA"]],"METERS", "SQUARE_METERS")


    #area intersect omision
    with arcpy.da.SearchCursor(omision, ['AREA_m2']) as cursor:
        b = 0
        for row in cursor:
            b += row[0]

    #area limite 
    with arcpy.da.SearchCursor(copy_limite, ['AREA_m2']) as cursor:
        a=0
        for row in cursor:
            a += row[0]

    file = open(os.path.join(str(salida),nombre_reporte), "w") 
    file.write(    'Reporte Porcentaje Omision ORTO\n' +
                    arrow +
                    '\nDatos Generales Ortoimagen'+
                    '\n\nNombre:' + espacio + str(desc.Name) +
                    '\nTipo:' + espacio + str(desc.dataType) + '\n\n'+
                    arrow +
                    '\nVariables'+
                    '\n\nArea limite proyecto:' + espacio + str(a) +
                    '\nArea omitida:' + espacio + espacio + str(a-b) + 
                    '\nPorcentaje de Omision:' + espacio + str(((a-b)/a)*100)+'%'
               )
    file.close()
    arcpy.management.Delete([background,background_shp,copy_limite,copy_raster,omision,os.path.join(salida, "select.shp"),os.path.join(salida,'raster_limite.shp')])


if __name__ == '__main__':
    
    arcpy.AddMessage("Validando el porcentaje de omision")
    validar(dataset, limite, salida)
    arcpy.AddMessage("Finalizado, el reporte fue generado en la ruta de salida indicada")
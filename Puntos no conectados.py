#Semillero de Investigación y Desarrollo
#Yaritza Quevedo
#------------------------------------------------------------------------------

import arcpy
import os

#Definir variables 

DGN_Entrada = arcpy.GetParameterAsText(0)
Ruta_Salida = arcpy.GetParameterAsText(1)
 
V1= arcpy.GetParameterAsText(2)
V2= arcpy.GetParameterAsText(3)
V3= arcpy.GetParameterAsText(4)
arcpy.env.overwriteOutput = True

#Funciones 
def CAD_to_GDB(DGN_Entrada_Entrada, Ruta_Salida):
    gdb = arcpy.management.CreateFileGDB(Ruta_Salida, 'vectores_GDB')
    cad= arcpy.conversion.CADToGeodatabase(DGN_Entrada, gdb, 'vectores', '10000', 'PROJCS["MAGNA-SIRGAS_Origen-Nacional",GEOGCS["GCS_MAGNA",DATUM["D_MAGNA",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",5000000.0],PARAMETER["False_Northing",2000000.0],PARAMETER["Central_Meridian",-73.0],PARAMETER["Scale_Factor",0.9992],PARAMETER["Latitude_Of_Origin",4.0],UNIT["Meter",1.0]];-618700 -8436100 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision')
    return cad

#Bosques y curvas de nivel 

SQL1 = "Layer = 'Level 40' OR Layer = 'Level 30' or Layer = 'Level 42' OR Layer = 'Level 43'" #Cuando hay 2 SQL en una función se tiene que sacar uno como variable y agregarlo como parámetro a la función 

def Seleccion_vectores(cad, ruta_salida,SQL1):
    SQL2 = "Layer = 'Level 62' OR Layer = 'Level 61' or Layer = 'Level 63'" #Niveles del muro, del borde del dgn
    select= arcpy.management.SelectLayerByAttribute(os.path.join(Ruta_Salida,'vectores_GDB.gdb','vectores/Polyline'), "NEW_SELECTION", SQL1)
    limite= arcpy.management.SelectLayerByAttribute(os.path.join(Ruta_Salida,'vectores_GDB.gdb','vectores/Polyline'), "NEW_SELECTION", SQL2)
    select_localizacion = arcpy.management.SelectLayerByLocation(select, "INTERSECT",limite, selection_type= "REMOVE_FROM_SELECTION", search_distance=1)
    copia =arcpy.management.CopyFeatures(select_localizacion, os.path.join(Ruta_Salida, 'seleccion.shp'))
    return copia

def Points(seleccion,ruta_salida):
    dangles = arcpy.management.FeatureVerticesToPoints(seleccion, os.path.join(ruta_salida,'Dangles.shp'), "DANGLE")
    return dangles

def Buffer(dangles, ruta_salida):
    buffer = arcpy.analysis.Buffer(dangles, os.path.join(Ruta_Salida, 'buffer.shp') , buffer_distance_or_field= 2)
    return buffer

def GDB_to_CAD(buffer, ruta_salida):
    cad_export = arcpy.conversion.ExportCAD(buffer, 'DGN_V8', os.path.join(Ruta_Salida, 'cad_export.dgn'), Seed_File=r"C:\Program Files\ArcGIS\Pro\Resources\ArcToolBox\Templates\CAD\template3d_Metric.dgn")

# Drenajes

def Drenajes(cad, ruta_salida):
    SQL3="Layer = 'Level 1' or Layer = 'Level 2' or Layer = 'Level 4' or Layer = 'Level 7' or Layer = 'Level 17' or Layer = 'Level 16' or Layer = 'Level 8'"
    select_attribute= arcpy.management.SelectLayerByAttribute(os.path.join(Ruta_Salida,'vectores_GDB.gdb','vectores/Polyline'), "NEW_SELECTION", SQL3)
    copia =arcpy.management.CopyFeatures(select_attribute, os.path.join(Ruta_Salida, 'seleccion_drenajes.shp'))
    return copia

def Points_drenajes_star(seleccion_drenajes, ruta_salida):
    drenajes_star = arcpy.management.FeatureVerticesToPoints(seleccion_drenajes, os.path.join(Ruta_Salida,'Drenajes_star.shp'), "START")
    return drenajes_star

def Drenajes_dangles (drenajes, ruta_salida):
    drenajes_star = arcpy.management.FeatureVerticesToPoints(drenajes, os.path.join(Ruta_Salida,'Drenajes_dangles.shp'), "DANGLE")
    return drenajes_star

def Switch_drenajes(drenajes_star, drenajes_dangles, ruta_salida):
    SQL2 = "Layer = 'Level 62' OR Layer = 'Level 61' or Layer = 'Level 63'"
    errores_drenajes = arcpy.management.SelectLayerByLocation(drenajes_dangles, "INTERSECT", drenajes_star, invert_spatial_relationship= True, search_distance=10)
    #limite= arcpy.management.SelectLayerByAttribute(os.path.join(Ruta_Salida,'vectores_GDB.gdb','vectores/Polyline'), "NEW_SELECTION", SQL2)
    #new_rows = arcpy.management.SelectLayerByLocation(errores, "INTERSECT", limite, selection_type= "REMOVE_FROM_SELECTION")
    buffer_drenajes= arcpy.analysis.Buffer(errores_drenajes, os.path.join(Ruta_Salida, 'Drenajes_errores.shp') , buffer_distance_or_field= 2)
    limite= arcpy.management.SelectLayerByAttribute(os.path.join(Ruta_Salida,'vectores_GDB.gdb','vectores/Polyline'), "NEW_SELECTION", SQL2)
    limite_capa = arcpy.management.CopyFeatures(limite, os.path.join(Ruta_Salida, 'copy_limites_d.shp'))
    new_rows = arcpy.management.SelectLayerByLocation(buffer_drenajes, "INTERSECT", limite_capa, selection_type= "NEW_SELECTION")
    arcpy.management.DeleteRows(new_rows)
    cad_drenajes= arcpy.conversion.ExportCAD(buffer_drenajes, 'DGN_V8', os.path.join(Ruta_Salida, 'cad_export_drenajes.dgn'), Seed_File=r"C:\Program Files\ArcGIS\Pro\Resources\ArcToolBox\Templates\CAD\template3d_Metric.dgn")
    return buffer_drenajes
#El seed_file siempre es el mismo para export dgn

#Vias
def Vias_dangles(cad, ruta_salida):
    SQL4="Layer = 'Level 20' or Layer = 'Level 18' or Layer = 'Level 19' or Layer = 'Level 53'  or Layer = 'Level 54'  or Layer = 'Level 55'"
    select_attribute_vias= arcpy.management.SelectLayerByAttribute(os.path.join(Ruta_Salida,'vectores_GDB.gdb','vectores/Polyline'), "NEW_SELECTION", SQL4)
    copy_vias =arcpy.management.CopyFeatures(select_attribute_vias, os.path.join(Ruta_Salida, 'seleccion_vias.shp'))
    return copy_vias

def Points_vias_star(seleccion_vias, ruta_salida):
    vias_star = arcpy.management.FeatureVerticesToPoints(seleccion_vias, os.path.join(Ruta_Salida,'vias_star.shp'), "START")
    return vias_star

def Points_vias_dangle(seleccion_vias, ruta_salida):
    vias_dangle = arcpy.management.FeatureVerticesToPoints(seleccion_vias, os.path.join(Ruta_Salida,'vias_dangle.shp'), "DANGLE")
    return vias_dangle

def Switch_vias(vias_star, vias_dangles, ruta_salida):
    SQL2 = "Layer = 'Level 62' OR Layer = 'Level 61' or Layer = 'Level 63'"
    errores_vias = arcpy.management.SelectLayerByLocation(vias_dangles, "INTERSECT", vias_star, invert_spatial_relationship= True, search_distance=10)
    buffer_vias= arcpy.analysis.Buffer(errores_vias, os.path.join(Ruta_Salida, 'vias_errores.shp') , buffer_distance_or_field= 2)
    limite_v= arcpy.management.SelectLayerByAttribute(os.path.join(Ruta_Salida,'vectores_GDB.gdb','vectores/Polyline'), "NEW_SELECTION", SQL2)
    limite_capa_v = arcpy.management.CopyFeatures(limite_v, os.path.join(Ruta_Salida, 'copy_limites_v.shp'))
    new_rows_v = arcpy.management.SelectLayerByLocation(buffer_vias, "INTERSECT", limite_capa_v, selection_type= "NEW_SELECTION")
    arcpy.management.DeleteRows(new_rows_v)
    cad_drenajes= arcpy.conversion.ExportCAD(buffer_vias, 'DGN_V8', os.path.join(Ruta_Salida, 'cad_export_vias.dgn'), Seed_File=r"C:\Program Files\ArcGIS\Pro\Resources\ArcToolBox\Templates\CAD\template3d_Metric.dgn")
    return buffer_vias

if __name__ == '__main__':
    vectores= CAD_to_GDB(DGN_Entrada, Ruta_Salida)
    if V1 == 'true': #Cuando se selecciona el botón se ejecuta 
        arcpy.AddMessage("--------------------------------------------------------------")
        SQL1 = "Layer = 'Level 40' OR Layer = 'Level 30' or Layer = 'Level 42' OR Layer = 'Level 43'"
        arcpy.AddMessage("seleccionando bosques y curvas de nivel")
        seleccion = Seleccion_vectores(vectores,Ruta_Salida,SQL1)
        arcpy.AddMessage("Se encontraron " + str(arcpy.management.GetCount(seleccion)) + " vectores en total") #arcpy.management.GetCount para realizar conteos 
        dangles = Points(seleccion,Ruta_Salida)
        arcpy.AddMessage("Se encontraron " + str(arcpy.management.GetCount(dangles)) + " errores en total")
        buffer = Buffer(dangles, Ruta_Salida)
        GDB_to_CAD(buffer, Ruta_Salida)
        
    if V2 == 'true':
        arcpy.AddMessage("--------------------------------------------------------------")
        drenajes = Drenajes(vectores, Ruta_Salida)
        arcpy.AddMessage("seleccionando drenajes")
        drenajes_star = Points_drenajes_star(drenajes, Ruta_Salida)
        arcpy.AddMessage("generando puntos de inicio")
        drenajes_dangles = Drenajes_dangles(drenajes, Ruta_Salida)
        arcpy.AddMessage("generando puntos dangles")
        Switch_drenajes = Switch_drenajes(drenajes_star, drenajes_dangles, Ruta_Salida)
        arcpy.AddMessage("Se encontraron " + str(arcpy.management.GetCount(Switch_drenajes)) + " errores en total")
        

    if V3 == 'true':
        arcpy.AddMessage("--------------------------------------------------------------")
        vias= Vias_dangles(vectores, Ruta_Salida)
        arcpy.AddMessage("seleccionando vias")
        vias_star = Points_vias_star(vias, Ruta_Salida)
        arcpy.AddMessage("generando puntos de inicio")
        vias_dangles= Points_vias_dangle(vias, Ruta_Salida)
        arcpy.AddMessage("seleccionando dangles")
        final_via=Switch_vias(vias_star, vias_dangles, Ruta_Salida)
        arcpy.AddMessage("Se encontraron " + str(arcpy.management.GetCount(final_via)) + " errores en total")
       
        

    
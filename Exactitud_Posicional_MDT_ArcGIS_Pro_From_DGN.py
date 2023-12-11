# -*- #################
# ---------------------------------------------------------------------------
# Direccion de Gestion de Información Geografica
# Created on: 2023-11-20
# Created by: Gabriel Hernan Gonzalez Buitrago
# # Usage: Validador de exactitud posicional 
# Description:
# ---------------------------------------------------------------------------

# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Direccion de Gestion de Información Geografica
# Created on: 2023-06-22
# Created by: Juan Pablo Merchán Puentes - Diego Rugeles (Supervisor Desarrollo DGIG)
# # Usage: ModelosDigitalesDeTerrenos
# Description:
# ---------------------------------------------------------------------------
# Importe librerias
import arcpy
import os
import math
from arcpy.sa import *
from datetime import datetime

ruta_dgn = arcpy.GetParameterAsText(0)
ruta_raster = arcpy.GetParameterAsText(1)
ruta_salida = arcpy.GetParameterAsText(2)

arcpy.env.overwriteOutput = True

def tiempo_actual():
    hora_actual = datetime.now()
    return str(hora_actual.hour)+str(hora_actual.minute)+str(hora_actual.hour)

#Crear GDB:
def crearGDB(path):
    GDB_output= arcpy.CreateFileGDB_management(out_folder_path=path,out_name='GDB_salida')
    return GDB_output

#Convertir CAD a GDB: 
def convertirCADtoGDB(CAD, GDB, dataset_name):
    arcpy.conversion.CADToGeodatabase(input_cad_datasets=CAD, out_gdb_path=GDB, out_dataset_name=dataset_name, reference_scale=1000, spatial_reference='PROJCS["MAGNA-SIRGAS_Origen-Nacional",GEOGCS["GCS_MAGNA",DATUM["D_MAGNA",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",5000000.0],PARAMETER["False_Northing",2000000.0],PARAMETER["Central_Meridian",-73.0],PARAMETER["Scale_Factor",0.9992],PARAMETER["Latitude_Of_Origin",4.0],UNIT["Meter",1.0]];-618700 -8436100 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision')
    select_level_61=arcpy.management.SelectLayerByAttribute (os.path.join (ruta_salida, 'GDB_salida.gdb', 'limite', 'Polygon'), "NEW_SELECTION", "Layer = 'Level 61'")
    level_61=arcpy.conversion.ExportFeatures(select_level_61, os.path.join (ruta_salida, 'GDB_salida.gdb', 'limite', 'Nivel_61'))
    return level_61

def make_points_from_dgn(ruta_dgn,ruta_salida):
    GDB_output=crearGDB(ruta_salida)  #Generar GDB de salida
    arcpy.env.workspace=str(GDB_output)  #Se define espacio de trabajo
    arcpy.env.overwriteOutput = True

    convertirCADtoGDB(ruta_dgn, GDB_output, 'limite')   #Conversion CAD a GDB

    #Se filtran los niveles requeridos: 
    polyline=os.path.join(str(GDB_output), 'limite','Polyline')
    polyline_filtered=arcpy.conversion.FeatureClassToFeatureClass(polyline, out_path=GDB_output, out_name="line_filtered", where_clause="Level IN (1,2,4,7,8,16,17,18,19,20,53,54,55,42,43,44,45)")     

    #Se convierten las polilineas a punto:
    PointsfromLine=arcpy.management.FeatureVerticesToPoints(polyline_filtered, os.path.join(str(GDB_output),"Extracted_Points"), "BOTH_ENDS")

    select_by_location_points=arcpy.management.SelectLayerByLocation(os.path.join (ruta_salida, 'GDB_salida.gdb', 'Extracted_Points'), "WITHIN", os.path.join (ruta_salida, 'GDB_salida.gdb', 'limite', 'Nivel_61'), selection_type="NEW_SELECTION", invert_spatial_relationship=True)
    Delete_rows=arcpy.management.DeleteRows(select_by_location_points)
    arcpy.AlterField_management(select_by_location_points, "Elevation", "COTA", "COTA")

    #Se crean campos para almacenar las variables de ESTE y NORTE y se realiza el calculo:
    arcpy.AddField_management(select_by_location_points, "ESTE", "Double")
    arcpy.AddField_management(select_by_location_points, "NORTE", "Double")
    arcpy.management.CalculateGeometryAttributes(in_features=select_by_location_points,  geometry_property="ESTE POINT_X;NORTE POINT_Y", coordinate_format="SAME_AS_INPUT")

    #Se limpian campos resultantes de importar el DGN
    arcpy.DeleteField_management(select_by_location_points, ["Entity","Handle","Layer","LvlDesc","LyrFrzan","LyrLock","LyrOn","LvlPlot","Color","EntColor","LyrColor","Linetype","EntLinetyp","LyrLnType","Class","GGroup","CadModel","CadMopdelID","Fill","LineWt","EntLineWt","LyrLineWt","LyrFrzn","EntLinetype","CadModelID","RefName","LTScale","QrotW","QrotX", "QrotY", "QrotZ", "DocName","DocPath","DocType","DocVer","DocUpdate","DocId"])

    return select_by_location_points


def RMSE (fotocontrol, ruta_raster, ruta_salida):
    
    file = open(os.path.join(str(ruta_salida),'Report_RMSE.txt'), "w") 
    #variables de entorno
    arrow = "=============================================="
    espacio= '	'
    
    Foto_2 = arcpy.MakeFeatureLayer_management(fotocontrol, os.path.join(str(ruta_salida),'ly_2_temp.shp'))#Capa falsa- punto
    
    arcpy.management.AddField(Foto_2, 'altura', 'double') #Agregar Campo
    arcpy.management.CalculateGeometryAttributes(Foto_2, [['altura','POINT_Z']], 'METERS') #Calculo distacia punto z

    Puntos_Validacion= ExtractValuesToPoints(Foto_2, ruta_raster, os.path.join(str(ruta_salida),"Puntos_Raster.shp"))
    
    
    arcpy.AddField_management(Puntos_Validacion, 'Z_RMSE', 'double')
    arcpy.CalculateField_management(Puntos_Validacion, 'Z_RMSE', '(!altura!-!RASTERVALU!)**(2)','PYTHON3')
    #arcpy.Delete_management(Foto_2)
    cont_id = 0
    with arcpy.da.SearchCursor(Puntos_Validacion, ['Z_RMSE']) as cursor:
        file.write('\nPositional Accuracy Report\n' + arrow +
                   '\n\nSpatial Reference Information\n'+
                   str(arcpy.Describe(fotocontrol).spatialReference.Name)+'\n'+arrow+
                   '\n\nPoint'+espacio+espacio+espacio+'delta Z')
        
        suma_z = 0
        
        for row in cursor:
            file.write('\n'+ str(cont_id+1) + espacio +espacio +espacio +
                       str(math.sqrt(row[0])) )
            
            suma_z += row[0]
            cont_id = cont_id+1
            
        n = str(arcpy.management.GetCount(Puntos_Validacion))
        
        rmse_z = suma_z/float(n)
        rmse_r = math.sqrt(rmse_z + rmse_z)
        rmse_e =rmse_r*1.96
        arcpy.AddMessage('El RMSE total es: ' + str(round(rmse_r, 2)))
        file.write('\n\n' + arrow + '\nError Report Section'+
                   '\nReport Units: '+espacio+espacio+espacio+'Meters'+
                   '\nConfidence Level: '+espacio+espacio+'95%'+
                   '\nNumber of observations: '+espacio+n+
                   '\nRMSE: '+espacio+espacio+espacio+espacio+ str(round(rmse_r, 2))+
                   '\n95% accuracy: '+espacio+espacio+espacio+ str(round(rmse_e, 2)))
    file.close()
if __name__ == '__main__':
    # Script arguments
    GDB_output=crearGDB(ruta_salida)
    puntos=make_points_from_dgn(ruta_dgn, ruta_salida)
    RMSE(puntos, ruta_raster, ruta_salida)
# -*- #################
# ---------------------------------------------------------------------------
# Direccion de Gestion de Información Geografica
# Created on: 2023-07-14
# Created by: Juan Pablo Merchán Puentes
# # Usage:  
# Description: Detección de elementos capturados en el archivo .dgn que no cumplen con la medida minima
#
# ---------------------------------------------------------------------------
# Import arcpy module
import arcpy
import os
from datetime import datetime
from arcpy.sa import *
####### Definicion funciones:
def tiempo_actual():
    hora_actual = datetime.now()
    return str(hora_actual.hour)+str(hora_actual.minute)+str(hora_actual.hour)
####### Crear GDB
def crearGDB(path, GDB_name):
    GDB_output= arcpy.CreateFileGDB_management(out_folder_path=path,out_name=GDB_name)
    return GDB_output

#Convertir CAD a GDB: 
def convertirCADtoGDB(CAD, GDB, dataset_name):
    arcpy.conversion.CADToGeodatabase(input_cad_datasets=CAD, out_gdb_path=GDB, out_dataset_name=dataset_name, reference_scale=1000, spatial_reference='PROJCS["MAGNA-SIRGAS_Origen-Nacional",GEOGCS["GCS_MAGNA",DATUM["D_MAGNA",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",5000000.0],PARAMETER["False_Northing",2000000.0],PARAMETER["Central_Meridian",-73.0],PARAMETER["Scale_Factor",0.9992],PARAMETER["Latitude_Of_Origin",4.0],UNIT["Meter",1.0]];-618700 -8436100 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision')
#Crear feature class
def createFeatureClass(out_path,out_name):
    arcpy.management.CreateFeatureclass(out_path, out_name, geometry_type='POLYLINE',has_z='ENABLED', spatial_reference='PROJCS["MAGNA-SIRGAS_Origen-Nacional",GEOGCS["GCS_MAGNA",DATUM["D_MAGNA",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",5000000.0],PARAMETER["False_Northing",2000000.0],PARAMETER["Central_Meridian",-73.0],PARAMETER["Scale_Factor",0.9992],PARAMETER["Latitude_Of_Origin",4.0],UNIT["Meter",1.0]];-618700 -8436100 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision' )
#Crear feature class
def createFeatureClass2(out_path,out_name):
    arcpy.management.CreateFeatureclass(out_path, out_name, geometry_type='POLYGON',has_z='ENABLED', spatial_reference='PROJCS["MAGNA-SIRGAS_Origen-Nacional",GEOGCS["GCS_MAGNA",DATUM["D_MAGNA",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",5000000.0],PARAMETER["False_Northing",2000000.0],PARAMETER["Central_Meridian",-73.0],PARAMETER["Scale_Factor",0.9992],PARAMETER["Latitude_Of_Origin",4.0],UNIT["Meter",1.0]];-618700 -8436100 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision' )
#Crear campos en un featureClass
def addFild(in_table, field_name):
    arcpy.management.AddField(in_table, field_name, "LONG",field_precision= 4,field_is_nullable="NULLABLE")
def addFild2(in_table, field_name):
    arcpy.management.AddField(in_table, field_name, "TEXT",field_is_nullable="NULLABLE")
def addFild3(in_table, field_name):
    arcpy.management.AddField(in_table, field_name, "LONG",field_precision= 4,field_is_nullable="NULLABLE")
def shapelength(lyr_poly):
    layercontoponimia=arcpy.management.SelectLayerByAttribute(lyr_poly,'NEW_SELECTION', where_clause="Level = 1 And Shape_Length < 90 And Shape_Length > -90 Or Level = 3 And Shape_Length < 90 And Shape_Length > -90 Or Level = 15 And Shape_Length < 70 And Shape_Length > -70 Or Level = 17 And Shape_Length < 90 And Shape_Length > -90 Or Level = 20 And Shape_Length < 70 And Shape_Length > -70")
    return layercontoponimia
def shapelength2(lyr_poly):
    layercontoponimia=arcpy.management.SelectLayerByAttribute(lyr_poly,'NEW_SELECTION', where_clause="Level = 2 And Shape_Area < 225 and Shape_Area > -225 Or Level = 4 And Shape_Area < 610 and Shape_Area > -610 Or Level = 30 And Shape_Area < 225 and Shape_Area > -225 Or Level = 31 And Shape_Area < 225 and Shape_Area > -225 Or Level = 40 And Shape_Area < 610 and Shape_Area > -610 ")
    return layercontoponimia
def shapelength2000(lyr_poly):
    layercontoponimia=arcpy.management.SelectLayerByAttribute(lyr_poly,'NEW_SELECTION', where_clause="Level = 40 And Shape_Area < 25 and Shape_Area > -25")
    return layercontoponimia

def exportCAD(in_features,Folder_Output,Name_Out):
    arcpy.conversion.ExportCAD(in_features,Ignore_FileNames= True,Append_To_Existing=False ,Output_Type ="DGN_V8", Output_File=os.path.join(Folder_Output,Name_Out+'.dgn'),Seed_File= r'C:\Program Files\ArcGIS\Pro\Resources\ArcToolBox\Templates\CAD\template3d_Metric.dgn')#Documentar semilla
def limpiezascript():
    arcpy.Delete_management(r'C:\Users\JUAN PABLO\OneDrive - Falabella\Documentos\Igac\Asignacion7\pp\GDB_P2.gdb')


"""
/***************************************************************************
Ejecución del programa
/***************************************************************************
"""

if __name__ == '__main__':

    #Script arguments
    dgn_Input= arcpy.GetParameterAsText(0)
    Scale = arcpy.GetParameterAsText(1)
    Folder_Output = arcpy.GetParameterAsText(2)
    Name_Out = arcpy.GetParameterAsText(3)

    # Showing templates
    sep= '###################'
    arrow= '-->'
    hasht= '##'
    longarrow='---->'
    # dataset_name
    dataset_name = "dgn_Error"
    #out_name
    out_name1="Polyline"
    out_name2="Polygon"
    
    #Filds setting GDB_temporal
    fieldName1 = "Layer"
    fieldName2 = "Level"
    fieldName3 = "Abs_Area"
    #Nombre del dataset

    #######--------------------> Inicio Herramienta <--------------------#######
    arcpy.AddMessage("\n{0} ...INICIANDO PROCESO DE GENERACION REPORTE... {1}.".format(sep, sep))
    #GDB principal
    arcpy.AddMessage("\nGenerando GDB_P1.gdb...\n".format(arrow))
    GDB_output = crearGDB(Folder_Output, "GDB_P1.gdb")  #Generar GDB de salida
    
    arcpy.AddMessage("\nConvertir CAD a GDB...\n".format(arrow))
    convertirCADtoGDB(dgn_Input, GDB_output,dataset_name)
    arcpy.AddMessage("\nConversión exitosa...\n".format(arrow))
    #GDB temporal
    arcpy.env.workspace = str(GDB_output)

    arcpy.AddMessage("\nGenerando GDB_P2.gdb...\n".format(arrow))
    GDB_Temp = crearGDB(Folder_Output,"GDB_P2.gdb")

    arcpy.AddMessage("\nCreando FeatureClass y AddFild...\n".format(arrow))
    createFeatureClass(GDB_Temp,out_name1)
    createFeatureClass2(GDB_Temp,out_name2)
    addFild(os.path.join(Folder_Output,'GDB_P2.gdb\Polyline'), fieldName2)
    addFild(os.path.join(Folder_Output,'GDB_P2.gdb\Polygon'), fieldName2)

    addFild2(os.path.join(Folder_Output,'GDB_P2.gdb\Polyline'), fieldName1)
    addFild2(os.path.join(Folder_Output,'GDB_P2.gdb\Polygon'), fieldName1)
    
    edit = arcpy.da.Editor(GDB_Temp)
    edit.startEditing(False, True)
    edit.startOperation()
    if(Scale == "10000"):
        arcpy.AddMessage("{0} Uniendo info a escala 10k de la GDB_P1 a GDB_P2/Polyline....".format(arrow))
        i=0
        with arcpy.da.SearchCursor(shapelength('dgn_Error/Polyline'),['SHAPE@','Level','Layer','Shape_Length']) as sCur:
            with arcpy.da.InsertCursor(os.path.join(Folder_Output,'GDB_P2.gdb\Polyline') ,['SHAPE@','Level','Layer','Shape_Length']) as iCur:
                for row in sCur:
                    i+=1
                    row_list = list(row)
                    row_list[0]= row[0].projectAs('9377')
                    row= tuple(row_list)
                    iCur.insertRow(row)
        arcpy.AddMessage("{0} Union Polyline exitosa.".format(arrow))
        
        i=0
        arcpy.AddMessage("{0} Uniendo info a escala 10k de la GDB_P1 a GDB_P2/Polygon....".format(arrow))
        with arcpy.da.SearchCursor(shapelength2('dgn_Error/Polygon'),['SHAPE@','Level','Layer','Shape_Area']) as sCur:
            with arcpy.da.InsertCursor(os.path.join(Folder_Output,'GDB_P2.gdb\Polygon') ,['SHAPE@','Level','Layer','Shape_Area']) as iCur:
                for row in sCur:
                    i+=1
                    row_list = list(row)
                    row_list[0]= row[0].projectAs('9377')
                    row= tuple(row_list)
                    iCur.insertRow(row)
        arcpy.AddMessage("{0} Union Polyline exitosa.".format(arrow))
        arcpy.AddMessage("{0} Exportando archivo .gdb a .dgn......".format(arrow))
        if(Name_Out == ''):
            Name_Out= 'Error_dgn10k'
            exportCAD([os.path.join(Folder_Output,'GDB_P2.gdb\Polyline'),os.path.join(Folder_Output,'GDB_P2.gdb\Polygon')],Folder_Output,Name_Out)
        else:
            exportCAD([os.path.join(Folder_Output,'GDB_P2.gdb\Polyline'),os.path.join(Folder_Output,'GDB_P2.gdb\Polygon')],Folder_Output,Name_Out)

    elif(Scale == "2000"):
        arcpy.AddMessage("{0} Uniendo info a escala 2k de la GDB_P1 a GDB_P2:".format(arrow))  
        i=0
        with arcpy.da.SearchCursor(shapelength2000('dgn_Error/Polygon'),['SHAPE@','Level','Layer','Shape_Area']) as sCur:
            with arcpy.da.InsertCursor(os.path.join(Folder_Output,'GDB_P2.gdb\Polygon') ,['SHAPE@','Level','Layer','Shape_Area']) as iCur:
                for row in sCur:
                    i+=1
                    row_list = list(row)
                    row_list[0]= row[0].projectAs('9377')
                    row= tuple(row_list)
                    iCur.insertRow(row)
        arcpy.AddMessage("{0} Union Polyline exitosa.".format(arrow))
        if(Name_Out == ''):
            Name_Out= 'Error_dgn_Polygon2k'
            exportCAD(os.path.join(Folder_Output,'GDB_P2.gdb\Polygon'),Folder_Output,Name_Out)
        else:
            exportCAD(os.path.join(Folder_Output,'GDB_P2.gdb\Polygon'),Folder_Output,Name_Out)
    else:
        arcpy.AddMessage("{0} No hay información para la escala selecionada.".format(arrow))
    edit.stopOperation()
    edit.stopEditing(True)
    arcpy.AddMessage("\n\n¡Finalizado correctamente!.\n".format(arrow))
    arcpy.AddMessage(dgn_Input)
# -*- #################
# ---------------------------------------------------------------------------
# Direccion de Gestion de Información Geografica
# Created on: 2023-07-14
# Created by: Juan Pablo Merchán Puentes
# # Usage:  
# Description: Validacion de topologia intersección dgn
#
# ---------------------------------------------------------------------------
"""
/***************************************************************************
Librerias
/***************************************************************************
"""
import arcpy
import os
from datetime import datetime
from arcpy.sa import *

#Librerias de pandas
import pandas as pd
import numpy as np

"""
/***************************************************************************
Funciones del programa
/***************************************************************************
"""
# Crear GDB 
def crearGDB(path, GDB_name):
    GDB_output= arcpy.CreateFileGDB_management(out_folder_path=path,out_name=GDB_name)
    return GDB_output

#Convertir CAD a GDB: 
def convertirCADtoGDB(CAD, GDB, dataset_name):
    arcpy.conversion.CADToGeodatabase(input_cad_datasets=CAD, out_gdb_path=GDB, out_dataset_name=dataset_name, reference_scale=1000, spatial_reference='PROJCS["MAGNA-SIRGAS_Origen-Nacional",GEOGCS["GCS_MAGNA",DATUM["D_MAGNA",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",5000000.0],PARAMETER["False_Northing",2000000.0],PARAMETER["Central_Meridian",-73.0],PARAMETER["Scale_Factor",0.9992],PARAMETER["Latitude_Of_Origin",4.0],UNIT["Meter",1.0]];-618700 -8436100 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision')
#Crear feature class
def createFeatureClass(out_path,out_name):
    arcpy.management.CreateFeatureclass(out_path, out_name, geometry_type='MULTIPOINT',has_z='ENABLED', spatial_reference='PROJCS["MAGNA-SIRGAS_Origen-Nacional",GEOGCS["GCS_MAGNA",DATUM["D_MAGNA",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",5000000.0],PARAMETER["False_Northing",2000000.0],PARAMETER["Central_Meridian",-73.0],PARAMETER["Scale_Factor",0.9992],PARAMETER["Latitude_Of_Origin",4.0],UNIT["Meter",1.0]];-618700 -8436100 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision' )

#Crear feature class
def createFeatureClass2(out_path,out_name):
    arcpy.management.CreateFeatureclass(out_path, out_name, geometry_type='POLYLINE',has_z='ENABLED', spatial_reference='PROJCS["MAGNA-SIRGAS_Origen-Nacional",GEOGCS["GCS_MAGNA",DATUM["D_MAGNA",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",5000000.0],PARAMETER["False_Northing",2000000.0],PARAMETER["Central_Meridian",-73.0],PARAMETER["Scale_Factor",0.9992],PARAMETER["Latitude_Of_Origin",4.0],UNIT["Meter",1.0]];-618700 -8436100 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision' )

def createFeatureClass3(out_path,out_name):
    arcpy.management.CreateFeatureclass(out_path, out_name, geometry_type='POINT',has_z='ENABLED', spatial_reference='PROJCS["MAGNA-SIRGAS_Origen-Nacional",GEOGCS["GCS_MAGNA",DATUM["D_MAGNA",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",5000000.0],PARAMETER["False_Northing",2000000.0],PARAMETER["Central_Meridian",-73.0],PARAMETER["Scale_Factor",0.9992],PARAMETER["Latitude_Of_Origin",4.0],UNIT["Meter",1.0]];-618700 -8436100 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision' )

#Filtros SQL
def Niveles_CNivel(lyr_poly):
    layercontoponimia=arcpy.management.SelectLayerByAttribute(lyr_poly,'NEW_SELECTION', where_clause="Level = 42 Or Level = 43 Or Level = 44 Or Level = 45")
    return layercontoponimia
def Niveles_Dsencillo(lyr_poly):
    layercontoponimia=arcpy.management.SelectLayerByAttribute(lyr_poly,'NEW_SELECTION', where_clause="Level = 1 ")
    return layercontoponimia
def Niveles_Pantanos(lyr_poly):
    layercontoponimia=arcpy.management.SelectLayerByAttribute(lyr_poly,'NEW_SELECTION', where_clause="Level = 4 ")
    return layercontoponimia
def Cotas_fotogrametricas(lyr_poly):
    layercontoponimia=arcpy.management.SelectLayerByAttribute(lyr_poly,'NEW_SELECTION', where_clause="Level = 41 ")
    return layercontoponimia
#Crear campos en un featureClass
def addFild(in_table, field_name):
    arcpy.management.AddField(in_table, field_name, "DOUBLE",field_precision= 4,field_is_nullable="NULLABLE")
def addFild2(in_table, field_name):
    arcpy.management.AddField(in_table, field_name, "TEXT",field_is_nullable="NULLABLE")
#Funcion que realiza la union de una linea que termina en punto y continua con linea
def unsplit(lyr_poly,Folder_Output):
    arcpy.management.UnsplitLine(in_features=lyr_poly, out_feature_class=Folder_Output)
def generater_near(in_features,near_features,out_table):
    search_radius = '1500 Meters'
    location = 'NO_LOCATION'
    angle = 'NO_ANGLE'
    closest = 'ALL'
    closest_count = 1
    arcpy.analysis.GenerateNearTable(in_features, near_features, out_table, search_radius, location, angle, closest, closest_count )
def join_table (inFeatures, joinField, joinTable, joinField2):
    arcpy.management.JoinField(inFeatures, joinField, joinTable, joinField2)

def migrar_puntos_cf(MRTerr_lyr,tabla_errores):
    union = arcpy.management.JoinField(MRTerr_lyr,"OBJECTID",tabla_errores, "ID_fotogrametricas")
    b = arcpy.management.SelectLayerByAttribute(union,'NEW_SELECTION', where_clause="ID_fotogrametricas IS NOT NULL")
    return b

def cotas_f_query(MRTerr_lyr, tuple):
    b = arcpy.management.SelectLayerByAttribute(MRTerr_lyr,'NEW_SELECTION', where_clause="OBJECTID IN {0}".format(tuple))
    return b 


#Funciones de validación
def Local_CNivel(lyr_poly):
    arcpy.management.SelectLayerByLocation(lyr_poly, overlap_type = 'INTERSECT', select_features= lyr_poly, selection_type ='SUBSET_SELECTION')

code_block ="""
def estado(a):
    if (a>1):
        b = "REVISAR"
        return b 
    else: 
        b = "OMITIR"
        return b"""

def DrenajL_CNivel(GDB_Entrada, GDB_Salida): #Curva de nivel no debe cruzar mas de una vez el mismo drenaje
    #arcpy.env.workspace = GDB_Entrada
    Feature_Class_Curvas_Nivel = os.path.join(str(GDB_Entrada),'Elevacion\CNivel')
    Feature_Class_Drenaje_L = os.path.join(str(GDB_Entrada),'Hidrografia\Drenaj_L')
    Puntos_Intersect = os.path.join(str(GDB_Salida),"Puntos_Intersect")                                       
    Puntos_Interseccion_Multipar = os.path.join(str(GDB_Salida),"Puntos_Interseccion_Multipar")              
    Puntos_Interseccion_Multip_stats = os.path.join(str(GDB_Salida),"Puntos_Interseccion_Multip_stats")
    Puntos_Intersect_Layer = os.path.join(str(GDB_Salida),"Puntos_Intersect_Layer")                          
    Puntos_Revision = os.path.join(str(GDB_Salida),"DrenajeL_CNivel")                                        
    #Salida_gdb = os.path.join(Ruta_Salida, "Revision_Curvas")  
    # Process: Intersect
    arcpy.Intersect_analysis([Feature_Class_Curvas_Nivel, Feature_Class_Drenaje_L], Puntos_Intersect, "ALL", "", "POINT")
    # Process: Multipart To Singlepart
    arcpy.management.MultipartToSinglepart(Puntos_Intersect, Puntos_Interseccion_Multipar)
    # Process: Summary Statistics
    arcpy.Statistics_analysis(Puntos_Interseccion_Multipar, Puntos_Interseccion_Multip_stats, "ORIG_FID COUNT", "ORIG_FID")
    # Process: Join Field
    arcpy.JoinField_management(Puntos_Intersect, "OBJECTID", Puntos_Interseccion_Multip_stats, "ORIG_FID", "FREQUENCY")
    # Process: Add Field
    arcpy.AddField_management(Puntos_Intersect, "Estado_Intersect", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    # Process: Add Field
    #arcpy.AddField_management(Puntos_Intersect, "Layer", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")####ACA
    #Process: Calculate Field
    arcpy.CalculateField_management(Puntos_Intersect, "Estado_Intersect", "estado(!FREQUENCY!)", "PYTHON3", code_block)
    # Process: Make Feature Layer
    arcpy.MakeFeatureLayer_management(Puntos_Intersect, Puntos_Intersect_Layer, "", "", "OBJECTID OBJECTID VISIBLE NONE;SHAPE SHAPE VISIBLE NONE;FID_Drenaj_L FID_Drenaj_L VISIBLE NONE;DIdentif DIdentif VISIBLE NONE;DEstado DEstado VISIBLE NONE;DDisperso DDisperso VISIBLE NONE;DNombre DNombre VISIBLE NONE;FID_CNivel FID_CNivel VISIBLE NONE;CNIdentif CNIdentif VISIBLE NONE;CNAltura CNAltura VISIBLE NONE;CNTipo CNTipo VISIBLE NONE;FREQUENCY FREQUENCY VISIBLE NONE;Estado_Intersect Estado_Intersect VISIBLE NONE")
    # Process: Select Layer By Attribute
    arcpy.SelectLayerByAttribute_management(Puntos_Intersect_Layer, "NEW_SELECTION", "Estado_Intersect = 'REVISAR'")
    # Process: Feature Class to Feature Class (2)
    arcpy.FeatureClassToFeatureClass_conversion(Puntos_Intersect_Layer, GDB_Salida, "DrenajeL_CNivel", "", "FREQUENCY \"FREQUENCY\" true true false 0 Long 0 0 ,First,#,Revision_Curvas.gdb\\Puntos_Intersect,FREQUENCY,-1,-1;Estado_Intersect \"Estado_Intersect\" true true false 0 Text 0 0 ,First,#,Revision_Curvas.gdb\\Puntos_Intersect,Estado_Intersect,-1,-1", "")
    # Process: Alter Field
    arcpy.AlterField_management(Puntos_Revision, "FREQUENCY", "NumIntersec", "Numero_de_Intersecciones")
    
    #eliminando capas temporales:
    arcpy.management.Delete(Puntos_Intersect)
    arcpy.management.Delete(Puntos_Interseccion_Multipar)
    arcpy.management.Delete(Puntos_Interseccion_Multip_stats)
    arcpy.management.Delete(Puntos_Intersect_Layer)
    total = arcpy.management.GetCount(Puntos_Revision)
    
    if str(total) == '0':
        arcpy.Delete_management(Puntos_Revision)
    
    return total  

def CNivel_DAguaR(GDB_Entrada,GDB_Salida,Ruta_Salida):
    arcpy.env.workspace= GDB_Entrada
    Feature_Class_CNivel = os.path.join(str(GDB_Entrada),'Elevacion\CNivel')
    ly_DAguaR = arcpy.MakeFeatureLayer_management('Hidrografia\DAgua_R',os.path.join(str(Ruta_Salida),'DAgua_R_temp.shp'))#Capa temporal
    salida = arcpy.Intersect_analysis([ly_DAguaR, Feature_Class_CNivel],os.path.join(str(GDB_Salida),'DAguaR_CNivel'))
    total = arcpy.management.GetCount(salida)
    return total

def CNivel_CotaCerrada(GDB_Entrada):
    arcpy.env.workspace= GDB_Entrada
    Feature_Class_CNivel = os.path.join(str(GDB_Entrada),'Elevacion\CNivel')

def Multipart_SinglePart(GDB_Entrada,GDB_Salida):#Funcion de Multipunto a punto
    arcpy.management.MultipartToSinglepart(GDB_Entrada, GDB_Salida)

def exportCAD(in_features,Folder_Output,Name_Out):#Función para exportar FeatureClass a CAD
    arcpy.conversion.ExportCAD(in_features,Ignore_FileNames= True,Append_To_Existing=True ,Output_Type ="DGN_V8", Output_File=os.path.join(Folder_Output,Name_Out),Seed_File= r'C:\Program Files\ArcGIS\Pro\Resources\ArcToolBox\Templates\CAD\template3d_Metric.dgn')#Documentar semilla
#os.path.join(Folder_Output,Name_Out+'.dgn')

#def table_join(in_data,in_field,join_table,join_field):
    
"""
/***************************************************************************
Ejecución del programa
/***************************************************************************
"""
if __name__ == "__main__":

    #Script arguments
    dgn_Input = arcpy.GetParameterAsText(0)
    gdb_v2_5 = arcpy.GetParameterAsText(1)
    Folder_Output = arcpy.GetParameterAsText(2)
    Escala = arcpy.GetParameterAsText(3)

    dgn_name = str(dgn_Input)
    #print(dgn_name)
    arcpy.AddMessage(dgn_name )
    x = 0
    y = 0
    Caracter = []
    for i in range (len(dgn_name)):
        y = y + 1
        Caracter.append(dgn_name[i])
        if(dgn_name[i] == "\\" ):
           x = y
    nombre_dgn = dgn_name[x:]
    
    # Showing templates
    sep= '###################'
    arrow= '-->'
    hasht= '##'
    longarrow='---->'

    #datasetName
    dataset_name = 'validacion_topologia'

    #Filds setting GDB_temporal
    fieldName1 = "Layer"
    fieldName2 = "Error_Numerico"
    fieldName3 = 'ID_fotogrametricas'

    out_name1= 'Errores_CNivel'
    out_name2='Errores_CotaCerrada'
    out_name3= 'Error_cotas_fotogrametricas'
    out_name4= 'Errores_Cotas_Fotogrametricas'

    #Descripciones layers
    row_values = 'Error Cruces CNivel'
    row_values_2 = 'Error entre más de un punto CNivel'
    row_values_3 = 'Error entre cruce de CNivel y Pantano'
    row_values_4 = 'Error Cota Cerrada'
    row_values_5 = 'Cruce en más de un punto CNivel y DSencillo'
    row_values_6 = 'Error cota fotogrametrica'

    #######--------------------> Inicio Herramienta <--------------------#######
    arcpy.AddMessage("\n{0} ...INICIANDO PROCESO DE GENERACION REPORTE... {1}.".format(sep, sep))

    #GDB principal
    arcpy.AddMessage("\nGenerando GDB_Temp.gdb...\n".format(arrow))
    GDB_output = crearGDB(Folder_Output, "GDB_Temp.gdb")  #Generar GDB de salida

    #Creamos las GDB para almacenar la errores de intersección en CNivel
    GDB_Errores = crearGDB(Folder_Output, "GDB_Errores_CNivel.gdb") 

    #Conversion CAD a GDB
    arcpy.AddMessage("\nConvertir CAD a GDB...\n".format(arrow))
    convertirCADtoGDB(dgn_Input, GDB_output,dataset_name)
    arcpy.AddMessage("\nConversión exitosa...\n".format(arrow))
    
    #Crear FeatureClass
    createFeatureClass(GDB_Errores,out_name1)
    createFeatureClass3(GDB_Errores,out_name3)
    createFeatureClass3(GDB_Errores,out_name4)
    createFeatureClass2(GDB_Errores,out_name2)
    
    #Creación de campos
    addFild2(os.path.join(Folder_Output,'GDB_Errores_CNivel.gdb\Errores_CNivel'), fieldName1)
    addFild(os.path.join(Folder_Output,'GDB_Errores_CNivel.gdb\Errores_CotaCerrada'), fieldName2)
    addFild(os.path.join(Folder_Output,'GDB_Errores_CNivel.gdb\Errores_Cotas_Fotogrametricas'), fieldName3)
    addFild2(os.path.join(Folder_Output,'GDB_Errores_CNivel.gdb\Errores_CotaCerrada'), fieldName1)
    addFild2(os.path.join(Folder_Output,'GDB_Errores_CNivel.gdb\Errores_Cotas_Fotogrametricas'), fieldName1)
    
    #Inicio workSpace
    arcpy.env.workspace = str(GDB_output)
    edit = arcpy.da.Editor(GDB_Errores)
    edit.startEditing(False, True)
    edit.startOperation()
    arcpy.AddMessage("{0} Iniciando validación intersección entre curvas de nivel....".format(arrow))
    prueba= Niveles_CNivel('validacion_topologia\Polyline')
    arcpy.AddMessage("{0} Aplicando unsplitline....".format(arrow))
    prueba1=arcpy.management.UnsplitLine(prueba, 'validacion_topologia\Curvas_Union')
    arcpy.AddMessage("{0} Realizando analisis de intersecciones....".format(arrow))
    curvas_error = arcpy.analysis.Intersect(prueba1, 'validacion_topologia\puntos_error_curvas','ALL','0','POINT')

    i=0
    with arcpy.da.SearchCursor(prueba,['SHAPE@','Elevation']) as sCur:
        with arcpy.da.InsertCursor(os.path.join(Folder_Output,'GDB_Errores_CNivel.gdb\Errores_CotaCerrada') ,['SHAPE@','Error_Numerico']) as iCur:
            for row in sCur:
                i+=1
                row_list = list(row)
                row_list[0]= row[0].projectAs('9377')
                row= tuple(row_list)
                iCur.insertRow(row)   
    with arcpy.da.UpdateCursor(os.path.join(Folder_Output,'GDB_Errores_CNivel.gdb\Errores_CotaCerrada') ,'Error_Numerico') as iCur:
        for row in iCur:
            if(round((row[0]%1),2)==0 or round((row[0]%1),2) == 1):
                iCur.deleteRow()
            else:
                pass
    with arcpy.da.UpdateCursor(os.path.join(Folder_Output,'GDB_Errores_CNivel.gdb\Errores_CotaCerrada') ,'Layer') as iCur:
        for row in iCur:
            row[0] = row_values_4
            iCur.updateRow(row)
    i=0 
    arcpy.AddMessage("{0} Almacenando info en GDB_Errores_Cnivel".format(arrow))
    with arcpy.da.SearchCursor(curvas_error,['SHAPE@']) as sCur:
        with arcpy.da.InsertCursor(os.path.join(Folder_Output,'GDB_Errores_CNivel.gdb\Errores_CNivel') ,['SHAPE@']) as iCur:
            for row in sCur:
                i+=1
                row_list = list(row)
                row_list[0]= row[0].projectAs('9377')
                row= tuple(row_list)
                iCur.insertRow(row)
    
    with arcpy.da.UpdateCursor(os.path.join(Folder_Output,'GDB_Errores_CNivel.gdb\Errores_CNivel') ,'Layer') as iCur:
        for row in iCur:
            row[0] = row_values
            iCur.updateRow(row)
    arcpy.AddMessage("{0} Conversión de FeatureClass de multipunto a punto....".format(arrow))
    Multipart_SinglePart(os.path.join(Folder_Output,'GDB_Errores_CNivel.gdb\Errores_CNivel'),os.path.join(str(GDB_Errores),'Errores_CNivel_Sencillo') )
    arcpy.AddMessage("{0} Proceso intersección curvas de nivel finalizado.".format(arrow))
    edit.stopOperation()
    edit.stopEditing(True)

    #Revision CNivel y Dsensillo
    arcpy.AddMessage("{0} Iniciamos intersección curvas de nivel y drenaje sencillo..".format(arrow))
    edit = arcpy.da.Editor(gdb_v2_5)
    edit.startEditing(False, True)
    edit.startOperation()
    
    arcpy.AddMessage("{0} Migrando CNivel a La gdb_2.5...".format(arrow))
    i=0
    with arcpy.da.SearchCursor(Niveles_CNivel('validacion_topologia\Polyline'),['SHAPE@','Elevation']) as sCur:
        with arcpy.da.InsertCursor(os.path.join(gdb_v2_5,'Elevacion\CNivel'),['SHAPE@','CNAltura']) as iCur:
            for row in sCur:
                i+=1
                row_list = list(row)
                row_list[0]= row[0].projectAs('9377')
                row= tuple(row_list)
                iCur.insertRow(row)
    arcpy.AddMessage("{0} Migrando Drenaje sencillo a La gdb_2.5...".format(arrow))
    i=0
    with arcpy.da.SearchCursor(Niveles_Dsencillo('validacion_topologia\Polyline'),['SHAPE@']) as sCur:
        with arcpy.da.InsertCursor(os.path.join(gdb_v2_5,'Hidrografia\Drenaj_L'),['SHAPE@']) as iCur:
            for row in sCur:
                i+=1
                row_list = list(row)
                row_list[0]= row[0].projectAs('9377')
                row= tuple(row_list)
                iCur.insertRow(row)
    arcpy.AddMessage("{0} Migrando Pantano a La gdb_2.5...".format(arrow))
    i=0
    with arcpy.da.SearchCursor(Niveles_Pantanos('validacion_topologia\Polygon'),['SHAPE@']) as sCur:
        with arcpy.da.InsertCursor(os.path.join(gdb_v2_5,'Hidrografia\DAgua_R'),['SHAPE@']) as iCur:
            for row in sCur:
                i+=1
                row_list = list(row)
                row_list[0]= row[0].projectAs('9377')
                row= tuple(row_list)
                iCur.insertRow(row)
    
    with arcpy.da.SearchCursor(Cotas_fotogrametricas('validacion_topologia\Point'),['SHAPE@','Elevation']) as sCur:
        with arcpy.da.InsertCursor(os.path.join(gdb_v2_5,'Geodesia\MRTerr'),['SHAPE@','MRTAltura']) as iCur:
            for row in sCur:
                i+=1
                row_list = list(row)
                row_list[0]= row[0].projectAs('9377')
                row= tuple(row_list)
                iCur.insertRow(row)
    arcpy.AddMessage("{0} Iniciando validación cotas fotogrametricas".format(arrow))
    generater_near(os.path.join(gdb_v2_5,'Geodesia\MRTerr'),os.path.join(gdb_v2_5,'Elevacion\CNivel'),os.path.join(Folder_Output,'GDB_Errores_CNivel.gdb\Error_cotas_fotogrametricas'))
    #Analisis vecino más cercano
    join_table(os.path.join(Folder_Output,'GDB_Errores_CNivel.gdb\Error_cotas_fotogrametricas'),'IN_FID',os.path.join(gdb_v2_5,'Geodesia\MRTerr'),'OBJECTID')
    join_table(os.path.join(Folder_Output,'GDB_Errores_CNivel.gdb\Error_cotas_fotogrametricas'),'NEAR_FID',os.path.join(gdb_v2_5,'Elevacion\CNivel'),'OBJECTID')
    
    #tabla de anailisis errores cota fotogrametrica
    table = os.path.join(Folder_Output,"GDB_Errores_CNivel.gdb\Error_cotas_fotogrametricas")

    # Obtener los nombres de las columnas no geométricas
    columns = [field.name for field in arcpy.ListFields(table) if field.type != "Geometry"]

    # Crear un DataFrame a partir de los datos de la tabla
    data = [row for row in arcpy.da.SearchCursor(table, columns)]
    df = pd.DataFrame(data, columns=columns) 
    #arcpy.AddMessage(df)
    #Lista para almacenar los ID con error cotafogrametrica
    lista_ids= []

    for i in range(len(df) - 1):  
        in_fid = df.iloc[i]['IN_FID']

        cn_altura = df.iloc[i]['CNAltura']
        mrt_altura = df.iloc[i]['MRTAltura']

        if Escala == '2000':
            if cn_altura - 2 < mrt_altura < cn_altura + 2:
                pass
            else:
                with arcpy.da.InsertCursor(os.path.join(Folder_Output, 'GDB_Errores_CNivel.gdb\Errores_Cotas_Fotogrametricas'), ['ID_fotogrametricas']) as cursor:
                    cursor.insertRow([in_fid])
                    lista_ids.append(in_fid)
                     
        elif Escala == '10000':
            if cn_altura - 10 < mrt_altura < cn_altura + 10:
                pass
            else:
                with arcpy.da.InsertCursor(os.path.join(Folder_Output, 'GDB_Errores_CNivel.gdb\Errores_Cotas_Fotogrametricas'), ['ID_fotogrametricas']) as cursor:
                    cursor.insertRow([in_fid])
                    lista_ids.append(in_fid)

        else:
            pass
    #Tupla para almacenar los identifricadores que se van a filtrar
    tupla_ids = tuple(lista_ids)
  
    with arcpy.da.SearchCursor(cotas_f_query(os.path.join(gdb_v2_5,'Geodesia\MRTerr'),tupla_ids),['SHAPE@','OBJECTID']) as sCur:
        with arcpy.da.InsertCursor(os.path.join(Folder_Output, 'GDB_Errores_CNivel.gdb\Errores_Cotas_Fotogrametricas'), ['SHAPE@','ID_fotogrametricas']) as cursor:
            for row in sCur:
                cursor.insertRow(row)
    #Reparando geometrias 
    arcpy.management.RepairGeometry(os.path.join(Folder_Output, 'GDB_Errores_CNivel.gdb\Errores_Cotas_Fotogrametricas'))
    with arcpy.da.UpdateCursor(os.path.join(Folder_Output,'GDB_Errores_CNivel.gdb\Errores_Cotas_Fotogrametricas') ,'Layer') as iCur:
        for row in iCur:
            row[0] = row_values_6
            iCur.updateRow(row)
    arcpy.AddMessage("{0} finalización proceso cota fotogrametrica".format(arrow))

                    
    try:
        arcpy.AddMessage("{0} Iniciando verificacion de intersecciones entre CNivel y Drenaje sencillo...(try..)".format(arrow))
        DrenajL_CNivel(gdb_v2_5,GDB_Errores)
        arcpy.AddMessage("{0} Intersección CNivel y Dsensillo finalizada.".format(arrow))
        addFild2(os.path.join(Folder_Output,'GDB_Errores_CNivel.gdb\DrenajeL_CNivel'), fieldName1)
        with arcpy.da.UpdateCursor(os.path.join(Folder_Output,'GDB_Errores_CNivel.gdb\DrenajeL_CNivel') ,'Layer') as iCur:
            for row in iCur:
                row[0] = row_values_5
                iCur.updateRow(row)
        arcpy.AddMessage("{0} Verificación Completa CNivel--> Drenaj_L...".format(arrow))
        arcpy.AddMessage("{0} Iniciando verificacion de intersecciones entre CNivel y Pantanos...".format(arrow))
        total=CNivel_DAguaR(gdb_v2_5,GDB_Errores,Folder_Output)
        if str(total) == '0':
            arcpy.AddMessage("Se encontraron " + str(total) + " errores en total")
        else:
            arcpy.AddMessage("Se encontraron " + str(total) + " errores en total \n->Validar en  Feature: DAguaR_CNivel")

        arcpy.AddMessage("{0} Verificación finalizada CNivel--> DAgua_R...".format(arrow))
        
        Multipart_SinglePart(os.path.join(Folder_Output,'GDB_Errores_CNivel.gdb\DrenajeL_CNivel'),os.path.join(str(GDB_Errores),'DrenajeL_CNivel_Sencillo') )

        arcpy.AddMessage("{0} Iniciando exportación a CAD...".format(arrow))
        CadExport = [os.path.join(Folder_Output,'GDB_Errores_CNivel.gdb\DAguaR_CNivel'),os.path.join(Folder_Output,'GDB_Errores_CNivel.gdb\DrenajeL_CNivel_Sencillo'),os.path.join(Folder_Output,'GDB_Errores_CNivel.gdb\Errores_CNivel_Sencillo'),os.path.join(Folder_Output,'GDB_Errores_CNivel.gdb\Errores_CotaCerrada'),os.path.join(Folder_Output,'GDB_Errores_CNivel.gdb\Errores_Cotas_Fotogrametricas')]
        #Name_Out = 'Errores_Prueba'
        
        for feature in CadExport:
            exportCAD(feature,Folder_Output,nombre_dgn)
            arcpy.AddMessage(feature + " " + "Exportado correctamente")
        arcpy.AddMessage("{0} Exportación correcta".format(arrow))
        edit.stopOperation()
        edit.stopEditing(True)
        
        arcpy.AddMessage("\n--------------------------------------------------------------")
        arcpy.AddMessage("FINALIZADO")
    except:
        arcpy.AddMessage("{0} Iniciando verificacion de intersecciones entre CNivel y Drenaje sencillo...".format(arrow))
        total=CNivel_DAguaR(gdb_v2_5,GDB_Errores,Folder_Output)
        if str(total) == '0':
            arcpy.AddMessage("Se encontraron " + str(total) + " errores en total")
        else:
            arcpy.AddMessage("Se encontraron " + str(total) + " errores en total \n->Validar en  Feature: DAguaR_CNivel")

        arcpy.AddMessage("{0} Verificación finalizada CNivel--> DAgua_R...".format(arrow))
        arcpy.AddMessage("{0} Iniciando exportación a CAD...".format(arrow))
        CadExport = [os.path.join(Folder_Output,'GDB_Errores_CNivel.gdb\DAguaR_CNivel'),os.path.join(Folder_Output,'GDB_Errores_CNivel.gdb\Errores_CNivel_Sencillo'),os.path.join(Folder_Output,'GDB_Errores_CNivel.gdb\Errores_CotaCerrada')]
        #Name_Out = 'Errores_Prueba'
        for feature in CadExport:
            exportCAD(feature,Folder_Output,nombre_dgn)
            arcpy.AddMessage(feature + " " + "Exportado correctamente")

        edit.stopOperation()
        edit.stopEditing(True)
        arcpy.AddMessage("{0} Exportación correcta".format(arrow))
        
        arcpy.AddMessage("\n--------------------------------------------------------------")
        arcpy.AddMessage("FINALIZADO")
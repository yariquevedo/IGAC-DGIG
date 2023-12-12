"""
Script documentation
"""
import os
from platform import processor 
import arcpy
from rapidfuzz import fuzz
#from rapidfuzz.utils import default_process
#Crear feature class
def createFeatureClass(out_path,out_name):
    arcpy.management.CreateFeatureclass(out_path, out_name, geometry_type='POINT',has_z='ENABLED', spatial_reference='PROJCS["MAGNA-SIRGAS_Origen-Nacional",GEOGCS["GCS_MAGNA",DATUM["D_MAGNA",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",5000000.0],PARAMETER["False_Northing",2000000.0],PARAMETER["Central_Meridian",-73.0],PARAMETER["Scale_Factor",0.9992],PARAMETER["Latitude_Of_Origin",4.0],UNIT["Meter",1.0]];-618700 -8436100 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision' )

if __name__ == "__main__":
    bnng = arcpy.GetParameterAsText(0)
    base_DANE = arcpy.GetParameterAsText(1)
    porcentaje = float(arcpy.GetParameterAsText(2))
    buffer =arcpy.GetParameterAsText(3)
    Escala = arcpy.GetParameterAsText(4)
    salida = arcpy.GetParameterAsText(5)
    """
    Caracteres especiales para la ejecución del script
    """
    sep= '######################################'
    arrow= '--'
    hasht= '##'
    
    out_name = 'tabla_similitud.shp'
    # creando shape file
    createFeatureClass(salida,out_name)
    arcpy.workspace = os.path.join(salida,out_name)
    #1. Generar copia a la capa de NG original
    bnng_c =arcpy.management.MakeFeatureLayer(bnng, 
                                              os.path.join(bnng,"bnng_lyr")
                                              )
    #2. Adicionar campos de comparación
    arcpy.management.AddFields(os.path.join(salida,out_name),[["id_comp", "LONG"],
                                                              ["Nombre_C", "TEXT"],
                                                              ["Porcentaje", "FLOAT"],
                                                              ["Escala","TEXT"],
                                                              ["idBNNG", "LONG"],
                                                              ["NombreBNNG","TEXT"] 
                                       ])
    #3. Busqueda de los toponimos con mayor cantidad de similitudes usando logica difusa para 10K 
    i = 0
    uCur =  arcpy.da.SearchCursor(os.path.join(bnng,"bnng_lyr"),['SHAPE@','NOMBRE_GEO','OID@'])
    inCur = arcpy.da.InsertCursor(os.path.join(salida,out_name) ,['SHAPE@','id_comp','Nombre_C','Porcentaje','Escala','idBNNG','NombreBNNG'])
    for ng in uCur:
        i = i+1
    
        
        arcpy.AddMessage("Analizando Nombre: " +ng[1] + " " + "OID: " + str(ng[2]))
        query = "FID = {0}".format(ng[2])
        a = arcpy.management.SelectLayerByAttribute(os.path.join(bnng,"bnng_lyr"), "NEW_SELECTION", query)
        b = arcpy.management.SelectLayerByLocation(base_DANE, "INTERSECT", a , buffer, "NEW_SELECTION")
        ng_select = arcpy.da.SearchCursor(b,['SHAPE@','NOMBRE_GEO','OID@','ngnoficial'])
       
        for ng_search in ng_select:
            arcpy.AddMessage( "ng_search :" )
            arcpy.AddMessage( ng_search )
            arcpy.AddMessage( "ng_select :" )
            arcpy.AddMessage( ng_select)
            list_ng_selected = []
            
            if fuzz.token_sort_ratio(ng[1], ng_select[1]) >= (porcentaje):
                arcpy.AddMessage(fuzz.ratio(ng[1], ng_select[1]))
                arcpy.AddMessage("porcentaje")
                arcpy.AddMessage(porcentaje)
                arcpy.AddMessage(ng[1])
                arcpy.AddMessage(ng_select[1])
                list_ng_selected.append(ng_search[0].projectAs('9377'))
                list_ng_selected.append(ng_search[2])
                list_ng_selected.append(ng_search[1])
                list_ng_selected.append(fuzz.ratio(ng[1], ng_select[1]))
                list_ng_selected.append(Escala)
                list_ng_selected.append(Escala)
                list_ng_selected.append(ng_select[1])
                
                row= tuple(list_ng_selected)
                inCur.insertRow(row)
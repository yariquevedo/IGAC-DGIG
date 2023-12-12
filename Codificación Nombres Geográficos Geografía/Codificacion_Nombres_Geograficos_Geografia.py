# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Direccion de Gestión de la Información Geografica
# Created on: 2023-09-20
# Created by: Diego Rugeles (Supervisor Desarrollo DGIG)
# # Usage: Codificacion Automatica de Rios (Geografía)
import arcpy 
import os 
# 1. Variables de entorno 
base_drenajes = arcpy.GetParameterAsText(0)
#r"C:\diego.rugeles\IGAC2023\Desarrollo\Geografia\V2\Carto100000_DG_RS_20171230_Migrada_V2.5.gdb"
base_et = arcpy.GetParameterAsText(1)
#r"C:\diego.rugeles\IGAC2023\Desarrollo\Geografia\V2\GDB_ET_Agosto_2023.gdb"
toponimos =arcpy.GetParameterAsText(2) 
#r"C:\diego.rugeles\IGAC2023\Desarrollo\Geografia\V2\NG\NG_hidrografia_100k.shp"
arcpy.env.workspace = toponimos
arcpy.env.overwriteOutput = True
salida = arcpy.GetParameterAsText(3)  
#r"C:\diego.rugeles\IGAC2023\Desarrollo\Geografia\V2\TEMP"
buffer = arcpy.GetParameterAsText(4)  
inicio_consecutivo = arcpy.GetParameterAsText(5)  
sep= '######################################'
arrow= '--'
hasht= '##'
#departamento = arcpy.da.SearchCursor('Departamento',['SHAPE@','CODIGO_DANE'])
#municipio = arcpy.da.SearchCursor('Municipio',['SHAPE@','CODIGO_DANE'])
#2. Asignación del identificador por drenaje_R en comun 
drenaje_select = arcpy.management.SelectLayerByLocation(os.path.join(base_drenajes,"Hidrografia\Drenaj_R"), "INTERSECT", toponimos , buffer, "NEW_SELECTION")
drenaje_final = arcpy.management.MakeFeatureLayer(drenaje_select, os.path.join(salida,"drenajes_select.shp"))
i = int(inicio_consecutivo)
sCur = arcpy.da.SearchCursor(drenaje_final,['SHAPE@','DNombre','OID@'])
for rios in sCur:
    if rios[1] not in [None,"<Null>"]:
        i = i+1
        arcpy.AddMessage("Rio Analizado: " +rios[1] + " " + "OID: " + str(rios[2]))
        query = "OBJECTID = {0} ".format(rios[2])
        a = arcpy.management.SelectLayerByAttribute(drenaje_final, "NEW_SELECTION", query)
        b = arcpy.management.SelectLayerByLocation(toponimos, "INTERSECT", a , buffer, "NEW_SELECTION")
        topo_select = arcpy.da.UpdateCursor(b,['SHAPE@','NGNPrincip','NGIdenti_1','NGSubcat_1'])
        for topo in topo_select:
            if(rios[1] == topo[1]):
                if(len(str(i))==1):
                    topo[2] = "01" + str(topo[3]) + "00000" + str(i)
                    topo_select.updateRow(topo)
                elif(len(str(i))==2):
                    topo[2] = "01" + str(topo[3]) + "0000" + str(i)
                    topo_select.updateRow(topo)
                elif(len(str(i))==3):
                    topo[2] ="01" + str(topo[3]) +  "000" + str(i)
                    topo_select.updateRow(topo)
                elif(len(str(i))==4):
                    topo[2] ="01" +str(topo[3]) +  "00" + str(i)
                    topo_select.updateRow(topo)
                elif(len(str(i))==5):
                    topo[2] =str(topo[3]) +  "0" + str(i)
                    topo_select.updateRow(topo)
                else:
                    arcpy.AddMessage("Existen mas de 1 millon de puntos no se puede asignar")
            else: 
                pass
            
    else:
        pass
#3. Convertir en m
#2. Asignación del identificador por Drenaje_L en comun 
drenaje_select = arcpy.management.SelectLayerByLocation(os.path.join(base_drenajes,"Hidrografia\Drenaj_L"), "INTERSECT", toponimos , buffer, "NEW_SELECTION")
drenaje_final = arcpy.management.MakeFeatureLayer(drenaje_select, os.path.join(salida,"drenajes_select.shp"))
i = int(inicio_consecutivo)
sCur = arcpy.da.SearchCursor(drenaje_final,['SHAPE@','DNombre','OID@'])
for rios in sCur:
    if rios[1] not in [None,"<Null>"]:
        i = i+1
        arcpy.AddMessage("Rio Analizado: " +rios[1] + " " + "OID: " + str(rios[2]))
        query = "OBJECTID = {0} ".format(rios[2])
        a = arcpy.management.SelectLayerByAttribute(drenaje_final, "NEW_SELECTION", query)
        b = arcpy.management.SelectLayerByLocation(toponimos, "INTERSECT", a , buffer, "NEW_SELECTION")
        topo_select = arcpy.da.UpdateCursor(b,['SHAPE@','NGNPrincip','NGIdenti_1','NGSubcat_1'])
        for topo in topo_select:
            if(rios[1] == topo[1]):
                if(len(str(i))==1):
                    topo[2] = "01" + str(topo[3]) + "00000" + str(i)
                    topo_select.updateRow(topo)
                elif(len(str(i))==2):
                    topo[2] = "01" + str(topo[3]) + "0000" + str(i)
                    topo_select.updateRow(topo)
                elif(len(str(i))==3):
                    topo[2] ="01" + str(topo[3]) +  "000" + str(i)
                    topo_select.updateRow(topo)
                elif(len(str(i))==4):
                    topo[2] ="01" +str(topo[3]) +  "00" + str(i)
                    topo_select.updateRow(topo)
                elif(len(str(i))==5):
                    topo[2] =str(topo[3]) +  "0" + str(i)
                    topo_select.updateRow(topo)
                else:
                    arcpy.AddMessage("Existen mas de 1 millon de puntos no se puede asignar")
            else: 
                pass
            
    else:
        pass
#3. Convertir en multipunto todos aquellos que tengan los identificadores iguales
           
mul_nom = arcpy.management.Dissolve(toponimos,
                                    os.path.join(salida,"topo_dissolve.shp"),
                                    "NGIdenti_1")
#4. Cursor para evaluar la intersección con municipio con la capa multipuntos
           
municipio = arcpy.da.SearchCursor(os.path.join(base_et,"Limites_Entidades_Territoriales\Munpio"),['SHAPE@','MpCodigo'])
           
for mun in municipio:
    arcpy.AddMessage("Municipio evaluado " + str(mun[1]))
    mul = arcpy.da.UpdateCursor(os.path.join(salida,"topo_dissolve.shp"),['SHAPE@','NGIdenti_1'])
    for top in mul:
        if(mun[0].contains(top[0]) == True):
            top[1] = str(mun[1]) + str(top[1])
            mul.updateRow(top)
            arcpy.AddMessage("Codificacion encontrada en: " +str(mun[1]))
        else:
            pass
              
#5. Cursor para evaluar la interseccion con departamentos
departamento = arcpy.da.SearchCursor(os.path.join(base_et,"Limites_Entidades_Territoriales\Depto"),['SHAPE@','DeCodigo','OID@'])
for depto in departamento:
    query = "OBJECTID = {0} ".format(depto[2])
    a = arcpy.management.SelectLayerByAttribute(os.path.join(base_et,"Limites_Entidades_Territoriales\Depto"), "NEW_SELECTION", query)
    b = arcpy.management.SelectLayerByLocation(os.path.join(salida,"topo_dissolve.shp"), "WITHIN", a , 0, "NEW_SELECTION")
    arcpy.AddMessage("Evaluado Departamento: " +str(depto[1]))
    mult = arcpy.da.UpdateCursor(b,['SHAPE@','NGIdenti_1'])
    for tops in mult:
        if(len(tops[1])<15):
            tops[1] = str(depto[1]) + "000" + str(tops[1])
            mult.updateRow(tops)
            arcpy.AddMessage("Codificacion encontrada en: " +str(depto[1]))
        else:
            pass
departamento = arcpy.da.SearchCursor(os.path.join(base_et,"Limites_Entidades_Territoriales\Depto"),['SHAPE@','DeCodigo','OID@'])
for depto in departamento:
    query = "OBJECTID = {0} ".format(depto[2])
    a = arcpy.management.SelectLayerByAttribute(os.path.join(base_et,"Limites_Entidades_Territoriales\Depto"), "NEW_SELECTION", query)
    b = arcpy.management.SelectLayerByLocation(os.path.join(salida,"topo_dissolve.shp"), "WITHIN", a , 0, "SWITCH_SELECTION")
    arcpy.AddMessage("Evaluado Departamento: " +str(depto[1]))
    mult = arcpy.da.UpdateCursor(b,['SHAPE@','NGIdenti_1'])
    for tops in mult:
        if(len(tops[1])<15):
            tops[1] = "00000" + str(tops[1])
            mult.updateRow(tops)
            arcpy.AddMessage("Codificacion encontrada en: " +str(depto[1]))
        else:
            pass
#6. Cursor para actualizar los IDs en la capa de toponimos original
with arcpy.da.SearchCursor(os.path.join(salida,"topo_dissolve.shp"),['SHAPE@','NGIdenti_1']) as temp:
    for topos in temp:
        arcpy.AddMessage("Codificando: " + topos[1])
        with arcpy.da.UpdateCursor(toponimos,['SHAPE@','NGIdenti_1']) as topo:
            for nombres in topo:
                a = str(topos[1])[-7:]
                b = str(nombres[1])[-7:]
                if(a == b):
                    nombres[1]= topos[1]
                    topo.updateRow(nombres)
                else:
                    pass
# 7. Borrar Capa Temporal 
                
arcpy.AddMessage("Codificacion completa")

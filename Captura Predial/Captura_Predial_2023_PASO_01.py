# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Direccion de Gestion de Información Geografica
# Created on: 2023-08-25
# Created by: Kelly Villamil - Diego Rugeles (Supervisor Desarrollo DGIG)
# # Usage: Captura Predial 2023 PASO01
# Description:
# ---------------------------------------------------------------------------
#Librerias
import arcpy
import os
# Script arguments
predios = arcpy.GetParameterAsText(0)
gdb_salida = arcpy.GetParameterAsText(1)
carpeta_temps = arcpy.GetParameterAsText(2)
arcpy.env.overwriteOutput = True
##PASO 1: APPEND DEL FETURE LAYER CON LOS PREDIOS A LA FEATURE CLASS R_TERRENO Y ASIGNACION DEL ID_DIGITALIZACION
def asignar(predios,gdb_salida,ruta_salida_temps):
    arcpy.env.workspace = str(gdb_salida)
    edit = arcpy.da.Editor(str(gdb_salida))
    arcpy.conversion.FeatureClassToShapefile(predios,ruta_salida_temps)
    #REPROYECTAR LOS DATOS DE ENTRADA
    sistema_referencia = arcpy.SpatialReference(9377)
    
    arcpy.management.Project(os.path.join(ruta_salida_temps,'R_TERRENO.shp'), 'RURAL\TEMP_DATA', sistema_referencia)
    edit.startEditing(False, True)
    edit.startOperation()
    #FIEL MAPPING DE LOS DATOS DE ENTRADA
    schemaType = "NO_TEST"
    fieldMappings = ""
    subtype = ""
    fieldMappings = arcpy.FieldMappings()
    fieldMappings.addTable('\RURAL\R_TERRENO') #target
    ##CODIGO
    fldMap = arcpy.FieldMap()
    fldMap.addInputField('RURAL\TEMP_DATA',"Codigo")
    Codigo = fldMap.outputField
    Codigo.name, Codigo.aliasName, Codigo.type = "CODIGO", "CODIGO", "TEXT"
    fldMap.outputField = Codigo
    fieldMappings.addFieldMap(fldMap)
    ##VEREDA_CODIGO
    fldMap_2 = arcpy.FieldMap()
    fldMap_2.addInputField('RURAL\TEMP_DATA',"Vereda_Cod")
    Vereda = fldMap_2.outputField
    Vereda.name, Vereda.aliasName, Vereda.type = "VEREDA_CODIGO", "VEREDA_CODIGO", "TEXT"
    fldMap_2.outputField = Vereda
    fieldMappings.addFieldMap(fldMap_2)
    ##NUMERO_SUBTERRANEOS
    fldMap = arcpy.FieldMap()
    fldMap.addInputField('RURAL\TEMP_DATA',"Numero_Sub")
    Subterraneos = fldMap.outputField
    Subterraneos.name, Subterraneos.aliasName, Subterraneos.type = "NUMERO_SUBTERRANEOS", "NUMERO_SUBTERRANEOS", "LONG"
    fldMap.outputField = Subterraneos
    fieldMappings.addFieldMap(fldMap)
    ##CODIGO_ANTERIOR
    fldMap = arcpy.FieldMap()
    fldMap.addInputField('RURAL\TEMP_DATA',"Codigo_Ant")
    Cod_Anterior = fldMap.outputField
    Cod_Anterior.name, Cod_Anterior.aliasName, Cod_Anterior.type = "CODIGO_ANTERIOR", "CODIGO_ANTERIOR", "TEXT"
    fldMap.outputField = Cod_Anterior
    fieldMappings.addFieldMap(fldMap)
    ##CODIGO_MUNICIPIO
    fldMap = arcpy.FieldMap()
    fldMap.addInputField('RURAL\TEMP_DATA',"codigo_mun")
    Cod_mun = fldMap.outputField
    Cod_mun.name, Cod_mun.aliasName, Cod_mun.type = "CODIGO_MUNICIPIO", "CODIGO_MUNICIPIO", "TEXT"
    fldMap.outputField = Cod_mun
    fieldMappings.addFieldMap(fldMap)
    #APPEND    
    arcpy.AddMessage('Migrando los datos a la feature class R_TERRENO.....')
    arcpy.management.Append('RURAL\TEMP_DATA', '\RURAL\R_TERRENO', schemaType, fieldMappings, subtype)
    #ASIGNACION ID_DIGITALIZACION
    arcpy.AddMessage('Asignando el ID_DIGITALIZACIÓN.....')
    cursor = arcpy.da.UpdateCursor('\RURAL\R_TERRENO', ['CODIGO_MUNICIPIO','ID_DIGITALIZACION'])
    posicion = 1
    for row in cursor:
        if posicion < 10:
            row[1] = str(row[0])+'00000'+str(posicion)
        elif posicion < 100:
            row[1] = str(row[0])+'0000'+str(posicion)
        elif posicion < 1000:
            row[1] = str(row[0])+'000'+str(posicion)
        elif posicion < 10000:
            row[1] = str(row[0])+'00'+str(posicion)
        elif posicion < 100000:
            row[1] = str(row[0])+'0'+str(posicion)
        elif posicion > 100000:
            row[1] = str(row[0])+ str(posicion)
        
        posicion = posicion + 1
        cursor.updateRow(row)
    edit.stopOperation()
    edit.stopEditing(True)
    #ELIMINAR TEMPORAL REPROYECTADO
    arcpy.management.Delete('RURAL\TEMP_DATA')
if __name__ == "__main__":
    arcpy.AddMessage('___________________________')
    arcpy.AddMessage('Ejecutando')
    asignar(predios,gdb_salida,carpeta_temps)
    arcpy.AddMessage('Finalizado')

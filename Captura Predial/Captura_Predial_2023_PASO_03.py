# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Direccion de Gestion de Información Geografica
# Created on: 2023-08-25
# Created by: Kelly Villamil - Diego Rugeles (Supervisor Desarrollo DGIG)
# # Usage: Captura Predial 2023 PASO 03
# Description:
# ---------------------------------------------------------------------------
#Librerias
import arcpy
import os
# Script arguments
gdb_salida = arcpy.GetParameterAsText(0)
inspeccion = arcpy.GetParameterAsText(1)
def registrosmigrados(x, ly_migrado):
    arcpy.AddMessage("    Han sido migrados {0} registros al Feature {1}.".format(x, ly_migrado))
##PASO 3: CONVIERTE LOS POLIGONOS EN LINEA MANTENIENDO EL ID_POLIGONO COMO ID_GLOBAL ELIMINANDO DUPLICADOS EN EL SHAPE DE INSPECCION SEÑALADO POR EL USUARIO
def validacion(gdb_salida,a):
    sep= '######################################'
    arrow= '--'
    hasht= '##'
    arcpy.env.workspace = str(gdb_salida)
    arcpy.env.overwriteOutput = True
    ##CONVERSION DE POLIGONO A LINEA Y ELIMINACION DE LINEAS DUPLICADAS
    arcpy.AddMessage('Convirtiendo los poligonos de la feature class R_TERRENO a linea.....')
    arcpy.management.FeatureToLine('\RURAL\R_TERRENO', 'VALIDACION\TEMP_LINE', '0 Meters', 'ATTRIBUTES')
    arcpy.management.DeleteIdentical('\VALIDACION\TEMP_LINE', 'SHAPE', '0 Meters', '0')
    edit = arcpy.da.Editor(str(gdb_salida))
    edit.startEditing(False, True)
    edit.startOperation()
        
    dic_inspeccion = {
                        1:'PREDIOS_L_INSP1',
                        2:'PREDIOS_L_INSP2',
                        3:'PREDIOS_L_INSP3',
                        4:'None'
    }
    arcpy.AddMessage("{0} Migración a la capa de validación:".format(arrow))
    i=0
    with arcpy.da.SearchCursor('\VALIDACION\TEMP_LINE',['SHAPE@','CODIGO','CODIGO_ANTERIOR','ID_DIGITALIZACION','ID_PARTE','ID_GLOBAL']) as sCur:
        with arcpy.da.InsertCursor('\VALIDACION\{0}'.format((dic_inspeccion[a])),['SHAPE@','CODIGO','CODIGO_ANTERIOR','ID_DIGITALIZACION','ID_PARTE','ID_POLIGONO']) as iCur:
            for row in sCur:
                i+=1
                row_list= list(row)
                row=tuple(row_list)
                iCur.insertRow(row)
    registrosmigrados(i, dic_inspeccion[a])
    edit.stopOperation()
    edit.stopEditing(True)
    arcpy.management.Delete('\VALIDACION\TEMP_LINE')
if __name__ == "__main__":
    arcpy.AddMessage(inspeccion)
    if inspeccion == "inspeccion_1": 
        a = 1
    elif inspeccion == 'inspeccion_2':
        a = 2
    elif inspeccion == 'inspeccion_3':
        a = 3
    else:
        pass
    arcpy.AddMessage('___________________________')
    arcpy.AddMessage('Ejecutando')
    validacion(gdb_salida,a)
    arcpy.AddMessage('Finalizado')

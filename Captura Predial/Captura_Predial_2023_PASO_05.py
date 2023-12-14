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
    edit = arcpy.da.Editor(str(gdb_salida))
    edit.startEditing(False, True)
    edit.startOperation()
    ##CONVERSION DE POLIGONO A LINEA Y ELIMINACION DE LINEAS DUPLICADAS
    dic_inspeccion = {
        1:"PREDIOS_L_INSP1",
        2:"PREDIOS_L_INSP2",
        3:"PREDIOS_L_INSP3"
    }
    arcpy.AddMessage("{0} Migración a la capa L_TERRENO:".format(arrow))
    i=0
    with arcpy.da.SearchCursor('\VALIDACION\{0}'.format((dic_inspeccion[a])),['SHAPE@','CODIGO','CODIGO_ANTERIOR','ID_DIGITALIZACION','ID_PARTE','ID_POLIGONO','ESTADO']) as sCur:
        with arcpy.da.InsertCursor('\RURAL\L_TERRENO',['SHAPE@','CODIGO','CODIGO_ANTERIOR','ID_DIGITALIZACION','ID_PARTE','ID_GLOBAL','ESTADO']) as iCur:
            for row in sCur:
                i+=1
                row_list= list(row)
                row=tuple(row_list)
                iCur.insertRow(row)
    registrosmigrados(i, 'L_TERRENO')
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

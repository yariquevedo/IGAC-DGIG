# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Direccion de Gestion de Información Geografica
# Created on: 2023-08-25
# Created by: Kelly Villamil - Diego Rugeles (Supervisor Desarrollo DGIG)
# # Usage: Captura Predial 2023 PASO 02
# Description:
# ---------------------------------------------------------------------------
#Librerias
import arcpy
import os
# Script arguments
gdb_salida = arcpy.GetParameterAsText(0)
##PASO 2: ASIGNA SEGUN LA CANTIDAD DE POLIGONOS CON EL MISMO ID_DIGITALIZACION EL ID_PARTE (P1, P2, P3) Y CONCATENA EL ID_GLOBAL
def asignar_partes(gdb_salida):
    arcpy.env.workspace = str(gdb_salida)
    arcpy.env.overwriteOutput = True
    edit = arcpy.da.Editor(str(gdb_salida))
    edit.startEditing(False, True)
    edit.startOperation()
    ##REORGANIZA LOS DATOS POR ID_DIGITALIZACION
    arcpy.AddMessage('Reorganizando los datos.....')
    arcpy.management.Sort('\RURAL\R_TERRENO', '\RURAL\R_TERRENO_sort', [['ID_DIGITALIZACION', 'ASCENDING']])
    #ASIGNA EL ID_PARTE
    arcpy.AddMessage('Asignando el ID_PARTE.....')
    with arcpy.da.SearchCursor('\RURAL\R_TERRENO_sort', ['ID_DIGITALIZACION','OBJECTID']) as cursor:
        for row in cursor:
            #arcpy.AddMessage(row[0])
            with arcpy.da.UpdateCursor('\RURAL\R_TERRENO_sort', ['ID_DIGITALIZACION','OBJECTID','ID_Parte']) as cursor_2:
                for row_2 in cursor_2:
                    if row_2[2] == None:
                        if row[0] == row_2[0] and row[1] == row_2[1]:
                            row_2[2] = "P1"
                        elif row[0] == row_2[0] and row[1] != row_2[1]:
                            row_2[2] = "P" + str(row_2[1]-row[1]+1) #SIEMPRE SE REPITE P1
                    cursor_2.updateRow(row_2)
            arcpy.AddMessage("Predio Actualizado: " + row[0])
    
    edit.stopOperation()
    edit.stopEditing(True)
    ##ELIMINA LA CAPA ORIGINAL Y RENOMBRA LA RESULTANTE DEL SORT Y ASIGNACION DEL ID_PARTE
    arcpy.management.Delete('\RURAL\RURAL_Topology')
    arcpy.management.Delete('\RURAL\R_TERRENO')
    
    arcpy.management.DeleteField('\RURAL\R_TERRENO_sort', 'ORIG_FID', 'DELETE_FIELDS')
    #CALCULA EL ID_GLOBAL
    arcpy.AddMessage('Asignando el ID_GLOBAL.....')
    arcpy.management.CalculateField('\RURAL\R_TERRENO_sort', 'ID_GLOBAL', '!ID_DIGITALIZACION!+!ID_PARTE!', 'PYTHON3')
    #CREA DE NUEVO LA TOPOLOGIA
    arcpy.management.Rename('\RURAL\R_TERRENO_sort', 'R_TERRENO')
    arcpy.management.CreateTopology('\RURAL', 'RURAL_Topology')
    arcpy.management.AddFeatureClassToTopology('\RURAL\RURAL_Topology', '\RURAL\R_TERRENO', 1, 1)
    arcpy.management.AddRuleToTopology('\RURAL\RURAL_Topology', 'Must Not Overlap (Area)', '\RURAL\R_TERRENO')
if __name__ == "__main__":
    arcpy.AddMessage('___________________________')
    arcpy.AddMessage('Ejecutando')
    asignar_partes(gdb_salida)
    arcpy.AddMessage('Finalizado')

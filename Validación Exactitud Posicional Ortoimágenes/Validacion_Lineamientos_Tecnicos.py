# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Direccion de Gestion de Información Geografica
# Created on: 2023-11-28
# Created by: Kelly Garro
# # Usage: Validacion ORTOIMAGENES
# Description:
# ---------------------------------------------------------------------------
import arcpy
import os
from arcpy.sa import *

arcpy.env.overwriteOutput = True

dataset = arcpy.GetParameterAsText(0) #orto
salida = arcpy.GetParameterAsText(1) #folder salida

def validar(dataset, salida):

    #variables de entorno
    arrow = "=================================================================================="
    espacio= '	'

    desc = arcpy.Describe(dataset) #raster
    sr = desc.spatialReference #spatial reference
    desc_b = arcpy.Describe(os.path.join(dataset,'Band_1'))

    nombre_reporte = 'Reporte_Lineamientos_Tecnicos_'+str(desc.Name[0:-4])+'.txt'
    
    pixel_type = {
        '0' :'1-bit',
        '1' : '2-bit',
        '2' : '4-bit',
        '3' : '8-bit unsigned integer',
        '4' : '8-bit signed integer',
        '5' : '16-bit unsigned integer',
        '6' : '16-bit signed integer',
        '7' : '32-bit unsigned integer',
        '8' : '32-bit signed integer',
        '9' : '32-bit floating point',
        '10' : '64-bit double precision',
        '11' : '8-bit complex',
        '12' : '16-bit complex',
        '13' : '32-bit complex',
        '14' : '64-bit complex'
        }
    
    #arcpy.management.CalculateStatistics(dataset)

    file = open(os.path.join(str(salida),nombre_reporte), "w")    
    
    file.write(     'Reporte Validacion Lineamientos Tecnicos ORTO\n' +
                    arrow +
                    '\nDatos Generales Ortoimagen'+
                    '\n\nNombre:' + espacio + str(desc.Name) +
                    '\nTipo:' + espacio + str(desc.dataType) + '\n\n' +
                    arrow +
                    '\nSistema de Referencia Horizontal'+
                    '\n\nTipo:'+ espacio + espacio + espacio + str(sr.type) +
                    '\nNombre:' + espacio + espacio + espacio +  str(sr.name) +
                    '\nWKID:' + espacio +  espacio + espacio + str(sr.factoryCode) +
                    '\nProyeccion:' + espacio + espacio +  str(sr.projectionName) +
                    '\nElipsoide:' + espacio + espacio +  str(sr.GCS.spheroidName) +'\n\n' +
                    arrow +
                    '\nDatos de Formato' +
                    '\n\nNumero de bandas: ' + espacio +espacio + str(desc.bandCount) +
                    '\nNivel de detalle - Malla (m): ' + espacio + str(desc_b.meanCellWidth) +
                    '\nTipo de Representacion:' + espacio + espacio + str(desc.format) +
                    '\nTipo de Compresion:' +espacio + espacio + str(desc.compressionType) +
                    '\nTipo de Pixel:' + espacio + espacio + espacio + str(desc_b.pixelType) + ' ' +
                    pixel_type[str(arcpy.management.GetRasterProperties(dataset, 'VALUETYPE'))] +
                    '\nValor maximo: ' + espacio + espacio + espacio + str(arcpy.management.GetRasterProperties(dataset, 'MAXIMUM')) +
                    '\nValor minimo: ' + espacio + espacio + espacio + str(arcpy.management.GetRasterProperties(dataset, 'MINIMUM'))

                    )
    file.close()

if __name__ == '__main__':
    validar(dataset, salida)
    arcpy.AddMessage("Generando reporte de lineamientos tecnicos generales")
    arcpy.AddMessage("Finalizado")
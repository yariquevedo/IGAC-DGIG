3# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Direccion de Gestion de Información Geografica
# Created on: 2023-08-09
# Created by: Kelly Villamil - Diego Rugeles (Supervisor Desarrollo DGIG)
# # Usage: Generación de Simbología de Zonas Ambientalmente Homogéneas
# Description:
# ---------------------------------------------------------------------------
#Librerias
from sre_constants import GROUPREF_EXISTS
from tkinter.tix import ComboBox
import arcpy
import os
from arcpy import env
from arcpy.sa import *

from os import system,chdir
from osgeo import ogr
from sys import exit
#Parametros

cobertura = arcpy.GetParameterAsText(0)
suelo = arcpy.GetParameterAsText(1)
clima_shp = arcpy.GetParameterAsText(2) 
carbon = arcpy.GetParameterAsText(3)
geomorfologia = arcpy.GetParameterAsText(4)
caracter = arcpy.GetParameterAsText(5)
ruta_salida = arcpy.GetParameterAsText(6)


def paso01(cobertura,suelo,carbon,geomorfologia,clima_shp,ruta_salida,caracter):

    ##modelo ambiental_homogenea

    arcpy.env.workspace = ruta_salida
    arcpy.env.overwriteOutput = True

    #copia de los shp
    copy_cobertura = os.path.join(ruta_salida,'cobertura_2.shp')
    copy_suelo = os.path.join(ruta_salida,'suelo_2.shp')
    copy_clima = os.path.join(ruta_salida,'clima_2.shp')
    copy_carbon = os.path.join(ruta_salida,'carbon_2.shp')
    copy_geomorfologia = os.path.join(ruta_salida,'geomorfologia_2.shp')

    arcpy.management.CopyFeatures(cobertura, copy_cobertura, '', '', '', '')
    arcpy.management.CopyFeatures(suelo, copy_suelo, '', '', '', '')
    arcpy.management.CopyFeatures(clima_shp, copy_clima, '', '', '', '')
    arcpy.management.CopyFeatures(carbon, copy_carbon, '', '', '', '')
    arcpy.management.CopyFeatures(geomorfologia, copy_geomorfologia, '', '', '', '')

    #calculo critreio suelo
    arcpy.AddMessage('Calculando el campo "Crit_Suelo"......')
    arcpy.management.CalculateField(copy_suelo, 'Crit_Suelo', '(!Profun_e!*0.481)+(!Textura_x!*0.405)+(!Drenaje_d!*0.114)', 'PYTHON3','','DOUBLE','')

    #eliminar atributos innecesarios
    lista_cobertura = ['VALOR','CARACTER']
    lista_carbon = ['carbon_cla']
    lista_geomorfologia = ['Calif']
    lista_suelo = ['Crit_Suelo','Drenaje_d','Profun_e','Textura_x']
    lista_clima = ['Crit_Clima','Simbolo']

    arcpy.management.DeleteField(copy_cobertura, lista_cobertura, 'KEEP_FIELDS')
    arcpy.management.DeleteField(copy_carbon, lista_carbon, 'KEEP_FIELDS')
    arcpy.management.DeleteField(copy_geomorfologia, lista_geomorfologia, 'KEEP_FIELDS')
    arcpy.management.DeleteField(copy_suelo, lista_suelo, 'KEEP_FIELDS')
    arcpy.management.DeleteField(copy_clima, lista_clima, 'KEEP_FIELDS')

    #intersect
    arcpy.AddMessage('Realizando la intersección de las capas......')
    intersect = os.path.join(ruta_salida, 'AAH.shp')
    arcpy.analysis.Intersect([copy_clima, copy_carbon, copy_cobertura, copy_geomorfologia, copy_suelo], intersect, 'ALL', '', 'INPUT')
    arcpy.management.DeleteField(intersect, ['FID_clima_','FID_carbon','FID_cobert','FID_geomor','FID_suelo_'], 'DELETE_FIELDS')

    arcpy.management.Delete([copy_cobertura,copy_suelo,copy_carbon,copy_clima,copy_geomorfologia]) #elimina las copias

    arcpy.management.CalculateField(intersect, 'Simb_Clima', '!Simbolo!', 'PYTHON3','','TEXT','')
    arcpy.management.CalculateField(intersect, 'Crit_Carb', '!carbon_cla!', 'PYTHON3','','DOUBLE','')
    arcpy.management.CalculateField(intersect, 'Crit_Cob', '!VALOR!', 'PYTHON3','','DOUBLE','')
    arcpy.management.CalculateField(intersect, 'Simb_Cob', '!CARACTER!', 'PYTHON3','','TEXT','')
    arcpy.management.CalculateField(intersect, 'Crit_Geo', '!Calif!', 'PYTHON3','','DOUBLE','')

    arcpy.management.DeleteField(intersect, ['Simbolo','carbon_cla','VALOR','CARACTER','Calif'], 'DELETE_FIELDS')
    arcpy.management.AddField(intersect,'AREA_m','FLOAT')

 

    #calculo de parametros para clasificacion
    arcpy.AddMessage('Calculando los campos "PF_Cob", "PF_Suelo", "PF_CO", "PF_Clima", "PF_Relieve", "SP_Dren", "SP_Prof", "SP_Text", "AAH", "AAH_Porc"......') 

    arcpy.management.CalculateField(intersect, 'PF_Cob', '(!Crit_Cob!*0.418)', 'PYTHON3','','DOUBLE','')
    arcpy.management.CalculateField(intersect, 'PF_Suelo', '(!Crit_Suelo!*0.267)', 'PYTHON3','','DOUBLE','')
    arcpy.management.CalculateField(intersect, 'PF_CO', '(!Crit_Carb!*0.171)', 'PYTHON3','','DOUBLE','')
    arcpy.management.CalculateField(intersect, 'PF_Clima', '(!Crit_Clima!*0.097)', 'PYTHON3','','DOUBLE','')
    arcpy.management.CalculateField(intersect, 'PF_Rel', '(!Crit_Geo!*0.047)', 'PYTHON3','','DOUBLE','')
    
    arcpy.management.CalculateField(intersect, 'SP_Dren', '(!Drenaje_d!*0.114)', 'PYTHON3','','DOUBLE','')
    arcpy.management.CalculateField(intersect, 'SP_Prof', '(!Profun_e!*0.481)', 'PYTHON3','','DOUBLE','')
    arcpy.management.CalculateField(intersect, 'SP_Text', '(!Textura_x!*0.405)', 'PYTHON3','','DOUBLE','')
    
    arcpy.management.CalculateField(intersect, 'AAH', '(!Crit_Cob!*0.418)+(!Crit_Suelo!*0.267)+(!Crit_Carb!*0.171)+(!Crit_Clima!*0.097)+(!Crit_Geo!*0.047)', 'PYTHON3','','DOUBLE','')
    arcpy.management.CalculateField(intersect, 'AAH_Porc', '(!AAH!*100)/5', 'PYTHON3','','DOUBLE','')

    arcpy.management.RepairGeometry(intersect, 'DELETE_NULL', 'ESRI')
    arcpy.management.CalculateField(intersect, 'AREA_m', '!Shape.area!', 'PYTHON3','','FLOAT','')


    arcpy.management.AddField(intersect,'SIMBOLO','TEXT')

    p01 = '' #posicion 1
    p02 = '' #posicion 2
    p03 = '' #posicion 3
    p04 = '' #posicion 4
    p05 = '' #posicion 5 AHH Porcentaje
    
    arcpy.AddMessage('Realizando la clasificación de las áreas......')
    with arcpy.da.UpdateCursor(intersect, ['PF_Cob','PF_Suelo','PF_CO','PF_Clima','PF_Rel','Simb_Clima','Simb_Cob','AAH_Porc','SP_Dren','SP_Prof','SP_Text','SIMBOLO']) as cursor: #cursor para asignar el porcentaje
        for row in cursor:
            ##POSICION 5 (PORCENTAJE AAH)
            if row[7] > 0 and row[7] <= 20:
                p05 = '10'
            elif row[7] > 20 and row[7] <= 40:
                p05 = '30'
            elif row[7] > 40 and row[7] <= 60:
                p05 = '50'
            elif row[7] > 60 and row[7] <= 80:
                p05 = '70'
            elif row[7] > 80 and row[7] <= 100:
                p05 = '90'
            
            #POSICION 1 y 3
            mayor = 0
            posicion = 0
            simbolo_cob = ''
            simbolo_clima = ''

            for i in range(5):
                if row[i] > mayor:
                    mayor = row[i]
                    simbolo_cob = row[6]
                    simbolo_clima = row[5]
                    posicion = i

            if posicion == 0: #si es cobertura
                p01 = 'B'
                p03 = simbolo_cob
            elif posicion == 1: #si es suelo
                p01 = 'H'
                p03 = 'aaa'
                mayor_3 = 0
                posicion_3 = 0
                
                for i in range(8,11):
                    if row[i] > mayor_3:
                        mayor_3 = row[i]
                        posicion_3 = i
                if posicion_3 == 8:
                    p03 = 'd'
                if posicion_3 == 9:
                    p03 = 'e'
                if posicion_3 == 10:
                    p03 = 'x'

            elif posicion == 2: #si es carbon organico
                p01 = 'O'
                p03 = 'o'
            elif posicion == 3: #si es clima
                p01 = 'C'
                p03 = simbolo_clima
            elif posicion == 4: #si es relieve
                p01= 'R'
                p03 = 'r'
            
            #POSICION 2 y 4
            mayor_2 = 0
            posicion_2 = 0
            simbolo_cob_2 = ''
            simbolo_clima_2 = ''

            for i in range(5):
                if row[i] < mayor and row[i] > mayor_2:
                    mayor_2 = row[i]
                    simbolo_cob_2 = row[6]
                    simbolo_clima_2 = row[5]
                    posicion_2 = i

            if posicion_2 == 0: #si es cobertura
                p02 = 'B'
                p04 = simbolo_cob_2
            elif posicion_2 == 1: #si es suelo
                p02 = 'H'
                p04 = 'aaa'
                mayor_4 = 0
                posicion_4 = 0
                
                for i in range(8,11):
                    if row[i] > mayor_4:
                        mayor_4 = row[i]
                        posicion_4 = i
                if posicion_4 == 8:
                    p04 = 'd'
                if posicion_4 == 9:
                    p04 = 'e'
                if posicion_4 == 10:
                    p04 = 'x'

            elif posicion_2 == 2: #si es carbon organico
                p02 = 'O'
                p04 = 'o'
            elif posicion_2 == 3: #si es clima
                p02 = 'C'
                p04 = simbolo_clima_2
            elif posicion_2 == 4: #si es relieve
                p02= 'R'
                p04 = 'r'
            row[11] = str(caracter + p01 + p02 +  p03 +  p04 + p05)
            #arcpy.AddMessage(str(row) + ' ' + p01 + ' ' + p02 + ' ' + p03 + ' ' + p04 + ' ' + p05)
            cursor.updateRow(row)
    arcpy.management.DeleteField(intersect, ['Crit_Clima','Drenaje_d','Profun_e','Textura_x','Crit_Suelo','Simb_Clima','Crit_Carb','Crit_Cob','Simb_Cob','Crit_Geo'], 'DELETE_FIELDS')
    arcpy.AddMessage('Generando archivos raster.....')
    raster_AAH = os.path.join(ruta_salida, 'AAH_raster.tif')
    raster_AAH_Porc = os.path.join(ruta_salida, 'AAH_Porcentaje.tif')
    raster_simbologia = os.path.join(ruta_salida, 'Simbologia.tif')
    
    arcpy.conversion.FeatureToRaster(intersect, 'AAH', raster_AAH, '2.5')
    arcpy.conversion.FeatureToRaster(intersect, 'AAH_Porc', raster_AAH_Porc, '2.5')
    arcpy.conversion.FeatureToRaster(intersect, 'SIMBOLO', raster_simbologia, '2.5')


if __name__ == "__main__":
    arcpy.AddMessage('Iniciando......')
    paso01(cobertura,suelo,carbon,geomorfologia,clima_shp,ruta_salida,caracter)
    
    arcpy.AddMessage('Finalizado......')
    arcpy.AddMessage('Resultados en la Ruta de Salida......')
    arcpy.AddMessage('AAH.shp')
    arcpy.AddMessage('AAH_raster.tif')
    arcpy.AddMessage('AAH_Porcentaje.tif')
    arcpy.AddMessage('Simbologia.tif')
    arcpy.AddMessage('..................................')
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Direccion de Gestion de Información Geografica
# Created on: 2023-11-28
# Created by: Kelly Garro
# # Usage: ModelosDigitalesDeTerrenos
# Description:
# ---------------------------------------------------------------------------
import arcpy, os, string, re, math
import sys
from arcpy import env
import random
import shutil #"shutil" used to remove existing directory
import statistics
import time
arcpy.env.overwriteOutput = True
codeblock = """rec=0
def autoIncrement():
    global rec
    pStart = 1
    pInterval = 1
    if (rec == 0):
        rec = pStart
    else:
        rec += pInterval
    return rec"""
def MarcosDeControlOrtoyMDT(Limite_Del_Proyecto,RutaSalida,Escala):
    def SelectRandomByCount(layer,count,salidapuntos):
        layerCount = int(arcpy.GetCount_management(layer).getOutput(0))
        if layerCount < count:
            arcpy.AddMessage('NO EXISTEN SUFICIENTES PUNTOS PARA SELECIONAR')
            return
        oids = [oid for oid, in arcpy.da.SearchCursor(layer, "OID@")]
        oidFldName = arcpy.Describe(layer).OIDFieldName
        delimOidFld = arcpy.AddFieldDelimiters(layer, oidFldName)
        randOids = random.sample(oids, count)
        oidsStr = ",".join(map(str, randOids))
        sql = "{0} IN ({1})".format(delimOidFld, oidsStr)
        arcpy.management.MakeFeatureLayer(layer, "stateslyrs")
        arcpy.management.SelectLayerByAttribute("stateslyrs", "NEW_SELECTION", sql, "NON_INVERT")
        arcpy.management.CopyFeatures("stateslyrs", salidapuntos)
        #arcpy.management.Delete("stateslyrs")
        
    def Marcos(param0, param1, param2):
        areas = {"1000":200, "2000":400, "5000":1000, "10000":2000, "25000":4000,"50000":8000}
        OutFc= param1
        nombregdb = "Marcos_Control_Orto_MDT.gdb"
        salida = arcpy.management.CreateFileGDB(OutFc, nombregdb)
        ruta_salida = param1 +  "\\" +  nombregdb
        escala = param2
        arcpy.AddMessage("Calculando marcos de control")
        valesc = areas[str(escala)]
        sptref = arcpy.Describe(param0).spatialreference
        extent = arcpy.Describe(param0).extent
        arcpy.env.outputCoordinateSystem = sptref
        Ymin = str(extent.YMin)
        Xmin = str(extent.XMin)
        Ymax = str(extent.YMax)
        Xmax = str(extent.XMax)
        Ymin_1 = str(extent.YMin + 1) 
        print(type(Ymin))
        coords = Xmin + " "+ (Ymin)
        yAxisCoordinate = Xmin + " " + Ymin_1 
        oppositeCoorner = Xmax + " " +Ymax
        outpg = ruta_salida + "\\" + "MarcosAT"
        arcpy.management.CreateFishnet(outpg, coords, yAxisCoordinate, valesc, valesc, "0", "0", oppositeCoorner, "NO_LABELS", "", "POLYGON")
        resultgr = int(arcpy.management.GetCount(outpg).getOutput(0))
        arcpy.AddMessage("Grilla Total Generada con "+str(resultgr)+" celdas...")
        # Creacion de marcos de control dentro del limite del proyecto 
        salidagrillain = ruta_salida + "\\" + 'MarcosInt'  # Only a path for now
        arcpy.management.MakeFeatureLayer(outpg, "grillat")
        arcpy.management.SelectLayerByLocation("grillat", "COMPLETELY_WITHIN", param0)
        arcpy.management.CopyFeatures("grillat", salidagrillain)  # Now 'MarcosInt' feature class really exists
        expression = "autoIncrement()"
        arcpy.management.CalculateField(salidagrillain, "Id", expression, "PYTHON3", codeblock)
        arcpy.management.AddField(salidagrillain, "Num_elm", "DOUBLE", 0, "", "", "", "NULLABLE", "NON_REQUIRED")
        resultgri = int(arcpy.management.GetCount(salidagrillain).getOutput(0))
        arcpy.AddMessage("Grilla Intersectada con area de trabajo, "+str(resultgri)+" celdas...")
        arcpy.management.Delete("grillat")
        conteo =  str(arcpy.management.GetCount(salidagrillain))
        fields = ["SHAPE@AREA"]
        with arcpy.da.SearchCursor(param0, fields) as cursor:
            #for every row in the shapefiles attribute table
            for row in cursor:
                a = round(row[0]/10000)
        if(param2 == "1000" and a <= 1000 or 
           param2 == "2000" and a <= 1000 or 
           param2 == "5000" and a <= 15000 or
           param2 == "10000" and a <= 25000 or
           param2 == "25000" and a <= 100000 or
           param2 == "50000" and a <= 1000000):
            marcos = int(conteo) *1
        elif(param2 == "1000" and a in range(1001,2000) or 
             param2 == "2000" and a in range(1001,2000) or 
             param2 == "5000" and a in range(15001,30000)  or
             param2 == "10000" and a in range(25001,50000) or
             param2 == "25000" and a in range(100001,500000)or
             param2 == "50000" and a in range(1000001,5050000)):
            marcos = int(conteo) *0.55
        elif(param2 == "1000" and a in range(2001,10000) or 
             param2 == "2000" and a in range(2001,10000) or 
             param2 == "5000" and a in range(30001,50000)  or
             param2 == "10000" and a in range(50001,100000) or
             param2 == "25000" and a in range(500001,1000000)or
             param2 == "50000" and a in range(5005001,10000000)):
            marcos = int(conteo) *0.35
        elif(param2 == "1000" and a > 10001 or 
             param2 == "2000" and a > 10001 or 
             param2 == "5000" and a > 50001 or
             param2 == "10000" and a > 100001 or
             param2 == "25000" and a > 1000001 or 
             param2 == "50000" and a > 10000001):
            marcos = int(conteo) *0.25
        marcos_int = math.trunc(marcos)
        salidagrillai = ruta_salida + "\\" + 'MarcosRevisar' # Only a path for now
        SelectRandomByCount(salidagrillain, marcos_int, salidagrillai)
        return
    # This is used to execute code if the file was run but not imported
    if __name__ == '__main__':
        # Tool parameter accessed with GetParameter or GetParameterAsText
      
        param0 = Limite_Del_Proyecto
        param1 = RutaSalida
        param2 = Escala
        Marcos(param0, param1, param2)
        
        # Update derived parameter values using arcpy.SetParameter() or arcpy.SetParameterAsText()
    return

if __name__ == '__main__':
    # Tool parameter accessed with GetParameter or GetParameterAsText
    RutaSalida = arcpy.GetParameterAsText(0)
    Escala = arcpy.GetParameterAsText(1)
    Limite_Del_Proyecto = arcpy.GetParameterAsText(2)
    
    MarcosDeControlOrtoyMDT(Limite_Del_Proyecto,RutaSalida,Escala)

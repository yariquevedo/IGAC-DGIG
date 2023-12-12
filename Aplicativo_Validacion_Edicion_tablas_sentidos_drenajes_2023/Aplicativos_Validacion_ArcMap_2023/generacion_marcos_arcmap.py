import arcpy
import random
from arcpy import env
from arcpy.sa import *
import os
import requests
import time
import argparse
import sys
import time
import math
from datetime import datetime
# import comtypes
# from comtypes.client import GetModule
# from comtypes.client import CreateObject

GeodatabaseEntrada=sys.argv[1]
GeodatabaseSalida=sys.argv[2]
ShapefileCorte=sys.argv[3]
escala = sys.argv[4]
#Xml=sys.argv[6]
arcpy.env.overwriteOutput=True;

arcpy.CheckOutExtension("Spatial")
areas = {"1000":50, "2000":100, "5000":250, "10000":500, "25000":1000,"100000":4000}
ruta = GeodatabaseSalida.split("\\")
rnew = ruta[:-1]
sep = "\\"
rutasal = sep.join(rnew)
namem = ruta[-1].split('.')[0]
rutasalida = rutasal + "\\" + namem
arcpy.AddMessage("Guardando Resultados en: "+rutasalida)
os.mkdir(rutasalida)
filet = open(rutasalida+"\\"+"Report_"+namem+".txt","a")
filet.write("---REPORTE DEL SCRIPT PARA LA GDB "+namem+ "-----\n")

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

def SelectRandomByCount(layer, count, salidapuntos):
    layerCount = int(arcpy.GetCount_management(layer).getOutput(0))
    if layerCount < count:
        print "NO EXISTEN SUFICIENTES PUNTOS PARA SELECIONAR"
        return
    oids = [oid for oid, in arcpy.da.SearchCursor(layer, "OID@")]
    oidFldName = arcpy.Describe(layer).OIDFieldName
    delimOidFld = arcpy.AddFieldDelimiters(layer, oidFldName)
    randOids = random.sample(oids, count)
    oidsStr = ",".join(map(str, randOids))
    sql = "{0} IN ({1})".format(delimOidFld, oidsStr)
    arcpy.MakeFeatureLayer_management (layer, "stateslyrs")
    arcpy.SelectLayerByAttribute_management("stateslyrs", "", sql)
    arcpy.CopyFeatures_management("stateslyrs", salidapuntos)
    arcpy.Delete_management("stateslyrs")

arcpy.CreateFileGDB_management(os.path.dirname(GeodatabaseSalida),os.path.basename(GeodatabaseSalida))

#####################
#arcpy.FeatureClassToFeatureClass_conversion(ShapefileCorte,GeodatabaseEntrada + "\\Indice_Mapas","CORTE" )
CORTE = ShapefileCorte
arcpy.AddMessage("Cortando Geodatabase")
arcpy.env.workspace = GeodatabaseEntrada
datasetList = arcpy.ListDatasets()
for dataset in datasetList:
    if(dataset!="IndiceMapas" and dataset!="OrdenamientoTerritorial"):
        arcpy.AddMessage('Analizando Dataset '+dataset)
        filet.write('Analizando Dataset '+dataset + "\n")
        arcpy.env.workspace = GeodatabaseEntrada + "\\" + dataset
        descd = arcpy.Describe(GeodatabaseEntrada + "\\" + dataset)
        sr = descd.spatialreference
        arcpy.CreateFeatureDataset_management(GeodatabaseSalida, dataset, sr)
        fcList = arcpy.ListFeatureClasses()
        for fc in fcList:
            result = int(arcpy.GetCount_management(fc).getOutput(0))
            try:
                if result>0:
                    if(fc!="Bosque" and fc!="Cerca"):
                        arcpy.AddMessage('Cortando FeatureClass '+fc)
                        filet.write("Corte del Feature "+fc + "\n")
                        fcSal=GeodatabaseSalida + "\\" + dataset + "\\" + fc
                        desc = arcpy.Describe(fc)
                        if(desc.featureType!="Annotation"):
                            if(arcpy.Exists(fc+"_Anot")):
                                arcpy.Clip_analysis(fc+"_Anot", CORTE , fcSal+"_Anot")
                            arcpy.Clip_analysis(fc, CORTE , fcSal)
            except Exception as ex:
                arcpy.AddMessage("Error..."+ex.message)

del datasetList
del fcList
arcpy.AddMessage("GDB Cortada...")
arcpy.AddMessage("Generando grilla...")
valesc = areas[str(escala)]
sptref = arcpy.Describe(ShapefileCorte).spatialreference
extent = arcpy.Describe(ShapefileCorte).extent
arcpy.env.outputCoordinateSystem = sptref
coords = str(extent.XMin) + " " + str(extent.YMin)
yAxisCoordinate = str(extent.XMin) + " " + str(extent.YMin+1)
oppositeCoorner = str(extent.XMax) + " " + str(extent.YMax)
outpg = rutasalida + "\\" + 'MarcosAT' + namem + '.shp'
arcpy.CreateFishnet_management(outpg, coords, yAxisCoordinate, valesc, valesc, "0", "0", oppositeCoorner, "NO_LABELS", "", "POLYGON")
resultgr = int(arcpy.GetCount_management(outpg).getOutput(0))
arcpy.AddMessage("Grilla Total Generada con "+str(resultgr)+" celdas...")
filet.write("Grilla Total Generada con "+str(resultgr)+" celdas..." + "\n")

#Interseccion Area Proyecto
salidagrillain = rutasalida + "\\" + 'MarcosInt_'+namem.replace('-','')+'.shp'
arcpy.MakeFeatureLayer_management (outpg, "grillat")
arcpy.SelectLayerByLocation_management("grillat", "COMPLETELY_WITHIN", ShapefileCorte)
arcpy.CopyFeatures_management("grillat", salidagrillain)
#arcpy.AddField_management(salidagrillai, "Id", "DOUBLE", 0, "", "", "", "NULLABLE", "REQUIRED")
expression = "autoIncrement()"
arcpy.CalculateField_management(salidagrillain, "Id", expression, "PYTHON_9.3", codeblock)
arcpy.AddField_management(salidagrillain, "Num_elm", "DOUBLE", 0, "", "", "", "NULLABLE", "NON_REQUIRED")
resultgri = int(arcpy.GetCount_management(salidagrillain).getOutput(0))
arcpy.AddMessage("Grilla Intersectada con area de trabajo, "+str(resultgri)+" celdas...")
filet.write("Grilla Intersectada con area de trabajo, "+str(resultgri)+" celdas..." + "\n")
arcpy.Delete_management("grillat")

if resultgri>30:
    arcpy.AddMessage("Se seleccionaran 30 marcos de los "+str(resultgri)+" intersectados...")
    filet.write("Se seleccionaran 30 marcos de los "+str(resultgri)+" intersectados..." + "\n")
    salidagrillai = rutasalida + "\\" + 'Marcos30_'+namem.replace('-','')+'.shp'
    SelectRandomByCount(salidagrillain,30,salidagrillai)
else:
    salidagrillai = rutasalida + "\\" + 'MarcosInt_'+namem.replace('-','')+'.shp'



field_names = [i.name for i in arcpy.ListFields(salidagrillai) if i.type != 'OID']
cursor = arcpy.da.SearchCursor(salidagrillai, field_names)
numelementos = 0
for row in cursor:
    idc = row[1]
    exp = "Id="+str(idc)
    arcpy.AddMessage('Calculando Grilla Id: '+ str(idc))
    filet.write('Calculando Grilla Id: '+ str(idc) + "\n")
    arcpy.MakeFeatureLayer_management(salidagrillai, "grillac")
    arcpy.SelectLayerByAttribute_management("grillac","NEW_SELECTION",exp)
    arcpy.env.workspace = GeodatabaseSalida
    datasetList = arcpy.ListDatasets()
    numcapas = 0
    for dataset in datasetList:
        arcpy.env.workspace = GeodatabaseSalida + "\\" + dataset
        fcList = arcpy.ListFeatureClasses()
        for fc in fcList:
            outName_gr = rutasalida + "\\" + 'Gr_'+str(idc)+str(fc)+'.shp'
            inFeatures_pc = ["grillac", fc]
            arcpy.Intersect_analysis(inFeatures_pc, outName_gr)
            result = int(arcpy.GetCount_management(outName_gr).getOutput(0))
            arcpy.AddMessage("El numero de elementos de "+str(fc)+" es: "+str(result))
            filet.write("El numero de elementos de "+str(fc)+" es: "+str(result) + "\n")
            numcapas += result
            arcpy.Delete_management(outName_gr)

    arcpy.CalculateField_management("grillac", "Num_elm", numcapas, "PYTHON_9.3")
    arcpy.AddMessage("El numero de elementos en la grilla "+ str(idc)+" es: "+ str(numcapas))
    filet.write("El numero de elementos en la grilla "+ str(idc)+" es: "+ str(numcapas) + "\n")
    arcpy.Delete_management("grillac")
    numelementos += numcapas

arcpy.AddMessage("El numero de elementos en todas las celdas es "+ str(numelementos))
filet.write("El numero de elementos en todas las celdas es "+ str(numelementos) + "\n")
arcpy.Delete_management("grillac")

salidatb = rutasalida + "\\tablagr"
#Sumar areas del area del proyecto
arcpy.Statistics_analysis(salidagrillai, salidatb, [["Num_elm", "SUM"]])
field_namespr = [i.name for i in arcpy.ListFields(salidatb) if i.type != 'OID']
cursorpr = arcpy.da.SearchCursor(salidatb, field_namespr)
datapr =[row for row in cursorpr]
numel_total = datapr[0][2]
result= arcpy.GetCount_management(salidagrillai)
numel_gr = int(result.getOutput(0))
pr_elmgr = numel_total/numel_gr
numel_totales = pr_elmgr*resultgri
# arcpy.AddMessage("numel_total es: "+ str(numel_total))
# arcpy.AddMessage("numel_totales es: "+ str(numel_totales))

count = int(numel_totales)
z = 1.96
p = 0.03
e = 0.01
a = (z*z)*(p)*(1-p)
b = (e*e)
c = (count-1)/ float(count)
d = count*(e*e)
ef = a/d
f = c + ef
g = a/b
o = g/f 
n = int(o)

num_mr = int(math.ceil(n/pr_elmgr))

arcpy.AddMessage("Tamaño de muestra minimo en elementos "+str(n))
filet.write("\n \n")
filet.write("Tamaño de muestra minimo en elementos "+str(n) + "\n")
if num_mr <= 15:
    arcpy.AddMessage("El numero de marcos obtenidos es "+str(num_mr)+ " se dejaran todos los marcos inicialmente generados, "+ str(numel_gr))
    filet.write("El numero de marcos obtenidos es "+str(num_mr)+ " se dejaran todos los marcos inicialmente generados, "+ str(numel_gr) + "\n")
else:
    arcpy.AddMessage("El numero de marcos obtenidos es "+str(num_mr)+ ", se extraera dicha cantidad de marcos.")
    filet.write("El numero de marcos obtenidos es "+str(num_mr)+ ", se extraera dicha cantidad de marcos." + "\n")
    arcpy.AddMessage("Generando Marcos Aleatorios..")
    # outName = 'PuntosA.shp'
    # arcpy.CreateRandomPoints_management(rutasalida, outName, ShapefileCorte, "", num_mr, valesc)
    # arcpy.MakeFeatureLayer_management (outpg, "grillati")
    # arcpy.SelectLayerByLocation_management("grillati", "intersect", rutasalida+"\\"+outName)
    # salidagrillap = rutasalida + "\\" + 'MarcosCS_'+namem.replace('-','')+'.shp'
    # arcpy.CopyFeatures_management("grillati", salidagrillap)
    out_points = rutasalida + "\\" + 'MarcosCS_'+namem.replace('-','')+'.shp'
    SelectRandomByCount(salidagrillain,num_mr,out_points)
    arcpy.AddMessage("Marcos de control generados")
    filet.write("Marcos de control generados" + "\n")
    # arcpy.Delete_management("grillati")
    # arcpy.Delete_management(rutasalida+"\\"+outName)
    

arcpy.Delete_management(salidatb)


filet.close()































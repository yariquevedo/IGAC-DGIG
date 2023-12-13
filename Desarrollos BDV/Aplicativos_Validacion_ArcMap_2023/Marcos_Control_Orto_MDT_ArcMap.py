import arcpy
import random
import math
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
    arcpy.MakeFeatureLayer_management (layer, "stateslyrs")
    arcpy.SelectLayerByAttribute_management("stateslyrs", "", sql)
    arcpy.CopyFeatures_management("stateslyrs", salidapuntos)
    arcpy.Delete_management("stateslyrs")
    

def Marcos(param0, param1, param2, codeblock):
    areas = {"1000":50, "2000":100, "5000":250, "10000":500, "25000":1000,"50000":2000,"100000":4000}
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
    arcpy.CreateFishnet_management(outpg, coords, yAxisCoordinate, valesc, valesc, "0", "0", oppositeCoorner, "NO_LABELS", "", "POLYGON")
    resultgr = int(arcpy.GetCount_management(outpg).getOutput(0))
    arcpy.AddMessage("Grilla Total Generada con "+str(resultgr)+" celdas...")
    # Creacion de marcos de control dentro del limite del proyecto 
    salidagrillain = ruta_salida + "\\" + 'MarcosInt'  # Only a path for now
    arcpy.MakeFeatureLayer_management(outpg, "grillat")
    arcpy.SelectLayerByLocation_management("grillat", "COMPLETELY_WITHIN", param0)
    arcpy.CopyFeatures_management("grillat", salidagrillain)  # Now 'MarcosInt' feature class really exists
    expression = "autoIncrement()"
    arcpy.management.AddField(salidagrillain, "Id", "LONG") 
    arcpy.management.CalculateField(salidagrillain, "Id", expression, "PYTHON_9.3", codeblock)
    arcpy.AddField_management(salidagrillain, "Num_elm", "DOUBLE", 0, "", "", "", "NULLABLE", "NON_REQUIRED")
    resultgri = int(arcpy.GetCount_management(salidagrillain).getOutput(0))
    arcpy.AddMessage("Grilla Intersectada con area de trabajo, "+str(resultgri)+" celdas...")
    arcpy.Delete_management("grillat")
    conteo =  str(arcpy.management.GetCount(salidagrillain))
    marcos = int(conteo) *0.30
    marcos_int = math.trunc(marcos)
    salidagrillai = ruta_salida + "\\" + 'MarcosRevisar' # Only a path for now
    SelectRandomByCount(salidagrillain, marcos_int, salidagrillai)
    return

# This is used to execute code if the file was run but not imported
if __name__ == '__main__':

    # Tool parameter accessed with GetParameter or GetParameterAsText
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
    param0 = sys.argv[1]
    param1 = sys.argv[2]
    param2 = sys.argv[3]
    Marcos(param0, param1, param2, codeblock)
    
    # Update derived parameter values using arcpy.SetParameter() or arcpy.SetParameterAsText()
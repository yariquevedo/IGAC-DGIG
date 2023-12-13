# -*- #################
# ---------------------------------------------------------------------------
# Direccion de Gestion de InformaciÃ³n Geografica
# Created on: 2023-03-24
# # Usage: A partir de un insumo (curvas de nivel y drenaje_L) se valida que no exitan interesecciones entre estos.
# Description: 
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
import os

# Script arguments
Ruta_GDB_Salida = arcpy.GetParameterAsText(0)
Feature_Class_Curvas_Nivel = arcpy.GetParameterAsText(1)
Feature_Class_Drenaje_L = arcpy.GetParameterAsText(2)

# Local variables:
Salida_gdb = os.path.join(Ruta_GDB_Salida, "Salida.gdb")   		  									#ok
Puntos_Intersect = os.path.join(Salida_gdb,"Puntos_Intersect")     									#ok 
Puntos_Interseccion_Multipar = os.path.join(Salida_gdb,"Puntos_Interseccion_Multipar")				#ok
Puntos_Interseccion_Multip_stats = os.path.join(Salida_gdb,"Puntos_Interseccion_Multip_stats")   	#ok
Puntos_Intersect_Layer = os.path.join(Salida_gdb,"Puntos_Intersect_Layer") 						  	#ok
Puntos_Revision = os.path.join(Salida_gdb,"Puntos_Revision") 					  					#ok

# Process: Create File GDB
arcpy.CreateFileGDB_management(Ruta_GDB_Salida, "Salida", "CURRENT")

# Process: Intersect
arcpy.Intersect_analysis([Feature_Class_Curvas_Nivel, Feature_Class_Drenaje_L], Puntos_Intersect, "ALL", "", "POINT")

# Process: Multipart To Singlepart
arcpy.MultipartToSinglepart_management(Puntos_Intersect, Puntos_Interseccion_Multipar)

# Process: Summary Statistics
arcpy.Statistics_analysis(Puntos_Interseccion_Multipar, Puntos_Interseccion_Multip_stats, "ORIG_FID COUNT", "ORIG_FID")

# Process: Join Field
arcpy.JoinField_management(Puntos_Intersect, "OBJECTID", Puntos_Interseccion_Multip_stats, "ORIG_FID", "FREQUENCY")

# Process: Add Field
arcpy.AddField_management(Puntos_Intersect, "Estado_Intersect", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Calculate Field
arcpy.CalculateField_management(Puntos_Intersect, "Estado_Intersect", "estado(!FREQUENCY!)", "PYTHON_9.3", "def estado(a):\\n    if (a>1):\\n        b = \"REVISAR\"\\n        return b \\n    else: \\n        b = \"OMITIR\"\\n        return b ")

# Process: Make Feature Layer
arcpy.MakeFeatureLayer_management(Puntos_Intersect, Puntos_Intersect_Layer, "", "", "OBJECTID OBJECTID VISIBLE NONE;SHAPE SHAPE VISIBLE NONE;FID_Drenaj_L FID_Drenaj_L VISIBLE NONE;DIdentif DIdentif VISIBLE NONE;DEstado DEstado VISIBLE NONE;DDisperso DDisperso VISIBLE NONE;DNombre DNombre VISIBLE NONE;FID_CNivel FID_CNivel VISIBLE NONE;CNIdentif CNIdentif VISIBLE NONE;CNAltura CNAltura VISIBLE NONE;CNTipo CNTipo VISIBLE NONE;FREQUENCY FREQUENCY VISIBLE NONE;Estado_Intersect Estado_Intersect VISIBLE NONE")

# Process: Select Layer By Attribute
arcpy.SelectLayerByAttribute_management(Puntos_Intersect_Layer, "NEW_SELECTION", "Estado_Intersect = 'REVISAR'")

# Process: Feature Class to Feature Class (2)
arcpy.FeatureClassToFeatureClass_conversion(Puntos_Intersect_Layer, Salida_gdb, "Puntos_Revision", "", "FREQUENCY \"FREQUENCY\" true true false 0 Long 0 0 ,First,#,Salida.gdb\\Puntos_Intersect,FREQUENCY,-1,-1;Estado_Intersect \"Estado_Intersect\" true true false 0 Text 0 0 ,First,#,Salida.gdb\\Puntos_Intersect,Estado_Intersect,-1,-1", "")

# Process: Alter Field
arcpy.AlterField_management(Puntos_Revision, "FREQUENCY", "NumIntersec", "Numero_de_Intersecciones", "", "", "NON_NULLABLE", "false")

arcpy.AddMessage("\n............................Resultados............................")
arcpy.AddMessage("Se encontraron {0} puntos intersectados entre Drenaje_L y Curvas de nivel. \n->Validar en  Feature: Puntos_Revision.".format(arcpy.GetCount_management(Puntos_Revision)))
arcpy.AddMessage("\n..................................................................")







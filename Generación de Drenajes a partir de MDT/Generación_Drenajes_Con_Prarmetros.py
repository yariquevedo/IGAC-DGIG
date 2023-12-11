import arcpy, os ,sys

entradaDEM = arcpy.GetParameterAsText(0)
resultadosCarpeta = arcpy.GetParameterAsText(1)
valorCeldas = arcpy.GetParameterAsText(2)
eliminacionSegmentos = arcpy.GetParameterAsText(3)
suavizar = arcpy.GetParameterAsText(4)
longitud = arcpy.GetParameterAsText(5)
Tolerancia = arcpy.GetParameterAsText(6)
Distancia_entre_curvas = arcpy.GetParameterAsText(7)
Tipo_flujo = arcpy.GetParameterAsText(8)
Metodologia_direccion_de_flujo = arcpy.GetParameterAsText(9)
flujo= arcpy.GetParameterAsText(10)

arcpy.env.overwriteOutput = True


arcpy.env.workspace=resultadosCarpeta
######################################################################################
rutaDrenajes = resultadosCarpeta+os.sep+os.path.basename(entradaDEM).replace(".tif","")+"_Dreanajes.shp"
rutaCurvas = resultadosCarpeta+"/"+os.path.basename(entradaDEM).replace(".tif","")+"_Curvas.shp"

arcpy.AddMessage("Rellenado vacios")
RellenoSalida = arcpy.sa.Fill(entradaDEM)
################################
arcpy.AddMessage("Dirección de drenaje")
direccionDrenajes = arcpy.sa.FlowDirection(in_surface_raster=RellenoSalida, force_flow=Tipo_flujo,flow_direction_type=Metodologia_direccion_de_flujo)
###############################
arcpy.AddMessage("Acumulación de flujo")
acumulacionFlujo= arcpy.sa.FlowAccumulation(direccionDrenajes, "", "FLOAT")
####################################################
arcpy.AddMessage("Reducción de Red de Drenajes")

acumulacionFlujoRestringida= arcpy.sa.SetNull(acumulacionFlujo, "1", "Value < " + valorCeldas)
#############################
arcpy.AddMessage("Orden de la red")
ordenDrenajes = arcpy.sa.StreamOrder(acumulacionFlujoRestringida, direccionDrenajes, flujo)

##############################

arcpy.AddMessage("Conversión de raster a Shape")
Drenajes= arcpy.sa.StreamToFeature(ordenDrenajes, direccionDrenajes, resultadosCarpeta+"/"+os.path.basename(entradaDEM).replace(".tif","")+"_Dreanajes.shp", "SIMPLIFY")
arcpy.AddMessage(resultadosCarpeta+os.sep+os.path.basename(entradaDEM).replace(".tif","")+"_Dreanajes.shp")
arcpy.AddMessage("Creación de curvas de nivel")
arcpy.sa.Contour(RellenoSalida, resultadosCarpeta+"/"+os.path.basename(entradaDEM).replace(".tif","")+"_Curvas.shp", Distancia_entre_curvas, "0", "1")

DrenajesCorregidos=arcpy.management.Dissolve(Drenajes,rutaDrenajes.replace(".shp","_DEF.shp"),"GRID_CODE","","SINGLE_PART","UNSPLIT_LINES")
arcpy.management.Delete(Drenajes)
arcpy.management.Rename(DrenajesCorregidos,rutaDrenajes)

if eliminacionSegmentos=="true":
    #!shape.length@meters!
    arcpy.AddMessage("Eliminando Segmentos cortos")
    arcpy.management.AddField(Drenajes,"Longitud","DOUBLE")
    arcpy.management.CalculateField(Drenajes,"Longitud","!shape.length@meters!","PYTHON3")
    arcpy.management.MakeFeatureLayer(Drenajes, "BorrarDrenajes", """ "Longitud" < {} AND "GRID_CODE"=1 """.format(longitud))
    #arcpy.AddMessage(""" "Longitud" < {} AND "GRID_CODE"=1 """.format(longitud))
    #arcpy.AddMessage(""" "Longitud" < 150 AND "GRID_CODE"=1 """)
    arcpy.management.DeleteFeatures("BorrarDrenajes")

if suavizar == "true":
    arcpy.AddMessage("Suavizando Curvas y Drenajes")
    arcpy.cartography.SmoothLine(rutaDrenajes,rutaDrenajes.replace(".shp","Suavisados.shp"),"PAEK", Tolerancia+" Meters", "FIXED_CLOSED_ENDPOINT", "FLAG_ERRORS")
    arcpy.cartography.SmoothLine(rutaCurvas,rutaCurvas.replace(".shp","Suavisados"),"PAEK", Tolerancia+" Meters", "FIXED_CLOSED_ENDPOINT", "FLAG_ERRORS")
    

    










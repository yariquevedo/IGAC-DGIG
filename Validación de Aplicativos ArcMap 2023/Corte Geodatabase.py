#RECIBE LOS PARÃMETROS DE ENTRADA
import arcpy
#arcpy.env.autoCancelling = False
gdb = arcpy.GetParameterAsText(0)
poligono =arcpy.GetParameterAsText(1)
foldersalida =arcpy.GetParameterAsText(2)
nombregdb =arcpy.GetParameterAsText(3)
#gdb = "C:/Users/marlon.ruiz/Documents/Toolbox_Corte_Geodatabase/100K_2019_V1.gdb"
#poligono = "C:/Users/marlon.ruiz/Documents/Toolbox_Corte_Geodatabase/CHIRIBIQUETE_50K.shp"
#foldersalida = "C:/Users/marlon.ruiz/Documents/Toolbox_Corte_Geodatabase"
#nombregdb = "prueba_xml"
try:
    if arcpy.env.isCancelled==False:
        if arcpy.Exists(foldersalida+"/"+nombregdb+".gdb")==False:
            arcpy.AddMessage("GDB de entrada:\n"+gdb+"\nPoligno de recorte:\n"+poligono+"\nGDB de salida:\n"+foldersalida+"/"+nombregdb+".gdb")
            arcpy.AddMessage("Exportando esquema de la base de datos de entrada")
            arcpy.ExportXMLWorkspaceDocument_management(gdb, foldersalida+"/"+nombregdb+".xml", "SCHEMA_ONLY", "BINARY", "METADATA")
            #Creando la nueva GDB
            dWs = arcpy.Describe(gdb)
            desc = arcpy.Describe(poligono)
            if (gdb[-4:]==".gdb" or gdb[-4:]==".mdb") and desc.shapeType == "Polygon":
                if dWs.workspaceFactoryProgID != "":
                    arcpy.AddMessage("***Creando la nueva base de datos")
                    arcpy.CreateFileGDB_management(foldersalida,nombregdb + ".gdb")
                    arcpy.AddMessage("***Base de datos creada "+nombregdb + ".gdb")
                    arcpy.AddMessage("Importando el esquema a la nueva base de datos")
                    arcpy.ImportXMLWorkspaceDocument_management(foldersalida+"/"+nombregdb+".gdb",  foldersalida+"/"+nombregdb+".xml", "SCHEMA_ONLY", "DEFAULTS")
                    arcpy.AddMessage("Esquema importado a la nueva base de datos")
                    arcpy.AddMessage("Creando una base de datos temporal en la ruta de salida")
                    arcpy.CreateFileGDB_management(foldersalida,"temporal.gdb")
                    arcpy.AddMessage("***\nPor favor no intente abrir la gdb Temporal ni la creada\n")
                    arcpy.env.workspace = dWs.path+"/"+dWs.baseName+".gdb"
                    LFD = arcpy.ListDatasets("","Feature")
                    arcpy.AddMessage("***Features Dataset dentro de la gdb de entrada \n ")
                    for l in LFD:
                        arcpy.AddMessage("\t"+l)
                    arcpy.AddMessage("***\nPor favor no intente abrir la gdb Temporal ni la creada\n")
                    for fd in LFD:
                        spreference = arcpy.Describe(fd).spatialReference
                        gdbentrada = foldersalida+"/temporal.gdb"
                        #la siguiente funcion varia respecto a pro
                        arcpy.management.CreateFeatureDataset(gdbentrada,fd,spreference)
                    LFC_vacios=[]
                    LFC=[]
                    arcpy.AddMessage("***\nPor favor no intente abrir la gdb Temporal ni la creada\n")
                    for fd in LFD:
                        arcpy.env.workspace = dWs.path+"/"+dWs.baseName+".gdb/"+str(fd)
                        datos=arcpy.ListFeatureClasses()
                        #arcpy.AddMessage(str(fd)+"\n\n"+str(datos)+"\n\n")
                        #Realizando el clip para las capas en los fature dataset creados
                        for i in datos:
                            entrada= dWs.path+"/"+dWs.baseName+".gdb/"+str(fd)+"/"+str(i)
                            salida=foldersalida+"/temporal.gdb"+"/"+str(fd)+"/"+str(i)
                            destino=foldersalida+"/"+nombregdb+".gdb"+"/"+str(fd)+"/"+str(i)
                            arcpy.analysis.Clip(entrada,poligono,salida, None)
                            #arcpy.AddMessage("\nRuta del Feature class generado, recortado por el poligono\n\n"+poligono+":\n"+str(salida))
                            if int(arcpy.management.GetCount(salida).getOutput(0)):
                                #arcpy.AddMessage("\n\n\t\t\t No esta vacia\n\n")
                                arcpy.management.Append(salida,destino,"NO_TEST")
                                LFC.append(destino)
                            else:
                                #arcpy.AddMessage("\n\n\t\t\t Vacia\n\n")
                                LFC_vacios.append(destino)
                    arcpy.AddMessage("***\nPor favor no intente abrir la gdb Temporal ni la creada\n")
                    arcpy.AddMessage("\n***Features Class con informacion dentro de la gdb de salida \n ")
                    for l1 in LFC:
                        arcpy.AddMessage("\t"+l1)
                    arcpy.AddMessage("***\nPor favor no intente abrir la gdb Temporal ni la creada\n")
                    arcpy.AddMessage("\n***Features Class vacios dentro de la gdb de salida \n ")
                    for l2 in LFC_vacios:
                        arcpy.AddMessage("\t"+l2)
            #arcpy.management.Delete(foldersalida+"/"+nombregdb+".xml")
            #arcpy.management.Delete(foldersalida+"/temporal.gdb")
            #arcpy.management.Delete(foldersalida+"/"+nombregdb+".gdb")
        else:
            arcpy.AddError("La base de datos de destino YA existe, por favor ingrese un nombre distinto para la GDB\n O elimine la base del directorio\n"+foldersalida)
    #elif arcpy.env.isCancelled==True:
    #    raise arcpy.ExecuteError
except arcpy.ExecuteError as err:
    arcpy.AddError(err)
finally:
    # If tool is cancelled or finishes successfully, clean up intermediate data
    #if arcpy.Exists(foldersalida+"/"+nombregdb+".gdb")==True:
    #    arcpy.management.Delete(foldersalida+"/"+nombregdb+".gdb")
    arcpy.AddMessage(arcpy.GetMessages())
    if arcpy.Exists(foldersalida+"/"+nombregdb+".xml")==True:
        arcpy.management.Delete(foldersalida+"/"+nombregdb+".xml")
    if arcpy.Exists(foldersalida+"/temporal.gdb")==True:
        arcpy.management.Delete(foldersalida+"/temporal.gdb")









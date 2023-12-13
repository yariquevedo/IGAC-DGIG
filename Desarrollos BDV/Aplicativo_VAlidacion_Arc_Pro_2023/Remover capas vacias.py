import arcpy
import os

def MapearFileGDB(admin_workspace):
    analyze_contents = []
    arcpy.AddMessage("\n***Mapeando la File Geoatabase")
    for dirpath, workspaces, datatypes in arcpy.da.Walk(
            admin_workspace,
            followlinks=True):
        # Cree una ruta completa y agregue tablas, clases de entidad y conjuntos de datos rÃ¡ster
        analyze_contents += [
            os.path.join(dirpath, datatype) for datatype in datatypes]
        # cree la ruta completa, agregue los conjuntos de datos de caracterÃ­sticas del archivo .GDB
        analyze_contents += [
            os.path.join(dirpath, workspace) for workspace in workspaces]
    return analyze_contents

def analizarGDB(analyze_contents):
    FC = []
    FD = []
    REL = []
    SID = []
    arcpy.AddMessage("\n***Analizando el contenido de la base de datos")
    for i in analyze_contents:
        description=arcpy.Describe(i)
        #print(description.dataElementType+"\t"+description.baseName+"\n")
        if description.dataElementType=="DEFeatureClass":
            FC.append(i)
        elif description.dataElementType=="DEFeatureDataset":
            FD.append(i)
        elif description.dataElementType=="DERelationshipClass":
            REL.append(i)
        else:
            SID.append(i)
    return FC,FD,REL,SID

def borrarFeatures(FC,FD,REL,SID):   
    arcpy.AddMessage("\n***Borrando los contenidos vacios")
    print("\n***Features Class")
    arcpy.AddMessage("\n***Features Class sin eliminar")
    for i in FC:
        if int(arcpy.management.GetCount(i).getOutput(0))==0:
            arcpy.management.Delete(i)
        else:
            print("**"+i)
            arcpy.AddMessage("**"+i)
    #print("\n***Relaciones")
    #for i in range(len(REL)):
    #    print("**"+i)
    print("\n***Features Dataset")
    arcpy.AddMessage("\n***Features Dataset sin eliminar")
    for i in FD:
        arcpy.env.workspace = i
        datos=arcpy.ListFeatureClasses()
        if len(datos) == 0 or datos ==[] :
            arcpy.management.Delete(i)
        else:
            print("**"+i)
            arcpy.AddMessage("**"+i)
    #print("\n***Elementos sin identificar")
    #for i in range(len(SID)):
    #    print("**"+i)
    #if int(arcpy.management.GetCount(i).getOutput(0)):

try:
    #admin_workspace = r"C:\Users\marlon.ruiz\Downloads\toolbook_corte\toolbook_corte\chibiriquete.gdb"
    admin_workspace = arcpy.GetParameterAsText(0)
    admin_workspace_output = arcpy.GetParameterAsText(1)
    des = arcpy.Describe(admin_workspace)
    if admin_workspace_output == '':
        arcpy.AddMessage("\n*** No hay directorio de trabajo seleccionado\nSe limpiarÃ¡n los features vacios de la base de datos: "+admin_workspace)
        #analyze_contents = MapearFileGDB(admin_workspace)
        FC,FD,REL,SID = analizarGDB(MapearFileGDB(admin_workspace))
        borrarFeatures(FC,FD,REL,SID)
    elif arcpy.Exists(admin_workspace_output+"/"+des.baseName+".gdb")==False:
        arcpy.AddMessage("*** Copiando la base de datos al directorio"+admin_workspace_output)
        arcpy.management.Copy(admin_workspace,admin_workspace_output+"/"+des.baseName+".gdb","Workspace", None)
        analyze_contents = MapearFileGDB(admin_workspace_output+"/"+des.baseName+".gdb")
        FC,FD,REL,SID = analizarGDB(analyze_contents)
        borrarFeatures(FC,FD,REL,SID)
        #arcpy.CreateFileGDB_management(admin_workspace_output,des.baseName + ".gdb")
    else:
        arcpy.AddError("La base de datos de destino YA existe en el directorio seleccionado, por favor ingrese un directorio distinto para la GDB\n O elimine la base del directorio\n"+admin_workspace_output)
    arcpy.AddWarning("En esta versiÃ³n esta herramienta borra Ãºnicamente Fetaure Dataset y Feature class de cualquier tipo de geometria con sus respectivas relaciones\n")
    arcpy.AddWarning("Si desea eliminar otro conjunto de datos vacios por favor contactese con el desarrollador para implementarlo en la herramienta\")
except arcpy.ExecuteError as err:
    arcpy.AddError(err)





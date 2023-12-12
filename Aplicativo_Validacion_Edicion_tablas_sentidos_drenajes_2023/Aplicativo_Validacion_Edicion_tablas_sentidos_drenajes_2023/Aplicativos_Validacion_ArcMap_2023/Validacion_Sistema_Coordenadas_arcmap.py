import arcpy , os
from arcpy import env 
def ScriptTool(param0, param1):
    env.workspace = param0
    file = open(os.path.join(param1,'Validacion_Corrdenadas_GDB.txt'), "w")
    # Script execution code goes here
    name = str(env.workspace).split("\\")
    print (name[-1])
    datasetList = arcpy.ListDatasets ('*','Feature')
    for i in datasetList:
        file.write((i) + ": "+ arcpy.Describe(i).spatialReference.name + " "+ "EPSG: " + str(arcpy.Describe(i).spatialReference.factoryCode) + "\n" )
    return
# This is used to execute code if the file was run but not imported
if __name__ == '__main__':
    # Tool parameter accessed with GetParameter or GetParameterAsText
    param0 = arcpy.GetParameterAsText(0)
    param1 = arcpy.GetParameterAsText(1)
    
    ScriptTool(param0, param1)
    
    # Update derived parameter values using arcpy.SetParameter() or arcpy.SetParameterAsText()

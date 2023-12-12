import arcpy, os
from arcpy import env 
def conteo_elementos(param0, param1):
    arcpy.env.workspace = param0
    file = open(os.path.join(param1,'Conteo_Elementos_GDB.txt'), "w")
    dsList = arcpy.ListDatasets(feature_type="feature")
    for ds in dsList:
        file.write("Dataset: {0}{1}".format(ds, "\n"))
        for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
            rowCount = arcpy.GetCount_management(fc)
            file.write("{0}{1} tiene {2} elementos {3}".format("\t", fc, rowCount,"\n"))
    return
if __name__ == '__main__':
    # Tool parameter accessed with GetParameter or GetParameterAsText
    param0 = arcpy.GetParameterAsText(0)
    param1 = arcpy.GetParameterAsText(1)
    conteo_elementos(param0, param1)
    


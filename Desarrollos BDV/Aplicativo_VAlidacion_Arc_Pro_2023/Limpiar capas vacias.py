import arcpy
try:
    mapa = arcpy.GetParameterAsText(0)
    arcpy.AddMessage(type(mapa))
    arcpy.AddMessage(mapa)
    lista_mapa = mapa.split(";")
    aprx = arcpy.mp.ArcGISProject("CURRENT")
    arcpy.AddMessage("Proyecto:\n"+aprx.filePath)
    #arcpy.AddMessage("Mapas de entrada: "+lista_mapa)
    for lis in lista_mapa:
        m = aprx.listMaps(lis)[0]
        arcpy.AddMessage(str(m.name))
        #m.name = mapa
        l = m.listLayers()
        remove = []
        for lyr in l:
            rowCount = arcpy.GetCount_management(lyr)
            if int(str(rowCount))==0:
                arcpy.AddMessage("Capas a remover: "+str(lyr)+"-"+str(rowCount)+"\n del mapa: "+str(m.name))
                print("Capas a remover: "+str(lyr)+"-"+str(rowCount))
                remove.append(lyr)
                arcpy.AddMessage(len(remove))
        if len(remove) != 0 or remove !=[]:
            arcpy.AddMessage("***Removiendo las capas sin información de la vista")
            print("***Removiendo las capas sin información de la vista")
            for lyr in remove:
                m.removeLayer(lyr)
                arcpy.AddMessage("***Se han removido las capas sin datos del mapa")
                print("***Se han removido las capas sin datos del mapa")
        else:
            arcpy.AddMessage("No existen capas vacias")
            print("No existen capas vacias")
except Exception as e:
    print("Error: " + e.args[0])

"""
import arcpy
mapa = arcpy.GetParameterAsText(0)
aprx = arcpy.mp.ArcGISProject("CURRENT")
arcpy.AddMessage("Proyecto:\n"+aprx.filePath)
arcpy.AddMessage(mapa)
arcpy.AddMessage(type(mapa))
lista_mapa = mapa.split(";")
arcpy.AddMessage("Mapas de entrada: "+lista_mapa)
"""


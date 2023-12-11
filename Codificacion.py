#Semillero de Investigación y Desarrollo
#Yaritza Quevedo

import arcpy
import os


#Variables

Poligonos_entrada = arcpy.GetParameterAsText(0)
Puntos_entrada = arcpy.GetParameterAsText(1)
# edit = arcpy.da.Editor(Puntos_entrada)
# edit.startEditing()
# edit.startOperation()



count = int(arcpy.GetCount_management(Puntos_entrada).getOutput(0))
i = 1 

for p_geograficos in range(count+1):
    query = "OBJECTID = {0}".format(p_geograficos) #un query es una consulta, lo que hace es monstrar la lista del rango de puntos 
    seleccion_atributos = arcpy.management.SelectLayerByAttribute(Puntos_entrada, "NEW_SELECTION", query)
    seleccion_localizacion = arcpy.management.SelectLayerByLocation(Poligonos_entrada, "INTERSECT", seleccion_atributos, 0 ,"NEW_SELECTION")
    with arcpy.da.UpdateCursor(seleccion_atributos, ['SHAPE@','Cod','NGCatego_1','NGSubcat_1']) as puntos: #Token: SHAPE@ es un atributo fijo, va seguido del @
        for elementos in puntos: #Los indices se enumeran desde 0, por ejemplo Shape sería 0, codigo sería 1
            arcpy.AddMessage("Evaluando punto {0}".format(i))
            with arcpy.da.UpdateCursor(seleccion_localizacion, ['SHAPE@','MpCodigo']) as poligonos:
                for municipios in poligonos:
                    if(municipios[0].contains(elementos[0], 'BOUNDARY')== True): 
                        if (len(str(elementos[2])) == 1 and (len(str(elementos[3])) == 1)): #En python los formatos tipo texto si se permite contar los digitos como el cursor elementos el indice 3 son tipo número en la tabla de atributos de ArcGIS se debe pasar a texto
                            if (len(str(i)) ==1):
                                elementos[1] = municipios[1] + "0" + str(elementos[2])+ "0"+ str(elementos[3]) + "00000"+ str(i)
                            elif (len(str(i)) ==2):
                                elementos[1] = municipios[1] + "0" + str(elementos[2]) + "0"+ str(elementos[3]) + "0000"+ str(i)
                            elif (len(str(i)) ==3):
                                elementos[1] = municipios[1] + "0" + str(elementos[2])+ "0"+ str(elementos[3])+ "000"+ str(i)
                            elif (len(str(i)) ==4):
                                elementos[1] = municipios[1] + "0" + str(elementos[2])+ "0"+ str(elementos[3]) + "00"+ str(i)
                            elif (len(str(i)) ==5):
                                elementos[1] = municipios[1] + "0" + str(elementos[2])+ "0"+ str(elementos[3]) + "0"+ str(i)
                            else:
                                elementos[1] = municipios[1] + "0" + str(elementos[2])+ "0"+ str(elementos[3])
                        elif(len(str(elementos[2])) == 2 and (len(str(elementos[3])) == 1)):
                            if (len(str(i)) ==1):
                                elementos[1] = municipios[1] + str(elementos[2])+ "0"+ str(elementos[3]) + "00000"+ str(i)
                            elif (len(str(i)) ==2):
                                elementos[1] = municipios[1] + str(elementos[2])+ "0"+ str(elementos[3]) + "0000"+ str(i)
                            elif (len(str(i)) ==3):
                                elementos[1] = municipios[1] + str(elementos[2])+ "0"+ str(elementos[3]) + "000"+ str(i)
                            elif (len(str(i)) ==4):
                                elementos[1] = municipios[1] + str(elementos[2])+ "0"+ str(elementos[3]) + "00"+ str(i)
                            elif (len(str(i)) ==5):
                                elementos[1] = municipios[1] + str(elementos[2])+ "0"+ str(elementos[3]) + "0"+ str(i)
                            else:
                                elementos[1] = municipios[1] + elementos[2]+ "0"+ elementos[3]
                        elif(len(str(elementos[2])) == 1 and (len(str(elementos[3])) == 2)):
                            if (len(str(i)) ==1):
                                elementos[1] = municipios[1] + "0" + str(elementos[2])+ str(elementos[3]) + "00000"+ str(i)
                            elif (len(str(i)) ==2):
                                elementos[1] = municipios[1] + "0" + str(elementos[2])+ str(elementos[3]) + "0000"+ str(i)
                            elif (len(str(i)) ==3):
                                elementos[1] = municipios[1] + "0" + str(elementos[2])+ str(elementos[3]) + "000"+ str(i)
                            elif (len(str(i)) ==4):
                                elementos[1] = municipios[1] + "0" + str(elementos[2])+ str(elementos[3]) + "00"+ str(i)
                            elif (len(str(i)) ==5):
                                elementos[1] = municipios[1] + "0" + str(elementos[2])+ str(elementos[3]) + "0"+ str(i)
                            else:
                                elementos[1] = municipios[1] + "0"+ str(elementos[2])+ str(elementos[3])
                        else:
                            if (len(str(i)) ==1):
                                elementos[1] = municipios[1] + str(elementos[2])+ str(elementos[3]) + "00000"+ str(i)
                            elif (len(str(i)) ==2):
                                elementos[1] = municipios[1] + str(elementos[2])+ str(elementos[3]) + "0000"+ str(i)
                            elif (len(str(i)) ==3):
                                elementos[1] = municipios[1] + str(elementos[2])+ str(elementos[3]) + "000"+ str(i)
                            elif (len(str(i)) ==4):
                                elementos[1] = municipios[1] + str(elementos[2])+ str(elementos[3]) + "00"+ str(i)
                            elif (len(str(i)) ==5):
                                elementos[1] = municipios[1] + str(elementos[2])+ str(elementos[3]) + "0"+ str(i)
                            else:
                                elementos[1] = municipios[1] + str(elementos[2])+ str(elementos[3])
                        puntos.updateRow(elementos)
                    else:
                        pass 
            i = i + 1

# edit.stopOperation()
# edit.stopEditing('True')




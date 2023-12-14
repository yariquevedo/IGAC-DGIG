import sys
import os
import pandas
import arcpy

#Función que lista los feature class dentro de la File Geodatabase
def listFcsInGDB(gdb):
    ''' list datasets Classes in a geodatabase, even feature clase inside  '''
    arcpy.env.workspace = gdb
    arcpy.AddMessage ('PROCESANDO '+ arcpy.env.workspace)
    fcs = []
    #all_fields = []
    
    for fds in arcpy.ListDatasets('','feature') + ['']:
        feature = arcpy.ListFeatureClasses('','',fds)
        feature.sort
        for fc in arcpy.ListFeatureClasses('','',fds):
            #workspace1 = gdb +os.sep + fc#
            #for campo in arcpy.ListFields(workspace1)#
            fcs.append(os.path.join(fds, fc))#
    return fcs

#Funcion que clcula incremento y da el codigo
def autoIncrement():
    global reco,M,F,B
    reco = int(str(reco))
    Start = 1
    Interval = 1
    if (reco == 0):
       reco = Start 
       return M+F+"000"+str(reco)+B
    elif (reco > 0 and reco<9):
        reco = reco + Interval 
        return M+F+"000"+str(reco)+B
    elif (reco >= 9 and reco < 99):
        reco = reco + Interval 
        return M+F+"00"+str(reco)+B
    elif (reco >= 99 and reco < 999):
        reco = reco + Interval 
        return M+F+"0"+str(reco)+B
    elif (reco >= 999 and reco < 9999):
        reco = reco + Interval 
        return M+F+str(reco)+B
    else:
        reco = reco + Interval 
        return M+F+"verificar"+str(reco)+B


def limpiarListas(fcs,lista2,lista3,lista4,lista5):
    for i in lista2:
        try:
            fcs.remove(i)
        except ValueError:
            pass
    for i in lista3:
        try:
            fcs.remove(i)
        except ValueError:
            pass
    for i in lista4:
        try:
            fcs.remove(i)
        except ValueError:
            pass
    for i in lista5:
        try:
            fcs.remove(i)
        except ValueError:
            pass
    return fcs

#variables globales del Script
F=""
reco=0
DATASET=["CoberturaTierra","CoberturaTierra","CoberturaTierra","Elevacion","Elevacion","Geodesia","Hidrografia","Hidrografia","Hidrografia","Hidrografia","Hidrografia","Hidrografia","Hidrografia","Hidrografia","Hidrografia","InfraestructuraServicios","InfraestructuraServicios","InfraestructuraServicios","InfraestructuraServicios","InfraestructuraServicios","NombresGeograficos","OrdenamientoTerritorial","OrdenamientoTerritorial","OrdenamientoTerritorial","OrdenamientoTerritorial","Transporte","Transporte","Transporte","Transporte","Transporte","Transporte","Transporte","Transporte","Transporte","ViviendaCiudadTerritorio","ViviendaCiudadTerritorio","ViviendaCiudadTerritorio","ViviendaCiudadTerritorio","ViviendaCiudadTerritorio","ViviendaCiudadTerritorio","ViviendaCiudadTerritorio","ViviendaCiudadTerritorio"]
FEATURECLASS=["AExtra","Bosque","ZVerde","CNivel","LDTerr","MRTerr","BArena","DAgua_P","DAgua_R","Drenaj_L","Humeda","Isla","Mangla","Drenaj_R","DAgua_L","PDistr","Pozo","RATens","TSPubl","Tuberi","NGeogr","Depart","LLimit","Fronte","MDANMu","LVia","Puente_L","SVial","Tunel","VFerre","Via","Ciclor","Puente_P","Telefe","Cerca","Constr_P","Constr_R","Muro","Piscin","ZDura","Terrap","LDemar"]
COD=["5002","5001","5003","6001","6002","1001","4005","4002","4002","4001","4006","4004","4003","4001","4002","8002","8004","8001","8003","8005","9001","7002","7001","7004","7003","3005","3002","3006","3003","3004","3001","3007","3002","3008","2002","2001","2001","2003","2005","2004","2007","6001"]
NOM=["Áreas de Extracción","Bosque","Zona verde","Curva de nivel","Línea de demarcación de terreno","Marco de referencia terrestre","Banco de arena","Deposito de agua","Deposito de agua","Drenaje","Humedal","Isla","Manglar","Drenaje","Deposito de agua","Punto de distribucion","Pozo","Red de alta tension","Tapa de servicios públicos"," tuberia","Nombre geogrâ€¡fico","Departamento","Línea limítrofe","Frontera","Municipio distrito y area no municipalizada","Limite via","Puente","Separador vial","Tunel","Via ferrea","Via"," cicloruta","Puente"," teleferico","Cerca","Construccion","Construccion","Muro","Piscina","Zona dura"," terraplen","linea de demarcacion"]
IDEN=["AEIdentif","BIdentif","ZVIdentif","CNIdentif","LDTIdentif","MRTIdentif","BAIdentif","DAIdentif","DAIdentif","DIdentif","HIdentif","IsIdentif","MgIdentif","DIdentif","DAIdentif","PDIdentif","PoIdentif","RATIdentif","TSPIdentif","TubIdentif","NGIdentif","DeCodigo","LLIdentif","FCodigo","MDANMCodig","LVIdentif","PIdentif","SVIdentif","TIdentif","VFIdentif","VIdentif","CiIdentif","PIdentif","TelIdentif","CeIdentif","CIdentif","CIdentif","MuIdentif","PiIdentif","ZDIdentif","TeIdentif","LDIdentif"]

dic = {'DATASET':DATASET,'FEATURECLASS':FEATURECLASS,'COD':COD,'NOM':NOM,'IDEN':IDEN}
CSV_STR = pandas.DataFrame(dic)

"""
/***************************************************************************
Ejecicón del programa
/***************************************************************************
"""
try:
    #Variables de entorno
    gdb = arcpy.GetParameterAsText(0)
    Codigo_municipio = arcpy.GetParameterAsText(1)
    B = arcpy.GetParameterAsText(2)
    
    arcpy.AddMessage("Codificación automativa V2.4, se creará el diccionario a partir de la siguiente tabla:")
    CSV_STR = pandas.DataFrame(dic)
    arcpy.AddMessage(CSV_STR.to_string())
    M = Codigo_municipio

    #Lógica de negocio
    fcs = listFcsInGDB(gdb)
    fcs.remove(r'IndiceMapas\Indice')
    #arcpy.AddWarning("No se códifica")
    lista2 = ["Hidrografia\DAgua_R","Hidrografia\DAgua_L","Hidrografia\DAgua_P"] #Para hidrografia, DAGUA
    lista3 = ["Hidrografia\Drenaj_R","Hidrografia\Drenaj_L"] #Para hidrogracia, DRENAJE
    lista4 = ["Transporte\Puente_L","Transporte\Puente_P"] #Para transporte, PUENTE
    lista5 = ["ViviendaCiudadTerritorio\Constr_R","ViviendaCiudadTerritorio\Constr_P"] #Para vivienda, CONSTRUCCION
    fcs = limpiarListas(fcs,lista2,lista3,lista4,lista5)
    for fc in fcs:
        arcpy.AddMessage("\tLISTA 1")
        reco = arcpy.management.GetCount(fc)
        print(reco)
        if int(reco.getOutput(0)):
            #if not fc in ["DAgua_R","DAgua_L","DAgua_P","Drenaj_R","Drenaj_L","Puente_L","Puente_P","Constr_R","Constr_P"]:
            print("\tFeatureClass a codificar: "+fc+"\n")
            arcpy.AddMessage("\tFeatureClass a codificar: "+fc+"\n")
            workspace = os.path.dirname(gdb +os.sep + fc)
            field = '*'
            campos = []
            fields = arcpy.ListFields(gdb +os.sep + fc)
            for field2 in fields:
                campos.append(field2)
                arcpy.AddMessage(str(field2.name))
                print(field2.name)
            codigo_n = campos[2].name
            shape =campos[1].name+"@"
            arcpy.AddMessage("Variable de codificación de interés: \t"+codigo_n)
            print("Variable de codificación de interés: \t"+codigo_n)
            edit = arcpy.da.Editor(gdb)
            edit.startEditing(False, True)
            edit.startOperation()
            reco = 0
            with arcpy.da.UpdateCursor((gdb +os.sep + fc), [codigo_n,shape]) as unificada_cursor: #ES UpdateCursor
                for fila in unificada_cursor:
                    F = (CSV_STR[CSV_STR["IDEN"]==codigo_n]["COD"]).values.tolist()[0]
                    dato = autoIncrement()
                    arcpy.AddMessage(dato)
                    fila[0] = dato
                    unificada_cursor.updateRow(fila)
            edit.stopOperation()
            edit.stopEditing(True)
        else:
            print("\tFeatureClass sin información: "+fc+"\n")
            arcpy.AddMessage("\tFeatureClass sin información: "+fc+"\n")
    ##Para la segunda lista
    reco = 0
    for fc in lista2:
        arcpy.AddMessage("\tLISTA 2")
        #reco = arcpy.management.GetCount(fc)
        #print(reco)
        if int(arcpy.management.GetCount(fc).getOutput(0)):
            #if not fc in ["DAgua_R","DAgua_L","DAgua_P","Drenaj_R","Drenaj_L","Puente_L","Puente_P","Constr_R","Constr_P"]:
            print("\tFeatureClass a codificar: "+fc+"\n")
            arcpy.AddMessage("\tFeatureClass a codificar: "+fc+"\n")
            workspace = os.path.dirname(gdb +os.sep + fc)
            field = '*'
            campos = []
            fields = arcpy.ListFields(gdb +os.sep + fc)
            for field2 in fields:
                campos.append(field2)
                arcpy.AddMessage(str(field2.name))
                print(field2.name)
            codigo_n = campos[2].name
            shape =campos[1].name+"@"
            arcpy.AddMessage("Variable de codificación de interés: \t"+codigo_n)
            print("Variable de codificación de interés: \t"+codigo_n)
            edit = arcpy.da.Editor(gdb)
            edit.startEditing(False, True)
            edit.startOperation()
            #reco = 0
            with arcpy.da.UpdateCursor((gdb +os.sep + fc), [codigo_n,shape]) as unificada_cursor: #ES UpdateCursor
                for fila in unificada_cursor:
                    F = (CSV_STR[CSV_STR["IDEN"]==codigo_n]["COD"]).values.tolist()[0]
                    dato = autoIncrement()
                    arcpy.AddMessage(dato)
                    fila[0] = dato
                    unificada_cursor.updateRow(fila)
            edit.stopOperation()
            edit.stopEditing(True)
        else:
            print("\tFeatureClass sin información: "+fc+"\n")
            arcpy.AddMessage("\tFeatureClass sin información: "+fc+"\n")
    ##Para la TERCERA lista
    reco = 0
    for fc in lista3:
        arcpy.AddMessage("\tLISTA 3")
        #reco = arcpy.management.GetCount(fc)
        #print(reco)
        if int(arcpy.management.GetCount(fc).getOutput(0)):
            #if not fc in ["DAgua_R","DAgua_L","DAgua_P","Drenaj_R","Drenaj_L","Puente_L","Puente_P","Constr_R","Constr_P"]:
            print("\tFeatureClass a codificar: "+fc+"\n")
            arcpy.AddMessage("\tFeatureClass a codificar: "+fc+"\n")
            workspace = os.path.dirname(gdb +os.sep + fc)
            field = '*'
            campos = []
            fields = arcpy.ListFields(gdb +os.sep + fc)
            for field2 in fields:
                campos.append(field2)
                arcpy.AddMessage(str(field2.name))
                print(field2.name)
            codigo_n = campos[2].name
            shape =campos[1].name+"@"
            arcpy.AddMessage("Variable de codificación de interés: \t"+codigo_n)
            print("Variable de codificación de interés: \t"+codigo_n)
            edit = arcpy.da.Editor(gdb)
            edit.startEditing(False, True)
            edit.startOperation()
            #reco = 0
            with arcpy.da.UpdateCursor((gdb +os.sep + fc), [codigo_n,shape]) as unificada_cursor: #ES UpdateCursor
                for fila in unificada_cursor:
                    F = (CSV_STR[CSV_STR["IDEN"]==codigo_n]["COD"]).values.tolist()[0]
                    dato = autoIncrement()
                    arcpy.AddMessage(dato)
                    fila[0] = dato
                    unificada_cursor.updateRow(fila)
            edit.stopOperation()
            edit.stopEditing(True)
        else:
            print("\tFeatureClass sin información: "+fc+"\n")
            arcpy.AddMessage("\tFeatureClass sin información: "+fc+"\n")
    ##Para la CUARTA lista
    reco = 0
    for fc in lista4:
        arcpy.AddMessage("\tLISTA 4")
        #reco = arcpy.management.GetCount(fc)
        #print(reco)
        if int(arcpy.management.GetCount(fc).getOutput(0)):
            #if not fc in ["DAgua_R","DAgua_L","DAgua_P","Drenaj_R","Drenaj_L","Puente_L","Puente_P","Constr_R","Constr_P"]:
            print("\tFeatureClass a codificar: "+fc+"\n")
            arcpy.AddMessage("\tFeatureClass a codificar: "+fc+"\n")
            workspace = os.path.dirname(gdb +os.sep + fc)
            field = '*'
            campos = []
            fields = arcpy.ListFields(gdb +os.sep + fc)
            for field2 in fields:
                campos.append(field2)
                arcpy.AddMessage(str(field2.name))
                print(field2.name)
            codigo_n = campos[2].name
            shape =campos[1].name+"@"
            arcpy.AddMessage("Variable de codificación de interés: \t"+codigo_n)
            print("Variable de codificación de interés: \t"+codigo_n)
            edit = arcpy.da.Editor(gdb)
            edit.startEditing(False, True)
            edit.startOperation()
            #reco = 0
            with arcpy.da.UpdateCursor((gdb +os.sep + fc), [codigo_n,shape]) as unificada_cursor: #ES UpdateCursor
                for fila in unificada_cursor:
                    F = (CSV_STR[CSV_STR["IDEN"]==codigo_n]["COD"]).values.tolist()[0]
                    dato = autoIncrement()
                    arcpy.AddMessage(dato)
                    fila[0] = dato
                    unificada_cursor.updateRow(fila)
            edit.stopOperation()
            edit.stopEditing(True)
        else:
            print("\tFeatureClass sin información: "+fc+"\n")
            arcpy.AddMessage("\tFeatureClass sin información: "+fc+"\n")
    ##Para la QUINTA lista
    reco = 0
    for fc in lista5:
        arcpy.AddMessage("\tLISTA 5")
        #reco = arcpy.management.GetCount(fc)
        #print(reco)
        if int(arcpy.management.GetCount(fc).getOutput(0)):
            #if not fc in ["DAgua_R","DAgua_L","DAgua_P","Drenaj_R","Drenaj_L","Puente_L","Puente_P","Constr_R","Constr_P"]:
            print("\tFeatureClass a codificar: "+fc+"\n")
            arcpy.AddMessage("\tFeatureClass a codificar: "+fc+"\n")
            workspace = os.path.dirname(gdb +os.sep + fc)
            field = '*'
            campos = []
            fields = arcpy.ListFields(gdb +os.sep + fc)
            for field2 in fields:
                campos.append(field2)
                arcpy.AddMessage(str(field2.name))
                print(field2.name)
            codigo_n = campos[2].name
            shape =campos[1].name+"@"
            arcpy.AddMessage("Variable de codificación de interés: \t"+codigo_n)
            print("Variable de codificación de interés: \t"+codigo_n)
            edit = arcpy.da.Editor(gdb)
            edit.startEditing(False, True)
            edit.startOperation()
            #reco = 0
            with arcpy.da.UpdateCursor((gdb +os.sep + fc), [codigo_n,shape]) as unificada_cursor: #ES UpdateCursor
                for fila in unificada_cursor:
                    F = (CSV_STR[CSV_STR["IDEN"]==codigo_n]["COD"]).values.tolist()[0]
                    dato = autoIncrement()
                    arcpy.AddMessage(dato)
                    fila[0] = dato
                    unificada_cursor.updateRow(fila)
            edit.stopOperation()
            edit.stopEditing(True)
        else:
            print("\tFeatureClass sin información: "+fc+"\n")
            arcpy.AddMessage("\tFeatureClass sin información: "+fc+"\n")
except arcpy.ExecuteError as err:
    arcpy.AddError(err)
#Dirección de Investigación y Desarrollo
#Reglas de topología
#Created by: 

#Liberias
import arcpy
import os

#Variables

GDB_Entrada = arcpy.GetParameterAsText(0)
Ruta_Salida = arcpy.GetParameterAsText(1)

T1 = arcpy.GetParameterAsText(2) #Cnivel_Piscin
T2 = arcpy.GetParameterAsText(3) #Bosque_Constr_R
T3 = arcpy.GetParameterAsText(4) #Bosque_DAgua_R
T4 = arcpy.GetParameterAsText(5) #Cerca_DAgua_R
T5 = arcpy.GetParameterAsText(6) #Muro-Deposito
T6 = arcpy.GetParameterAsText(7) #Muro_DAgua_R
T7 = arcpy.GetParameterAsText(8) #LVia_ZDura
arcpy.env.overwriteOutput = True

#Funciones 
def Cnivel_Piscin(GDB_Entrada, Ruta_Salida, GDB_Salida):
    arcpy.env.workspace = GDB_Entrada
    Feature_Class_Curvas_Nivel = os.path.join(str(GDB_Entrada),'Elevacion\Cnivel')
    Feature_Class_Piscinas= os.path.join(str(GDB_Entrada),'ViviendaCiudadTerritorio\Piscin')
    salida = arcpy.analysis.Intersect([Feature_Class_Curvas_Nivel, Feature_Class_Piscinas],os.path.join(str(GDB_Salida),'Cnivel_Piscin'),'ALL','','LINE')
    total = arcpy.management.GetCount(salida)
    if str(total) == '0':
        arcpy.Delete_management(salida)
    else:
        pass
    return total 
#Las curvas de nivel no pueden cruzar sobre las piscinas.


def Bosque_Constr_R(GDB_Entrada, Ruta_Salida, GDB_Salida): 
    arcpy.env.workspace = GDB_Entrada
    Feature_Class_Bosque = os.path.join(str(GDB_Entrada),'CoberturaTierra\Bosque')
    Feature_Class_Construccion = os.path.join(str(GDB_Entrada),'ViviendaCiudadTerritorio\Constr_R')
    seleccion= arcpy.management.SelectLayerByLocation(Feature_Class_Construccion, 'WITHIN', Feature_Class_Bosque,'', 'NEW_SELECTION','')
    salida=arcpy.analysis.Intersect([Feature_Class_Bosque, seleccion],os.path.join(str(GDB_Salida),'Bosque_Constr_R'),'ALL','','INPUT')
    total = arcpy.management.GetCount(salida)
    if str(total) == '0':
        arcpy.Delete_management(salida)
    else:
        pass
    return total 
#si la construcción tipo contrucción esta contenida completamente dentro de un bosque se debe dejar un claro (Anillo dentro del poligono del bosque) donde se encuentre la construcción


def Bosque_DAgua_R(GDB_Entrada, Ruta_Salida, GDB_Salida):
    arcpy.env.workspace = GDB_Entrada
    Feature_Class_Bosque = os.path.join(str(GDB_Entrada),'CoberturaTierra\Bosque')
    Feature_Class_Deposito_Agua= os.path.join(str(GDB_Entrada),'Hidrografia\DAgua_R')
    salida = arcpy.analysis.Intersect([Feature_Class_Bosque, Feature_Class_Deposito_Agua],os.path.join(str(GDB_Salida),'Bosque_DAgua_R'),'ALL','','INPUT')
    total = arcpy.management.GetCount(salida)
    if str(total) == '0':
        arcpy.Delete_management(salida)
    else:
        pass
    return total

#los depositos de agua no deben intersectar a los bosques.

def Cerca_DAgua_R(GDB_Entrada, Ruta_Salida, GDB_Salida):
    arcpy.env.workspace = GDB_Entrada
    Feature_Class_Cerca = os.path.join(str(GDB_Entrada),'ViviendaCiudadTerritorio\Cerca')
    Feature_Class_Deposito_Agua= os.path.join(str(GDB_Entrada),'Hidrografia\DAgua_R')
    salida = arcpy.analysis.Intersect([Feature_Class_Cerca, Feature_Class_Deposito_Agua],os.path.join(str(GDB_Salida),'Cerca_DAgua_R'),'ALL','','LINE')
    total = arcpy.management.GetCount(salida)
    if str(total) == '0':
        arcpy.Delete_management(salida)
    else:
        pass
    return total

#Las cercas no pueden cruzar los depositos de agua

def Muro_DAgua_R(GDB_Entrada, Ruta_Salida, GDB_Salida):
    arcpy.env.workspace = GDB_Entrada
    Feature_Class_Muro = os.path.join(str(GDB_Entrada),'ViviendaCiudadTerritorio\Muro')
    Feature_Class_Deposito_Agua= os.path.join(str(GDB_Entrada),'Hidrografia\DAgua_R')
    salida = arcpy.analysis.Intersect([Feature_Class_Muro, Feature_Class_Deposito_Agua],os.path.join(str(GDB_Salida),'Muro_DAgua_R'),'ALL','','LINE')
    total = arcpy.management.GetCount(salida)
    if str(total) == '0':
        arcpy.Delete_management(salida)
    else:
        pass
    return total

#Los muros no pueden cruzar los depositos de agua

def LVia_Muro(GDB_Entrada, Ruta_Salida, GDB_Salida):
    arcpy.env.workspace = GDB_Entrada
    Feature_Class_LVia = os.path.join(str(GDB_Entrada),'Transporte\LVia')
    Feature_Class_Muro= os.path.join(str(GDB_Entrada),'ViviendaCiudadTerritorio\Muro')
    salida = arcpy.analysis.Intersect([Feature_Class_LVia, Feature_Class_Muro],os.path.join(str(GDB_Salida),'LVia_Muro'),'ALL','','POINT')
    total = arcpy.management.GetCount(salida)
    if str(total) == '0':
        arcpy.Delete_management(salida)
    else:
        pass
    return total

    #Los limites de Via no pueden Cruzar a los muros.

def LVia_ZDura(GDB_Entrada, Ruta_Salida, GDB_Salida):
    arcpy.env.workspace = GDB_Entrada
    Feature_Class_LVia = os.path.join(str(GDB_Entrada),'Transporte\LVia')
    Feature_Class_Zonas_Duras= os.path.join(str(GDB_Entrada),'ViviendaCiudadTerritorio\ZDura')
    salida = arcpy.analysis.Intersect([Feature_Class_LVia, Feature_Class_Zonas_Duras],os.path.join(str(GDB_Salida),'LVia_ZDura'),'ALL','','LINE')
    total = arcpy.management.GetCount(salida)
    if str(total) == '0':
        arcpy.Delete_management(salida)
    else:
        pass
    return total

#los limites de via no pueden cruzar los poligonos de las zonas duras.

if __name__ == '__main__':
    GDB_Salida = arcpy.management.CreateFileGDB(Ruta_Salida, 'Validacion_DataReviewer')
    arcpy.AddMessage("-------------------------RESULTADOS-------------------------")
    if T1 == 'true': #Curva_nivel-Piscina
        arcpy.AddMessage("--------------------------------------------------------------")
        arcpy.AddMessage("Validando Topologia entre Curva de nivel y Piscina")
        total = Cnivel_Piscin(GDB_Entrada, Ruta_Salida, GDB_Salida)
        if str(total) == '0':
            arcpy.AddMessage("Se encontraron " + str(total) + " errores en total")
        else:
            arcpy.AddMessage("Se encontraron " + str(total) + " errores en total \n->Validar en  Feature: Cnivel_Piscin")

    if T2 == 'true': #Bosque_Construccion
        arcpy.AddMessage("--------------------------------------------------------------")
        arcpy.AddMessage("Validando Topologia entre Bosque y Construccion")
        total = Bosque_Constr_R(GDB_Entrada, Ruta_Salida, GDB_Salida)
        if str(total) == '0':
            arcpy.AddMessage("Se encontraron " + str(total) + " errores en total")
        else:
            arcpy.AddMessage("Se encontraron " + str(total) + " errores en total \n->Validar en  Feature: Bosque_Constr_R")

    if T3 == 'true': #Bosque-Deposito
        arcpy.AddMessage("--------------------------------------------------------------")
        arcpy.AddMessage("Validando Topologia entre Bosque y Deposito")
        total = Bosque_DAgua_R(GDB_Entrada, Ruta_Salida, GDB_Salida)
        if str(total) == '0':
            arcpy.AddMessage("Se encontraron " + str(total) + " errores en total")
        else:
            arcpy.AddMessage("Se encontraron " + str(total) + " errores en total \n->Validar en  Feature: Bosque_DAgua_R")

    if T4 == 'true': #Cerca-Deposito
        arcpy.AddMessage("--------------------------------------------------------------")
        arcpy.AddMessage("Validando Topologia entre Cerca y Deposito")
        total = Cerca_DAgua_R(GDB_Entrada, Ruta_Salida, GDB_Salida)
        if str(total) == '0':
            arcpy.AddMessage("Se encontraron " + str(total) + " errores en total")
        else:
            arcpy.AddMessage("Se encontraron " + str(total) + " errores en total \n->Validar en  Feature: Cerca_DAgua_R")

    if T5 == 'true': #Muro-Deposito
        arcpy.AddMessage("--------------------------------------------------------------")
        arcpy.AddMessage("Validando Topologia entre Muro y Deposito")
        total = Muro_DAgua_R(GDB_Entrada, Ruta_Salida, GDB_Salida)
        if str(total) == '0':
            arcpy.AddMessage("Se encontraron " + str(total) + " errores en total")
        else:
            arcpy.AddMessage("Se encontraron " + str(total) + " errores en total \n->Validar en  Feature: Muro_DAgua_R")

    if T6 == 'true': #Limite_via-Muro
        arcpy.AddMessage("--------------------------------------------------------------")
        arcpy.AddMessage("Validando Topologia entre LVia y Muro")
        total = LVia_Muro(GDB_Entrada, Ruta_Salida, GDB_Salida)
        if str(total) == '0':
            arcpy.AddMessage("Se encontraron " + str(total) + " errores en total")
        else:
            arcpy.AddMessage("Se encontraron " + str(total) + " errores en total \n->Validar en  Feature: LVia_Muro")

    if T7 == 'true': #Limite_via-Zonas_duras
        arcpy.AddMessage("--------------------------------------------------------------")
        arcpy.AddMessage("Validando Topologia entre LVia y ZDuras")
        total = LVia_ZDura(GDB_Entrada, Ruta_Salida, GDB_Salida)
        if str(total) == '0':
            arcpy.AddMessage("Se encontraron " + str(total) + " errores en total")
        else:
            arcpy.AddMessage("Se encontraron " + str(total) + " errores en total \n->Validar en  Feature: LVia_ZDura")


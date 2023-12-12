# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Direccion de Gestión de la Información Geografica
# Created on: 2023-05-20
# Created by: Kelly Villamil - Yaritza Quevedo - Michael Rojas - Diego Rugeles (Supervisor Desarrollo DGIG) 
# # Usage: DataReviwer ArcGIS Pro  - GDB 2.4- 2.5  Reglas Topológicas
# Description:
# ---------------------------------------------------------------------------
# Import arcpy module
import arcpy
import os
#Parameters
## Operadores logicos
# Iteradores
GDB_Entrada = arcpy.GetParameterAsText(0)
Ruta_Salida = arcpy.GetParameterAsText(1)
R1 = arcpy.GetParameterAsText(2) #LVia_ConstrR
R2 = arcpy.GetParameterAsText(3) #Via_DrenajL
R3 = arcpy.GetParameterAsText(4) #Via_Bosque
R4 = arcpy.GetParameterAsText(5) #DAguaR_CNivel
R5 = arcpy.GetParameterAsText(6) #Bosque_ConstrR
R6 = arcpy.GetParameterAsText(7) #Cerca_DAguaR
R7 = arcpy.GetParameterAsText(8) #Muro_DAguaR
R8 = arcpy.GetParameterAsText(9) #LVia_DAguaR
R9 = arcpy.GetParameterAsText(10) #DrenajeL_CNivel
R10 = arcpy.GetParameterAsText(11) #Via_Construccciones
T1 = arcpy.GetParameterAsText(12) #Cnivel_Piscin
T2 = arcpy.GetParameterAsText(13) #Cerca_Constr_R
T3 = arcpy.GetParameterAsText(14) #Bosque_DAgua_R
T4 = arcpy.GetParameterAsText(15) #Cerca_DAgua_R
T5 = arcpy.GetParameterAsText(16) #Muro-Deposito
T6 = arcpy.GetParameterAsText(17) #Muro_DAgua_R
T7 = arcpy.GetParameterAsText(18) #LVia_ZDura
V1 = arcpy.GetParameterAsText(19) #LVia_Deposito
V2 = arcpy.GetParameterAsText(20) #Via_Cercas
V3 = arcpy.GetParameterAsText(21) #ConstruccionR_ConstruccionP
V4 = arcpy.GetParameterAsText(22) #Vias_Deposito
V5 = arcpy.GetParameterAsText(23) #Deposito_DrenajeL
V6 = arcpy.GetParameterAsText(24) #Deposito_DrenajeR
V7 = arcpy.GetParameterAsText(25) #JagueyP_JagueyR
V8 = arcpy.GetParameterAsText(26)#Deposito_Deposito
V9 = arcpy.GetParameterAsText(27) # Muro Construcciones
V10  = arcpy.GetParameterAsText(28) # Construccion_R Tapa de servicio Publico
V11 = arcpy.GetParameterAsText(29) # Construccion_R Punto de distribución
V12 = arcpy.GetParameterAsText(30) # Vias - Zonas Duras
arcpy.env.overwriteOutput = True
def LVia_ConstrR(GDB_Entrada, Ruta_Salida, GDB_Salida): #Limite via y construccion no se pueden cruzar
    arcpy.env.workspace = GDB_Entrada
    Feature_Class_LVia = os.path.join(str(GDB_Entrada),'Transporte\LVia')
    Feature_Class_ConstrR = os.path.join(str(GDB_Entrada),'ViviendaCiudadTerritorio\Constr_R')
    salida = arcpy.Clip_analysis(Feature_Class_LVia, Feature_Class_ConstrR, os.path.join(str(GDB_Salida),'LVia_ConstrR'))
    total = arcpy.management.GetCount(salida)
    if str(total) == '0':
        arcpy.Delete_management(salida)
    
    return total
def Via_DrenajL(GDB_Entrada, Ruta_Salida, GDB_Salida): #Verificar donde se cruza y revisar si existe el elemento tipo puente
    arcpy.env.workspace = GDB_Entrada
    Feature_Class_Via = os.path.join(str(GDB_Entrada),'Transporte\Via')
    Feature_Class_DrenajeL = os.path.join(str(GDB_Entrada), 'Hidrografia\Drenaj_L')
    intersect = arcpy.Intersect_analysis([Feature_Class_Via, Feature_Class_DrenajeL],os.path.join(str(Ruta_Salida),'intersect_temp.shp'),'ALL','','POINT')
    ly_intersect=arcpy.MakeFeatureLayer_management(os.path.join(str(Ruta_Salida),'intersect_temp.shp'),os.path.join(str(Ruta_Salida),'lyr_intersect.shp'))                                                 
    ly_puente=arcpy.MakeFeatureLayer_management('Transporte\Puente_L', os.path.join(str(Ruta_Salida),'ly_puente.shp'))
    select=arcpy.SelectLayerByLocation_management(ly_intersect,'WITHIN_A_DISTANCE',ly_puente, '5 Meters', 'NEW_SELECTION','NOT_INVERT')
    ly_select=arcpy.MakeFeatureLayer_management(select, os.path.join(str(Ruta_Salida),'select_temp.shp'))
    salida = arcpy.Erase_analysis (ly_intersect, ly_select, os.path.join(str(GDB_Salida),'Via_DrenajL'))
    total = arcpy.management.GetCount(salida)
    
    if str(total) == '0':
        arcpy.Delete_management(salida)
    
    arcpy.Delete_management(intersect)
    arcpy.Delete_management(ly_intersect)
    arcpy.Delete_management(ly_puente)
    arcpy.Delete_management(ly_select)
    return total
def Via_Bosque(GDB_Entrada, Ruta_Salida, GDB_Salida): #La vía primaria y bosque no se pueden cruzar
    arcpy.env.workspace = GDB_Entrada
    Feature_Class_Via = os.path.join(str(GDB_Entrada),'Transporte\Via')
    Feature_Class_Bosque = os.path.join(str(GDB_Entrada),'CoberturaTierra\Bosque')
    
    via_primaria=arcpy.MakeFeatureLayer_management(Feature_Class_Via,os.path.join(str(Ruta_Salida),'via_primaria_temp.shp'),where_clause='VTipo=1')
    Bosque=arcpy.MakeFeatureLayer_management(Feature_Class_Bosque,os.path.join(str(Ruta_Salida),'bosque_temp.shp'))
    salida=arcpy.Intersect_analysis([via_primaria, Bosque], os.path.join(str(GDB_Salida),'Via_Bosque'),'ALL','','LINE')
    total = arcpy.management.GetCount(salida)
    arcpy.Delete_management(via_primaria)
    arcpy.Delete_management(Bosque)
    if str(total) == '0':
        arcpy.Delete_management(salida)
    
    return total
def DAguaR_CNivel(GDB_Entrada, Ruta_Salida, GDB_Salida): #Las curvas de nivel no pueden cruzar sobre los depositos de agua, a excepción de pantanos
    arcpy.env.workspace=GDB_Entrada
    Feature_Class_Curvas_Nivel = os.path.join(str(GDB_Entrada),'Elevacion\CNivel')
    ly_DepAgua_Sel=arcpy.MakeFeatureLayer_management('Hidrografia\DAgua_R',os.path.join(str(Ruta_Salida),'DAgua_R_temp.shp'),where_clause='DATipo <> 5')
    salida = arcpy.Intersect_analysis([ly_DepAgua_Sel, Feature_Class_Curvas_Nivel],os.path.join(str(GDB_Salida),'DAguaR_CNivel'))
    total = arcpy.management.GetCount(salida)
    arcpy.Delete_management(ly_DepAgua_Sel)
    if str(total) == '0':
        arcpy.Delete_management(salida)
         
    return total
def Bosque_ConstrR(GDB_Entrada, Ruta_Salida, GDB_Salida): #Extrae la construcción si esta contenida completamente dentro de un bosque
    arcpy.env.workspace=GDB_Entrada
    Feature_Class_Bosque = os.path.join(str(GDB_Entrada),'CoberturaTierra\Bosque')
    Feature_Class_Construccion = os.path.join(str(GDB_Entrada),'ViviendaCiudadTerritorio\Constr_R')
    ly_Bosque = arcpy.MakeFeatureLayer_management(Feature_Class_Bosque, os.path.join(str(Ruta_Salida),'ly_bosque_temp.shp'))
    ly_Construccion = arcpy.MakeFeatureLayer_management(Feature_Class_Construccion, os.path.join(str(Ruta_Salida),'ly_construccion_temp.shp'))
    select = arcpy.SelectLayerByLocation_management(ly_Construccion,'COMPLETELY_WITHIN',ly_Bosque,'','NEW_SELECTION', 'NOT_INVERT')
    ly_select = arcpy.MakeFeatureLayer_management(select, os.path.join(str(Ruta_Salida),'ly_select.shp'))
    salida = arcpy.Intersect_analysis([ly_Construccion,ly_select],os.path.join(str(GDB_Salida),'Bosque_ConstrR'))
    total = arcpy.management.GetCount(salida)
    arcpy.Delete_management(ly_Bosque)
    arcpy.Delete_management(ly_Construccion)
    arcpy.Delete_management(ly_select)
    if str(total) == '0':
        arcpy.Delete_management(salida)
         
    return total
def Cerca_DAguaR(GDB_Entrada, Ruta_Salida, GDB_Salida): #Cerca y deposito de agua no se pueden cruzar
    arcpy.env.workspace = GDB_Entrada
    Feature_Class_DAgua = os.path.join(str(GDB_Entrada),'Hidrografia\DAgua_R')
    Feature_Class_Cerca = os.path.join(str(GDB_Entrada),'ViviendaCiudadTerritorio\Cerca')
    salida = arcpy.Clip_analysis(Feature_Class_Cerca, Feature_Class_DAgua, os.path.join(str(GDB_Salida),'Cerca_DAguaR'))
    total = arcpy.management.GetCount(salida)
    if str(total) == '0':
        arcpy.Delete_management(salida)
         
    return total
def Muro_DAguaR(GDB_Entrada, Ruta_Salida, GDB_Salida): #Muro y deposito de agua no se pueden cruzar
    arcpy.env.workspace = GDB_Entrada
    Feature_Class_DAgua = os.path.join(str(GDB_Entrada),'Hidrografia\DAgua_R')
    Feature_Class_Muro = os.path.join(str(GDB_Entrada),'ViviendaCiudadTerritorio\Muro')
    salida = arcpy.Clip_analysis(Feature_Class_Muro, Feature_Class_DAgua, os.path.join(str(GDB_Salida),'Muro_DAguaR'))
    total = arcpy.management.GetCount(salida)
    if str(total) == '0':
        arcpy.Delete_management(salida)
         
    return total
def LVia_DAguaR(GDB_Entrada, Ruta_Salida, GDB_Salida): #Limite de via y deposito de agua no se pueden cruzar
    arcpy.env.workspace = GDB_Entrada
    Feature_Class_DAgua = os.path.join(str(GDB_Entrada),'Hidrografia\DAgua_R')
    Feature_Class_LVia = os.path.join(str(GDB_Entrada),'Transporte\LVia')
    salida = arcpy.Clip_analysis(Feature_Class_LVia, Feature_Class_DAgua, os.path.join(str(GDB_Salida),'LVia_DAguaR'))
    total = arcpy.management.GetCount(salida)
    if str(total) == '0':
        arcpy.Delete_management(salida)
    
    
    return total
code_block ="""
def estado(a):
    if (a>1):
        b = "REVISAR"
        return b 
    else: 
        b = "OMITIR"
        return b"""
def DrenajL_CNivel(GDB_Entrada, GDB_Salida): #Curva de nivel no debe cruzar mas de una vez el mismo drenaje
    
    arcpy.env.workspace = GDB_Entrada
    Feature_Class_Curvas_Nivel = os.path.join(str(GDB_Entrada),'Elevacion\CNivel')
    Feature_Class_Drenaje_L = os.path.join(str(GDB_Entrada),'Hidrografia\Drenaj_L')
    Puntos_Intersect = os.path.join(str(GDB_Salida),"Puntos_Intersect")                                       
    Puntos_Interseccion_Multipar = os.path.join(str(GDB_Salida),"Puntos_Interseccion_Multipar")              
    Puntos_Interseccion_Multip_stats = os.path.join(str(GDB_Salida),"Puntos_Interseccion_Multip_stats")
    Puntos_Intersect_Layer = os.path.join(str(GDB_Salida),"Puntos_Intersect_Layer")                          
    Puntos_Revision = os.path.join(str(GDB_Salida),"DrenajeL_CNivel")                                        
    #Salida_gdb = os.path.join(Ruta_Salida, "Revision_Curvas")  
    # Process: Intersect
    arcpy.Intersect_analysis([Feature_Class_Curvas_Nivel, Feature_Class_Drenaje_L], Puntos_Intersect, "ALL", "", "POINT")
    # Process: Multipart To Singlepart
    arcpy.management.MultipartToSinglepart(Puntos_Intersect, Puntos_Interseccion_Multipar)
    # Process: Summary Statistics
    arcpy.Statistics_analysis(Puntos_Interseccion_Multipar, Puntos_Interseccion_Multip_stats, "ORIG_FID COUNT", "ORIG_FID")
    # Process: Join Field
    arcpy.JoinField_management(Puntos_Intersect, "OBJECTID", Puntos_Interseccion_Multip_stats, "ORIG_FID", "FREQUENCY")
    # Process: Add Field
    arcpy.AddField_management(Puntos_Intersect, "Estado_Intersect", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    #Process: Calculate Field
    arcpy.CalculateField_management(Puntos_Intersect, "Estado_Intersect", "estado(!FREQUENCY!)", "PYTHON3", code_block)
    # Process: Make Feature Layer
    arcpy.MakeFeatureLayer_management(Puntos_Intersect, Puntos_Intersect_Layer, "", "", "OBJECTID OBJECTID VISIBLE NONE;SHAPE SHAPE VISIBLE NONE;FID_Drenaj_L FID_Drenaj_L VISIBLE NONE;DIdentif DIdentif VISIBLE NONE;DEstado DEstado VISIBLE NONE;DDisperso DDisperso VISIBLE NONE;DNombre DNombre VISIBLE NONE;FID_CNivel FID_CNivel VISIBLE NONE;CNIdentif CNIdentif VISIBLE NONE;CNAltura CNAltura VISIBLE NONE;CNTipo CNTipo VISIBLE NONE;FREQUENCY FREQUENCY VISIBLE NONE;Estado_Intersect Estado_Intersect VISIBLE NONE")
    # Process: Select Layer By Attribute
    arcpy.SelectLayerByAttribute_management(Puntos_Intersect_Layer, "NEW_SELECTION", "Estado_Intersect = 'REVISAR'")
    # Process: Feature Class to Feature Class (2)
    arcpy.FeatureClassToFeatureClass_conversion(Puntos_Intersect_Layer, GDB_Salida, "DrenajeL_CNivel", "", "FREQUENCY \"FREQUENCY\" true true false 0 Long 0 0 ,First,#,Revision_Curvas.gdb\\Puntos_Intersect,FREQUENCY,-1,-1;Estado_Intersect \"Estado_Intersect\" true true false 0 Text 0 0 ,First,#,Revision_Curvas.gdb\\Puntos_Intersect,Estado_Intersect,-1,-1", "")
    # Process: Alter Field
    arcpy.AlterField_management(Puntos_Revision, "FREQUENCY", "NumIntersec", "Numero_de_Intersecciones")
    #eliminando capas temporales:
    arcpy.management.Delete(Puntos_Intersect)
    arcpy.management.Delete(Puntos_Interseccion_Multipar)
    arcpy.management.Delete(Puntos_Interseccion_Multip_stats)
    arcpy.management.Delete(Puntos_Intersect_Layer)
    total = arcpy.management.GetCount(Puntos_Revision)
    if str(total) == '0':
        arcpy.Delete_management(Puntos_Revision)
    
    return total
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
def Cerca_Constr_R(GDB_Entrada, Ruta_Salida, GDB_Salida): 
    arcpy.env.workspace = GDB_Entrada
    Feature_Class_Cerca = os.path.join(str(GDB_Entrada),'ViviendaCiudadTerritorio\Cerca')
    Feature_Class_Construccion = os.path.join(str(GDB_Entrada),'ViviendaCiudadTerritorio\Constr_R')
    salida=arcpy.analysis.Intersect([Feature_Class_Cerca, Feature_Class_Construccion],os.path.join(Ruta_Salida,str(GDB_Salida),'Cerca_ConstrR'), output_type= 'LINE')
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
##LVia_Deposito----------------------------------------------------------------------------------------------------------------------------------------------
def LVia_DAguaR(GDB_Entrada,Ruta_Salida,GDB_Salida):
    arcpy.env.workspace = GDB_Entrada
    LVia = 'Transporte\LVia'
    DAguaR = 'Hidrografia\DAgua_R'
    salida = arcpy.analysis.Intersect([LVia,DAguaR], os.path.join(Ruta_Salida,str(GDB_Salida),'LVia_DAguaR'),'ALL','','LINE')
    total = arcpy.management.GetCount(salida)
    if str(total) == '0':
        arcpy.Delete_management(salida)
    return total
##Via_Cercas-----------------------------------------------------------------------------------------------------------------------------------------------
def LVia_Cerca(GDB_Entrada,Ruta_Salida,GDB_Salida):
     arcpy.env.workspace = GDB_Entrada
     LVia = 'Transporte/LVia'
     Cerca = 'ViviendaCiudadTerritorio/Cerca'
     salida = arcpy.analysis.Intersect([LVia,Cerca], os.path.join(Ruta_Salida,str(GDB_Salida),'LVia_Cerca'),'ALL','','POINT')
     total = arcpy.management.GetCount(salida)
     if str(total) == '0':
          arcpy.Delete_management(salida)
     return total
##ConstruccionR_ConstruccionP-----------------------------------------------------------------------------------------------------------------------------------------------
def ConstruccionR_ConstruccionP(GDB_Entrada,Ruta_Salida,GDB_Salida):
     arcpy.env.workspace = GDB_Entrada
     ConstruccionR = 'ViviendaCiudadTerritorio/Constr_R'
     ConstruccionP = 'ViviendaCiudadTerritorio/Constr_P'
     salida = arcpy.analysis.Intersect([ConstruccionR,ConstruccionP], os.path.join(Ruta_Salida,str(GDB_Salida),'ConstruccionR_ConstruccionP'),'ALL','','POINT')
     total = arcpy.management.GetCount(salida)
     if str(total) == '0':
          arcpy.Delete_management(salida)
     return total
##Via_Deposito----------------------------------------------------------------------------------------------------------------------------------------------
def Via_DAguaR(GDB_Entrada,Ruta_Salida,GDB_Salida):
    arcpy.env.workspace = GDB_Entrada
    Via = 'Transporte\Via'
    DAguaR = 'Hidrografia\DAgua_R'
    salida = arcpy.analysis.Intersect([Via,DAguaR], os.path.join(Ruta_Salida,str(GDB_Salida),'Via_DAguaR'),'ALL','','LINE')
    total = arcpy.management.GetCount(salida)
    if str(total) == '0':
        arcpy.Delete_management(salida)
    return total
##Deposito_DrenajeL----------------------------------------------------------------------------------------------------------------------------------------------
#Se realiza seleccion invertida para dar la excepcion a los depositos tipo pantano
def Deposito_DrenajeL(GDB_Entrada,Ruta_Salida,GDB_Salida):
    arcpy.env.workspace = GDB_Entrada
    DAguaR = 'Hidrografia\DAgua_R'
    Drenaj_L = 'Hidrografia\Drenaj_L'
    #Drenaj_R = 'Hidrografia\Drenaj_R'
    seleccion = arcpy.management.SelectLayerByAttribute(DAguaR,'NEW_SELECTION', "DATipo = 5", True)
    salida = arcpy.analysis.Intersect([seleccion,Drenaj_L], os.path.join(Ruta_Salida,str(GDB_Salida),'Deposito_DrenajeLR'),'ALL','','LINE')
    total = arcpy.management.GetCount(salida)
    if str(total) == '0':
        arcpy.Delete_management(salida)
    return total
##Deposito_DrenajeR----------------------------------------------------------------------------------------------------------------------------------------------
def Deposito_DrenajeR(GDB_Entrada,Ruta_Salida,GDB_Salida):
    arcpy.env.workspace = GDB_Entrada
    Drenaj_R = 'Hidrografia\Drenaj_R'
    DAguaR = 'Hidrografia\DAgua_R'
    salida = arcpy.analysis.Intersect([DAguaR,Drenaj_R], os.path.join(Ruta_Salida,str(GDB_Salida),'DAguaR_Drenaj_R'),'ALL','','INPUT')
    total = arcpy.management.GetCount(salida)
    if str(total) == '0':
        arcpy.Delete_management(salida)
    return total
##JagueyP_JagueyR----------------------------------------------------------------------------------------------------------------------------------------------
#Se realiza seleccion para unicamente los tipo Jaguey en el feature de puntos y poligonos
def JagueyP_JagueyR(GDB_Entrada,Ruta_Salida,GDB_Salida):
    arcpy.env.workspace = GDB_Entrada
    DAguaR = 'Hidrografia\DAgua_R'
    DAguaP = 'Hidrografia\DAgua_P'
    seleccion = arcpy.management.SelectLayerByAttribute(DAguaP,'NEW_SELECTION', "DATipo = 1", False)
    seleccion2 = arcpy.management.SelectLayerByAttribute(DAguaR,'NEW_SELECTION', "DATipo = 6", False)
    salida = arcpy.analysis.Intersect([seleccion,seleccion2], os.path.join(Ruta_Salida,str(GDB_Salida),'JagueyP_JagueyR'),'ALL','','POINT')
    total = arcpy.management.GetCount(salida)
    if str(total) == '0':
        arcpy.Delete_management(salida)
    return total
def via_constr_r(GDB_Entrada,Ruta_Salida,GDB_Salida):
    arcpy.env.workspace = GDB_Entrada
    Via = 'Transporte\Via'
    ConstrR = 'ViviendaCiudadTerritorio\Constr_R'
    seleccion = arcpy.management.SelectLayerByAttribute(Via,'NEW_SELECTION', "VTipo = 1", False)
    salida = arcpy.analysis.Intersect([seleccion,ConstrR], os.path.join(Ruta_Salida,str(GDB_Salida),'Via_Construccion_R'),'ALL','','LINE')
    total = arcpy.management.GetCount(salida)
    if str(total) == '0':
        arcpy.Delete_management(salida)
    return total
def muro_constrR(GDB_Entrada,Ruta_Salida,GDB_Salida):
    arcpy.env.workspace = GDB_Entrada
    Muro = 'ViviendaCiudadTerritorio\Muro'
    ConstrR = 'ViviendaCiudadTerritorio\Constr_R'
    salida = arcpy.analysis.Intersect([Muro,ConstrR], os.path.join(Ruta_Salida,str(GDB_Salida),'Muro_ConstrR'),'ALL','','LINE')
    total = arcpy.management.GetCount(salida)
    if str(total) == '0':
        arcpy.Delete_management(salida)
    return total
def via_zdura(GDB_Entrada,Ruta_Salida,GDB_Salida):
    arcpy.env.workspace = GDB_Entrada
    ZDura = 'ViviendaCiudadTerritorio\ZDura'
    Via = 'Transporte\Via'
    salida = arcpy.analysis.Intersect([Via,ZDura], os.path.join(Ruta_Salida,str(GDB_Salida),'Via_ZDura'),'ALL','','LINE')
    total = arcpy.management.GetCount(salida)
    if str(total) == '0':
        arcpy.Delete_management(salida)
    return total
def constrR_TP(GDB_Entrada,Ruta_Salida,GDB_Salida):
    arcpy.env.workspace = GDB_Entrada
    Tpsp = 'InfraestructuraServicios\TSPubl'
    ConstrR = 'ViviendaCiudadTerritorio\Constr_R'
    salida = arcpy.analysis.Intersect([Tpsp,ConstrR], os.path.join(Ruta_Salida,str(GDB_Salida),'TS_Publ_ConstrR'),'ALL','','POINT')
    total = arcpy.management.GetCount(salida)
    if str(total) == '0':
        arcpy.Delete_management(salida)
    return total
def constrR_PD(GDB_Entrada,Ruta_Salida,GDB_Salida):
    arcpy.env.workspace = GDB_Entrada
    PDistr = 'InfraestructuraServicios\PDistr'
    ConstrR = 'ViviendaCiudadTerritorio\Constr_R'
    salida = arcpy.analysis.Intersect([PDistr,ConstrR], os.path.join(Ruta_Salida,str(GDB_Salida),'TS_Publ_ConstrR'),'ALL','','POINT')
    total = arcpy.management.GetCount(salida)
    if str(total) == '0':
        arcpy.Delete_management(salida)
    return total
##Deposito_Deposito----------------------------------------------------------------------------------------------------------------------------------------------
#Se realiza seleccion para unicamente los tipo Jaguey
def Deposito_Deposito(GDB_Entrada,Ruta_Salida,GDB_Salida):
    arcpy.env.workspace = GDB_Entrada
    DAguaR1 = 'Hidrografia\DAgua_R'
    
    
    salida = arcpy.analysis.Intersect([DAguaR1], os.path.join(Ruta_Salida,str(GDB_Salida),'Deposito_Deposito'),'ALL','','INPUT')
    total = arcpy.management.GetCount(salida)
    if str(total) == '0':
        arcpy.Delete_management(salida)
    return total
if __name__ == '__main__':
    GDB_Salida = arcpy.management.CreateFileGDB(Ruta_Salida, 'Validacion_DataReviewer')
    arcpy.AddMessage("--------------------------RESULTADOS--------------------------")
    if R1 == 'true': #LVia_ConstrR
        arcpy.AddMessage("--------------------------------------------------------------")
        arcpy.AddMessage("Validando Topologia entre Limite Via y Construccion")
        total = LVia_ConstrR(GDB_Entrada, Ruta_Salida, GDB_Salida)
        if str(total) == '0':
            arcpy.AddMessage("Se encontraron " + str(total) + " errores en total")
        else:
            arcpy.AddMessage("Se encontraron " + str(total) + " errores en total \n->Validar en  Feature: LVia_ConstrR")
        
    if R2 == 'true': #Via_DrenajL
        arcpy.AddMessage("\n--------------------------------------------------------------")
        arcpy.AddMessage("Validando Topologia entre Via y Drenaje")
        total = Via_DrenajL(GDB_Entrada, Ruta_Salida, GDB_Salida)
        if str(total) == '0':
            arcpy.AddMessage("Se encontraron " + str(total) + " errores en total")
        else:
            arcpy.AddMessage("Se encontraron " + str(total) + " errores en total \n->Validar en  Feature: Via_DrenajL")
         
    if R3 == 'true': #Via_Bosque
        arcpy.AddMessage("\n--------------------------------------------------------------")
        arcpy.AddMessage("Validando Topologia entre Via y Bosque")
        total = Via_Bosque(GDB_Entrada, Ruta_Salida, GDB_Salida)
        if str(total) == '0':
            arcpy.AddMessage("Se encontraron " + str(total) + " errores en total")
        else:
            arcpy.AddMessage("Se encontraron " + str(total) + " errores en total \n->Validar en  Feature: Via_Bosque")
        
    if R4 == 'true': #DAguaR_CNivel
        arcpy.AddMessage("\n--------------------------------------------------------------")
        arcpy.AddMessage("Validando Topologia entre Deposito de agua y Curva de nivel")
        total = DAguaR_CNivel(GDB_Entrada, Ruta_Salida, GDB_Salida)
        if str(total) == '0':
            arcpy.AddMessage("Se encontraron " + str(total) + " errores en total")
        else:
            arcpy.AddMessage("Se encontraron " + str(total) + " errores en total \n->Validar en  Feature: DAguaR_CNivel")
        
    if R5 == 'true': #Bosque_ConstrR
        arcpy.AddMessage("\n--------------------------------------------------------------")
        arcpy.AddMessage("Validando Topologia entre Bosque y Construccion")
        total = Bosque_ConstrR(GDB_Entrada, Ruta_Salida, GDB_Salida)
        if str(total) == '0':
            arcpy.AddMessage("Se encontraron " + str(total) + " errores en total")
        else:
            arcpy.AddMessage("Se encontraron " + str(total) + " errores en total \n->Validar en  Feature: Bosque_ConstrR")
        
    if R6 == 'true': #Cerca_DAguaR
        arcpy.AddMessage("\n--------------------------------------------------------------")
        arcpy.AddMessage("Validando Topologia entre Cerca y Deposito de agua")
        total = Cerca_DAguaR(GDB_Entrada, Ruta_Salida, GDB_Salida)
        if str(total) == '0':
            arcpy.AddMessage("Se encontraron " + str(total) + " errores en total")
        else:
            arcpy.AddMessage("Se encontraron " + str(total) + " errores en total \n->Validar en  Feature: Cerca_DAguaR")
        
    if R7 == 'true': #Muro_DAguaR
        arcpy.AddMessage("\n--------------------------------------------------------------")
        arcpy.AddMessage("Validando Topologia entre Muro y Deposito de agua")
        total = Muro_DAguaR(GDB_Entrada, Ruta_Salida, GDB_Salida)
        if str(total) == '0':
            arcpy.AddMessage("Se encontraron " + str(total) + " errores en total")
        else:
            arcpy.AddMessage("Se encontraron " + str(total) + " errores en total \n->Validar en  Feature: Muro_DAguaR")
        
    if R8 == 'true': #LVia_DAguaR
        arcpy.AddMessage("\n--------------------------------------------------------------")
        arcpy.AddMessage("Validando Topologia entre Limite Via y Deposito de agua")
        total = LVia_DAguaR(GDB_Entrada, Ruta_Salida, GDB_Salida)
        if str(total) == '0':
            arcpy.AddMessage("Se encontraron " + str(total) + " errores en total")
        else:
            arcpy.AddMessage("Se encontraron " + str(total) + " errores en total \n->Validar en  Feature: LVia_DAguaR")
    
    if R9 == 'true': #DrenajeL_CNivel
        arcpy.AddMessage("\n--------------------------------------------------------------")
        arcpy.AddMessage('Validando Topologia entre Drenaje y Curva de Nivel')
        total = DrenajL_CNivel(GDB_Entrada, GDB_Salida)
        if str(total) == '0':
            arcpy.AddMessage("Se encontraron " + str(total) + " errores en total")
        else:
            arcpy.AddMessage("Se encontraron " + str(total) + " errores en total \n->Validar en  Feature: DrenajeL_CNivel")
    
    if R10 == 'true': #Via_Const_R
        arcpy.AddMessage("\n--------------------------------------------------------------")
        arcpy.AddMessage('Validando Topologia entre Vía y Construccion _R')
        total = via_constr_r(GDB_Entrada,Ruta_Salida ,GDB_Salida)
        if str(total) == '0':
            arcpy.AddMessage("Se encontraron " + str(total) + " errores en total")
        else:
            arcpy.AddMessage("Se encontraron " + str(total) + " errores en total \n->Validar en  Feature: Via_Construccion_R")
    if T1 == 'true': #Curva_nivel-Piscina
        arcpy.AddMessage("--------------------------------------------------------------")
        arcpy.AddMessage("Validando Topologia entre Curva de nivel y Piscina")
        total = Cnivel_Piscin(GDB_Entrada, Ruta_Salida, GDB_Salida)
        if str(total) == '0':
            arcpy.AddMessage("Se encontraron " + str(total) + " errores en total")
        else:
            arcpy.AddMessage("Se encontraron " + str(total) + " errores en total \n->Validar en  Feature: Cnivel_Piscin")
    if T2 == 'true': #Cerca_Construccion
        arcpy.AddMessage("--------------------------------------------------------------")
        arcpy.AddMessage("Validando Topologia entre Cercas y Construccion")
        total = Cerca_Constr_R(GDB_Entrada, Ruta_Salida, GDB_Salida)
        if str(total) == '0':
            arcpy.AddMessage("Se encontraron " + str(total) + " errores en total")
        else:
            arcpy.AddMessage("Se encontraron " + str(total) + " errores en total \n->Validar en  Feature: Cerca_ConstrR")
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
    
    if V1 == 'true': #LVia_Deposito
        arcpy.AddMessage("--------------------------------------------------------------")
        arcpy.AddMessage("Validando Topologia entre Limite Via y Deposito de agua")
        validacion = LVia_DAguaR(GDB_Entrada, Ruta_Salida, GDB_Salida)
        if str(validacion) == '0':
            arcpy.AddMessage("Se encontraron " + str(validacion) + " errores en total")
        else:
            arcpy.AddMessage("Se encontraron " + str(validacion) + " errores en total \n->Validar en  Feature: LVia_Deposito")
    
    if V2 == 'true': #Via_Cercas
        arcpy.AddMessage("--------------------------------------------------------------")
        arcpy.AddMessage("Validando Topologia entre Limite Via y Cerca")
        validacion = LVia_Cerca(GDB_Entrada, Ruta_Salida, GDB_Salida)
        if str(validacion) == '0':
            arcpy.AddMessage("Se encontraron " + str(validacion) + " errores en total")
        else:
            arcpy.AddMessage("Se encontraron " + str(validacion) + " errores en total \n->Validar en  Feature: Via_Cerca")
    if V3 == 'true': #ConstruccionR_ConstruccionP
        arcpy.AddMessage("--------------------------------------------------------------")
        arcpy.AddMessage("Validando Topologia entre ConstruccionR y ConstruccionP")
        validacion = ConstruccionR_ConstruccionP(GDB_Entrada, Ruta_Salida, GDB_Salida)
        if str(validacion) == '0':
            arcpy.AddMessage("Se encontraron " + str(validacion) + " errores en total")
        else:
            arcpy.AddMessage("Se encontraron " + str(validacion) + " errores en total \n->Validar en  Feature: ConstruccionR_ConstruccionP")
    if V4 == 'true': #Via_Deposito
        arcpy.AddMessage("--------------------------------------------------------------")
        arcpy.AddMessage("Validando Topologia entre Via y Deposito de agua")
        validacion = Via_DAguaR(GDB_Entrada, Ruta_Salida, GDB_Salida)
        if str(validacion) == '0':
            arcpy.AddMessage("Se encontraron " + str(validacion) + " errores en total")
        else:
            arcpy.AddMessage("Se encontraron " + str(validacion) + " errores en total \n->Validar en  Feature: Via_Deposito")
    if V5 == 'true': #Deposito_DrenajeL
        arcpy.AddMessage("--------------------------------------------------------------")
        arcpy.AddMessage("Validando Topologia entre Deposito de agua Y Drenajes L")
        validacion = Deposito_DrenajeL(GDB_Entrada, Ruta_Salida, GDB_Salida)
        if str(validacion) == '0':
            arcpy.AddMessage("Se encontraron " + str(validacion) + " errores en total")
        else:
            arcpy.AddMessage("Se encontraron " + str(validacion) + " errores en total \n->Validar en  Feature: Deposito_DrenajeL")
    if V6 == 'true': #Deposito_DrenajeR
        arcpy.AddMessage("--------------------------------------------------------------")
        arcpy.AddMessage("Validando Topologia entre Deposito de agua Y Drenajes R")
        validacion = Deposito_DrenajeR(GDB_Entrada, Ruta_Salida, GDB_Salida)
        if str(validacion) == '0':
            arcpy.AddMessage("Se encontraron " + str(validacion) + " errores en total")
        else:
            arcpy.AddMessage("Se encontraron " + str(validacion) + " errores en total \n->Validar en  Feature: Deposito_DrenajeR")
    if V7 == 'true': #JagueyP_JagueyR
        arcpy.AddMessage("--------------------------------------------------------------")
        arcpy.AddMessage("Validando Topologia entre Jagueys P y Jagueys R")
        validacion = JagueyP_JagueyR(GDB_Entrada, Ruta_Salida, GDB_Salida)
        if str(validacion) == '0':
            arcpy.AddMessage("Se encontraron " + str(validacion) + " errores en total")
        else:
            arcpy.AddMessage("Se encontraron " + str(validacion) + " errores en total \n->Validar en  Feature: JagueyP_JagueyR")
    
    if V8 == 'true': #Deposito_Deposito
        arcpy.AddMessage("--------------------------------------------------------------")
        arcpy.AddMessage("Validando Topologia entre Depositos (No se pueden intersecar así sean del mismo tipo)")
        validacion = Deposito_Deposito(GDB_Entrada, Ruta_Salida, GDB_Salida)
        if str(validacion) == '0':
            arcpy.AddMessage("Se encontraron " + str(validacion) + " errores en total")
        else:
            arcpy.AddMessage("Se encontraron " + str(validacion) + " errores en total \n->Validar en  Feature: Deposito_Deposito")
    if V9 == 'true': #Muro_ConstrR
        arcpy.AddMessage("--------------------------------------------------------------")
        arcpy.AddMessage("Validando Topologia entre Muro y Construccion R")
        validacion = muro_constrR(GDB_Entrada, Ruta_Salida, GDB_Salida)
        if str(validacion) == '0':
            arcpy.AddMessage("Se encontraron " + str(validacion) + " errores en total")
        else:
            arcpy.AddMessage("Se encontraron " + str(validacion) + " errores en total \n->Validar en  Feature: Muro_ConstrR")
    
    if V10 == 'true': #ConstrR_TSPubl
        arcpy.AddMessage("--------------------------------------------------------------")
        arcpy.AddMessage("Validando Topologia entre Construccion R y Tapa de servicio Publico")
        validacion = constrR_TP(GDB_Entrada, Ruta_Salida, GDB_Salida)
        if str(validacion) == '0':
            arcpy.AddMessage("Se encontraron " + str(validacion) + " errores en total")
        else:
            arcpy.AddMessage("Se encontraron " + str(validacion) + " errores en total \n->Validar en  Feature: TS_Publ_ConstrR")
    
    if V11 == 'true': #ConstrR_ PDistr
        arcpy.AddMessage("--------------------------------------------------------------")
        arcpy.AddMessage("Validando Topologia entre Construccion R y punto de distribucion")
        validacion = constrR_PD(GDB_Entrada, Ruta_Salida, GDB_Salida)
        if str(validacion) == '0':
            arcpy.AddMessage("Se encontraron " + str(validacion) + " errores en total")
        else:
            arcpy.AddMessage("Se encontraron " + str(validacion) + " errores en total \n->Validar en  Feature: TS_Publ_ConstrR")
    
    if V12 == 'true': #Via - Zona dura
        arcpy.AddMessage("--------------------------------------------------------------")
        arcpy.AddMessage("Validando Topologia entre Vía y Zona Dura")
        validacion = via_zdura(GDB_Entrada, Ruta_Salida, GDB_Salida)
        if str(validacion) == '0':
            arcpy.AddMessage("Se encontraron " + str(validacion) + " errores en total")
        else:
            arcpy.AddMessage("Se encontraron " + str(validacion) + " errores en total \n->Validar en  Feature: TS_Publ_ConstrR")
    arcpy.AddMessage("\n--------------------------------------------------------------")
    arcpy.AddMessage("FINALIZADO")

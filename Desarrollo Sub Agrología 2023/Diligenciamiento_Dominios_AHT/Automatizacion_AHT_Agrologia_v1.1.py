# -*- #################
# ---------------------------------------------------------------------------
# Direccion de Gestion de InformaciÃ³n Geografica
# Created on: 2023-06-05
# Created by: Gabriel Hernan Gonzalez Buitrago
# # Usage: Recalculo de valores a BD Agrologia 
# Description:
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
import os

# Script arguments
GDB_input = arcpy.GetParameterAsText(0)
#GDB_input ='D:/22_IGAC/2. Proyectos/3. Desarrollos/5. Calculos_sobre_GDB_Agrologia/1_Insumos/AHT_20032_Ces_Astrea_2023.gdb'
arcpy.env.workspace=GDB_input

# Showing templates
sep= '######################################'
arrow= '--'
hasht= '##'

# Construccion funciones: 
def creartabladestino(feature_insumo, GDB):  # Crea tabla donde seran completados las columnas en funcion del campo simbolo
    x=arcpy.FeatureClassToFeatureClass_conversion(feature_insumo,out_path=os.path.join(GDB_input, 'AHT'),out_name="AREA_HOMOGENEA_TIERRA_filled")
    arcpy.DeleteFeatures_management(x)
    return "Feature de salida creado correctamente."

#Creacion de diccionarios:
clase_valor=	["Sin dato","ZU","CA","02","03","04","05","06","07","08","10","11","12","13","01","09"]
clase_clave=	["0","14","16","2","3","4","5","6","7",	"8","10","11","12","13","1","9"]
diccionario_clase = {clase_valor:clase_clave for (clase_valor,clase_clave) in zip(clase_valor,clase_clave)}

subclaseclima_valor=	["SinDato",	"CA",	"CM",	"CS",	"CH",	"CU",	"MM",	"MS",	"MH",	"MU",	"MP",	"FS",	"FH",	"FU",	"FP",	"mFH",	"mFU",	"mFP",	"MUtMP",	"EFP",	"CHtMH",	"MStMH",	"FStFH",	"MStFS",	"mFHtEFP",	"MHtFH",	"MStFH",	"MHtMU",	"FUtmFH",	"CStCH",	"CHtCU",	"MUtFU",	"FHtFU",	"FHtFP",	"FUtFP",	"FHtmFH",	"CStMH",	"FHtmFU",	"N",	"CAtCS",	"CAtMM",	"CAtMS",	"CHtMP",	"CHtMS",	"CHtMU",	"CStMM",	"CStMS",	"CStMU",	"CUtMH",	"CUtMP",	"CUtMU",	"EFH",	"EFU",	"FStFU",	"mFHtEFH",	"mFHtEFU",	"mFUtEFH",	"mFUtEFP",	"mFUtEFU",	"MHtFS",	"MHtFU",	"MHtMP",	"MMtFS",	"MMtMH",	"MMtMS",	"MStMU",	"MUtFH",	"MUtFP",	"MUtFS",	"FUtmFU",	"FStFP",	"FStmFH",	"FStmFU",	"MHtFP",	"MPtFP",	"CP",	"CPtMP",	"MPtFU",	"mFPtEFP",	"FPtmFP",	"FHtmFP",	"FUtmFP",	"CMtCS",	"CAtCM",	"CMtMH",	"CMtMM",	"CMtMS",	"SN"]
subclaseclima_clave=	["0",	"1",	"2",	"3",	"4",	"5",	"7",	"8",	"9",	"10",	"11",	"12",	"13",	"14",	"15",	"16",	"17",	"18",	"19",	"20",	"22",	"24",	"25",	"28",	"30",	"31",	"32",	"35",	"36",	"40",	"41",	"43",	"44",	"45",	"46",	"47",	"50",	"57",	"58",	"72",	"73",	"74",	"81",	"82",	"83",	"96",	"97",	"98",	"105",	"107",	"109",	"110",	"116",	"136",	"149",	"150",	"152",	"153",	"154",	"159",	"160",	"162",	"169",	"170",	"171",	"185",	"190",	"191",	"192",	"193",	"216",	"217",	"218",	"230",	"236",	"244",	"247",	"248",	"249",	"250",	"251",	"252",	"48",	"71",	"89",	"90",	"91",	"253"]
diccionario_subclaseclima = {subclaseclima_valor:subclaseclima_clave for (subclaseclima_valor,subclaseclima_clave) in zip(subclaseclima_valor,subclaseclima_clave)}

subclapendiente_valor= ["Sin Dato",	"a",	"b",	"c",	"d",	"e",	"f",	"g"]
subclapendiente_clave=["0",	"1",	"2",	"3",	"4",	"5",	"6",	"7"]
diccionario_subclapendiente={subclapendiente_valor:subclapendiente_clave for (subclapendiente_valor,subclapendiente_clave) in zip(subclapendiente_valor,subclapendiente_clave)}

suberosionh_valor= ["No hay",	"2",	"3",	"1"]
suberosionh_clave=["0",	"2",	"3",	"1"]
diccionario_suberosionh={suberosionh_valor:suberosionh_clave for (suberosionh_valor,suberosionh_clave) in zip(suberosionh_valor,suberosionh_clave)}

suberosione_valor= ["No hay",	"k2",	"k3",	"k1"]
suberosione_clave=["0",	"1",	"2",	"3"]
diccionario_suberosione={suberosione_valor:suberosione_clave for (suberosione_valor,suberosione_clave) in zip(suberosione_valor,suberosione_clave)}

subremocion_valor= ["No hay",	"m2",	"m3",	"m1"]
subremocion_clave=["0",	"1",	"2",	"3"]
diccionario_subremocion={subremocion_valor:subremocion_clave for (subremocion_valor,subremocion_clave) in zip(subremocion_valor,subremocion_clave)}

subinundacion_valor= ["No se presenta",	"i"]
subinundacion_clave=["0",	"1"]
diccionario_subinundacion={subinundacion_valor:subinundacion_clave for (subinundacion_valor,subinundacion_clave) in zip(subinundacion_valor,subinundacion_clave)}

subencharca_valor= ["No se presenta",	"E"]
subencharca_clave=["0",	"1"]
diccionario_subencharca={subencharca_valor:subencharca_clave for (subencharca_valor,subencharca_clave) in zip(subencharca_valor,subencharca_clave)}

subfrea_valor= ["No se presenta",	"h"]
subfrea_clave=["0",	"1"]
diccionario_subfrea={subfrea_valor:subfrea_clave for (subfrea_valor,subfrea_clave) in zip(subfrea_valor,subfrea_clave)}

subprof_valor= ["No se presenta",	"s"]
subprof_clave=["0",	"1"]
diccionario_subprof={subprof_valor:subprof_clave for (subprof_valor,subprof_clave) in zip(subprof_valor,subprof_clave)}

subhoriz_valor= ["No se presenta",	"D"]
subhoriz_clave=["0",	"1"]
diccionario_subhoriz={subhoriz_valor:subhoriz_clave for (subhoriz_valor,subhoriz_clave) in zip(subhoriz_valor,subhoriz_clave)}

subfrag_valor= ["No se presenta",	"q"]
subfrag_clave=["0",	"1"]
diccionario_subfrag={subfrag_valor:subfrag_clave for (subfrag_valor,subfrag_clave) in zip(subfrag_valor,subfrag_clave)}

subpedregosidad_valor= ["No se presenta",	"p"]
subpedregosidad_clave=["0",	"1"]
diccionario_subpedregosidad={subpedregosidad_valor:subpedregosidad_clave for (subpedregosidad_valor,subpedregosidad_clave) in zip(subpedregosidad_valor,subpedregosidad_clave)}

subrocos_valor= ["No se presenta",	"r"]
subrocos_clave=["0",	"1"]
diccionario_subrocos={subrocos_valor:subrocos_clave for (subrocos_valor,subrocos_clave) in zip(subrocos_valor,subrocos_clave)}

subsodic_valor= ["No se presenta",	"n"]
subsodic_clave=["0",	"1"]
diccionario_subsodic={subsodic_valor:subsodic_clave for (subsodic_valor,subsodic_clave) in zip(subsodic_valor,subsodic_clave)}

subsalin_valor= ["No se presenta",	"z"]
subsalin_clave=["0",	"1"]
diccionario_subsalin={subsalin_valor:subsalin_clave for (subsalin_valor,subsalin_clave) in zip(subsalin_valor,subsalin_clave)}

subyeso_valor= ["No se presenta",	"y"]
subyeso_clave=["0",	"1"]
diccionario_subyeso={subyeso_valor:subyeso_clave for (subyeso_valor,subyeso_clave) in zip(subyeso_valor,subyeso_clave)}

subdrenaje_valor= ["No se presenta",	"v"]
subdrenaje_clave=["0",	"1"]
diccionario_subdrenaje={subdrenaje_valor:subdrenaje_clave for (subdrenaje_valor,subdrenaje_clave) in zip(subdrenaje_valor,subdrenaje_clave)}

subacidez_valor= ["No se presenta",	"L"]
subacidez_clave=["0",	"1"]
diccionario_subacidez={subacidez_valor:subacidez_clave for (subacidez_valor,subacidez_clave) in zip(subacidez_valor,subacidez_clave)}

submiscelaneos_valor= ["No se presenta",	"MR",	"ME",	"BA",	"PN",	"ZM",	"FM",	"SL",	"MN",	"CL",	"RS",	"NP",	"BP",	"EP",	"IS",	"RN"]
submiscelaneos_clave=["0",	"1","2","3","5","6","7","8","9","10","11","13","4","12","14","15"]
diccionario_submiscelaneos={submiscelaneos_valor:submiscelaneos_clave for (submiscelaneos_valor,submiscelaneos_clave) in zip(submiscelaneos_valor,submiscelaneos_clave)}

subpotencial_valor= ["-",	"-92",	"-80",	"-73",	"-67",	"-61",	"-55",	"-49",	"-44",	"-38",	"-30",	"-23",	"-17",	"-6"]
subpotencial_clave=["0",	"1",	"2",	"3",	"4",	"5",	"6",	"7",	"8",	"9",	"10",	"11",	"12",	"13"]
diccionario_subpotencial={subpotencial_valor:subpotencial_clave for (subpotencial_valor,subpotencial_clave) in zip(subpotencial_valor,subpotencial_clave)}



#### Inicio Herramienta

arcpy.AddMessage("\n{0} ...INICIANDO PROCESO DE DILIGENCIAMIENTO BD AGROLOGIA... {1}.".format(sep, sep))

creartabladestino('AHT/AREA_HOMOGENEA_TIERRA',GDB_input)


a='' ##almacena la cadena de items del simbolo que va acoplando en cada iteraciÃ³n
clase=0

with arcpy.da.SearchCursor('AHT/AREA_HOMOGENEA_TIERRA',['SHAPE@', 'SIMBOLO', 'CLASE','UClimatica','PENDIENTE','EHidrica','EEolica','ERemosion', 'INUNDACION','Encharcami','FNFreatico','PEfectiva','HDensicos','FGPerfil','PSuperfici','LRocosidad','LSodicidad','LSalinidad','CYeso','DArtificia','AIntercamb','Miscelaneo','VPotencial','Divipola', 'UCSuelo','Observacio','Fecha','TRelieve','MParental', 'CSimbolo']) as sCur:
    with arcpy.da.InsertCursor(os.path.join(GDB_input, 'AHT/AREA_HOMOGENEA_TIERRA_filled'),['SHAPE@', 'SIMBOLO', 'CLASE','UClimatica','PENDIENTE','EHidrica','EEolica','ERemosion', 'INUNDACION','Encharcami','FNFreatico','PEfectiva','HDensicos','FGPerfil','PSuperfici','LRocosidad','LSodicidad','LSalinidad','CYeso','DArtificia','AIntercamb','Miscelaneo','VPotencial','Divipola', 'UCSuelo','Observacio','Fecha','TRelieve','MParental', 'CSimbolo']) as iCur:
        for row in sCur:
            row_list= list(row)
            simbol=row[1]
            simbolo=simbol.replace(" ", "").replace("'","") #Quitando espacios a simbolo y comillas sencillas.
            #arcpy.AddMessage("\n Buscando simbolo: {0}.".format(simbolo))

            a_clase=simbolo[0:2] 
            clase=0
            for indice in range(len(a_clase) , -1, -1):
                if clase !=1:
                    a=a_clase[:indice]
                    if str(a) in diccionario_clase:
                        #arcpy.AddMessage("Encontrado en diccionario. a="+str(a))
                        row_list[2]=diccionario_clase[str(a)] ## -----------------------------------------------------------Clase
                        clase=1 # 1 encontrado | o no encontrado.
                        posc_clase=indice
                        a_climatica=simbolo[posc_clase:posc_clase+7] #Se carga el maximo de caracteres para la validaciÃ³n del campo UClimatica. 
                    else:   #No encontrado en diccionario                 
                        row_list[2]=0
                        climatica=0 # 1 encontrado | o no encontrado.
                        posc_clase=0
                        a_climatica=simbolo[posc_clase:posc_clase+7] #Se carga el maximo de caracteres para la validaciÃ³n del campo UClimatica. 

            climatica=0
            for indice in range(len(a_climatica) , -1, -1):
                if climatica !=1:
                    b=a_climatica[:indice]
                    if str(b) in diccionario_subclaseclima:
                        row_list[3]=diccionario_subclaseclima[str(b)] ## -----------------------------------------------------------UClimatica
                        a=''  # se limpian las siglas coincidentes
                        clase=1 # 1 encontrado | o no encontrado.
                        climatica=1
                        posc_climatica=posc_clase+indice
                        c_pendiente=simbolo[posc_climatica:posc_climatica+1] #Se carga el maximo de caracteres para la validaciÃ³n del campo Pendiente. 
                    else:                    
                        row_list[3]=0
                        climatica=0 # 1 encontrado | o no encontrado.
                        posc_climatica=posc_clase
                        c_pendiente=simbolo[posc_climatica:posc_climatica+1] #Se carga el maximo de caracteres para la validaciÃ³n del campo Pendiente. 
                
            pendiente=0
            for indice in range(len(c_pendiente) , -1, -1):
                if pendiente !=1:
                    c=c_pendiente[:indice]
                    if str(c) in diccionario_subclapendiente:
                        row_list[4]=diccionario_subclapendiente[str(c)] ## -----------------------------------------------------------Pendiente
                        a=''  # se limpian las siglas coincidentes
                        pendiente=1 # 1 encontrado | o no encontrado.
                        posc_pendiente=posc_climatica+indice
                        d_erosionh=simbolo[posc_pendiente:posc_pendiente+1] #Se carga el maximo de caracteres para la validaciÃ³n del campo ErosionH. 
                    else:                    
                        row_list[4]=0
                        pendiente=0 # 1 encontrado | o no encontrado.
                        posc_pendiente=posc_climatica
                        d_erosionh=simbolo[posc_pendiente:posc_pendiente+1] #Se carga el maximo de caracteres para la validaciÃ³n del campo ErosionH. 
            
            erosionh=0
            for indice in range(len(d_erosionh) , -1, -1):
                if erosionh !=1:
                    d=d_erosionh[:indice]
                    if str(d) in diccionario_suberosionh:
                        row_list[5]=diccionario_suberosionh[str(d)] ## -----------------------------------------------------------ErosionHidrica
                        a=''  # se limpian las siglas coincidentes
                        erosionh=1 # 1 encontrado | o no encontrado.
                        posc_erosionh=posc_pendiente+indice
                        e_erosione=simbolo[posc_erosionh:posc_erosionh+2] #Se carga el maximo de caracteres para la validaciÃ³n del campo ErosionE. 
                    else:                    
                        row_list[5]=0
                        erosionh=0 # 1 encontrado | o no encontrado.
                        posc_erosionh=posc_pendiente
                        e_erosione=simbolo[posc_erosionh:posc_erosionh+2] #Se carga el maximo de caracteres para la validaciÃ³n del campo ErosionE

            erosione=0
            for indice in range(len(e_erosione) , -1, -1):
                if erosione !=1:
                    e=e_erosione[:indice]
                    if str(e) in diccionario_suberosione:
                        row_list[6]=diccionario_suberosione[str(e)] ## -----------------------------------------------------------ErosionEolica
                        a=''  # se limpian las siglas coincidentes
                        erosione=1 # 1 encontrado | o no encontrado.
                        posc_erosione=posc_erosionh+indice
                        f_remocion=simbolo[posc_erosione:posc_erosione+2] #Se carga el maximo de caracteres para la validaciÃ³n del campo Remocion
                    else:                    
                        row_list[6]=0
                        pendiente=0 # 1 encontrado | o no encontrado.
                        posc_erosione=posc_erosionh
                        f_remocion=simbolo[posc_erosione:posc_erosione+2] #Se carga el maximo de caracteres para la validaciÃ³n del campo Remocion

            remocion=0
            for indice in range(len(f_remocion) , -1, -1):
                if remocion !=1:
                    f=f_remocion[:indice]
                    if str(f) in diccionario_subremocion:
                        row_list[7]=diccionario_subremocion[str(f)] ## -----------------------------------------------------------Remocion
                        remocion=1 # 1 encontrado | o no encontrado.
                        posc_remocion=posc_erosione+indice
                        g_inundacion=simbolo[posc_remocion:posc_remocion+1] #Se carga el maximo de caracteres para la validaciÃ³n del campo inundacion
                    else:                    
                        row_list[7]=0
                        remocion=0 # 1 encontrado | o no encontrado.
                        posc_remocion=posc_erosione
                        g_inundacion=simbolo[posc_remocion:posc_remocion+1] #Se carga el maximo de caracteres para la validaciÃ³n del campo inundacion
        
            inundacion=0
            for indice in range(len(g_inundacion) , -1, -1):
                if inundacion !=1:
                    g=g_inundacion[:indice]
                    if str(g) in diccionario_subinundacion:
                        row_list[8]=diccionario_subinundacion[str(g)] ## -----------------------------------------------------------Inundacion
                        inundacion=1 # 1 encontrado | o no encontrado.
                        posc_inundacion=posc_remocion+indice
                        h_encharcamiento=simbolo[posc_inundacion:posc_inundacion+1] #Se carga el maximo de caracteres para la validaciÃ³n del campo Encharcamiento
                    else:                    
                        row_list[8]=0
                        inundacion=0 # 1 encontrado | o no encontrado.
                        posc_inundacion=posc_remocion
                        h_encharcamiento=simbolo[posc_inundacion:posc_inundacion+1] #Se carga el maximo de caracteres para la validaciÃ³n del campo Encharcamiento
            
            encharcamiento=0
            for indice in range(len(h_encharcamiento) , -1, -1):
                if encharcamiento !=1:
                    h=h_encharcamiento[:indice]
                    if str(h) in diccionario_subencharca:
                        row_list[9]=diccionario_subencharca[str(h)] ## -----------------------------------------------------------Encharcamiento
                        encharcamiento=1 # 1 encontrado | o no encontrado.
                        posc_encharcamiento=posc_inundacion+indice
                        i_freatico=simbolo[posc_encharcamiento:posc_encharcamiento+1] #Se carga el maximo de caracteres para la validaciÃ³n del campo Freatico
                    else:                    
                        row_list[9]=0
                        inundacion=0 # 1 encontrado | o no encontrado.
                        posc_encharcamiento=posc_inundacion
                        i_freatico=simbolo[posc_encharcamiento:posc_encharcamiento+1] #Se carga el maximo de caracteres para la validaciÃ³n del campo Freatico
            
            freatico=0
            for indice in range(len(i_freatico) , -1, -1):
                if freatico !=1:
                    i=i_freatico[:indice]
                    if str(i) in diccionario_subfrea:
                        row_list[10]=diccionario_subfrea[str(i)] ## -----------------------------------------------------------Freatico
                        freatico=1 # 1 encontrado | o no encontrado.
                        posc_freatico=posc_encharcamiento+indice
                        j_profundidad=simbolo[posc_freatico:posc_freatico+1] #Se carga el maximo de caracteres para la validaciÃ³n del campo profundidad
                    else:                    
                        row_list[10]=0
                        freatico=0 # 1 encontrado | o no encontrado.
                        posc_freatico=posc_encharcamiento
                        j_profundidad=simbolo[posc_freatico:posc_freatico+1] #Se carga el maximo de caracteres para la validaciÃ³n del campo Profundidad
            
            profundidad=0
            for indice in range(len(j_profundidad) , -1, -1):
                if profundidad !=1:
                    j=j_profundidad[:indice]
                    if str(j) in diccionario_subprof:
                        row_list[11]=diccionario_subprof[str(j)] ## -----------------------------------------------------------Profundidad
                        profundidad=1 # 1 encontrado | o no encontrado.
                        posc_profundidad=posc_freatico+indice
                        k_horizonte=simbolo[posc_profundidad:posc_profundidad+1] #Se carga el maximo de caracteres para la validaciÃ³n del campo horizonte
                    else:                    
                        row_list[11]=0
                        profundidad=0 # 1 encontrado | o no encontrado.
                        posc_profundidad=posc_freatico
                        k_horizonte=simbolo[posc_profundidad:posc_profundidad+1] #Se carga el maximo de caracteres para la validaciÃ³n del campo horizonte
            
            horizonte=0
            for indice in range(len(k_horizonte) , -1, -1):
                if horizonte !=1:
                    k=k_horizonte[:indice]
                    if str(k) in diccionario_subhoriz:
                        row_list[12]=diccionario_subhoriz[str(k)] ## -----------------------------------------------------------Horizonte
                        horizonte=1 # 1 encontrado | o no encontrado.
                        posc_horizonte=posc_profundidad+indice
                        l_frag=simbolo[posc_horizonte:posc_horizonte+1] #Se carga el maximo de caracteres para la validaciÃ³n del campo fragmento
                    else:                    
                        row_list[12]=0
                        profundidad=0 # 1 encontrado | o no encontrado.
                        posc_horizonte=posc_profundidad
                        l_frag=simbolo[posc_horizonte:posc_horizonte+1] #Se carga el maximo de caracteres para la validaciÃ³n del campo fragmento
            
            frag=0
            for indice in range(len(l_frag) , -1, -1):
                if frag !=1:
                    l=l_frag[:indice]
                    if str(l) in diccionario_subfrag:
                        row_list[13]=diccionario_subfrag[str(l)] ## -----------------------------------------------------------fragmento
                        frag=1 # 1 encontrado | o no encontrado.
                        posc_frag=posc_horizonte+indice
                        m_pedrego=simbolo[posc_frag:posc_frag+1] #Se carga el maximo de caracteres para la validaciÃ³n del campo pedregosidad
                    else:                    
                        row_list[13]=0
                        profundidad=0 # 1 encontrado | o no encontrado.
                        posc_frag=posc_horizonte
                        m_pedrego=simbolo[posc_frag:posc_frag+1] #Se carga el maximo de caracteres para la validaciÃ³n del campo pedregosidad
            
            pedrego=0
            for indice in range(len(m_pedrego) , -1, -1):
                if pedrego !=1:
                    m=m_pedrego[:indice]
                    if str(m) in diccionario_subpedregosidad:
                        row_list[14]=diccionario_subpedregosidad[str(m)] ## -----------------------------------------------------------pedregosidad
                        pedrego=1 # 1 encontrado | o no encontrado.
                        posc_pedrego=posc_frag+indice
                        n_roco=simbolo[posc_pedrego:posc_pedrego+1] #Se carga el maximo de caracteres para la validaciÃ³n del campo rocosidad
                    else:                    
                        row_list[14]=0
                        pedrego=0 # 1 encontrado | o no encontrado.
                        posc_pedrego=posc_frag
                        n_roco=simbolo[posc_pedrego:posc_pedrego+1] #Se carga el maximo de caracteres para la validaciÃ³n del campo rocosidad
            
            roco=0
            for indice in range(len(n_roco) , -1, -1):
                if roco !=1:
                    n=n_roco[:indice]
                    if str(n) in diccionario_subrocos:
                        row_list[15]=diccionario_subrocos[str(n)] ## -----------------------------------------------------------rocosidad
                        roco=1 # 1 encontrado | o no encontrado.
                        posc_roco=posc_pedrego+indice
                        o_sodicidad=simbolo[posc_roco:posc_roco+1] #Se carga el maximo de caracteres para la validaciÃ³n del campo sodicidad
                    else:                    
                        row_list[15]=0
                        roco=0 # 1 encontrado | o no encontrado.
                        posc_roco=posc_pedrego
                        o_sodicidad=simbolo[posc_roco:posc_roco+1] #Se carga el maximo de caracteres para la validaciÃ³n del campo sodicidad
            
            sodicidad=0
            for indice in range(len(o_sodicidad) , -1, -1):
                if sodicidad !=1:
                    o=o_sodicidad[:indice]
                    if str(o) in diccionario_subsodic:
                        row_list[16]=diccionario_subsodic[str(o)] ## -----------------------------------------------------------sodicidad
                        sodicidad=1 # 1 encontrado | o no encontrado.
                        posc_sodicidad=posc_roco+indice
                        p_salinidad=simbolo[posc_sodicidad:posc_sodicidad+1] #Se carga el maximo de caracteres para la validaciÃ³n del campo salinidad
                    else:                    
                        row_list[16]=0
                        sodicidad=0 # 1 encontrado | o no encontrado.
                        posc_sodicidad=posc_roco
                        p_salinidad=simbolo[posc_sodicidad:posc_sodicidad+1] #Se carga el maximo de caracteres para la validaciÃ³n del campo salinidad
            
            salinidad=0
            for indice in range(len(p_salinidad) , -1, -1):
                if salinidad !=1:
                    p=p_salinidad[:indice]
                    if str(p) in diccionario_subsalin:
                        row_list[17]=diccionario_subsalin[str(p)] ## -----------------------------------------------------------salinidad
                        salinidad=1 # 1 encontrado | o no encontrado.
                        posc_salinidad=posc_sodicidad+indice
                        q_yeso=simbolo[posc_salinidad:posc_salinidad+1] #Se carga el maximo de caracteres para la validaciÃ³n del campo yeso
                    else:                    
                        row_list[17]=0
                        salinidad=0 # 1 encontrado | o no encontrado.
                        posc_salinidad=posc_sodicidad
                        q_yeso=simbolo[posc_salinidad:posc_salinidad+1] #Se carga el maximo de caracteres para la validaciÃ³n del campo yeso
            
            yeso=0
            for indice in range(len(q_yeso) , -1, -1):
                if yeso !=1:
                    q=q_yeso[:indice]
                    if str(q) in diccionario_subyeso:
                        row_list[18]=diccionario_subyeso[str(q)] ## -----------------------------------------------------------Yeso
                        yeso=1 # 1 encontrado | o no encontrado.
                        posc_yeso=posc_salinidad+indice
                        r_drenaje=simbolo[posc_yeso:posc_yeso+1] #Se carga el maximo de caracteres para la validaciÃ³n del campo Drenaje
                    else:                    
                        row_list[18]=0
                        yeso=0 # 1 encontrado | o no encontrado.
                        posc_yeso=posc_salinidad
                        r_drenaje=simbolo[posc_yeso:posc_yeso+1] #Se carga el maximo de caracteres para la validaciÃ³n del campo Drenaje
            
            drenaje=0
            for indice in range(len(r_drenaje) , -1, -1):
                if drenaje !=1:
                    r=r_drenaje[:indice]
                    if str(r) in diccionario_subdrenaje:
                        row_list[19]=diccionario_subdrenaje[str(r)] ## -----------------------------------------------------------Drenaje
                        drenaje=1 # 1 encontrado | o no encontrado.
                        posc_drenaje=posc_yeso+indice
                        s_acidez=simbolo[posc_drenaje:posc_drenaje+1] #Se carga el maximo de caracteres para la validaciÃ³n del campo Acidez
                    else:                    
                        row_list[19]=0
                        drenaje=0 # 1 encontrado | o no encontrado.
                        posc_drenaje=posc_yeso
                        s_acidez=simbolo[posc_drenaje:posc_drenaje+1] #Se carga el maximo de caracteres para la validaciÃ³n del campo Acidez
            
            acidez=0
            for indice in range(len(s_acidez) , -1, -1):
                if acidez !=1:
                    s=s_acidez[:indice]
                    if str(s) in diccionario_subacidez:
                        row_list[20]=diccionario_subacidez[str(s)] ## -----------------------------------------------------------Acidez
                        acidez=1 # 1 encontrado | o no encontrado.
                        posc_acidez=posc_drenaje+indice
                        t_miscelaneos=simbolo[posc_acidez:posc_acidez+2] #Se carga el maximo de caracteres para la validaciÃ³n del campo Miscelaneos
                    else:                    
                        row_list[20]=0
                        acidez=0 # 1 encontrado | o no encontrado.
                        posc_acidez=posc_drenaje
                        t_miscelaneos=simbolo[posc_acidez:posc_acidez+2] #Se carga el maximo de caracteres para la validaciÃ³n del campo Miscelaneos
            
            miscelaneos=0
            for indice in range(len(t_miscelaneos) , -1, -1):
                if miscelaneos !=1:
                    t=t_miscelaneos[:indice]
                    if str(t) in diccionario_submiscelaneos:
                        row_list[21]=diccionario_submiscelaneos[str(t)] ## -----------------------------------------------------------Miscelaneo
                        miscelaneos=1 # 1 encontrado | o no encontrado.
                        posc_miscelaneos=posc_acidez+indice
                        u_potencial=simbolo[posc_miscelaneos:posc_miscelaneos+3] #Se carga el maximo de caracteres para la validaciÃ³n del campo Potencial
                    else:                    
                        row_list[21]=0
                        miscelaneos=0 # 1 encontrado | o no encontrado.
                        posc_miscelaneos=posc_acidez
                        u_potencial=simbolo[posc_miscelaneos:posc_miscelaneos+3] #Se carga el maximo de caracteres para la validaciÃ³n del campo Potencial
            
            potencial=0
            for indice in range(len(u_potencial) , -1, -1):
                if potencial !=1:
                    u=u_potencial[:indice]
                    if str(u) in diccionario_subpotencial:
                        row_list[22]=diccionario_subpotencial[str(u)] ## -----------------------------------------------------------Potencial
                        potencial=1 # 1 encontrado | o no encontrado.
                        posc_potencial=posc_miscelaneos+indice
                    else:                    
                        row_list[22]=0
                        potencial=0 # 1 encontrado | o no encontrado.
                        posc_potencial=posc_miscelaneos
            row=tuple(row_list)
            iCur.insertRow(row)


arcpy.AddMessage("\n\n{0}Finalizado exitosamente!.\n".format(arrow))



# -*- #################
# ---------------------------------------------------------------------------
# Direccion de Gestion de InformaciÃ³n Geografica
# Created on: 2023-04-12
# Created by: Gabriel Hernan Gonzalez Buitrago
# # Usage:
# Description:
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
import os

# Script arguments
GDB = arcpy.GetParameterAsText(0)
#GDB ='D:/22_IGAC/2. Proyectos/3. Desarrollos/2. DominiosRuleid/Carto10000_41016_RS_20220812.gdb'
#global Variable:
edit = arcpy.da.Editor(GDB)

# Showing templates
sep= '######################################'
arrow= '--'
hasht= '##'


def activeeditsesion():
    arcpy.env.workspace=GDB
    edit = arcpy.da.Editor(arcpy.env.workspace)
    edit.startEditing(False, True)
    edit.startOperation()
    return 'sesion abierta'

def closeeditsesion():
    edit.stopOperation()
    edit.stopEditing(True)
    return 'sesion cerrada y cambios salvados'

def contarregistros(layer):
    result = arcpy.GetCount_management(layer)
    count = int(result.getOutput(0))
    return int(result.getOutput(0))

#------- Validacion-------------#
#-------------------------------#
arcpy.env.workspace=GDB
arcpy.AddMessage("\n{0} VALIDADOR DE DOMINIOS SOBRE RULEID {1}.".format(sep, sep))
arcpy.AddMessage("{0}{1}{2}\n".format(sep, sep,sep))

#### Cobertura_tierra
arcpy.AddMessage("{0} Dataset Cobertura Tierra... ".format(hasht))

#activeeditsesion()
arcpy.env.workspace=GDB
edit = arcpy.da.Editor(arcpy.env.workspace)
edit.startEditing(False, True)
edit.startOperation()

##   AExtra:
arcpy.AddMessage("{0} AExtra:".format(arrow))
arcpy.CalculateField_management(in_table='CoberturaTierra\AExtra', field="RuleID", expression="1", expression_type="VB", code_block="")
arcpy.AddMessage("\t Procesados {0} registros.\n".format(contarregistros('CoberturaTierra\AExtra')))

##   Bosque:
arcpy.AddMessage("{0} Bosque:".format(arrow))
arcpy.CalculateField_management(in_table='CoberturaTierra\Bosque', field="RuleID", expression="1", expression_type="VB", code_block="")
arcpy.AddMessage("\t Procesados {0} registros.\n".format(contarregistros('CoberturaTierra\Bosque')))

##   Zona Verde:
arcpy.AddMessage("{0} Zona Verde:".format(arrow))
arcpy.CalculateField_management(in_table='CoberturaTierra\ZVerde', field="RuleID", expression="1", expression_type="VB", code_block="")
arcpy.AddMessage("\t Procesados {0} registros.\n".format(contarregistros('CoberturaTierra\ZVerde')))
#### End_Cobertura_tierra



#### Elevacion
arcpy.AddMessage("{0} Dataset Elevacion... ".format(hasht))
## Curva de Nivel:
arcpy.AddMessage("{0} Curva de Nivel:".format(arrow))
arcpy.CalculateField_management(in_table='Elevacion\CNivel', field="RuleID", expression="calcular_Rule( !CNTipo! , !RuleID! )", expression_type="PYTHON_9.3", code_block="def calcular_Rule(x,r):\n if r is None:\n  return x\n else:\n  return r")
arcpy.CalculateField_management(in_table='Elevacion\CNivel', field="CNTipo", expression="calcular_Rule( !CNTipo! , !RuleID! )", expression_type="PYTHON_9.3", code_block="def calcular_Rule(x,r):\n return r")
arcpy.AddMessage("\t Procesados {0} registros.\n".format(contarregistros('Elevacion\CNivel')))
#### End_Elevacion


#### Hidrografia
arcpy.AddMessage("{0} Dataset Hidrografia... ".format(hasht))
## Banco Arena:
arcpy.AddMessage("{0} Banco Arena:".format(arrow))
arcpy.CalculateField_management(in_table='Hidrografia\BArena', field="RuleID", expression="1", expression_type="VB", code_block="")
arcpy.AddMessage("\t Procesados {0} registros.\n".format(contarregistros('Hidrografia\BArena')))

## Deposito Agua P:
arcpy.AddMessage("{0} Deposito Agua P:".format(arrow))
arcpy.CalculateField_management(in_table='Hidrografia\DAgua_P', field="RuleID", expression="1", expression_type="VB", code_block="")
arcpy.CalculateField_management(in_table='Hidrografia\DAgua_P', field="DATipo", expression="1", expression_type="VB", code_block="")
arcpy.AddMessage("\t Procesados {0} registros.\n".format(contarregistros('Hidrografia\DAgua_P')))

## Deposito Agua R:
arcpy.AddMessage("{0} Deposito Agua R:".format(arrow))
arcpy.CalculateField_management(in_table='Hidrografia\DAgua_R', field="RuleID", expression="calcular_Rule( !DATipo! , !RuleID! )", expression_type="PYTHON_9.3", code_block="def calcular_Rule(x,r):\n if r is None:\n  return x\n else:\n  return r")
arcpy.CalculateField_management(in_table='Hidrografia\DAgua_R', field="DATipo", expression="calcular_Rule( !DATipo! , !RuleID! )", expression_type="PYTHON_9.3", code_block="def calcular_Rule(x,r):\n return r")
arcpy.AddMessage("\t Procesados {0} registros.\n".format(contarregistros('Hidrografia\DAgua_R')))

## Humedal:
arcpy.AddMessage("{0} Humedal:".format(arrow))
arcpy.CalculateField_management(in_table='Hidrografia\Humeda', field="RuleID", expression="1", expression_type="VB", code_block="")
arcpy.AddMessage("\t Procesados {0} registros.\n".format(contarregistros('Hidrografia\Humeda')))

## Manglar:
arcpy.AddMessage("{0} Manglar:".format(arrow))
arcpy.CalculateField_management(in_table='Hidrografia\Mangla', field="RuleID", expression="1", expression_type="VB", code_block="")
arcpy.AddMessage("\t Procesados {0} registros.\n".format(contarregistros('Hidrografia\Mangla')))

## Isla:
arcpy.AddMessage("{0} Isla:".format(arrow))
arcpy.CalculateField_management(in_table='Hidrografia\Isla', field="RuleID", expression="1", expression_type="VB", code_block="")
arcpy.AddMessage("\t Procesados {0} registros.\n".format(contarregistros('Hidrografia\Isla')))
#### End_Hidrografia


#### IndiceMapas
arcpy.AddMessage("{0} Dataset Indice Mapas... ".format(hasht))
## Indice Mapas
arcpy.AddMessage("{0} Indice Hoja Carto:".format(arrow))
arcpy.CalculateField_management(in_table='IndiceMapas\Indice', field="RuleID", expression="1", expression_type="VB", code_block="")
arcpy.AddMessage("\t Procesados {0} registros.\n".format(contarregistros('IndiceMapas\Indice')))

#### End_IndiceMapas


#### InfraestructuraServicios
arcpy.AddMessage("{0} Dataset Infraestructura Servicios... ".format(hasht))
## Red alta tension:
arcpy.AddMessage("{0} Red alta tension:".format(arrow))
arcpy.CalculateField_management(in_table='InfraestructuraServicios\RATens', field="RuleID", expression="1", expression_type="VB", code_block="")
arcpy.AddMessage("\t Procesados {0} registros.\n".format(contarregistros('InfraestructuraServicios\RATens')))


## Red alta tensiÃ³n:
arcpy.AddMessage("{0} Tapa servicio publico:".format(arrow))
arcpy.CalculateField_management(in_table='InfraestructuraServicios\TSPubl', field="RuleID", expression="1", expression_type="VB", code_block="")
arcpy.AddMessage("\t Procesados {0} registros.\n".format(contarregistros('InfraestructuraServicios\TSPubl')))


## Pozo:
arcpy.AddMessage("{0} Pozo:".format(arrow))
arcpy.CalculateField_management(in_table='InfraestructuraServicios\Pozo', field="RuleID", expression="1", expression_type="VB", code_block="")
arcpy.AddMessage("\t Procesados {0} registros.\n".format(contarregistros('InfraestructuraServicios\Pozo')))

## Punto distribucion:
arcpy.AddMessage("{0} Punto Distribucion:".format(arrow))
arcpy.CalculateField_management(in_table='InfraestructuraServicios\PDistr', field="RuleID", expression="calcular_Rule( !PDTipo! , !RuleID! )", expression_type="PYTHON_9.3", code_block="def calcular_Rule(x,r):\n if r is None:\n  return x\n else:\n  return r")
arcpy.CalculateField_management(in_table='InfraestructuraServicios\PDistr', field="PDTipo", expression="calcular_Rule( !PDTipo! , !RuleID! )", expression_type="PYTHON_9.3", code_block="def calcular_Rule(x,r):\n return r")
arcpy.AddMessage("\t Procesados {0} registros.\n".format(contarregistros('InfraestructuraServicios\PDistr')))

#### End_InfraestructuraServicios


#### NombresGeograficos
arcpy.AddMessage("{0} Dataset Nombres Geograficos... ".format(hasht))
## Nombre geografico:
arcpy.AddMessage("{0} Nombre geografico:".format(arrow))
arcpy.CalculateField_management(in_table='NombresGeograficos\NGeogr', field="RuleID", expression="calcular_Rule( !NGSubcateg! , !RuleID! )", expression_type="PYTHON_9.3", code_block="def calcular_Rule(x,r):\n if r is None:\n  return x\n else:\n  return r")
arcpy.CalculateField_management(in_table='NombresGeograficos\NGeogr', field="NGCategori", expression="calcular_Rule( !NGSubcateg! , !RuleID! )", expression_type="PYTHON_9.3", code_block="def calcular_Rule(x,r):\n if r in (15,16,17,18):\n  return 11\n else:\n  return r")
arcpy.AddMessage("\t Procesados {0} registros.\n".format(contarregistros('NombresGeograficos\NGeogr')))

#### End_NombresGeograficos

#### Transpoorte
arcpy.AddMessage("{0} Dataset Transporte... ".format(hasht))
## Puente_P:
arcpy.AddMessage("{0} Puente_P:".format(arrow))
arcpy.CalculateField_management(in_table='Transporte\Puente_P', field="RuleID", expression="calcular_Rule( !PuFuncion! , !RuleID! )", expression_type="PYTHON_9.3", code_block="def calcular_Rule(x,r):\n if r is None:\n  return x\n else:\n  return r")
arcpy.CalculateField_management(in_table='Transporte\Puente_P', field="PuFuncion", expression="calcular_Rule( !PuFuncion! , !RuleID! )", expression_type="PYTHON_9.3", code_block="def calcular_Rule(x,r):\n return r")
arcpy.AddMessage("\t Procesados {0} registros.\n".format(contarregistros('Transporte\Puente_P')))


## Puente_L:
arcpy.AddMessage("{0} Puente_L:".format(arrow))
arcpy.CalculateField_management(in_table='Transporte\Puente_L', field="RuleID", expression="calcular_Rule( !PuFuncion! , !RuleID! )", expression_type="PYTHON_9.3", code_block="def calcular_Rule(x,r):\n if r is None:\n  return x\n else:\n  return r")
arcpy.CalculateField_management(in_table='Transporte\Puente_L', field="PuFuncion", expression="calcular_Rule( !PuFuncion! , !RuleID! )", expression_type="PYTHON_9.3", code_block="def calcular_Rule(x,r):\n return r")
arcpy.AddMessage("\t Procesados {0} registros.\n".format(contarregistros('Transporte\Puente_L')))

## Via:
arcpy.AddMessage("{0} Via:".format(arrow))
#Los campos "RuleID" y "VTipo" deben ser iguales:
arcpy.CalculateField_management(in_table='Transporte\Via', field="RuleID", expression="calcular_Rule( !VTipo! , !RuleID! )", expression_type="PYTHON_9.3", code_block="def calcular_Rule(x,r):\n if r is None:\n  return x\n else:\n  return r")
arcpy.CalculateField_management(in_table='Transporte\Via', field="VTipo", expression="calcular_Rule( !VTipo! , !RuleID! )", expression_type="PYTHON_9.3", code_block="def calcular_Rule(x,r):\n return r")

#Si el campo "Vtipo" es â€œVia Primaria", el campo "Vestado" debe ser "Pavimentada", el campo "Vcarril" debe ser " Carretera de 2 o mÃ¡s carriles" y el campo "Vacceso" debe ser "Permanente":
arcpy.CalculateField_management(in_table="Transporte\Via", field="VEstado", expression="calculoa( !VTipo! , !VEstado! )", expression_type="PYTHON_9.3", code_block="def calculoa(vtipo,vestado):\n if str(vtipo) ==1:\n  return 1\n else:\n  return vestado\n")
arcpy.CalculateField_management(in_table="Transporte\Via", field="VCarril", expression="calculob( !VTipo! , !VEstado! , !VCarril! )", expression_type="PYTHON_9.3", code_block='def calculob(vtipo,vestado,vcarril):\n if str(vtipo) =="1" and str(vestado)=="1":\n  return 1\n else:\n  return vcarril')
arcpy.CalculateField_management(in_table="Transporte\Via", field="VAcceso", expression="calculoc( !VTipo! , !VEstado! , !VCarril!, !VAcceso! )", expression_type="PYTHON_9.3", code_block='def calculoc(vtipo,vestado,vcarril,vacceso):\n if str(vtipo) =="1" and str(vestado)=="1" and str(vcarril)=="1":\n  return 1\n else:\n  return vacceso')
arcpy.CalculateField_management(in_table="Transporte\Via", field="VAcceso", expression="calculoc( !VTipo! , !VEstado! , !VCarril!, !VAcceso! )", expression_type="PYTHON_9.3", code_block='def calculoc(vtipo,vestado,vcarril,vacceso):\n if str(vtipo) =="1" and str(vestado)=="1" and str(vcarril)=="1":\n  return 1\n else:\n  return vacceso')

#Si el campo "Vtipo" es â€œVia Secundaria", el campo "Vestado" debe ser "Pavimentada" o "Sin Pavimentar", el campo "Vcarril" debe ser " Carretera angosta" y el campo "Vacceso" debe ser "Permanente"
arcpy.CalculateField_management(in_table="Transporte\Via", field="VEstado", expression="calculod( !VTipo! , !VEstado! )", expression_type="PYTHON_9.3", code_block='def calculod(vtipo,vestado):\n if str(vtipo) =="2":\n  if str(vestado) =="1" or str(vestado) =="2":\n   return vestado\n  else: \n   return 1\n else:\n  return vestado')
arcpy.CalculateField_management(in_table="Transporte\Via", field="VCarril", expression="calculoe( !VTipo! , !VEstado!, !VCarril! )", expression_type="PYTHON_9.3", code_block='def calculoe(vtipo,vestado,vcarril):\n if str(vtipo) =="2" and (str(vestado) =="1" or str(vestado) =="2"):\n  return 2\n else: \n  return vcarril')
arcpy.CalculateField_management(in_table="Transporte\Via", field="VAcceso", expression="calculof( !VTipo! , !VEstado!, !VCarril!, !VAcceso!)", expression_type="PYTHON_9.3", code_block='def calculof(vtipo,vestado,vcarril,vacceso):\n if str(vtipo) =="2" and (str(vestado) =="1" or str(vestado) =="2") and str(vcarril)=="2":\n  return 1\n else: \n  return vacceso')

#Si el campo "Vtipo" es â€œVia terciaria", el campo "Vestado" debe ser "Sin Pavimentar" o "sin afirmado", el campo "Vcarril" debe ser " sin valor" y el campo "Vacceso" debe ser "temporal"
arcpy.CalculateField_management(in_table="Transporte\Via", field="VEstado", expression="calculog( !VTipo! , !VEstado!)", expression_type="PYTHON_9.3", code_block='def calculog(vtipo,vestado):\n if str(vtipo) =="3" and (str(vestado) =="2" or str(vestado) =="3"):\n  return vestado\n else: \n  return 2')
arcpy.CalculateField_management(in_table="Transporte\Via", field="VCarril", expression="calculoh( !VTipo! , !VEstado!, !VCarril! )", expression_type="PYTHON_9.3", code_block='def calculoh(vtipo,vestado, vcarril):\n if str(vtipo) =="3" and (str(vestado) =="2" or str(vestado) =="3"):\n  return 0\n else: \n  return vcarril')
arcpy.CalculateField_management(in_table="Transporte\Via", field="VAcceso", expression="calculoi( !VTipo! , !VEstado!, !VAcceso! )", expression_type="PYTHON_9.3", code_block='def calculoi(vtipo,vestado, vacceso):\n if str(vtipo) =="3" and (str(vestado) =="2" or str(vestado) =="3"):\n  return 2\n else: \n  return vacceso')

#Si el campo "Vtipo" es â€œPlaca Huella", el campo "Vestado" debe ser "en construccion", el campo "Vcarril" debe ser " sin valor" y el campo "Vacceso" debe ser "temporal":
arcpy.CalculateField_management(in_table="Transporte\Via", field="VEstado", expression="calculoi( !VTipo! , !VEstado!)", expression_type="PYTHON_9.3", code_block='def calculoi(vtipo,vestado):\n if str(vtipo) =="4" :\n  return 4\n else: \n  return vestado')
arcpy.CalculateField_management(in_table="Transporte\Via", field="VCarril", expression="calculoj( !VTipo! , !VCarril!)", expression_type="PYTHON_9.3", code_block='def calculoj(vtipo, vcarril):\n if str(vtipo) =="4" :\n  return 0\n else: \n  return vcarril')
arcpy.CalculateField_management(in_table="Transporte\Via", field="VAcceso", expression="calculok( !VTipo! , !VAcceso!)", expression_type="PYTHON_9.3", code_block='def calculok(vtipo, vacceso):\n if str(vtipo) =="4" :\n  return 2\n else: \n  return vacceso')

#Si el campo "Vtipo" es â€œcamino, sendero", el campo "Vestado" debe ser " sin valor", el campo "Vcarril" debe ser " sin valor" y el campo "Vacceso" debe ser "sin valor"
arcpy.CalculateField_management(in_table="Transporte\Via", field="VEstado", expression="calculol( !VTipo! , !VEstado!)", expression_type="PYTHON_9.3", code_block='def calculol(vtipo, vestado):\n if str(vtipo) =="5" :\n  return 0\n else: \n  return vestado')
arcpy.CalculateField_management(in_table="Transporte\Via", field="VCarril", expression="calculom( !VTipo! , !VCarril!)", expression_type="PYTHON_9.3", code_block='def calculom(vtipo, vcarril):\n if str(vtipo) =="5" :\n  return 0\n else: \n  return vcarril')
arcpy.CalculateField_management(in_table="Transporte\Via", field="VAcceso", expression="calculok( !VTipo! , !VAcceso!)", expression_type="PYTHON_9.3", code_block='def calculok(vtipo, vacceso):\n if str(vtipo) =="5" :\n  return 0\n else: \n  return vacceso')

#Si el campo "Vtipo" es â€œvÃ­a peatonal", el campo "Vestado" debe ser " sin valor", el campo "Vcarril" debe ser " sin valor" y el campo "Vacceso" debe ser "sin valor":
arcpy.CalculateField_management(in_table="Transporte\Via", field="VEstado", expression="calculon( !VTipo! , !VEstado!)", expression_type="PYTHON_9.3", code_block='def calculon(vtipo, vestado):\n if str(vtipo) =="6" :\n  return 0\n else: \n  return vestado')
arcpy.CalculateField_management(in_table="Transporte\Via", field="VCarril", expression="calculoo( !VTipo! , !VCarril!)", expression_type="PYTHON_9.3", code_block='def calculoo(vtipo, vcarril):\n if str(vtipo) =="6" :\n  return 0\n else: \n  return vcarril')
arcpy.CalculateField_management(in_table="Transporte\Via", field="VAcceso", expression="calculop( !VTipo! , !VAcceso!)", expression_type="PYTHON_9.3", code_block='def calculop(vtipo, vacceso):\n if str(vtipo) =="6" :\n  return 0\n else: \n  return vacceso')
arcpy.AddMessage("\t Procesados {0} registros.\n".format(contarregistros('Transporte\Via')))

## Via ferrea:
arcpy.AddMessage("{0} Via Ferrea:".format(arrow))
arcpy.CalculateField_management(in_table='Transporte\VFerre', field="RuleID", expression="calcular_Rule( !VFTipo! , !RuleID! )", expression_type="PYTHON_9.3", code_block="def calcular_Rule(x,r):\n if r is None:\n  return x\n else:\n  return r")
arcpy.CalculateField_management(in_table='Transporte\VFerre', field="VFTipo", expression="calcular_Rule( !VFTipo! , !RuleID! )", expression_type="PYTHON_9.3", code_block="def calcular_Rule(x,r):\n return r")
arcpy.AddMessage("\t Procesados {0} registros.\n".format(contarregistros('Transporte\VFerre')))

## Tunel:
arcpy.AddMessage("{0} Tunel:".format(arrow))
arcpy.CalculateField_management(in_table='Transporte\Tunel', field="RuleID", expression="1", expression_type="VB", code_block="")
arcpy.AddMessage("\t Procesados {0} registros.\n".format(contarregistros('Transporte\Tunel')))

## SVial:
arcpy.AddMessage("{0} Separador Vial:".format(arrow))
arcpy.CalculateField_management(in_table='Transporte\SVial', field="RuleID", expression="1", expression_type="VB", code_block="")
arcpy.AddMessage("\t Procesados {0} registros.\n".format(contarregistros('Transporte\SVial')))

## Limite via:
arcpy.AddMessage("{0} Limite via:".format(arrow))
arcpy.CalculateField_management(in_table='Transporte\LVia', field="RuleID", expression="calcular_Rule( !LVTipo! , !RuleID! )", expression_type="PYTHON_9.3", code_block="def calcular_Rule(x,r):\n if r is None:\n  return x\n else:\n  return r")
arcpy.CalculateField_management(in_table='Transporte\LVia', field="LVTipo", expression="calcular_Rule( !LVTipo! , !RuleID! )", expression_type="PYTHON_9.3", code_block="def calcular_Rule(x,r):\n return r")
arcpy.AddMessage("\t Procesados {0} registros.\n".format(contarregistros('Transporte\LVia')))

## Cicloruta:
arcpy.AddMessage("{0} Cicloruta:".format(arrow))
arcpy.CalculateField_management(in_table='Transporte\Ciclor', field="RuleID", expression="1", expression_type="VB", code_block="")
arcpy.AddMessage("\t Procesados {0} registros.\n".format(contarregistros('Transporte\Ciclor')))
#### End_Transporte


#### Vivienda, Ciudad y Territorio
arcpy.AddMessage("{0} Dataset Vivienda Ciudad Territorio... ".format(hasht))
## Construccion P:
arcpy.AddMessage("{0} Construccion_P:".format(arrow))
arcpy.CalculateField_management(in_table='ViviendaCiudadTerritorio\Constr_P', field="RuleID", expression="calcular_Rule( !CTipo!, !RuleID! )", expression_type="PYTHON_9.3", code_block="def calcular_Rule(x,r):\n if r is None:\n  return x\n else:\n  return r")
arcpy.CalculateField_management(in_table='ViviendaCiudadTerritorio\Constr_P', field="CTipo", expression="calcular_Rule( !CTipo!, !RuleID! )", expression_type="PYTHON_9.3", code_block="def calcular_Rule(x,r):\n return r")

# Si campo "Ctipo" es "convencional"(2), el campo "Ccategor" debe ser "Residencial", "Comercial", "Industrial", "Educativo", "Institucional", "Recreacional" o "Religioso". En caso de no, se asigna Residencial:
arcpy.CalculateField_management(in_table='ViviendaCiudadTerritorio\Constr_P', field="CCategor", expression="calculoq( !CTipo!, !CCategor! )", expression_type="PYTHON_9.3", code_block='def calculoq(tipo,categor):\n if str(tipo) == "2":\n  if str(categor) not in ("1","2","3","4","5","6","7","17"):\n   return 1\n else: \n  return categor')

# Si campo "Ctipo" es "No convencional", el campo "Ccategor" debe ser "Agropecuario", "Enramada, cobertizo o caney", "GalpÃ³n y gallinero", "Establo y pesebrera", "Cochera, marranera y porqueriza", "Tanque", "Secadero", "Minero", "Cementerio o parque cementerio" u " Otra construcciÃ³n".  En caso de no, se asigna OtraConstruccion (17):
arcpy.CalculateField_management(in_table='ViviendaCiudadTerritorio\Constr_P', field="CCategor", expression="calculor( !CTipo!, !CCategor! )", expression_type="PYTHON_9.3", code_block='def calculor(tipo,categor):\n if str(tipo) == "1":\n  if str(categor) not in ("8","13","14","15","9","10","11","12","16","17"):\n   return 17\n else: \n  return categor')
arcpy.AddMessage("\t Procesados {0} registros.\n".format(contarregistros('ViviendaCiudadTerritorio\Constr_P')))

## Cerca:
arcpy.AddMessage("{0} Cerca:".format(arrow))
arcpy.CalculateField_management(in_table='ViviendaCiudadTerritorio\Cerca', field="RuleID", expression="calcular_Rule( !CeTipo!, !RuleID! )", expression_type="PYTHON_9.3", code_block="def calcular_Rule(x,r):\n if r is None:\n  return x\n else:\n  return r")
arcpy.CalculateField_management(in_table='ViviendaCiudadTerritorio\Cerca', field="CeTipo", expression="calcular_Rule( !CeTipo!, !RuleID! )", expression_type="PYTHON_9.3", code_block="def calcular_Rule(x,r):\n return r")
arcpy.AddMessage("\t Procesados {0} registros.\n".format(contarregistros('ViviendaCiudadTerritorio\Cerca')))

## Piscina:
arcpy.AddMessage("{0} Piscina:".format(arrow))
arcpy.CalculateField_management(in_table='ViviendaCiudadTerritorio\Piscin', field="RuleID", expression="1", expression_type="VB", code_block="")
arcpy.AddMessage("\t Procesados {0} registros.\n".format(contarregistros('ViviendaCiudadTerritorio\Piscin')))

## Zona dura:
arcpy.AddMessage("{0} Zona dura:".format(arrow))
arcpy.CalculateField_management(in_table='ViviendaCiudadTerritorio\ZDura', field="RuleID", expression="1", expression_type="VB", code_block="")
arcpy.AddMessage("\t Procesados {0} registros.\n".format(contarregistros('ViviendaCiudadTerritorio\ZDura')))
#### End_Vivienda, Ciudad y Territorio


edit.stopOperation()
edit.stopEditing(True)

arcpy.AddMessage("{0}{0}{0} Sesion de edicion cerrada. El proceso ha finalizado con exito... ".format(hasht))



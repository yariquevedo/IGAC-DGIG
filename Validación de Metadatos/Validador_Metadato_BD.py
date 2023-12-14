from arcpy import metadata as md
import arcpy
import os
import xml.etree.ElementTree as ET
from datetime import datetime
from lxml import etree


####### Definicion funciones:
def tiempo_actual():
    hora_actual = datetime.now()
    return str(hora_actual.hour)+str(hora_actual.minute)+str(hora_actual.hour)

#Crear GDB:
def crearGDB(path):
    GDB_output= arcpy.CreateFileGDB_management(out_folder_path=path,out_name='GDB_salida'+str(tiempo_actual()))
    return GDB_output

#Funcion que retorna datos del XML
def getdata_from_xml(atributo):
    global tree
    tofind= (str('.//{http://www.isotc211.org/2005/gmd}'+str(atributo)))
    x_element= tree.find(tofind)
    value_element=x_element.find(".//{http://www.isotc211.org/2005/gco}CharacterString").text
    return value_element

#Funcion para validar exactitud de diligenciamiento en valores de las etiquetas del xml: 
def validar_param(nombreetiqueta, valorabuscar, idregla):
    error=0
    x=getdata_from_xml(nombreetiqueta)
    if not str(valorabuscar).replace(" ","").replace("\n","")== str(x).replace(" ","").replace("\n",""):
        error+=1
    else:
        error=0
    if error>0:
        row_values = [(idregla,nombreetiqueta, 'No corresponde al valor del metadato establecido.')]
        with arcpy.da.InsertCursor(summary, ['id_validacion', 'etiqueta', 'observacion']) as cursor:
            for row in row_values:
                cursor.insertRow(row)
    return 1


####Inputs:
layer= arcpy.GetParameterAsText(0)
#layer= "E:\\22_IGAC\\2. Proyectos\\3. Desarrollos\\8. Validacion_Metadatos\\Insumos\\ORTO_METADATO_CONSOLIDADO\\Orto10_25438003_20211001.tif"
folder_output= arcpy.GetParameterAsText(1)
#folder_output= "E:\\22_IGAC\\2. Proyectos\\3. Desarrollos\\8. Validacion_Metadatos\\Desarrollo\\Salida"
revision_metadatos_igac=arcpy.GetParameter(2)

###### Ejecución desarrollo:
item_md = md.Metadata(layer)   # Se cargan los metadatos
"""
print("Tags:", item_md.tags)
print("Summary:", item_md.summary)
print("Description:", item_md.description)
print("Credits:", item_md.credits)
print("Access Constraints:", item_md.accessConstraints)
""" 

##Exportar metadato de capa deseada a XML en formato GML32:
#exported_xml= os.path.join(folder_output, 'xml_gml_32.xml')
exported_xml= os.path.join(folder_output, 'xml'+str(os.path.basename(layer)).replace(".","_"))
item_md.exportMetadata(exported_xml, 'ISO19139_GML32')



###################################################
###############Inicio de validaciones##############: 
###################################################

#Se crea tabla que contendrá el resumen y sus respectivos campos:

gdb=crearGDB(folder_output)
summary=arcpy.CreateTable_management(out_path=gdb, out_name='summary')
arcpy.management.AddField(in_table=summary, field_name='id_validacion', field_type="TEXT")
arcpy.management.AddField(in_table=summary, field_name='etiqueta', field_type="TEXT")
arcpy.management.AddField(in_table=summary, field_name='observacion', field_type="TEXT")

### Navegar sobre XML:
tree = etree.parse(exported_xml)

#print(getdata_from_xml("CI_Telephone"))
#print(getdata_from_xml("keyword"))
#print(getdata_from_xml("electronicMailAddress"))

################ INICIO VALIDACION #####################
date_format = '%Y%m%d'

##1. fileIdentifier:   Orto10_Metadato_25438003_20210110
error=0
print(getdata_from_xml("fileIdentifier"))
x=getdata_from_xml("fileIdentifier")
if not str(x).startswith('Carto') or ('Metadato') not in x:
    error+=1
else:
    error=0 
try:
   dateObject = datetime.strptime(x[-8:], date_format)
   print(dateObject)
except ValueError:
    error+=1
    print("Incorrect data format, should be YYYYMMDD")

if error>0:
    row_values = [('1','fileidentifier', 'No cumple con la estructura')]
    with arcpy.da.InsertCursor(summary, ['id_validacion', 'etiqueta', 'observacion']) as cursor:
        for row in row_values:
            cursor.insertRow(row)

if revision_metadatos_igac is True:      
    ##2. organisationName. Instituto Geográfico Agustín Codazzi
    validar_param('organisationName','Instituto Geográfico Agustín Codazzi','2')

    ##3. organisationName. Subdirección Cartográfica y Geodésica
    validar_param('positionName','Subdirección Cartográfica y Geodésica','3')

    ##4. CI_Telephone. +57 (601) 6531888
    validar_param('CI_Telephone','+57 (601) 6531888','4')

    ##5. deliveryPoint. Carrera 30 # 48 - 51 – Sede Central
    validar_param('deliveryPoint','Carrera 30 # 48 - 51 – Sede Central','5')

    ##6. city. Bogotá
    validar_param('city','Bogotá D.C','6')

    ##7. administrativeArea. Cundinamarca
    validar_param('administrativeArea','Cundinamarca','7')

    ##8. postalCode. 111321
    validar_param('postalCode','111321','8')

    ##9. electronicMailAddress. contactenos@igac.gov.co
    validar_param('electronicMailAddress','contactenos@igac.gov.co','9')

    ##10. contactInstructions. texto
    validar_param('contactInstructions','Abierto al público de lunes a viernes de 9:00 a.m. a 4:00 p.m. jornada continua Sede Central y territorial Cundinamarca','10')

else: 
    pass
##11. metadataStandardName. texto
validar_param('metadataStandardName','ISO 19139 Geographic Information - Metadata - Implementation Specification','11')

"""
##11b. pointInPixel. texto
error=0
md_pixel_orientation_code = tree.find(".//pointInPixel/MD_PixelOrientationCode")
if md_pixel_orientation_code is not None:
    valor = md_pixel_orientation_code.text
    if valor =="center":
        pass
    else:
        error+=1
    print("Valor de MD_PixelOrientationCode:", valor)
else:
    print("MD_PixelOrientationCode no encontrado en el XML")

if error>0:
    row_values = [('11b','PointInPixel', 'No es igual a: center')]
    with arcpy.da.InsertCursor(summary, ['id_validacion', 'etiqueta', 'observacion']) as cursor:
        for row in row_values:
            cursor.insertRow(row)
"""
##12. title:   Ortoimagen. Departamento de XXX. Municipio de XXXXX. GSD XXX cm. Año XXXX
error=0
x=getdata_from_xml("title")

if not str(x).startswith('Cartografía Básica Digital. Departamento de ') or ('. Municipio de ' not in x)  or ('. Escala ' not in x) or ('. Año ' not in x):
    error+=1
else:
    error=0

if error>0:
    row_values = [('12','title', 'No cumple con la estructura')]
    with arcpy.da.InsertCursor(summary, ['id_validacion', 'etiqueta', 'observacion']) as cursor:
        for row in row_values:
            cursor.insertRow(row)

##13. alternateTitle:   Orto10_25740013_20230823
error=0
x=getdata_from_xml("alternateTitle")
if not str(x).startswith('Carto') or ('_' not in x):
    error+=1
else:
    error=0

if error>0:
    row_values = [('13','alternateTitle', 'No cumple con la estructura')]
    with arcpy.da.InsertCursor(summary, ['id_validacion', 'etiqueta', 'observacion']) as cursor:
        for row in row_values:
            cursor.insertRow(row)


##14. date:   2023-01-05T08:05:56
# Encuentra la etiqueta <gco:DateTime>
gco_datetime = tree.find('.//{http://www.isotc211.org/2005/gco}DateTime')
if gco_datetime is not None:
    datetime_value = gco_datetime.text
else:
    datetime_value=''

date_format = '%Y-%m-%d'
error=0
x=datetime_value
if 'T' not in x:
    error+=1
else:
    error=0
try:
   dateObject = datetime.strptime(x[0:10], date_format)
   print(dateObject)
except ValueError:
    error+=1
    print("Incorrect data format, should be YYYY-MM-DD")

if error>0:
    row_values = [('14','date', 'No cumple con la estructura')]
    with arcpy.da.InsertCursor(summary, ['id_validacion', 'etiqueta', 'observacion']) as cursor:
        for row in row_values:
            cursor.insertRow(row)


##15. abstract:
error=0
x=getdata_from_xml("abstract")
if 'Producto cartográfico básico a escala ' not in str(x) or ' que contiene: a) Elementos altimétricos, los cuales se obtienen a partir de procesos fotogramétricos o técnicas de interferometría. Intervalo básico de curvas de nivel intermedias cada ' not in x or ' metros. Curvas de nivel índice cada' not in x or ' metros. b) Elementos planimétricos, obtenidos desde procesos fotogramétricos o fotointerpretación, los cuales son estructurados en una base de datos en formato Geodatabase, conforme al modelo de datos vigente de producción cartográfica. Se captura los elementos para la escala de carácter permanente, hasta el límite determinado para el proyecto.' not in x or ' El ' not in x or ', tiene un cubrimiento aproximado de ' not in x or ' d) El proceso se realizó con ' not in x or '. Compilación toponímica insumo de: ' not in x: 
    error+=1
else:
    error=0

if error>0:
    row_values = [('15','abstract', 'No cumple con la estructura')]
    with arcpy.da.InsertCursor(summary, ['id_validacion', 'etiqueta', 'observacion']) as cursor:
        for row in row_values:
            cursor.insertRow(row)


##16. purpose:
error=0
x=getdata_from_xml("purpose")
if not str(x).startswith('La información contenida en este producto permite georreferenciar con precisión los elementos espaciales para múltiples aplicaciones de tipo temático entre ellas: diseño y establecimiento de redes de servicios públicos, obras civiles urbanas, determinación de secciones para la organización política administrativa del municipio. Así mismo, se utiliza como base para la implementación de Sistemas de Información Geográfica para la planificación y gestión a nivel municipal.'):
    error+=1
else:
    error=0

if error>0:
    row_values = [('16','purpose', 'No cumple con la estructura')]
    with arcpy.da.InsertCursor(summary, ['id_validacion', 'etiqueta', 'observacion']) as cursor:
        for row in row_values:
            cursor.insertRow(row)



##17. keyword:
# error=0
# x=getdata_from_xml("keyword")
# if not str(x).startswith('Cartografía Básica Digital, República de Colombia') or ' Departamento de ' not in x: 
#     error+=1
# else:
#     error=0

# if error>0:
#     row_values = [('17','keyword', 'No cumple con la estructura')]
#     with arcpy.da.InsertCursor(summary, ['id_validacion', 'etiqueta', 'observacion']) as cursor:
#         for row in row_values:
#             cursor.insertRow(row)



##18. useLimitation:
error=0
x=getdata_from_xml("useLimitation")
if not str(x).startswith('Producto generado para cálculo de áreas y longitudes de acuerdo a la escala de precisión de generación, sin embargo, no se recomienda generación de nuevos productos de carácter temática de mayor precisión a este ya que puede presentar valores inconsistentes.'): 
    error+=1
else:
    error=0

if error>0:
    row_values = [('18','useLimitation', 'No cumple con la estructura')]
    with arcpy.da.InsertCursor(summary, ['id_validacion', 'etiqueta', 'observacion']) as cursor:
        for row in row_values:
            cursor.insertRow(row)


##19. statement:
error=0
x=getdata_from_xml("statement")
if 'La calidad se valida a los elementos contenidos en la base de datos cartográficos del proyecto ' not in str(x) or '; el aseguramiento de la calidad se valida al 100% de los elementos contenidos a la base de datos geográficos. ' not in x or ', tiene un área de ' not in x or ' hectáreas. Se verificó el cumplimiento de los parámetros de calidad definidos en la especificación 471-2020 / 529-2020 / 197-2022, en los siguientes elementos y subelementos de calidad, determinándose que el sistema de referencia cumple ya que tiene asignado el sistema de referencia MAGNA-SIRGAS Origen-Nacional, el esquema de la base de datos cumple con el esquema IGAC, así mismo cumple con los parámetros de calidad de Totalidad (omisión, comisión), Consistencia Lógica (Topológica, conceptual o de formato y de dominio), Exactitud Temática (Clasificación de elementos, exactitud atributos cualitativos y atributos cuantitativos) y Exactitud Temporal. Posterior se realizó el proceso de validación en el cual se pudo determinar el cumplimiento de estos parámetros; lo cual permitió dar el concepto de APROBADO.' not in x:
    error+=1
else:
    error=0

if error>0:
    row_values = [('19','statement', 'No cumple con la estructura')]
    with arcpy.da.InsertCursor(summary, ['id_validacion', 'etiqueta', 'observacion']) as cursor:
        for row in row_values:
            cursor.insertRow(row)

"""
##20. cornerPoints:
error=0

# Buscar todas las etiquetas <gml:pos>
pos_elements = tree.findall(".//gml:pos", namespaces={"gml": "http://www.opengis.net/gml"})

# Obtener los valores de <gml:pos>
for pos_element in pos_elements:
    value = pos_element.text.strip()  # Obtener el texto dentro de la etiqueta
    arcpy.AddMessage("Valor de <gml:pos>:", value)


##21. tranformationDimesionDecription. Transformación Bilienal
#validar_param('tranformationDimesionDecription','Transformación Bilienal','21')
"""


##22. code. Transformación Bilienal
validar_param('code','9377','22')


##23. MD_format.
error=0
md_format_element = tree.find(".//MD_Format")
if md_format_element is not None:
    md_format_element = md_format_element.text
    arcpy.AddMessage ("md_format:"+ str(md_format_element))
    if "GeoDatabase (File Geodatabase)"  in md_format_element:
        error=0
    else:
        error+=1
else: 
    error=0

if error>0:
    row_values = [('23','MD_Format', 'No cumple con la estructura')]
    with arcpy.da.InsertCursor(summary, ['id_validacion', 'etiqueta', 'observacion']) as cursor:
        for row in row_values:
            cursor.insertRow(row)

"""
##24. distance:
distance_element = tree.find('.//{http://www.isotc211.org/2005/gco}Distance')
if distance_element is not None:
    # Obtiene el valor y la unidad del atributo "uom"
    distance_value = distance_element.text
    uom = distance_element.get("uom")
    if distance_value==0 or  len(distance_value)==0 or  distance_value is None:
        error+=1
    else:
        error=0
if error>0:
    row_values = [('24','distance', 'Distancia incorrecta')]
    with arcpy.da.InsertCursor(summary, ['id_validacion', 'etiqueta', 'observacion']) as cursor:
        for row in row_values:
            cursor.insertRow(row)
if distance_element is not None:
    # Obtiene el valor y la unidad del atributo "uom"
    distance_value = distance_element.text
    uom = distance_element.get("uom")
    if uom==0 or  len(uom)==0 or uom is None:
        error+=1
    else: 
        error=0
if error>0:
    row_values = [('24','distance', 'Unidad de medida incorrecta')]
    with arcpy.da.InsertCursor(summary, ['id_validacion', 'etiqueta', 'observacion']) as cursor:
        for row in row_values:
            cursor.insertRow(row)
"""
            
arcpy.TableToExcel_conversion(summary, os.path.join(folder_output, 'ValidacionMetadato_'+str(tiempo_actual())+'_'+str(os.path.basename(exported_xml)).replace(".","_")+'.xlsx'))
try:
    arcpy.Delete_management(gdb)
except:
    pass
finally:
    pass
    #arcpy.Delete_management(exported_xml)
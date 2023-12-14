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
if not str(x).startswith('Orto') or ('Metadato' not in x):
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
    validar_param('city','Bogotá','6')

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


##12. title:   Ortoimagen. Departamento de XXX. Municipio de XXXXX. GSD XXX cm. Año XXXX
error=0
x=getdata_from_xml("title")

if not str(x).startswith('Ortoimagen. Departamento de ') or ('. Municipio de ' not in x)  or ('. GSD ' not in x) or (' cm. Año ' not in x):
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
if not str(x).startswith('Orto') or ('_' not in x):
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
if 'de imágenes ortorectificadas provenientes del sensor ' not in str(x) or 'a las cuales se les aplicó un proceso de balance radiométrico y edición de líneas de costura, garantizando la continuidad cromática y geométrica de los elementos. Este producto contiene información ' not in x or 'epartamento de' not in x or ', República de Colombia. Tiene un área de ' not in x or ' hectáreas. Cuenta con un GSD de ' not in x or 'aplicable para cartografía a escala 1:' not in x or ', los insumos ' not in x:
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
if not str(x).startswith('Servir como insumo básico para la realización de estudios suburbanos y rurales como levantamientos catastrales, planificación de ordenación y manejo ambiental, ordenamiento territorial, deslindes, análisis espacial, ruteo, entre otros.'):
    error+=1
else:
    error=0

if error>0:
    row_values = [('16','purpose', 'No cumple con la estructura')]
    with arcpy.da.InsertCursor(summary, ['id_validacion', 'etiqueta', 'observacion']) as cursor:
        for row in row_values:
            cursor.insertRow(row)



##17. keyword:
error=0
x=getdata_from_xml("keyword")
if not str(x).startswith('República de Colombia, Departamento de ') or ' Municipio de ' not in x: 
    error+=1
else:
    error=0

if error>0:
    row_values = [('17','keyword', 'No cumple con la estructura')]
    with arcpy.da.InsertCursor(summary, ['id_validacion', 'etiqueta', 'observacion']) as cursor:
        for row in row_values:
            cursor.insertRow(row)



##18. useLimitation:
error=0
x=getdata_from_xml("useLimitation")
if not str(x).startswith('Producto generado para escalas iguales o menores a escala 1:'): 
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
if not str(x).startswith('El aseguramiento de la calidad se realiza al 100% de los elementos contenidos en la Ortoimagen') or  'cual cuenta con un GSD de ' not in x or 'cm y un área ' not in x or ' hectáreas que cubre totalmente' not in x or 'Se verificó el cumplimiento de los parámetros de calidad definidos para ortoimágenes en las resoluciones 471-2020/529-2020/197-2022 en los siguientes elementos: totalidad, exactitud en posición, consistencia lógica, consistencia temporal y formato lo cual permitió dar el concepto de APROBADO' not in x: 
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

##23. attributeDescription. Niveles Digitales
error=0
record_type_element = tree.find('.//{http://www.isotc211.org/2005/gco}RecordType')
if record_type_element is not None:
    # Obtiene el valor de <gco:RecordType>
    record_type_value = record_type_element.text
    if "Niveles Digitales"  in record_type_value:
        error=0
    else:
        error+=1
else: 
    error+=1

if error>0:
    row_values = [('23','attributeDescription', 'No cumple con la estructura')]
    with arcpy.da.InsertCursor(summary, ['id_validacion', 'etiqueta', 'observacion']) as cursor:
        for row in row_values:
            cursor.insertRow(row)


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

arcpy.TableToExcel_conversion(summary, os.path.join(folder_output, 'ValidacionMetadato_'+str(tiempo_actual())+'_'+str(os.path.basename(layer)).replace(".","_")+'.xlsx'))
try:
    arcpy.Delete_management(gdb)
except:
    pass
finally:
    pass
    #arcpy.Delete_management(exported_xml)
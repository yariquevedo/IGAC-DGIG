# -*- #################
# ---------------------------------------------------------------------------
# Direccion de Gestion de Información Geografica
# Created on: 2023-07-02
# Created by: Gabriel Hernan Gonzalez Buitrago - Juan Pablo Merchán Puentes
# # Usage: Cuantificacion y generacion de reporte para Restitucion 
# Description:
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
import os,sys,arcinfo
from datetime import datetime
from arcpy.sa import *
import pandas as pd

# Script arguments
dgn_planimetria=arcpy.GetParameterAsText(0)
#dgn_planimetria= 'D:/22_IGAC/2. Proyectos/3. Desarrollos/7. Informe Lineas_Puntos_Restitucion/1_Insumos/LA PRIMAVERA_10K_P59_V8.dgn'
dgn_dtm=arcpy.GetParameterAsText(1)
#dgn_dtm= 'D:/22_IGAC/2. Proyectos/3. Desarrollos/7. Informe Lineas_Puntos_Restitucion/1_Insumos/LA PRIMAVERA_10K_P59_V8.dgn'
folder_output=arcpy.GetParameterAsText(2)
#folder_output='D:/22_IGAC/2. Proyectos/3. Desarrollos/7. Informe Lineas_Puntos_Restitucion/2_Desarrollo/Salida'
dgn_limite=arcpy.GetParameterAsText(3)
#dgn_limite= 'D:/22_IGAC/2. Proyectos/3. Desarrollos/7. Informe Lineas_Puntos_Restitucion/1_Insumos/LA PRIMAVERA_10K_P59_V8_LIMITE.dgn'
dgn_hueco=arcpy.GetParameterAsText(4)
#dgn_hueco= 'D:/22_IGAC/2. Proyectos/3. Desarrollos/7. Informe Lineas_Puntos_Restitucion/1_Insumos/LA PRIMAVERA_10K_P59_V8_HUECO_CARTOGRAFICO.dgn'
#PoligonoArea=arcpy.GetParameterAsText(5)
#######################################################################################
######################################################################
################################################################################
###########################################################################


arcpy.env.overwriteOutput=True
###################

# Showing templates
sep= '###################'
arrow= '-->'
hasht= '##'
longarrow='---->'
contadorDGN_importados=0

strShape=folder_output+os.sep+"Shape_p.shp"
strShape2=folder_output+os.sep+"Shape2.shp"
strTin=folder_output+os.sep+"Tin"
strRaster=folder_output+os.sep+"Raster.tif"
strRasterCorte=folder_output+os.sep+"RasterCorte.tif"
strSlope=folder_output+os.sep+"Slope.tif"
strReclass=folder_output+os.sep+"Reclass.tif"
strPoligono = folder_output +os.sep+ "Pol.shp"
strEliminate1 = folder_output+os.sep+ "Eliminate1.shp"
strEliminate2 = folder_output+os.sep+ "Eliminate2.shp"
strEliminate3 = folder_output+os.sep+ "Eliminate3.shp"
strEliminate4 = folder_output+os.sep+ "Eliminate4.shp"
strEliminate5 = folder_output+os.sep+ "Eliminate5.shp"
strEliminateF = folder_output+os.sep+ "EliminateF.shp"

RECLASIFICAR = "0.000000 3.000000 1; 3.000001 12.000000 2; 12.000001 9999999999.0000 3"

strDissolve=folder_output+os.sep+"Dissolve.shp"


def CalcularArea( Feat):
    try:
        arcpy.AddField_management(Feat,"AREA","DOUBLE")
    except:
        pass
    shapeName = arcpy.Describe(Feat).shapeFieldName
    rows = arcpy.UpdateCursor(Feat)
    for row in rows:
        geom=row.getValue(shapeName)
        row.AREA=geom.area
        rows.updateRow(row)
    del row
    del rows

def areaCorte(Feat):
    rows = arcpy.SearchCursor(Feat)
    AreaTotal=0
    for row in rows:
        AreaTotal=AreaTotal+row.AREA
    return AreaTotal




####### Definicion funciones:
def tiempo_actual():
    hora_actual = datetime.now()
    return str(hora_actual.hour)+str(hora_actual.minute)+str(hora_actual.hour)

#Crear GDB:
def crearGDB(path):
    GDB_output= arcpy.CreateFileGDB_management(out_folder_path=path,out_name='GDB_salida'+str(tiempo_actual()))
    return GDB_output

#Convertir CAD a GDB: 
def convertirCADtoGDB(CAD, GDB, dataset_name):
    arcpy.conversion.CADToGeodatabase(input_cad_datasets=CAD, out_gdb_path=GDB, out_dataset_name=dataset_name, reference_scale=1000, spatial_reference='PROJCS["MAGNA-SIRGAS_Origen-Nacional",GEOGCS["GCS_MAGNA",DATUM["D_MAGNA",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",5000000.0],PARAMETER["False_Northing",2000000.0],PARAMETER["Central_Meridian",-73.0],PARAMETER["Scale_Factor",0.9992],PARAMETER["Latitude_Of_Origin",4.0],UNIT["Meter",1.0]];-618700 -8436100 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision')

#Crear campos numericos de longitud:
def crear_campo_numerico(fc, name_field, alias):
    arcpy.AddField_management(in_table=fc, field_name=name_field, field_type="DOUBLE", field_alias=alias, field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED")

##Crear campos para calcular longitudes de polilineas en metros y decimetros:
def calculo_distancias (fc):
    global GDB_output
    crear_campo_numerico(os.path.join(str(GDB_output), "planimetria",'Polyline'), 'Longitud_m','Longitud_m')
    crear_campo_numerico(os.path.join(str(GDB_output), "planimetria",'Polyline'), 'Longitud_d','Longitud_dm')
    arcpy.management.CalculateGeometryAttributes(in_features=os.path.join(str(GDB_output), 'planimetria','Polyline'), geometry_property="Longitud_m LENGTH_3D;Longitud_d LENGTH_3D",length_unit="METERS", area_unit="", coordinate_system='PROJCS["MAGNA-SIRGAS_Origen-Nacional",GEOGCS["GCS_MAGNA",DATUM["D_MAGNA",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",5000000.0],PARAMETER["False_Northing",2000000.0],PARAMETER["Central_Meridian",-73.0],PARAMETER["Scale_Factor",0.9992],PARAMETER["Latitude_Of_Origin",4.0],UNIT["Meter",1.0]]',coordinate_format="SAME_AS_INPUT")
    arcpy.management.CalculateField(in_table=os.path.join(str(GDB_output), 'planimetria','Polyline'), field="Longitud_d", expression="!Longitud_d!/10", expression_type="PYTHON3", code_block="",field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")


##Exportar tabla a excel: 
def exportar_a_excel(table, outputfile):
    arcpy.conversion.TableToExcel( Input_Table=table, Output_Excel_File=outputfile, Use_field_alias_as_column_header="NAME", Use_domain_and_subtype_description="CODE" ) 

def crear_mapa_de_pendiente(GDB_output):      
    arcpy.AddMessage("{0}Generando mapa de pendientes...".format(arrow))
    #En el bloque de excepecion se crean el escenario para la funcionalidad conjunta de ambas partes: 
    #Control de cambios
    #arcpy.analysis.Clip()
    dataset=os.path.join(str(GDB_output), 'dtm')
    polyline=os.path.join(str(GDB_output), 'dtm','Polyline')
    
    limite_prueba =arcpy.conversion.FeatureClassToFeatureClass(polyline, out_path=dataset, out_name="Polyline_2", where_clause="Level NOT IN (60,61,62)")
    #clip_prueba=arcpy.Clip_analysis(polyline,limite_prueba)
    global contadorDGN_importado
    arcpy.AddMessage("van" +str(contadorDGN_importados))
    if contadorDGN_importados==0:
        tin=arcpy.ddd.CreateTin(
            out_tin=os.path.join(str(GDB_output), 'tin'),
            spatial_reference='PROJCS["MAGNA-SIRGAS_Origen-Nacional",GEOGCS["GCS_MAGNA",DATUM["D_MAGNA",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",5000000.0],PARAMETER["False_Northing",2000000.0],PARAMETER["Central_Meridian",-73.0],PARAMETER["Scale_Factor",0.9992],PARAMETER["Latitude_Of_Origin",4.0],UNIT["Meter",1.0]]',
            #in_features=r"'dtm\Polyline' Shape.Z Hard_Line <None>",
            in_features =arcpy.Clip_analysis(polyline,limite_prueba),
            constrained_delaunay="DELAUNAY"
        )
    elif contadorDGN_importados==1:
        tin=arcpy.ddd.CreateTin(
            out_tin=os.path.join(str(GDB_output), 'tin'),
            spatial_reference='PROJCS["MAGNA-SIRGAS_Origen-Nacional",GEOGCS["GCS_MAGNA",DATUM["D_MAGNA",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",5000000.0],PARAMETER["False_Northing",2000000.0],PARAMETER["Central_Meridian",-73.0],PARAMETER["Scale_Factor",0.9992],PARAMETER["Latitude_Of_Origin",4.0],UNIT["Meter",1.0]]',
            #in_features=r"'dtm\Polyline' Shape.Z Hard_Line <None>",
            in_features =arcpy.Clip_analysis(polyline,limite_prueba),
            constrained_delaunay="DELAUNAY"
        )
    elif contadorDGN_importados==2:
        tin=arcpy.ddd.CreateTin(
            out_tin=os.path.join(str(GDB_output), 'tin'),
            spatial_reference='PROJCS["MAGNA-SIRGAS_Origen-Nacional",GEOGCS["GCS_MAGNA",DATUM["D_MAGNA",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",5000000.0],PARAMETER["False_Northing",2000000.0],PARAMETER["Central_Meridian",-73.0],PARAMETER["Scale_Factor",0.9992],PARAMETER["Latitude_Of_Origin",4.0],UNIT["Meter",1.0]]',
            #in_features=r"'dtm\Polyline_1' Shape.Z Hard_Line <None>",
            in_features =arcpy.Clip_analysis(polyline,limite_prueba),
            constrained_delaunay="DELAUNAY"
        )
    elif contadorDGN_importados==3:
        tin=arcpy.ddd.CreateTin(
            out_tin=os.path.join(str(GDB_output), 'tin'),
            spatial_reference='PROJCS["MAGNA-SIRGAS_Origen-Nacional",GEOGCS["GCS_MAGNA",DATUM["D_MAGNA",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",5000000.0],PARAMETER["False_Northing",2000000.0],PARAMETER["Central_Meridian",-73.0],PARAMETER["Scale_Factor",0.9992],PARAMETER["Latitude_Of_Origin",4.0],UNIT["Meter",1.0]]',
            #in_features=r"'dtm\Polyline_2' Shape.Z Hard_Line <None>",
            in_features =arcpy.Clip_analysis(polyline,limite_prueba),
            constrained_delaunay="DELAUNAY"
        )
    elif contadorDGN_importados==4:
        tin=arcpy.ddd.CreateTin(
            out_tin=os.path.join(str(GDB_output), 'tin'),
            spatial_reference='PROJCS["MAGNA-SIRGAS_Origen-Nacional",GEOGCS["GCS_MAGNA",DATUM["D_MAGNA",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",5000000.0],PARAMETER["False_Northing",2000000.0],PARAMETER["Central_Meridian",-73.0],PARAMETER["Scale_Factor",0.9992],PARAMETER["Latitude_Of_Origin",4.0],UNIT["Meter",1.0]]',
            #in_features=r"'dtm\Polyline_2' Shape.Z Hard_Line <None>",
            in_features =arcpy.Clip_analysis(polyline,limite_prueba),
            constrained_delaunay="DELAUNAY"
        )
    
    elif contadorDGN_importados==5:
        tin=arcpy.ddd.CreateTin(
            out_tin=os.path.join(str(GDB_output), 'tin'),
            spatial_reference='PROJCS["MAGNA-SIRGAS_Origen-Nacional",GEOGCS["GCS_MAGNA",DATUM["D_MAGNA",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",5000000.0],PARAMETER["False_Northing",2000000.0],PARAMETER["Central_Meridian",-73.0],PARAMETER["Scale_Factor",0.9992],PARAMETER["Latitude_Of_Origin",4.0],UNIT["Meter",1.0]]',
            #in_features=r"'dtm\Polyline_3' Shape.Z Hard_Line <None>",
            in_features =arcpy.Clip_analysis(polyline,limite_prueba),
            constrained_delaunay="DELAUNAY"
        )

    #Se genera TIN:
    tin_raster= arcpy.ddd.TinRaster(in_tin=tin,out_raster=os.path.join(str(GDB_output), 'tin_raster'),  data_type="FLOAT", method="LINEAR", sample_distance="OBSERVATIONS",
        z_factor=1, sample_value=250)
    out_raster = arcpy.sa.Slope(in_raster=tin_raster, output_measurement="DEGREE",z_factor=1, method="PLANAR", z_unit="METER", analysis_target_device="GPU_THEN_CPU")
    out_raster.save(os.path.join(str(GDB_output), 'slope'))
    return  out_raster
    

def calcular_pendiente(GDB_output,raster):
    arcpy.AddMessage("{0}Calculando extensión de terreno por pendiente...".format(arrow))
    #Reclasificacion del mapa de pendiente:
    out_raster1 = arcpy.sa.Reclassify(in_raster=raster, reclass_field="VALUE", remap="0.000000 3.000000 1; 3.000001 12.000000 2; 12.000001 9999999999.0000 3", missing_values="DATA")  #0 a 7 plano; 7 - 25 Ondulado; >25 Montañoso 
    out_raster1.save(os.path.join(str(GDB_output), 'slope_reclasified'))   ##validacion ok
    #Recortar raster de pendiente si el usuario ingresa capa limite:
    if len(str(dgn_limite))>3:
        arcpy.AddMessage("\n-Recortando limite al DTM ---.".format(hasht, hasht))
        try: 
            convertirCADtoGDB(dgn_limite, GDB_output, 'limite')   #Conversion CAD a GDB
            contadorDGN_importados+=1
        except:
            pass
        #Seleccionar Poligono de limite:
        shapefile_polygon=[]
        lista_shapefile = arcpy.ListFeatureClasses(feature_dataset="limite", feature_type="Polygon")
        for shapefile in lista_shapefile:
            shapefile_polygon.append(shapefile)
        poligono_limite = shapefile_polygon[0]
        
        """
        out_raster1=arcpy.management.Clip(
            in_raster=out_raster1,
            out_raster=os.path.join(str(GDB_output), 'slope_reclasified'),
            in_template_dataset=poligono_limite,
            nodata_value="3,4e+38",
            clipping_geometry="NONE",
            maintain_clipping_extent="NO_MAINTAIN_EXTENT"
        )
        """
        
    #Raster reclasificado a poligono:
    polygon_reclassified=arcpy.conversion.RasterToPolygon( in_raster=out_raster1, out_polygon_features=os.path.join(str(GDB_output), 'slope_polygon_reclasified'),
    simplify="SIMPLIFY", raster_field="Value", create_multipart_features="MULTIPLE_OUTER_PART", max_vertices_per_feature=None) 
    
    #Control cambios
    arcpy.Dissolve_management(os.path.join(str(GDB_output), 'slope_polygon_reclasified'), os.path.join(str(GDB_output), 'prueba'), "GRIDCODE", "", "SINGLE_PART")

    ## Generalizando
    arcpy.EliminatePolygonPart_management(os.path.join(str(GDB_output), 'prueba'), os.path.join(str(GDB_output), 'prueba2'), "AREA",10000, "", "ANY")

    ##Seleccion por atributo
    if len(str(dgn_limite))>3:
        arcpy.AddMessage("-Recorte a Raster para generar DTM realizado. --- .".format(hasht, hasht))
        polygon_reclassified=arcpy.analysis.Clip(in_features=polygon_reclassified,clip_features="limite/"+str(poligono_limite),out_feature_class=os.path.join(str(GDB_output), 'slope_polygon_reclasified_2'),cluster_tolerance=None
        )

    #Realizar mediciones:
    crear_campo_numerico(os.path.join(str(GDB_output), 'prueba2'), 'areaha', 'areaha')
    crear_campo_numerico(os.path.join(str(GDB_output), 'prueba2'), 'areadm', 'areadm')
    arcpy.management.CalculateGeometryAttributes(in_features=os.path.join(str(GDB_output), 'prueba2'), geometry_property="areaha AREA", length_unit="",  area_unit="HECTARES",
    coordinate_system='PROJCS["MAGNA-SIRGAS_Origen-Nacional",GEOGCS["GCS_MAGNA",DATUM["D_MAGNA",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",5000000.0],PARAMETER["False_Northing",2000000.0],PARAMETER["Central_Meridian",-73.0],PARAMETER["Scale_Factor",0.9992],PARAMETER["Latitude_Of_Origin",4.0],UNIT["Meter",1.0]]',coordinate_format="SAME_AS_INPUT")
    arcpy.management.CalculateField(in_table=os.path.join(str(GDB_output), 'prueba2'), field="areadm", expression="!areaha!/1000000", expression_type="PYTHON3", code_block="",field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")
    arcpy.AddField_management(os.path.join(str(GDB_output), 'prueba2'), field_name='tipo', field_type='text')
    arcpy.management.CalculateField(in_table=os.path.join(str(GDB_output), 'prueba2'), field="tipo",
    expression="calcular(!gridcode!)",
    expression_type="PYTHON3",
    code_block="""def calcular(x):
    if x==1:
        return 'Plano'
    if x==2:
        return 'Ondulado'
    if x==3:
        return 'Montanioso'""",
    field_type="TEXT"
    )
    return os.path.join(str(GDB_output), 'prueba2')

def limpiezascript():
    arcpy.Delete_management("Pointfiltered_Statistics")
    arcpy.Delete_management("Polylinefiltered_Statistics")
    arcpy.Delete_management("slope")
    arcpy.Delete_management("slope_polygon_reclasified")
    arcpy.Delete_management("slope_reclasified")
    arcpy.Delete_management("tin_raster")
    return 1

def planimetria():
    ###################Parte 1. Planimetria ################################
    arcpy.AddMessage("\n{0}{0} ---Parte A. Conteo de puntos y polilineas--- {0}{0}.".format(hasht, hasht))
    convertirCADtoGDB(dgn_planimetria, GDB_output, 'planimetria')   #Conversion CAD a GDB
    global contadorDGN_importados
    contadorDGN_importados+=1

    #Generar estadisticas Polilinea:
    arcpy.AddMessage("\n{0}Generando conteo de polilineas...".format(arrow))
    dataset=os.path.join(str(GDB_output), 'planimetria')
    polyline=os.path.join(str(GDB_output), 'planimetria','Polyline')
    #arcpy.AddField_management(in_table=polyline, field_name='test', field_type="DOUBLE", field_alias='test')
    calculo_distancias(polyline)
    polyline_filtered=arcpy.conversion.FeatureClassToFeatureClass(polyline, out_path=dataset, out_name="Polyline_filtered", where_clause="Level NOT IN (42,43,44,45,58,59,60,61,62)")  ## Se tienen en cuenta los niveles solicitados para el NO conteo 
    #si añaden DGN limite, no contar los puntos 5 metros hacia dentro desde el borde:
    if len(str(dgn_limite))>3:
        arcpy.AddMessage("\n{0}-Importando limite.dgn --- {0}{0}.".format(hasht, hasht))
        convertirCADtoGDB(dgn_limite, GDB_output, 'limite')   #Conversion CAD a GDB
        contadorDGN_importados+=1
        #Seleccionar Poligono de hueco:
        shapefile_polygon=[]
        lista_shapefile = arcpy.ListFeatureClasses(feature_dataset="limite", feature_type="Polygon")
        for shapefile in lista_shapefile:
            shapefile_polygon.append(shapefile)
        poligono_limite = shapefile_polygon[0]
        limite_less_5m=arcpy.analysis.Buffer(poligono_limite, out_feature_class=os.path.join(str(GDB_output), 'limite', 'limite_less_5m'), buffer_distance_or_field="-5 Meters", line_side="FULL", line_end_type="ROUND", dissolve_option="ALL", dissolve_field=None, method="PLANAR")
        #Se cortan  los segmentos de polilinea 5 metros atras del limite.
        polyline_filtered=arcpy.analysis.Clip(in_features="planimetria/Polyline_filtered", clip_features="limite_less_5m",  out_feature_class=os.path.join(str(dataset), 'polyline_limite_less_5m'),cluster_tolerance=None)
        arcpy.AddMessage("-Son cortadas las polilineas inscritas a 5m desde el limite hacia adentro. ---.".format(hasht))

    #si añaden DGN Hueco, cortar las polilineas en el interior:
    if len(str(dgn_hueco))>3:
        arcpy.AddMessage("\n{0}-Importando hueco.dgn --- {0}{0}.".format(hasht, hasht))
        convertirCADtoGDB(dgn_hueco, GDB_output, 'hueco')   #Conversion CAD a GDB
        contadorDGN_importados+=1
        #Se cortan  los segmentos de polilinea que toquen el hueco.
        #Seleccionar Poligono de hueco:
        shapefile_polygon=[]
        lista_shapefile = arcpy.ListFeatureClasses(feature_dataset="hueco", feature_type="Polygon")
        for shapefile in lista_shapefile:
            shapefile_polygon.append(shapefile)
        poligono_hueco = shapefile_polygon[0]
        polyline_filtered=arcpy.analysis.Erase(in_features="planimetria/Polyline_filtered", erase_features="hueco/"+str(poligono_hueco), out_feature_class=os.path.join(str(dataset), 'polyline_no_hole'),cluster_tolerance=None)
        arcpy.AddMessage("-Son cortadas las polilineas inscritas en el poligono 'hueco'.".format(hasht))

    polylinefiltered_statistics=arcpy.analysis.Statistics(in_table=polyline_filtered, out_table=os.path.join(str(GDB_output),"Polylinefiltered_Statistics"), statistics_fields="Longitud_m SUM;Longitud_d SUM")
    arcpy.AddMessage("{0} {1} polilineas.".format(longarrow,arcpy.GetCount_management(polyline_filtered)))

    #Generar estadisticas Punto:
    arcpy.AddMessage("\n{0}Generando conteo de puntos...".format(arrow))
    point=os.path.join(str(GDB_output), 'planimetria','Point')
    point_filtered=arcpy.conversion.FeatureClassToFeatureClass(point, out_path=dataset, out_name="Point_filtered", where_clause="Level NOT IN (42,43,44,45,58,59,60,61,62)")  ##(42,43,44,45,58,59,60,61,62) Se tienen en cuenta los niveles solicitados para el NO conteo 
    #si añaden DGN limite, no contar los puntos 5 metros hacia dentro desde el borde:
    if len(str(dgn_limite))>3:
        #Se eliminan puntos que no estan contenidos dentro del limite en 5 metros.
        point_filtered=arcpy.edit.ErasePoint(in_features="planimetria/Point_filtered", remove_features="limite_less_5m", operation_type="OUTSIDE")
        arcpy.AddMessage("-No son contados los puntos 5m desde el limite hacia adentro. ---.".format(hasht))

    #si añaden DGN Hueco, no contar los puntos en el interior:
    if len(str(dgn_hueco))>3:
        arcpy.AddMessage("\n{0}-Importando hueco.dgn --- {0}{0}.".format(hasht, hasht))
        convertirCADtoGDB(dgn_hueco, GDB_output, 'hueco')   #Conversion CAD a GDB
        contadorDGN_importados+=1
        #Se cortan  los segmentos de polilinea que toquen el hueco.
        #Seleccionar Poligono de hueco:
        shapefile_polygon=[]
        lista_shapefile = arcpy.ListFeatureClasses(feature_dataset="hueco", feature_type="Polygon")
        for shapefile in lista_shapefile:
            shapefile_polygon.append(shapefile)
        poligono_hueco = shapefile_polygon[0]
        arcpy.AddMessage("-No son contados los puntos dentro del poligono 'hueco' capa_poligono_hueco={0}.".format(poligono_hueco))
        point_filtered=arcpy.edit.ErasePoint(in_features="planimetria/Point_filtered", remove_features="hueco/"+str(poligono_hueco), operation_type="INSIDE")
        arcpy.AddMessage("-No son contados los puntos dentro del poligono 'hueco' capa_poligono_hueco={0}.".format(hasht,poligono_hueco))


    pointfiltered_statistics=arcpy.analysis.Statistics(in_table=point_filtered, out_table=os.path.join(str(GDB_output),"Pointfiltered_Statistics"), statistics_fields="DocType COUNT")
    arcpy.AddMessage("{0} {1} puntos.".format(longarrow,arcpy.GetCount_management(point_filtered)))

    #Crear informe final
    arcpy.AddMessage("\nReporte de Excel generado en la ruta: \n{1} ".format(arrow,str(os.path.join(str(folder_output), 'informe_planimetria.xlsx'))))
    #Se crea tabla que contendrá el resumen y sus respectivos campos:
    summary=arcpy.CreateTable_management(out_path=GDB_output, out_name='summary')
    arcpy.management.AddField(in_table=summary, field_name='item', field_type="TEXT")
    crear_campo_numerico(summary, 'cantidad','cantidad')
    crear_campo_numerico(summary, 'Longitud_m','Longitud_m')
    crear_campo_numerico(summary, 'Longitud_dm','Longitud_dm')

    # Se completa la tabla summary con las estadisticas obtenidas previamente:
    with arcpy.da.SearchCursor(polylinefiltered_statistics,['FREQUENCY','FREQUENCY', 'SUM_Longitud_m', 'SUM_Longitud_d']) as sCur:
        with arcpy.da.InsertCursor(summary,['item', 'cantidad', 'Longitud_m', 'Longitud_dm']) as iCur:
            for row in sCur:
                row_list= list(row)
                row_list[0]='Polilineas'  ###Para polilinea
                row=tuple(row_list)
                iCur.insertRow(row)

    with arcpy.da.SearchCursor(pointfiltered_statistics,['FREQUENCY','FREQUENCY', 'FREQUENCY', 'FREQUENCY']) as sCur:
        with arcpy.da.InsertCursor(summary,['item', 'cantidad', 'Longitud_m', 'Longitud_dm']) as iCur:
            for row in sCur:
                row_list= list(row)
                row_list[0]='Puntos'  ###Para punto
                row_list[2]=-1
                row_list[3]=-1
                row=tuple(row_list)
                iCur.insertRow(row)

    #Generando informe
    exportar_a_excel(summary, os.path.join(str(folder_output), 'informe_planimetria.xlsx'))
    return 1


def pendiente():
    ###################Parte 2. Revision Pendiente ################################
    arcpy.AddMessage("\n{0}{0} ---Parte B. Identificación Pendientes del terreno--- {0}{0}.".format(hasht, hasht))
    #Importando DGN_MDT 
    convertirCADtoGDB(dgn_dtm, GDB_output, 'dtm')   #Conversion CAD a GDB
    global contadorDGN_importados
    contadorDGN_importados+=1
    pendiente=crear_mapa_de_pendiente(GDB_output)
    slope_polygon_reclasified=calcular_pendiente(GDB_output, pendiente)

    #Crear informe final
    arcpy.AddMessage("\nReporte de Excel generado en la ruta: \n{1} ".format(arrow,str(os.path.join(str(folder_output), 'informe_pendientes.xlsx'))))
    #Se crea tabla que contendrá el resumen y sus respectivos campos:
    summary_m=arcpy.CreateTable_management(out_path=GDB_output, out_name='summary_m')
    arcpy.management.AddField(in_table=summary_m, field_name='item', field_type="TEXT")
    crear_campo_numerico(summary_m, 'Area_ha','Area_ha')
    crear_campo_numerico(summary_m, 'Area_dm2','Area_dm2')

    # Se completa la tabla summary_m con las estadisticas obtenidas previamente:
    with arcpy.da.SearchCursor(slope_polygon_reclasified,['tipo','areaha', 'areadm']) as sCur:
        with arcpy.da.InsertCursor(summary_m,['item', 'Area_ha', 'Area_dm2']) as iCur:
            for row in sCur:
                iCur.insertRow(row)

    #Generando informe
    exportar_a_excel(summary_m, os.path.join(str(folder_output), 'informe_pendientes.xlsx'))

    #limpiezascript() #Se eliminan tablas temporales.
    return 1
def CalcularArea( Feat):
    try:
        arcpy.AddField_management(Feat,"AREA","DOUBLE")
    except:
        pass
    shapeName = arcpy.Describe(Feat).shapeFieldName
    rows = arcpy.UpdateCursor(Feat)
    for row in rows:
        geom=row.getValue(shapeName)
        row.AREA=geom.area
        rows.updateRow(row)
    del rows


def CAD_to_GDB(DGN_Entrada, Ruta_Salida):
    gdb = arcpy.management.CreateFileGDB(Ruta_Salida, 'Vectores_GDB')
    cad= arcpy.conversion.CADToGeodatabase(DGN_Entrada, gdb, 'Vectores_GDB', '10000', 'PROJCS["MAGNA-SIRGAS_Origen-Nacional",GEOGCS["GCS_MAGNA",DATUM["D_MAGNA",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",5000000.0],PARAMETER["False_Northing",2000000.0],PARAMETER["Central_Meridian",-73.0],PARAMETER["Scale_Factor",0.9992],PARAMETER["Latitude_Of_Origin",4.0],UNIT["Meter",1.0]];-618700 -8436100 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision')
    return cad


def areaCorte(Feat):
    rows = arcpy.SearchCursor(Feat)
    AreaTotal=0
    for row in rows:
        AreaTotal=AreaTotal+row.AREA
    return AreaTotal

def convert_shp():
    arcpy.env.workspace = dgn_limite
    ListaFeat= arcpy.ListFeatureClasses()
    for fc in ListaFeat:
        if fc == "Polygon" :
             arcpy.FeatureClassToFeatureClass_conversion(fc,folder_output,"Shape_limite.shp")
             limite = os.path.join(folder_output,"Shape_limite.shp")
    return limite

def pendiente_old():
        arcpy.AddMessage("\n{0}{0} ---Parte B. Identificación Pendientes del terreno--- {0}{0}.".format(hasht, hasht))
        limite_shp = convert_shp()
        arcpy.env.workspace = dgn_dtm
        ListaFeat= arcpy.ListFeatureClasses()
        for fc in ListaFeat:
            if fc == "Polyline":
                arcpy.FeatureClassToFeatureClass_conversion(fc,folder_output,"Shape_p.shp")
                arcpy.Clip_analysis(strShape,limite_shp,strShape2)
        
        CalcularArea(limite_shp)
        ##Conversion Tin
        arcpy.CreateTin_3d(strTin,"","'"+strShape2+"'" +" Shape.Z masspoints <None>","DELAUNAY")
        ## Tin a Raster
        arcpy.TinRaster_3d(strTin,strRaster,"INT", "LINEAR", "OBSERVATIONS 250")
        ##Cortando raster
        outExtractByMask = ExtractByMask(strRaster, limite_shp)
        outExtractByMask.save(strRasterCorte)
        ## Slope Raster
        arcpy.Slope_3d(strRasterCorte, strSlope, "PERCENT_RISE", "1")
        ## Reclasificar Raster
        arcpy.Reclassify_3d (strSlope, "Value", RECLASIFICAR, strReclass, "NODATA")
        ## Raster To Polygon
        arcpy.RasterToPolygon_conversion(strReclass, strPoligono, "NO_SIMPLIFY", "Value")
        ## Unir Poligonos
        arcpy.Dissolve_management(strPoligono, strDissolve, "GRIDCODE", "", "SINGLE_PART")
        ## Calculando Areas
        CalcularArea(strDissolve)
        ## Generalizando
        arcpy.EliminatePolygonPart_management(strDissolve, strEliminate4, "AREA",10000, "", "ANY")
        ## Creando Layer
        arcpy.MakeFeatureLayer_management(strEliminate4, "eliminateLYR")
        ##Seleccion por atributo
        arcpy.SelectLayerByAttribute_management("eliminateLYR", "NEW_SELECTION",""" "AREA"<100000  """)
        arcpy.Eliminate_management ("eliminateLYR", strEliminate1, "LENGTH")
        CalcularArea(strEliminate1)


        arcpy.MakeFeatureLayer_management(strEliminate1, "eliminateLYR2")
        arcpy.SelectLayerByAttribute_management("eliminateLYR2", "NEW_SELECTION",""" "AREA"<100000  """)
        arcpy.Eliminate_management ("eliminateLYR2", strEliminate2, "LENGTH")
        CalcularArea(strEliminate2)

        arcpy.MakeFeatureLayer_management(strEliminate2, "eliminateLYR3")
        arcpy.SelectLayerByAttribute_management("eliminateLYR3", "NEW_SELECTION",""" "AREA"<100000  """)
        arcpy.Eliminate_management ("eliminateLYR3", strEliminate3, "LENGTH")
        CalcularArea(strEliminate3)

        arcpy.MakeFeatureLayer_management(strEliminate3, "eliminateLYR4")
        arcpy.SelectLayerByAttribute_management( "eliminateLYR4", "NEW_SELECTION",""" "AREA"<100000  """)
        arcpy.Eliminate_management ("eliminateLYR4", strEliminate5, "LENGTH")
        arcpy.Dissolve_management(strEliminate5, strEliminateF, "GRIDCODE", "", "MULTI_PART")
        CalcularArea(strEliminateF)




        arcpy.Delete_management("eliminateLYR")
        arcpy.Delete_management("eliminateLYR2")
        arcpy.Delete_management("eliminateLYR3")
        arcpy.Delete_management("eliminateLYR4")

        plano = 0
        ondulado = 0
        montanoso = 0
        AreaTotal2= areaCorte(limite_shp)
        rows = arcpy.SearchCursor(strEliminateF)
        for row in rows:
            if row.GRIDCODE==1:
                plano = row.AREA
            elif row.GRIDCODE==2:
                ondulado = row.AREA
            elif row.GRIDCODE==3:
                montanoso = row.AREA
        AreaTotal = plano + ondulado + montanoso

        if AreaTotal== AreaTotal2:
            plano = plano / 10000
            ondulado = ondulado / 10000
            montanoso = montanoso / 10000
        elif AreaTotal< AreaTotal2:
            resto = AreaTotal2 - AreaTotal
            plano = (((plano / AreaTotal) * resto) + plano) / 10000
            ondulado = (((ondulado / AreaTotal) * resto) + ondulado) / 10000
            montanoso = (((montanoso / AreaTotal) * resto) + montanoso) / 10000
        elif AreaTotal > AreaTotal2:
            resto = AreaTotal - AreaTotal2
            plano = (plano - ((plano / AreaTotal) * resto)) / 10000
            ondulado = (ondulado - ((ondulado / AreaTotal) * resto)) / 10000
            montanoso = (montanoso - ((montanoso / AreaTotal) * resto)) / 10000

        planoT=str(round(plano,1))
        onduladoT=str(round(ondulado,1))
        montanosoT=str(round(montanoso,1))

        data = {
            "Zona": ["Plana", "Ondulada", "Montañosa"],
            "Área (Ha)": [planoT, onduladoT, montanosoT]
        }

        df = pd.DataFrame(data)
        xlsx_file = os.path.join(folder_output,"reporte_areas_pendiente.xlsx")  # Nombre del archivo CSV
        df.to_excel(xlsx_file, index=False)
        #Crear informe final
        arcpy.AddMessage("\nReporte de Excel generado en la ruta: \n{1} ".format(arrow,str(os.path.join(str(folder_output), 'reporte_areas_pendiente.xlsx'))))
        # Informar al usuario
        #arcpy.AddMessage(f"Resultados guardados en: {csv_file}" )
        #print("Resultados guardados en:", folder_output)


#######--------------------> Inicio Herramienta <--------------------#######

arcpy.AddMessage("\n{0} ...INICIANDO PROCESO DE GENERACION REPORTE... {1}.".format(sep, sep))
GDB_output=crearGDB(folder_output)  #Generar GDB de salida
arcpy.env.workspace=str(GDB_output)  #Se define espacio de trabajo
arcpy.env.overwriteOutput = True



if len(str(dgn_planimetria)) >3:
    planimetria()

if len(str(dgn_dtm)) >3:
    
    #pendiente()
    pendiente_old()
    
arcpy.AddMessage("\n\n¡Finalizado correctamente!.\n".format(arrow))
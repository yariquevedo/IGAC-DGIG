##########################################################################################################
#                          Script "03_Generacion_Marcos_Control_2022_Final"
#
# December 4th, 2022 - Nicolas GRÉHANT (IGN FI) in collaboration with Diego RUGELES (IGAC)
#
# ArcGIS PRO adapatation of IGAC Script "MARCOS DE CONTROL", keeping 2021 production of only 30 cells,
# but taking into account Bosque and Cerca. Validation of GDB is included.
#
# Usage:
# ------
#    Control/Validation of a GDB in IGAC model ("gdbEntrada") allowing to :
#           1) Create a sample of square cells for future visual control
#                > Using an area of interest ("areaDeCorte"), or if not furnished, calculating the 
#                     bounding box of contour lines feature class
#                > Taking into account the refence scale of the input GDB data
#           2) Perform GDB tables validation  
#
#    INPUT
#           > Geodatabase Entrada: the GDB to control
#           > Zona Urbana:
#                 - if checked, the script will control the entities ID with Urban parameters   
#                 - if unchecked, use of Rural paraetrs to control IDs
#           > Escala: the scale of input GDB data
#           > Area de Corte (optional): area of interest where will be created the cells,
#                 or if empty, calculating the bounding box of contour lines feature class
#           > Creacion de Marcos: unchecked only if the GDB is a merge of previously controled blocks,
#                 and that the idea is only to perform final GDB validation
#           > Validacion GDB: checked to perform GDB validation in addition to the creation of cells
#     >>> cells objects "Marcos..." are stored within the "gdbValidacion"
#              (an empty gdb which is created by the script)
#     >>> log file gives info about all process.
#
##########################################################################################################
import arcpy
import os
import random
import shutil #"shutil" used to remove existing directory
import statistics
import time
###Authorization to overwrite existing data
arcpy.env.overwriteOutput = True
##########################################################################################################
###Get parameters
###-------------------------------------------------------------------------------------------------------
gdbEntrada=sys.argv[1]
urban = sys.argv[2]
escala = sys.argv[3]
areaDeCorte = sys.argv[4]
arcpy.AddMessage('areaDeCorte: ' + areaDeCorte)
script = sys.argv[5]
validGDB =  sys.argv[6]  #Validacion tablas GDB
### Matrix giving values according to the map scale, used to define the pitch of the control grid (Fishnet).
areas = {"1000":50, "2000":100, "5000":250, "10000":500, "25000":1000,"50000":2000,"100000":4000}
##########################################################################################################
##########################################################################################################
### Splitting of the different directory levels of the input GDB, down to the name of the GDB itself
### then creating the Log directory and Log file
###-------------------------------------------------------------------------------------------------------
ruta = gdbEntrada.split("\\")
#Keeping all the elements except the last one (the GDB itself)
rnew = ruta[:-1]
# Rebuilding the path to the input GDB directory
sep = "\\"
rutasal = sep.join(rnew)
# Name of the input GDB, without the .gdb extension
namem = ruta[-1].split('.')[0]
#### Creation of Validation (output) GDB
# The name of the GDB + its extension
GDB_name = "BD_Validacion_" + namem + ".gdb" 
# Real creation of the GDB
arcpy.CreateFileGDB_management(rutasal,GDB_name)
# Full path to the GDB
gdbValidacion = rutasal + "\\" + GDB_name
#### Creation of a Log directory and Log file
# Path to the future LOG directory
rutasalida = rutasal + "\\Log_" + namem
# Creation of the LOG directory (destroying it first if already exists)
if os.path.exists(rutasalida):
	shutil.rmtree(rutasalida)
os.mkdir(rutasalida)
arcpy.AddMessage(">>> LOG resultados en: "+rutasalida+"\\"+"Report_"+namem+".txt")
arcpy.AddMessage(" -------------------------------------------------------------------------")
arcpy.AddMessage(" -------------------------------------------------------------------------")
### Creation of the LOG file
filet = open(rutasalida+"\\"+"Report_"+namem+".txt","a")
filet.write("-------- REPORTE DEL SCRIPT PARA LA GDB " + namem + " --------\n")
filet.write("> Creación de Marcos... feature classes en " + gdbValidacion + "\n\n")
##########################################################################################################
##########################################################################################################
###  Creation of a function "autoIncrement()" allowing to create the auto-incremented identifiers of the "salidagrillain" objects,
### i.e. of the "MarcosInt_..." (which are the set of complete squares in the polygon defining the cutting area.
###-------------------------------------------------------------------------------------------------------
codeblock = """rec=0
def autoIncrement():
	global rec
	pStart = 1
	pInterval = 1
	if (rec == 0):
		rec = pStart
	else:
		rec += pInterval
	return rec"""
##########################################################################################################
### Fonction "SelectRandomByCount"
###---------------------------------------------------------------------------------------------------------
def SelectRandomByCount(layer, count, salidapuntos):
	layerCount = int(arcpy.GetCount_management(layer).getOutput(0))
	if layerCount < count:
		arcpy.AddMessage('NO EXISTEN SUFICIENTES PUNTOS PARA SELECIONAR')
		return
	oids = [oid for oid, in arcpy.da.SearchCursor(layer, "OID@")]
	oidFldName = arcpy.Describe(layer).OIDFieldName
	delimOidFld = arcpy.AddFieldDelimiters(layer, oidFldName)
	randOids = random.sample(oids, count)
	oidsStr = ",".join(map(str, randOids))
	sql = "{0} IN ({1})".format(delimOidFld, oidsStr)
	arcpy.MakeFeatureLayer_management (layer, "stateslyrs")
	arcpy.SelectLayerByAttribute_management("stateslyrs", "", sql)
	arcpy.CopyFeatures_management("stateslyrs", salidapuntos)
	arcpy.Delete_management("stateslyrs")
##########################################################################################################
##########################################################################################################
#                                          --- MARCOS ---
##########################################################################################################
if script == 'true':
	# Keeping time stamp
	marcos_start_time = time.localtime()
	time_string = time.strftime("%H:%M:%S", marcos_start_time)
	arcpy.AddMessage('Creacion de los Marcos - Start time: ' + time_string)
	filet.write("Creacion de los Marcos - Start time: " + time_string + "\n")
	### STEP 0 - If the area of interest ("Area de Corte") value is empty (which will be translated
	# in '#'), the script will use contour lines bounding box (Elevacion/CNivel) as default AOI
	if areaDeCorte == '#':
		inFc = os.path.join(gdbEntrada, 'Elevacion', 'CNivel')
		outFc = os.path.join(gdbValidacion, 'Default_Area_de_Corte')
		result = int(arcpy.GetCount_management(inFc).getOutput(0))
		arcpy.AddMessage(">>>No se especifico area de corte, se calculara usando los datos de las curvas de nivel")
		filet.write("> No se especifico area de corte, se calculara usando los datos de las curvas de nivel\n\n")
		if result > 0:
			arcpy.MinimumBoundingGeometry_management(inFc, outFc, "CONVEX_HULL", "ALL")
			fcCorte=outFc
			#arcpy.AddMessage('fcCorte: ' + fcCorte)
		else:
			arcpy.AddMessage(">>>No hay datos sufifientes para calcular el area de corte, por favor generela manuelmente")
			arcpy.AddMessage(">>>                     END OF SCRIPT")
			filet.write("> No hay datos sufifientes para calcular el area de corte, por favor generela manuelmente. END OF SCRIPT\n\n")
			sys.exit()
	else:
		fcCorte = areaDeCorte
		arcpy.AddMessage('>>>Uso del área de corte: '+ fcCorte)
		filet.write("> Uso del área de corte: " + fcCorte + "\n\n")
	arcpy.AddMessage(" -------------------------------------------------------------------------")
	arcpy.AddMessage(" -------------------------------------------------------------------------")
	### STEP 1 - Input GDB is clipped with area of interest
	CORTE = fcCorte
	arcpy.AddMessage("Fase 1 - Cortando Geodatabase.")
	filet.write("Fase 1 - Cortando Geodatabase.\n")
	arcpy.env.workspace = gdbEntrada
	#
	datasetList = arcpy.ListDatasets()
	for dataset in datasetList:
		if(dataset!="IndiceMapas" and dataset!="OrdenamientoTerritorial"):
			#arcpy.AddMessage('>>Analizando Dataset '+dataset)
			filet.write('>>Analizando Dataset '+dataset + "\n")
			arcpy.env.workspace = gdbEntrada + "\\" + dataset
			descd = arcpy.Describe(gdbEntrada + "\\" + dataset)
			sr = descd.spatialreference
			arcpy.CreateFeatureDataset_management(gdbValidacion, dataset, sr)
			fcList = arcpy.ListFeatureClasses()
			for fc in fcList:
				result = int(arcpy.GetCount_management(fc).getOutput(0))
				try:
					if result>0:
						#arcpy.AddMessage('-----Cortando FeatureClass '+fc)
						filet.write("-----Corte del Feature "+fc + "\n")
						fcSal=gdbValidacion + "\\" + dataset + "\\" + fc
						desc = arcpy.Describe(fc)
						if(desc.featureType!="Annotation"):
							if(arcpy.Exists(fc+"_Anot")):
								arcpy.Clip_analysis(fc+"_Anot", CORTE , fcSal+"_Anot")
							arcpy.Clip_analysis(fc, CORTE , fcSal)
				except Exception as ex:
					arcpy.AddMessage("Error..."+ex.message)
	del datasetList
	del fcList
	arcpy.AddMessage("GDB Cortada.")
	filet.write("GDB Cortada.\n")
	### STEP 2 - Creation of control square areas (Marcos)
	arcpy.AddMessage("Fase 2 - Generando grilla.")
	filet.write("Fase 2 - Generando grilla.")
	### Sub-Step 2-1 - First "MarcosAT" which covers with squares the whole bounding box the the area of interest)
	valesc = areas[str(escala)]
	sptref = arcpy.Describe(fcCorte).spatialreference
	extent = arcpy.Describe(fcCorte).extent
	arcpy.env.outputCoordinateSystem = sptref
	coords = str(extent.XMin) + " " + str(extent.YMin)
	yAxisCoordinate = str(extent.XMin) + " " + str(extent.YMin+1)
	oppositeCoorner = str(extent.XMax) + " " + str(extent.YMax)
	###'MarcosAT' is directlty stored in the Validation GDB
	outpg = gdbValidacion + "\\" + 'MarcosAT'
	arcpy.CreateFishnet_management(outpg, coords, yAxisCoordinate, valesc, valesc, "0", "0", oppositeCoorner, "NO_LABELS", "", "POLYGON")
	resultgr = int(arcpy.GetCount_management(outpg).getOutput(0))
	arcpy.AddMessage("Grilla Total Generada con "+str(resultgr)+" celdas...")
	filet.write("Grilla Total Generada con "+str(resultgr)+" celdas..." + "\n")
	### Sub-Step 2-2 - Creation of second feature class "MarcosInt" keeping only squares within the AOI
	#Interseccion Area Proyecto
	salidagrillain = gdbValidacion + "\\" + 'MarcosInt'  # Only a path for now
	# Creation of a temporary layer pointing on 'MarcosAT' feature class
	arcpy.MakeFeatureLayer_management (outpg, "grillat")
	# Selection of 'MarcosAT' features which are completely within the AOI (Area de Corte)
	arcpy.SelectLayerByLocation_management("grillat", "COMPLETELY_WITHIN", fcCorte)
	# Result is stored
	arcpy.CopyFeatures_management("grillat", salidagrillain)  # Now 'MarcosInt' feature class really exists
	# Utilisation of the function created before to add an unique ID 'Id' to each object of 'MarcosInt'
	expression = "autoIncrement()"
	arcpy.management.CalculateField(salidagrillain, "Id", expression, "PYTHON3", codeblock)
	# New field 'Num_elm' that will be used later to store the number of elements within each square
	arcpy.AddField_management(salidagrillain, "Num_elm", "DOUBLE", 0, "", "", "", "NULLABLE", "NON_REQUIRED")
	# Calculation of total number of cells in 'MarcosInt'
	resultgri = int(arcpy.GetCount_management(salidagrillain).getOutput(0))
	arcpy.AddMessage("Grilla Intersectada con area de trabajo, "+str(resultgri)+" celdas...")
	filet.write("Grilla Intersectada con area de trabajo, "+str(resultgri)+" celdas..." + "\n")
	# The temporary layer is no more useful
	arcpy.Delete_management("grillat")
	
	
	### STEP 3 - Keeping 30 cells of 'MarcosInt' (or all if not enough)
	arcpy.AddMessage("Fase 3 - Selección de las celdas.")
	filet.write("Fase 3 - Selección de las celdas.")
	if resultgri>30:
		arcpy.AddMessage("Se seleccionaran 30 marcos de los "+str(resultgri)+" intersectados...")
		filet.write("Se seleccionaran 30 marcos de los "+str(resultgri)+" intersectados..." + "\n")
		salidagrillai = gdbValidacion + "\\" + 'Marcos30' # Only a path for now
		SelectRandomByCount(salidagrillain,30,salidagrillai)  # 30 squares randomly among 'MarcosInt'
		opcion = 'Caso 1'
	else:
		arcpy.AddMessage('Guardamos todas las '+ str(resultgri) + ' celdas de MarcosInt')
		filet.write("Guardamos todas las " + str(resultgri) + " celdas de MarcosInt" + "\n")
		salidagrillai = gdbValidacion + "\\" + 'MarcosInt'  # Not only a path as 'MarcosInt' already exists with its (<=30) objects
		opcion = 'Caso 2'
	### STEP 4 - Calculation of number of entities for each feature class for each of the 30 (or less) cells
	field_names = [i.name for i in arcpy.ListFields(salidagrillai) if i.type != 'OID']
	#['Shape', 'Id', 'Num_elm', 'Shape_Length', 'Shape_Area'] (if 'Marcos30')
	cursor = arcpy.da.SearchCursor(salidagrillai, field_names)
	# These will store the total number of each group for the whole 30 (or less) cells
	numelementos = 0   # Otros que Bosque y Cerca
	numelementos_bacm = 0  # Bosque and Cerca
	#For each of the 30 (or less) cells:
	for row in cursor:
		#arcpy.AddMessage('row: ' + str(row))
		#Position of "Id" field is different according to slidagrillai source (Marcos30 or MarcosInt)
		if opcion == 'Caso 1':  # Marcos30
			idc = row[1]
		elif opcion == 'Caso 2': # MarcosInt
			idc = row[3]
		arcpy.AddMessage('Calculando Grilla Id: '+ str(idc))
		filet.write('Calculando Grilla Id: '+ str(idc) + "\n")
		# Creation of a temporary layer pointing on the selected cells
		arcpy.MakeFeatureLayer_management(salidagrillai, "grillac")
		# Creation of expression to select only the current cell
		exp = "Id = '"+str(idc)+"'"
		arcpy.SelectLayerByAttribute_management("grillac","NEW_SELECTION",exp)
		# Then with all the feature classes clipped from the input GDB
		arcpy.env.workspace = gdbValidacion
		datasetList = arcpy.ListDatasets()
		# These will store the total number of each group for each cell
		numcapas = 0
		numcapas_bacm = 0
		# For each dataset:
		for dataset in datasetList:
			arcpy.env.workspace = gdbValidacion + "\\" + dataset
			fcList = arcpy.ListFeatureClasses()
			#For each Feature Class:
			for fc in fcList:
				#a SHP is created to keep only the objects of the FC which intersect the current cell,
				# only to count them, then the SHP is deleted...
				outName_gr = rutasalida + "\\" + 'Gr_'+str(idc)+str(fc)+'.shp'  # Just a path
				inFeatures_pc = ["grillac", fc]
				#arcpy.AddMessage('inFeatures_pc: ' + str(inFeatures_pc))
				arcpy.Intersect_analysis(inFeatures_pc, outName_gr)
				result = int(arcpy.GetCount_management(outName_gr).getOutput(0))
				#arcpy.AddMessage("El numero de elementos de "+str(fc)+" es: "+str(result))
				filet.write("El numero de elementos de "+str(fc)+" es: "+str(result) + "\n")
				#
				if (str(fc) == 'Bosque' or str(fc) == 'Cerca'):
					numcapas_bacm += result
				else:
					numcapas += result
				arcpy.Delete_management(outName_gr)
		# The 'Num_elm' field of the selected cell is given the 'numcapas' value
		arcpy.management.CalculateField("grillac", "Num_elm", numcapas, "PYTHON3")
		#arcpy.AddMessage("El numero de elementos en la grilla "+ str(idc)+" categoria otros es: "+ str(numcapas))
		#arcpy.AddMessage("El numero de elementos en la grilla "+ str(idc)+" categoria bacm es: "+ str(numcapas_bacm))
		filet.write("El numero de elementos en la grilla "+ str(idc)+" categoria otros es: "+ str(numcapas) + "\n")
		filet.write("El numero de elementos en la grilla "+ str(idc)+" categoria bacm es: "+ str(numcapas_bacm) + "\n")
		
		arcpy.Delete_management("grillac")
		# Total number of objects in each cell
		numelementos += numcapas
		numelementos_bacm += numcapas_bacm
	arcpy.AddMessage("El numero de elementos categoria otros en todas las celdas es "+ str(numelementos))
	arcpy.AddMessage("El numero de elementos categoria bacm en todas las celdas es "+ str(numelementos_bacm))
	filet.write("El numero de elementos categoria otros en todas las celdas es "+ str(numelementos) + "\n")
	filet.write("El numero de elementos categoria bacm en todas las celdas es "+ str(numelementos_bacm) + "\n")
	# Temporary layer is deleted
	arcpy.Delete_management("grillac")
	### STEP 5 - Statistics
	if numelementos < numelementos_bacm:
		arcpy.AddMessage("El mayor conteo de elementos fue en la categoria bacm y se usará un p de 0.05 ")
		p = 0.03
		count = int (numelementos_bacm)
		salidatb = rutasalida + "\\tablagr"
		arcpy.Statistics_analysis(salidagrillai, salidatb, [["Num_elm", "SUM"]])
		field_namespr = [i.name for i in arcpy.ListFields(salidatb) if i.type != 'OID']
		cursorpr = arcpy.da.SearchCursor(salidatb, field_namespr)
		datapr =[row for row in cursorpr]
		numel_total = datapr[0][2]
	else:
		arcpy.AddMessage("El mayor conteo de elementos fue en la categoria otros y se usará un p de 0.03 ")
		p = 0.05
		count = int(numelementos)
		salidatb = rutasalida + "\\tablagr"
		arcpy.Statistics_analysis(salidagrillai, salidatb, [["Num_elm", "SUM"]])
		field_namespr = [i.name for i in arcpy.ListFields(salidatb) if i.type != 'OID']
		cursorpr = arcpy.da.SearchCursor(salidatb, field_namespr)
		datapr =[row for row in cursorpr]
		numel_total = datapr[0][2]
		
	
	arcpy.AddMessage('numel_total: ' + str(numel_total))
	### Final number of cells (30 or less)
	result= arcpy.GetCount_management(salidagrillai)
	numel_gr = int(result.getOutput(0))
	arcpy.AddMessage('numel_gr: ' + str(numel_gr))
	### Mean number of objects per cell
	pr_elmgr = (numel_total/numel_gr)
	###
	arcpy.AddMessage("pr_elmgr es: "+ str(pr_elmgr))
	### This result is multiplied by the total number of elements of 'MarcosInt'
	numel_totales = pr_elmgr*resultgri
	### Activation 2 messages commentés
	arcpy.AddMessage("numel_total es: "+ str(numel_total))      #1317
	arcpy.AddMessage("numel_totales es: "+ str(numel_totales))  #13916,3
	### Formula: https://www.qualtrics.com/fr/gestion-de-l-experience/etude-marche/calcul-taille-echantillon/
	### 1,96 is scoreZ for a 95% level of confidence
	z = 1.96
	### "p" is standard deviation. "p" can be 0.03 or 0.05 depending on previous tests
	### "e" = margin of error?
	e = 0.01
	a = (z*z)*(p)*(1-p)
	b = (e*e)
	g = a/b
	count = int(numel_totales)
	c = (count-1)/ float(count)
	d = count*(e*e)
	ef = a/d
	f = c + ef
	o = g/f 
	n = int(o)
	###
	arcpy.AddMessage("n es: "+ str(n))
	filet.write("n es: "+ str(n) + "\n")
	###Arrondi à l'entier le plus proche :
	num_mr = int(math.ceil(n/pr_elmgr))
	###
	arcpy.AddMessage("num_mr es: "+ str(num_mr))
	filet.write("num_mr es: "+ str(num_mr) + "\n")
	
	### 2 possibilties according to "num_mr" value:
	#    - if <=15: all previously created Marcos are kept
	#    - if >15: new "MarcosCS_..." are calculated
	arcpy.AddMessage("Tamaño de muestra minimo en elementos "+str(n))
	filet.write("\n \n")
	filet.write("Tamaño de muestra minimo en elementos "+str(n) + "\n")
	if num_mr <= 15:
		arcpy.AddMessage("El numero de marcos obtenidos es "+str(num_mr)+ " se dejaran todos los marcos inicialmente generados, "+ str(numel_gr))
		filet.write("El numero de marcos obtenidos es "+str(num_mr)+ " se dejaran todos los marcos inicialmente generados, "+ str(numel_gr) + "\n")
	else:
		arcpy.AddMessage("El numero de marcos obtenidos es "+str(num_mr)+ ", se extraera dicha cantidad de marcos.")
		filet.write("El numero de marcos obtenidos es "+str(num_mr)+ ", se extraera dicha cantidad de marcos." + "\n")
		arcpy.AddMessage("Generando Marcos Aleatorios..")
		out_points = gdbValidacion + "\\" + 'MarcosCS'
		SelectRandomByCount(salidagrillain,num_mr,out_points)
		arcpy.AddMessage("Marcos de control generados")
		filet.write("Marcos de control generados" + "\n")
##########################################################################################################
#                                     --- GDB VALIDATION ---
##########################################################################################################
#########################################################################################################
if validGDB == 'true':
	arcpy.AddMessage(" ")
	arcpy.AddMessage(" *************************************************************************")
	arcpy.AddMessage("Validacion tablas GDB: OK")
	arcpy.AddMessage(" *************************************************************************")
	
	
	valid_gdb_start_time = time.localtime()
	time_string = time.strftime("%H:%M:%S", valid_gdb_start_time)
	arcpy.AddMessage('GDB Analysis start time: ' + time_string)
	
	
	filet.write("-----REPORTE DE ANALISIS GDB CBASICA-----\n")
	
	def elimina_tildes(cadena):
		s = ''.join((c for c in unicodedata.normalize('NFD',unicode(cadena)) if unicodedata.category(c) != 'Mn'))
		return s.decode()
	
	def findindex(table,fieldname):
		return [i.name for i in arcpy.ListFields(table)].index(fieldname)
	
	
	### Buscar identificadores duplicados
	def repetido(featureclass):
		field_names = [i.name for i in arcpy.ListFields(featureclass) if 'Identif' in i.name]
		cpt = 0
		for field in field_names:
			#arcpy.AddMessage('   -Field: ' + field)
			tablerepetido = rutasalida + "\\repetido.dbf"
			arcpy.Statistics_analysis(featureclass, tablerepetido, [[field, "COUNT"]], field)
			#field_names_1 = ['BIdentif', 'COUNT_BIde']
			cursor = arcpy.da.SearchCursor(tablerepetido, '*')
			for row in cursor:
				identifi = row[1]
				#arcpy.AddMessage('identifi: ' + str(identifi))
				count = row[3]
				#arcpy.AddMessage('count: ' + str(count))
				if (count >= 2):
					filet.write('---En el Featureclass ' + featureclass +' el elemento con identificador: '+ str(identifi) +' se encuentra '+ str(count) + ' veces' + "\n")
					arcpy.AddMessage('En el Featureclass ' + featureclass +' el elemento con identificador: '+ str(identifi) +' se encuentra '+ str(count) + ' veces')	
					cpt = cpt + 1
				#if len(identifi) != 13:
				#    filet.write('En el Featureclass ' + featureclass +' el elemento con identificador: '+ str(identifi) +' tiene un numero erroneo de digitos' + "\n")
				#    arcpy.AddMessage('En el Featureclass ' + featureclass +' el elemento con identificador: '+ str(identifi) +' tiene un numero erroneo de digitos')
		if cpt == 0:
			arcpy.AddMessage('--- Ningún problema')
	
	### Buscar campos vacíos
	def vacios(featureclass):
		field_names = [i.name for i in arcpy.ListFields(featureclass) if i.type != 'OID']
		rows = arcpy.da.SearchCursor(featureclass, field_names)
		cpt = 0
		for row in rows:
			identifi = row[2]
			#arcpy.AddMessage('Esta es el dato: ' + str(row))
			for i in range(0, len(row)):
				#arcpy.AddMessage(row[i])
				if row[i] == 'Null' or row[i]=='NULO' or row[i]=='Nulo' or row[i]=='nulo' or row[i]=='' or row[i]=='NULL' or row[i]=='null' or row[i]==str('None') or row[i]=='None':
					filet.write('En el Featureclass ' + featureclass +' hay elementos con campos vacios '+ "\n")
					arcpy.AddMessage('En el Featureclass ' + featureclass +' hay elementos con campos vacios ')
					cpt = cpt + 1
		if cpt == 0:
			arcpy.AddMessage('--- Ningún problema')
	  
	#### Verificación del identificador
	def conse_field(featureclass):
		# IGAC identifier
		# - If Rural area:
		#     * 5 first numbers are for the Municipio
		#     * 4 next numbers are for the feature class number in IGAC specifications catalog
		#     * all the others ([9:]) are for the unique numero for each entity, which can be 01,02,...(2 numbers),100,...,999 (3 numbers),1000... (4 numbers) depending on how many objects are in the feature class
		# - If Urban area:
		#     * 8 first numbers are for the Municipio
		#     * 4 next numbers are for the feature class number in IGAC specifications catalog
		#     * all the others ([12:]) are for the unique numero for each entity, which can be 01,02,...(2 numbers),100,...,999 (3 numbers),1000... (4 numbers) depending on how many objects are in the feature class
		total = int(arcpy.GetCount_management(fc).getOutput(0))  # Useful for consecutive id verification
		list_conse_field_2 = []
		list_conse_field_3 = []
		list_conse_field_4 = []
		list_conse_field_5 = []
		field_names = [i.name for i in arcpy.ListFields(featureclass) if 'Identif' in i.name]
		rows = arcpy.da.SearchCursor(featureclass, field_names)
		num_row = 0
		for row in rows:
			num_row = num_row + 1
			#arcpy.AddMessage('---Row ' + str(num_row))
			identifi = row[0]
			if identifi is None:
				arcpy.AddMessage('---ERROR - Object ID is Null!')
			else:
				#arcpy.AddMessage('-----identifi: ' + identifi)
				#longitud_identifi = len(identifi)
				#arcpy.AddMessage('-----(La longitud del identificador es: ' + str(longitud_identifi) +')')
				# Nicolas (urban/rural)
				if urban == 'true':    # All but the the 12 first
					#arcpy.AddMessage('----- Urban -----"')
					if len(identifi) < 14:
						arcpy.AddMessage('---ERROR - El identificador ' + identifi + ' tiene un numero de caracteres diferente al permitido (14 Urban), por favor revisar el featuclass ' + featureclass )
						continue
					consecutivo = identifi[12:]
					#arcpy.AddMessage('-----El consecutivo es:' + str(consecutivo))
					if len(consecutivo) == 2:
						list_conse_field_2.append(consecutivo)
					elif len(consecutivo) == 3:
						if total < 100:
							arcpy.AddMessage('---ERROR - Extraño, sólo hay ' + str(total) + ' entidades, este identificador (' + str(consecutivo) + ') no es consistente,por favor revisar el featuclass ' + featureclass + ' (identificador:' + identifi +')')
							break
						else:
							list_conse_field_3.append(consecutivo)
					elif len(consecutivo) == 4:
						if total < 1000:
							arcpy.AddMessage('---ERROR - Extraño, sólo hay ' + str(total) + ' entidades, este identificador (' + str(consecutivo) + ') no es consistente,por favor revisar el featuclass ' + featureclass + ' (identificador:' + identifi +')')
							break
						else:
							list_conse_field_4.append(consecutivo)
					elif len(consecutivo) == 5:
						if total < 10000:
							arcpy.AddMessage('---ERROR - Extraño, sólo hay ' + str(total) + ' entidades, este identificador (' + str(consecutivo) + ') no es consistente,por favor revisar el featuclass ' + featureclass + ' (identificador:' + identifi +')')
							break
						else:
							list_conse_field_5.append(consecutivo)
					else:
						if total < 100000:
							arcpy.AddMessage('---ERROR - Extraño, sólo hay ' + str(total) + ' entidades, este identificador (' + str(consecutivo) + ') no es consistente,por favor revisar el featuclass ' + featureclass + ' (identificador:' + identifi +')')
							break
						else:
							arcpy.AddMessage('---ERROR - CUIDADO: mas que 99999 entidades, no se puede verificar con este script')
							break
				else:   # rural          All but the 9 first
					#arcpy.AddMessage('----- Rural -----')
					if len(identifi) < 11:
						arcpy.AddMessage('---ERROR - El identificador ' + identifi + ' tiene un numero de caracteres diferente al permitido (11 Rural), por favor revisar el featuclass ' + featureclass )
						continue
					consecutivo = identifi[9:]
					#arcpy.AddMessage('-----El consecutivo es:' + str(consecutivo))
					if len(consecutivo) == 2:
						list_conse_field_2.append(consecutivo)
					elif len(consecutivo) == 3:
						if total < 100:
							arcpy.AddMessage('---ERROR - Extraño, sólo hay ' + str(total) + ' entidades, este identificador (' + str(consecutivo) + ') no es consistente,por favor revisar el featuclass ' + featureclass + ' (identificador:' + identifi +')')
							break
						else:
							list_conse_field_3.append(consecutivo)
					elif len(consecutivo) == 4:
						if total < 1000:
							arcpy.AddMessage('---ERROR - Extraño, sólo hay ' + str(total) + ' entidades, este identificador (' + str(consecutivo) + ') no es consistente,por favor revisar el featuclass ' + featureclass + ' (identificador:' + identifi +')')
							break
						else:
							list_conse_field_4.append(consecutivo)
					elif len(consecutivo) == 5:
						if total < 10000:
							arcpy.AddMessage('---ERROR - Extraño, sólo hay ' + str(total) + ' entidades, este identificador (' + str(consecutivo) + ') no es consistente,por favor revisar el featuclass ' + featureclass + ' (identificador:' + identifi +')')
							break
						else:
							list_conse_field_5.append(consecutivo)
					else:
						if total < 100000:
							arcpy.AddMessage('---ERROR - Extraño, sólo hay ' + str(total) + ' entidades, este identificador (' + str(consecutivo) + ') no es consistente,por favor revisar el featuclass ' + featureclass + ' (identificador:' + identifi +')')
							break
						else:
							arcpy.AddMessage('---ERROR - CUIDADO: mas que 99999 entidades, no se puede verificar con este script')
							break
		
		list_conse_field_2.sort()
		list_conse_field_3.sort()
		list_conse_field_4.sort()
		list_conse_field_5.sort()
		
		w = 0
		for num in list_conse_field_5[1:]:
			#arcpy.AddMessage(int(num))
			if (int(list_conse_field_5[w]) + int(1)) == int(num):
				''
			else:
				arcpy.AddMessage('---ERROR - Se debe revisar el consecutivo del campo identificador del feature class: ' + featureclass)
				arcpy.AddMessage('---(Hay un problema con el consecutivo: ' + str(int(num)-1) + ' que no existe)')
				filet.write('Se debe revisar el consecutivo del campo identificador del feature class: ' + featureclass + "\n")
				break
			w = w + 1
		
		z = 0
		for num in list_conse_field_4[1:]:
			#arcpy.AddMessage(int(num))
			if (int(list_conse_field_4[z]) + int(1)) == int(num):
				''
			else:
				arcpy.AddMessage('---ERROR - Se debe revisar el consecutivo del campo identificador del feature class: '+ featureclass)
				arcpy.AddMessage('---(Hay un problema con el consecutivo: ' + str(int(num)-1) + ' que no existe)')
				filet.write('Se debe revisar el consecutivo del campo identificador del feature class: '+ featureclass + "\n")
				break
			z = z + 1
		
		x = 0
		for num in list_conse_field_3[1:]:
			#arcpy.AddMessage(int(num))
			if (int(list_conse_field_3[x]) + int(1)) == int(num):
				''
			else:
				arcpy.AddMessage('---ERROR - Se debe revisar el consecutivo del campo identificador del feature class: ' + featureclass)
				arcpy.AddMessage('---(Hay un problema con el consecutivo: ' + str(int(num)-1) + ' que no existe)')
				filet.write('Se debe revisar el consecutivo del campo identificador del feature class: ' + featureclass + "\n")
				break
			x = x + 1
		
		y = 0
		for num in list_conse_field_2[1:]:
			#arcpy.AddMessage(int(num))
			if (int(list_conse_field_2[y]) + int(1)) == int(num):
				''
			else:
				arcpy.AddMessage('---ERROR - Se debe revisar el consecutivo del campo identificador del feature class: ' + featureclass)
				arcpy.AddMessage('---(Hay un problema con el consecutivo: ' + str(int(num)-1) + ' que no existe)')
				filet.write('Se debe revisar el consecutivo del campo identificador del feature class: ' + featureclass + "\n")
				break
			y = y + 1
		
	
	
	#####################
	arcpy.AddMessage("Analizando Geodatabase")
	arcpy.env.workspace = gdbEntrada
	datasetList = arcpy.ListDatasets()
	for dataset in datasetList:
		if(dataset!="IndiceMapas" and dataset!="OrdenamientoTerritorial"):
			filet.write("\n")
			arcpy.AddMessage(' ')
			arcpy.AddMessage('-------------------------------------------------------------')
			arcpy.AddMessage('************ Analizando Dataset ' + dataset + ' *************')
			arcpy.AddMessage('-------------------------------------------------------------')
			filet.write('------------------------Analizando Dataset '+dataset + '------------------------' + "\n")
			arcpy.env.workspace = gdbEntrada + "\\" + dataset
			if(dataset=="CoberturaTierra"):
				fcList = arcpy.ListFeatureClasses()
				#arcpy.AddMessage('fcList: ' + str(fcList))
				for fc in fcList:
					arcpy.AddMessage('---Analizando FeatureClass '+fc)
					#arcpy.AddMessage('-------------------------------------------------')
					# Checking that feature class is not empty
					result = int(arcpy.GetCount_management(fc).getOutput(0))
					if result == 0:
						arcpy.AddMessage('> Feature Class ' + str(fc) + ' está vacía. No se controla.')
						arcpy.AddMessage(' ')
						continue
					else:
						arcpy.AddMessage('> Feature Class ' + str(fc) + ' tiene ' + str(result) + ' entidade(s) para controlar')
					arcpy.AddMessage('> Buscar campos vacíos') #
					vacios(fc)
					arcpy.AddMessage(' ') #
					arcpy.AddMessage('> Buscar repetido') #
					repetido(fc)
					arcpy.AddMessage(' ') #
					arcpy.AddMessage('> Verificación del identificador y del RuleID') #
					try:
						if result>0:
							#arcpy.AddMessage('-conse_field funcion')
							conse_field(fc)
							aliasn = arcpy.Describe(fc).aliasName
							#filet.write("\n \n")
							#arcpy.AddMessage('-Analizando FeatureClass '+fc)
							#filet.write('Analizando FeatureClass '+fc + "\n")
							field_names = [i.name for i in arcpy.ListFields(fc) if i.type != 'OID']
							cursor = arcpy.da.SearchCursor(fc, field_names)
							i = 0
							for field_name in field_names:
								if field_name == 'RuleID':
									index_RuleID = findindex(fc,field_name)-1
							for row in cursor:
								ruleid = row[index_RuleID]
								if(ruleid!=1):
									arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+' se encuentra mal diligenciado ruleid, el valor diligenciado es: '+str(ruleid))
									filet.write('---En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+' se encuentra mal diligenciado ruleid, el valor diligenciado es: '+str(ruleid) + "\n")
									i+=1
								
								
							if i == 0:
								arcpy.AddMessage('--- Ningún problema (RuleID)')
							else:
								arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el numero de errores encontrados (RuleID) son: '+ str(i))
								filet.write('En el Featureclass ' +fc+' el numero de errores encontrados (RuleID) son: '+ str(i) + "\n")
						else:
							arcpy.AddMessage('-El FeatureClass '+fc +' se encuentra vacio')
							filet.write('El FeatureClass '+fc +' se encuentra vacio' + "\n")
					except Exception as ex:
						arcpy.AddMessage("Error..."+ex.message)
					arcpy.AddMessage(' ')
					arcpy.AddMessage('-------------------------------------------------')
			if(dataset=="Elevacion"):
				fcList = arcpy.ListFeatureClasses()
				for fc in fcList:
					arcpy.AddMessage('---Analizando FeatureClass '+fc)
					#arcpy.AddMessage('-------------------------------------------------')
					# Checking that feature class is not empty
					result = int(arcpy.GetCount_management(fc).getOutput(0))
					if result == 0:
						arcpy.AddMessage('> Feature Class ' + str(fc) + ' está vacía. No se controla.')
						arcpy.AddMessage(' ')
						continue
					else:
						arcpy.AddMessage('> Feature Class ' + str(fc) + ' tiene ' + str(result) + ' entidade(s) para controlar')
					arcpy.AddMessage('> Buscar campos vacíos') #
					vacios(fc)
					arcpy.AddMessage(' ') #
					arcpy.AddMessage('> Buscar repetido') #
					repetido(fc)
					arcpy.AddMessage(' ') #
					arcpy.AddMessage('> Verificación del identificador y del RuleID') #
					try:
						if result>0:
							conse_field(fc)
							aliasn = arcpy.Describe(fc).aliasName
							#filet.write("\n \n")
							#arcpy.AddMessage('Analizando FeatureClass '+fc)
							#filet.write('Analizando FeatureClass '+fc + "\n")
							field_names = [i.name for i in arcpy.ListFields(fc) if i.type != 'OID']
							cursor = arcpy.da.SearchCursor(fc, field_names)
							i=0
							for field_name in field_names:
								if field_name == 'RuleID':
									index_RuleID = findindex(fc,field_name)-1
								elif field_name == 'CNTipo':
									index_CNTipo = findindex(fc,field_name)-1
								elif field_name == 'LDTTipo':
									index_LDTTipo = findindex(fc,field_name)-1
								elif field_name == 'LDTFuente':
									index_LDTFuente = findindex(fc,field_name)-1
						 
							#arcpy.AddMessage('En el Featureclass' + fc+ ' el campo '+ field_name + 'el indice es ' + str(index_RuleID))
							#index_RuleID_1 = index_RuleID
							for row in cursor:
								if(fc=='CNivel'):
									ruleid = row[index_RuleID]
									#ruleid = row[5]
									tipo = row[index_CNTipo]
									
									if(ruleid!=tipo):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+' los campos RuleId y Tipo no coinciden, el valor diligenciado es, Tipo:'+str(tipo)+', RuleId: '+str(ruleid))
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+' los campos RuleId y Tipo no coinciden, el valor diligenciado es, Tipo:'+str(tipo)+', RuleId: '+str(ruleid) + "\n")
										i+=1
								else:
									ruleid = row[index_RuleID]
									tipo = row[index_LDTTipo]
									fuente = row[index_LDTFuente]
									if(ruleid!=None and (tipo==None or fuente==None)):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+' los campos Tipo o Fuente no estan diligenciados, el valor de RuleId es, '+str(ruleid))
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+' los campos Tipo o Fuente no estan diligenciados, el valor de RuleId es, '+str(ruleid) + "\n")
										i+=1
									else:
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+' el valor de RuleId esta vacio')
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+' el valor de RuleId esta vacio' + "\n")
										i+=1
							if i == 0:
								arcpy.AddMessage('--- Ningún problema (RuleID)')
							else:
								arcpy.AddMessage('En el Featureclass ' +fc+' el numero de errores encontrados son: '+ str(i))
								filet.write('En el Featureclass ' +fc+' el numero de errores encontrados son: '+ str(i) + "\n")
						else:
							arcpy.AddMessage('El FeatureClass '+fc +' se encuentra vacio')
							filet.write('El FeatureClass '+fc +' se encuentra vacio' + "\n")
					except Exception as ex:
						arcpy.AddMessage("Error..."+ex.message)
					arcpy.AddMessage(' ')
					arcpy.AddMessage('-------------------------------------------------')
			if(dataset=="Hidrografia"):
				fcList = arcpy.ListFeatureClasses()
				#arcpy.AddMessage('fcList: ' + str(fcList)) #
				for fc in fcList:
					arcpy.AddMessage('---Analizando FeatureClass '+fc)
					#arcpy.AddMessage('-------------------------------------------------')
					# Checking that feature class is not empty
					result = int(arcpy.GetCount_management(fc).getOutput(0))
					if result == 0:
						arcpy.AddMessage('> Feature Class ' + str(fc) + ' está vacía. No se controla.')
						arcpy.AddMessage(' ')
						continue
					else:
						arcpy.AddMessage('> Feature Class ' + str(fc) + ' tiene ' + str(result) + ' entidade(s) para controlar')
					arcpy.AddMessage('> Buscar campos vacíos') #
					vacios(fc)
					arcpy.AddMessage(' ') #
					arcpy.AddMessage('> Buscar repetido') #
					repetido(fc)
					arcpy.AddMessage(' ') #
					arcpy.AddMessage('> Verificación del identificador y del RuleID') #
					try:
						if result>0:
							conse_field(fc)
							aliasn = arcpy.Describe(fc).aliasName
							#filet.write("\n \n")
							#arcpy.AddMessage('#1#Analizando FeatureClass '+fc)
							#filet.write('Analizando FeatureClass '+fc + "\n")
							field_names = [i.name for i in arcpy.ListFields(fc) if i.type != 'OID']
							#arcpy.AddMessage("field_names: " + str(field_names))
							cursor = arcpy.da.SearchCursor(fc, field_names)
							i=0
							for field_name in field_names:
								if field_name == 'RuleID':
									#arcpy.AddMessage("-->field_name: " + field_name)
									index_RuleID = findindex(fc,field_name)-1
									#arcpy.AddMessage("index_RuleID: " + str(index_RuleID))
								elif field_name == 'DATipo':
									#arcpy.AddMessage("-->field_name: " + field_name)
									index_DATipo = findindex(fc,field_name)-1
									#arcpy.AddMessage("index_DATipo: " + str(index_DATipo))
								elif field_name == 'DEstado':
									#arcpy.AddMessage("-->field_name: " + field_name)
									index_DEstado = findindex(fc,field_name)-1
									#arcpy.AddMessage("index_DEstado: " + str(index_DEstado))
								elif field_name == 'DDisperso':
									#arcpy.AddMessage("-->field_name: " + field_name)
									index_DDisperso = findindex(fc,field_name)-1
									#arcpy.AddMessage("index_DDisperso: " + str(index_DDisperso))
								elif field_name == 'DNombre':
									#arcpy.AddMessage("-->field_name: " + field_name)
									index_DNombre = findindex(fc,field_name)-1 
									#arcpy.AddMessage("index_DNombre: " + str(index_DNombre))
								#else:
								#	arcpy.AddMessage("-->>" + field_name + " is not used")
							for row in cursor:
								#arcpy.AddMessage('row: ' + str(row))
								# Security if Identif is NULL
								if row[1] == None:
									row1 = '(NULL)'
								else:
									row1 = row[1]
								#arcpy.AddMessage('row1: ' + row1)
								if(fc=='BArena'):
									ruleid = row[index_RuleID]
									if(ruleid!=1):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +' se encuentra mal diligenciado Ruleid, el valor diligenciado es: '+str(ruleid))
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +' se encuentra mal diligenciado Ruleid, el valor diligenciado es: '+str(ruleid)+ "\n")
										i+=1
								elif(fc=='DAgua_P'):
									ruleid = row[index_RuleID]
									tipo = row[index_DATipo]
									if(ruleid!=tipo):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +', los campos Tipo y RuleId son diferentes, los valores son: '+str(tipo) + ', '+ str(ruleid)+' respectivamente.')
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +', los campos Tipo y RuleId son diferentes, los valores son: '+str(tipo) + ', '+ str(ruleid)+' respectivamente.' + "\n")
										i+=1
								elif(fc=='DAgua_R'):
									ruleid = row[index_RuleID]
									tipo = row[index_DATipo]
									if(ruleid!=tipo):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +', los campos Tipo y RuleId son diferentes, los valores son: '+str(tipo) + ', '+ str(ruleid)+' respectivamente.')
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +', los campos Tipo y RuleId son diferentes, los valores son: '+str(tipo) + ', '+ str(ruleid)+' respectivamente.' + "\n")
										i+=1
								elif(fc=='Drenaj_L'):
									ruleid = row[index_RuleID]
									estado = row[index_DEstado]
									disperso = row[index_DDisperso]
									nombre = row[index_DNombre]
									if(estado==1 and disperso=='2' and ruleid!=3):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +', el campo RuleId esta mal diligenciado, los valores son, estado: '+str(estado) + ', Ddisperso: '+ str(disperso)+' y ruleid es: '+str(ruleid))
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +', el campo RuleId esta mal diligenciado, los valores son, estado: '+str(estado) + ', Ddisperso: '+ str(disperso)+' y ruleid es: '+str(ruleid) + "\n")
										i+=1
									elif(estado==1 and disperso=='2' and (nombre=='' or nombre==None)):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +', el campo Nombre esta vacio.')
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +', el campo Nombre esta vacio.' + "\n")
										i+=1
									elif(estado==1 and disperso=='1' and ruleid!=4):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +', el campo RuleId esta mal diligenciado, los valores son, estado: '+str(estado) + ', Ddisperso: '+ str(disperso)+' y ruleid es: '+str(ruleid))
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +', el campo RuleId esta mal diligenciado, los valores son, estado: '+str(estado) + ', Ddisperso: '+ str(disperso)+' y ruleid es: '+str(ruleid) + "\n")
										i+=1
									elif(estado==2 and disperso=='2' and ruleid!=1):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +', el campo RuleId esta mal diligenciado, los valores son, estado: '+str(estado) + ', Ddisperso: '+ str(disperso)+' y ruleid es: '+str(ruleid))
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +', el campo RuleId esta mal diligenciado, los valores son, estado: '+str(estado) + ', Ddisperso: '+ str(disperso)+' y ruleid es: '+str(ruleid) + "\n")
										i+=1
									elif(estado==2 and disperso=='1' and ruleid!=2):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +', el campo RuleId esta mal diligenciado, los valores son, estado: '+str(estado) + ', Ddisperso: '+ str(disperso)+' y ruleid es: '+str(ruleid))
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +', el campo RuleId esta mal diligenciado, los valores son, estado: '+str(estado) + ', Ddisperso: '+ str(disperso)+' y ruleid es: '+str(ruleid) + "\n")
										i+=1
									elif((nombre=='' or nombre==None) and estado==1):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +', el campo Estado esta mal diligenciado, ya que debe ser Intermitente (2) los valores son, estado: '+str(estado) + ', Nombre: '+ str(nombre))
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +', el campo Estado esta mal diligenciado, ya que debe ser Intermitente (2) los valores son, estado: '+str(estado) + ', Nombre: '+ str(nombre) + "\n")
										i+=1
									if(nombre=='Null' or nombre=='NULO' or nombre=='Nulo' or nombre=='nulo' or nombre=='' or nombre=='NULL' or nombre=='null'):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +' el campo Nombre, se encuentra mal diligenciado, el valor diligenciado es: '+str(nombre))
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +' el campo Nombre, se encuentra mal diligenciado, el valor diligenciado es: '+str(nombre) + "\n")
										i+=1
									if(disperso=='Null' or disperso=='NULO' or disperso=='Nulo' or disperso=='nulo' or disperso=='' or disperso=='NULL' or disperso=='null'):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +' el campo Disperso, se encuentra mal diligenciado, el valor diligenciado es: '+str(disperso))
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +' el campo Disperso, se encuentra mal diligenciado, el valor diligenciado es: '+str(disperso) + "\n")
										i+=1
								
								elif(fc=='DAgua_L'):
									ruleid = row[index_RuleID]
									tipo = row[index_DATipo]
									if(ruleid!=tipo):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +', los campos Tipo y RuleId son diferentes, los valores son: '+str(tipo) + ', '+ str(ruleid)+' respectivamente.')
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +', los campos Tipo y RuleId son diferentes, los valores son: '+str(tipo) + ', '+ str(ruleid)+' respectivamente.' + "\n")
										i+=1
								elif(fc=='Drenaj_R'):
									ruleid = row[index_RuleID]
									tipo = row[2]
									ngeog = row[3]
									if(ruleid!=tipo):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +', los campos Tipo y RuleId son diferentes, los valores son: '+str(tipo) + ', '+ str(ruleid)+' respectivamente.')
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +', los campos Tipo y RuleId son diferentes, los valores son: '+str(tipo) + ', '+ str(ruleid)+' respectivamente.' + "\n")
										i+=1
									if(ngeog=='Null' or ngeog=='NULO' or ngeog=='Nulo' or ngeog=='nulo' or ngeog==''):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +' el campo Nombre_Geografico, se encuentra mal diligenciado, el valor diligenciado es: '+str(ngeog))
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +' el campo Nombre_Geografico, se encuentra mal diligenciado, el valor diligenciado es: '+str(ngeog) + "\n")
										i+=1
								else:
									ruleid = row[index_RuleID]
									if(ruleid!=1):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +' se encuentra mal diligenciado Ruleid, el valor diligenciado es: '+str(ruleid))
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +' se encuentra mal diligenciado Ruleid, el valor diligenciado es: '+str(ruleid) + "\n")
										i+=1
							'''
							if(fc=='Drenaj_L'):
								arcpy.AddField_management(fc, "Nametmp", "TEXT", 200, "", "", "", "", "")
								exp2 = '[DNombre] & "_N"'
								arcpy.CalculateField_management(fc, "Nametmp", exp2, "VB")
								fld_cave = 'Nametmp'
								caves = list(set(r[0] for r in arcpy.da.SearchCursor(fc,fld_cave)))
								tableng = rutasalida + "\\Namedrl.dbf"
								arcpy.CreateTable_management (rutasalida, "Namedrl.dbf")
								arcpy.AddField_management(tableng, "NameLayer", "TEXT", 200, "", "", "", "", "")
								arcpy.AddField_management(tableng, "FREQUENCY", "LONG", 0, "", "", "", "", "")
								arcpy.AddField_management(tableng, "COUNT", "LONG", 0, "", "", "", "", "")
								arcpy.AddMessage('Analizando Repeticion de Nombres de Drenajes...')
								for cave in caves:
									where = '"{0}" = \'{1}\''.format(fld_cave, cave)    
									caveObj = arcpy.MakeFeatureLayer_management(fc, "cave", where)
									caven = elimina_tildes(cave)
									outFS = os.path.join(rutasalida, caven + '.dbf')
									arcpy.Statistics_analysis(caveObj, outFS , [["Nametmp", "COUNT"]])
									arcpy.AddField_management(outFS, "NameLayer", "TEXT", 200, "", "", "", "", "")
									exp2 = '"'+cave+'"'
									arcpy.CalculateField_management(outFS, "NameLayer", exp2, "PYTHON_9.3")
									arcpy.Append_management(outFS, tableng, "NO_TEST","","")
									arcpy.Delete_management("cave")
									arcpy.Delete_management(outFS)
								field_names2 = [j.name for j in arcpy.ListFields(tableng) if j.type != 'OID']
								cursor2 = arcpy.da.SearchCursor(tableng, field_names2)
								for row2 in cursor2:
									name = row2[1].split('_')[0]
									name = 'Null' if name=='' else name
									frec = row2[2]
									if frec > 1:
										arcpy.AddMessage('En el Featureclass ' +fc+' el elemento con nombre: '+name+', se encuentra repetido, '+str(frec)+ ' veces.')
										filet.write('En el Featureclass ' +fc+' el elemento con nombre: '+name+', se encuentra repetido, '+str(frec)+ ' veces.' + "\n")
										i+=1
								arcpy.DeleteField_management(fc, ["Nametmp"])
								arcpy.Delete_management(tableng)'''
							if i == 0:
								arcpy.AddMessage('--- Ningún problema (RuleID)')
							else:
								arcpy.AddMessage('En el Featureclass ' +fc+' el numero de errores encontrados son: '+ str(i))
								filet.write('En el Featureclass ' +fc+' el numero de errores encontrados son: '+ str(i) + "\n")
						else:
							arcpy.AddMessage('El FeatureClass '+fc +' se encuentra vacio')
							filet.write('El FeatureClass '+fc +' se encuentra vacio' + "\n")
					except Exception as ex:
						arcpy.AddMessage("Error..."+ex.message) #PB with message
			if(dataset=="Geodesia"):
				fcList = arcpy.ListFeatureClasses()
				for fc in fcList:
					arcpy.AddMessage('---Analizando FeatureClass '+fc)
					#arcpy.AddMessage('-------------------------------------------------')
					# Checking that feature class is not empty
					result = int(arcpy.GetCount_management(fc).getOutput(0))
					if result == 0:
						arcpy.AddMessage('> Feature Class ' + str(fc) + ' está vacía. No se controla.')
						arcpy.AddMessage(' ')
						continue
					else:
						arcpy.AddMessage('> Feature Class ' + str(fc) + ' tiene ' + str(result) + ' entidade(s) para controlar')
					arcpy.AddMessage('> Buscar campos vacíos') #
					vacios(fc)
					arcpy.AddMessage(' ') #
					arcpy.AddMessage('> Buscar repetido') #
					repetido(fc)
					arcpy.AddMessage(' ') #
					arcpy.AddMessage('> Verificación del identificador y del RuleID') #
					try:
						if result>0:
							conse_field(fc)
							aliasn = arcpy.Describe(fc).aliasName
							#filet.write("\n \n")
							#arcpy.AddMessage('Analizando FeatureClass '+fc)
							#filet.write('Analizando FeatureClass '+fc + "\n")
							field_names = [i.name for i in arcpy.ListFields(fc) if i.type != 'OID']
							cursor = arcpy.da.SearchCursor(fc, field_names)
							i=0
							for field_name in field_names:
								if field_name == 'RuleID':
									index_RuleID = findindex(fc,field_name)-1
								elif field_name == 'MRTNomencl':
									index_MRTNomencl = findindex(fc,field_name)-1
							for row in cursor:
								ruleid = row[index_RuleID]
								nomencl = row[index_MRTNomencl]
								if(ruleid==None):
									arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+' se encuentra mal diligenciado Ruleid, el valor diligenciado es: '+str(ruleid))
									filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+' se encuentra mal diligenciado Ruleid, el valor diligenciado es: '+str(ruleid) + "\n")
									i+=1
								if(nomencl=='Null' or nomencl=='NULO' or nomencl=='Nulo' or nomencl=='nulo' or nomencl=='' or nomencl=='NULL' or nomencl=='null'):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+' el campo Nomenclatura, se encuentra mal diligenciado, el valor diligenciado es: '+str(nomencl))
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+' el campo Nomenclatura, se encuentra mal diligenciado, el valor diligenciado es: '+str(nomencl) + "\n")
										i+=1
							if i == 0:
								arcpy.AddMessage('--- Ningún problema (RuleID)')
							else:
								arcpy.AddMessage('En el Featureclass ' +fc+' el numero de errores encontrados son: '+ str(i))
								filet.write('En el Featureclass ' +fc+' el numero de errores encontrados son: '+ str(i) + "\n")
						else:
							arcpy.AddMessage('El FeatureClass '+fc +' se encuentra vacio')
							filet.write('El FeatureClass '+fc +' se encuentra vacio' + "\n")
					except Exception as ex:
						arcpy.AddMessage("Error..."+ex.message)
			if(dataset=="InfraestructuraServicios"):
				fcList = arcpy.ListFeatureClasses()
				for fc in fcList:
					arcpy.AddMessage('---Analizando FeatureClass '+fc)
					#arcpy.AddMessage('-------------------------------------------------')
					# Checking that feature class is not empty
					result = int(arcpy.GetCount_management(fc).getOutput(0))
					if result == 0:
						arcpy.AddMessage('> Feature Class ' + str(fc) + ' está vacía. No se controla.')
						arcpy.AddMessage(' ')
						continue
					else:
						arcpy.AddMessage('> Feature Class ' + str(fc) + ' tiene ' + str(result) + ' entidade(s) para controlar')
					arcpy.AddMessage('> Buscar campos vacíos') #
					vacios(fc)
					arcpy.AddMessage(' ') #
					arcpy.AddMessage('> Buscar repetido') #
					repetido(fc)
					arcpy.AddMessage(' ') #
					arcpy.AddMessage('> Verificación del identificador y del RuleID') #
					try:
						if result>0:
							conse_field(fc)
							aliasn = arcpy.Describe(fc).aliasName
							#filet.write("\n \n")
							#arcpy.AddMessage('Analizando FeatureClass '+fc)
							#filet.write('Analizando FeatureClass '+fc + "\n")
							field_names = [i.name for i in arcpy.ListFields(fc) if i.type != 'OID']
							cursor = arcpy.da.SearchCursor(fc, field_names)
							i=0
							for field_name in field_names:
								if field_name == 'RuleID':
									index_RuleID = findindex(fc,field_name)-1
								elif field_name == 'PDTipo':
									index_PDTipo = findindex(fc,field_name)-1
								elif field_name == 'TubTipo':
									index_TubTipo = findindex(fc,field_name)-1
							for row in cursor:
								if(fc=='PDistr'):
									ruleid = row[index_RuleID]
									tipo = row[index_PDTipo]
									if((ruleid == 2 and tipo == 2) or (ruleid == 3 and tipo == 3) or (ruleid == 1 and tipo == 2) or (ruleid == 1 and tipo == 2)):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+', los campos Tipo y RuleId son diferentes, los valores son: '+str(tipo) + ', '+ str(ruleid)+' respectivamente.')
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+', los campos Tipo y RuleId son diferentes, los valores son: '+str(tipo) + ', '+ str(ruleid)+' respectivamente.' + "\n")
										i+=1
								elif(fc=='RATens'):
									ruleid = row[index_RuleID]
									#if(ruleid!=1):
									if(ruleid not in (1,1)):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+' se encuentra mal diligenciado Ruleid, el valor diligenciado es: '+str(ruleid))
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+' se encuentra mal diligenciado Ruleid, el valor diligenciado es: '+str(ruleid) + "\n")
										i+=1
								elif(fc=='TSPubl'):
									ruleid = row[index_RuleID]
									if(ruleid != 1):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+' se encuentra mal diligenciado Ruleid, el valor diligenciado es: '+str(ruleid))
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+' se encuentra mal diligenciado Ruleid, el valor diligenciado es: '+str(ruleid) + "\n")
										i+=1    
								elif(fc=='Pozo'):
									ruleid = row[index_RuleID]
									if(ruleid != 1):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+' se encuentra mal diligenciado Ruleid, el valor diligenciado es: '+str(ruleid))
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+' se encuentra mal diligenciado Ruleid, el valor diligenciado es: '+str(ruleid) + "\n")
										i+=1                                                                 
								elif(fc=='Tuberi'):
									ruleid = row[index_RuleID]
									Tubtipo = row[index_TubTipo]
									if(ruleid != 1):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+' se encuentra mal diligenciado Ruleid, el valor diligenciado es: '+str(ruleid))
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+' se encuentra mal diligenciado Ruleid, el valor diligenciado es: '+str(ruleid) + "\n")
										i+=1      
									if(Tubtipo > 5):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+' se encuentra mal diligenciado TubTipo, el valor diligenciado es: '+str(Tubtipo))
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+' se encuentra mal diligenciado TubTipo, el valor diligenciado es: '+str(Tubtipo) + "\n")
										i+=1                                              
								else:
									ruleid = row[index_RuleID]
									if(ruleid!=2):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+' se encuentra mal diligenciado Ruleid, el valor diligenciado es: '+str(ruleid))
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+' se encuentra mal diligenciado Ruleid, el valor diligenciado es: '+str(ruleid) + "\n")
										i+=1
							if i == 0:
								arcpy.AddMessage('--- Ningún problema (RuleID)')
							else:
								arcpy.AddMessage('En el Featureclass ' +fc+' el numero de errores encontrados son: '+ str(i))
								filet.write('En el Featureclass ' +fc+' el numero de errores encontrados son: '+ str(i) + "\n")
						else:
							arcpy.AddMessage('El FeatureClass '+fc +' se encuentra vacio')
							filet.write('El FeatureClass '+fc +' se encuentra vacio' + "\n")
					except Exception as ex:
						arcpy.AddMessage("Error..."+ex.message)
			if(dataset=="NombresGeograficos"):
				fcList = arcpy.ListFeatureClasses()
				for fc in fcList:
					arcpy.AddMessage('---Analizando FeatureClass '+fc)
					#arcpy.AddMessage('-------------------------------------------------')
					# Checking that feature class is not empty
					result = int(arcpy.GetCount_management(fc).getOutput(0))
					if result == 0:
						arcpy.AddMessage('> Feature Class ' + str(fc) + ' está vacía. No se controla.')
						arcpy.AddMessage(' ')
						continue
					else:
						arcpy.AddMessage('> Feature Class ' + str(fc) + ' tiene ' + str(result) + ' entidade(s) para controlar')
					arcpy.AddMessage('> Buscar campos vacíos') #
					vacios(fc)
					arcpy.AddMessage(' ') #
					arcpy.AddMessage('> Buscar repetido') #
					repetido(fc)
					arcpy.AddMessage(' ') #
					arcpy.AddMessage('> Verificación del identificador y del RuleID') #
					try:
						if result>0:
							conse_field(fc)
							aliasn = arcpy.Describe(fc).aliasName
							#filet.write("\n \n")
							#arcpy.AddMessage('Analizando FeatureClass '+fc)
							#filet.write('Analizando FeatureClass '+fc + "\n")
							field_names = [i.name for i in arcpy.ListFields(fc) if i.type != 'OID']
							#arcpy.AddMessage('field_names: ' + str(field_names))   # ['SHAPE', 'NGIdentif', 'NGNPrincip', 'NGNAlterno', 'NGCategori', 'NGSubcateg', 'NGIdioma', 'NGEstado', 'NGFuente', 'NGEMaxima', 'NGEMinima', 'NGIORelaci', 'RuleID', 'Override']
							cursor = arcpy.da.SearchCursor(fc, field_names)
							i=0
							for field_name in field_names:
								if field_name == 'RuleID':
									index_RuleID = findindex(fc,field_name)-1
								elif field_name == 'NGNPrincip':
									index_NGNPrincip = findindex(fc,field_name)-1
								elif field_name == 'NGNAlterno':
									index_NGNAlterno = findindex(fc,field_name)-1
								elif field_name == 'NGCategori':
									index_NGCategori = findindex(fc,field_name)-1
								elif field_name == 'NGIdioma':
									index_NGIdioma = findindex(fc,field_name)-1
								elif field_name == 'NGFuente':
									index_NGFuente = findindex(fc,field_name)-1
								elif field_name == 'NGEMaxima':
									index_NGEMaxima = findindex(fc,field_name)-1
								elif field_name == 'NGEMinima':
									index_NGEMinima = findindex(fc,field_name)-1
								elif field_name == 'NGIORelaci':
									index_NGIORelaci = findindex(fc,field_name)-1
								
							for row in cursor:
								#arcpy.AddMessage('row: ' + str(row)) # ((4729113.535837, 1721752.2366704997), None, 'Estación de Gasolina', None, 2, 3, None, 1, None, None, None, '18410000200102', 2, None)
								# Security if Identif is NULL
								if row[1] == None:
									row1 = '(NULL)'
								else:
									row1 = row[1]
								#arcpy.AddMessage('row1: ' + row1)
								ruleid = row[index_RuleID]
								#arcpy.AddMessage('ruleid: ' + str(ruleid)) # NICO
								ngnpri = row[index_NGNPrincip]
								ngnalt = row[index_NGNAlterno]
								categoria = row[index_NGCategori]
								#arcpy.AddMessage('categoria: ' + str(categoria)) # NICO
								ngnid = row[index_NGIdioma]
								ngnfuente = row[index_NGFuente]
								ngnmax = row[index_NGEMaxima]
								ngnmin = row[index_NGEMinima]
								ngnrelac = row[index_NGIORelaci]
								if(ruleid!=categoria):
									arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +', los campos Categoria y RuleId son diferentes, los valores son: '+str(categoria) + ', '+ str(ruleid)+' respectivamente.')
									filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +', los campos Categoria y RuleId son diferentes, los valores son: '+str(categoria) + ', '+ str(ruleid)+' respectivamente.' + "\n")
									i+=1
								if(ngnpri=='Null' or ngnpri=='NULO' or ngnpri=='Nulo' or ngnpri=='nulo' or ngnpri=='' or ngnpri=='NULL' or ngnpri=='null'):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +' el campo NGNPrincip, se encuentra mal diligenciado, el valor diligenciado es: '+str(ngnpri))
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +' el campo NGNPrincip, se encuentra mal diligenciado, el valor diligenciado es: '+str(ngnpri) + "\n")
										i+=1
								if(ngnalt=='Null' or ngnalt=='NULO' or ngnalt=='Nulo' or ngnalt=='nulo' or ngnalt=='' or ngnalt=='NULL' or ngnalt=='null'):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +' el campo NGNAlterno, se encuentra mal diligenciado, el valor diligenciado es: '+str(ngnalt))
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +' el campo NGNAlterno, se encuentra mal diligenciado, el valor diligenciado es: '+str(ngnalt) + "\n")
										i+=1
								if(ngnid=='Null' or ngnid=='NULO' or ngnid=='Nulo' or ngnid=='nulo' or ngnid=='' or ngnid=='NULL' or ngnid=='null'):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +' el campo NGNIdioma, se encuentra mal diligenciado, el valor diligenciado es: '+str(ngnid))
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +' el campo NGNIdioma, se encuentra mal diligenciado, el valor diligenciado es: '+str(ngnid) + "\n")
										i+=1
								if(ngnfuente=='Null' or ngnfuente=='NULO' or ngnfuente=='Nulo' or ngnfuente=='nulo' or ngnfuente=='' or ngnfuente=='NULL' or ngnfuente=='null'):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +' el campo NGNFuente, se encuentra mal diligenciado, el valor diligenciado es: '+str(ngnfuente))
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +' el campo NGNFuente, se encuentra mal diligenciado, el valor diligenciado es: '+str(ngnfuente) + "\n")
										i+=1
								if(ngnmax=='Null' or ngnmax=='NULO' or ngnmax=='Nulo' or ngnmax=='nulo' or ngnmax=='' or ngnmax=='NULL' or ngnmax=='null'):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +' el campo NGNMaxima, se encuentra mal diligenciado, el valor diligenciado es: '+str(ngnmax))
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +' el campo NGNMaxima, se encuentra mal diligenciado, el valor diligenciado es: '+str(ngnmax) + "\n")
										i+=1
								if(ngnmin=='Null' or ngnmin=='NULO' or ngnmin=='Nulo' or ngnmin=='nulo' or ngnmin=='' or ngnmin=='NULL' or ngnmin=='null'):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +' el campo NGNMinima, se encuentra mal diligenciado, el valor diligenciado es: '+str(ngnmin))
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +' el campo NGNMinima, se encuentra mal diligenciado, el valor diligenciado es: '+str(ngnmin) + "\n")
										i+=1
								if(ngnrelac=='Null' or ngnrelac=='NULO' or ngnrelac=='Nulo' or ngnrelac=='nulo' or ngnrelac=='' or ngnrelac=='NULL' or ngnrelac=='null'):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +' el campo NGNRelac, se encuentra mal diligenciado, el valor diligenciado es: '+str(ngnrelac))
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +' el campo NGNRelac, se encuentra mal diligenciado, el valor diligenciado es: '+str(ngnrelac) + "\n")
										i+=1
							'''
							arcpy.AddField_management(fc, "ConcNgnc", "TEXT", 200, "", "", "", "", "")
							exp3 = '[NGNPrincip] & "_" & [NGCategori]'
							arcpy.CalculateField_management(fc, "ConcNgnc", exp3, "VB")
							fld_cave2 = 'ConcNgnc'
							caves2 = list(set(r[0] for r in arcpy.da.SearchCursor(fc,fld_cave2)))
							tableng2 = rutasalida + "\\Ngeog.dbf"
							arcpy.CreateTable_management (rutasalida, "Ngeog.dbf")
							arcpy.AddField_management(tableng2, "NameLayer", "TEXT", 200, "", "", "", "", "")
							arcpy.AddField_management(tableng2, "FREQUENCY", "LONG", 0, "", "", "", "", "")
							arcpy.AddField_management(tableng2, "COUNT", "LONG", 0, "", "", "", "", "")
							arcpy.AddMessage('Analizando Repeticion de Nombres y Categorias de NG...')
							for cave in caves2:
								where = '"{0}" = \'{1}\''.format(fld_cave2, cave)    
								caveObj = arcpy.MakeFeatureLayer_management(fc, "cave", where)
								caven = elimina_tildes(cave)
								outFS = os.path.join(rutasalida, caven + '.dbf')
								arcpy.Statistics_analysis(caveObj, outFS , [["ConcNgnc", "COUNT"]])
								arcpy.AddField_management(outFS, "NameLayer", "TEXT", 200, "", "", "", "", "")
								exp2 = '"'+cave+'"'
								arcpy.CalculateField_management(outFS, "NameLayer", exp2, "PYTHON_9.3")
								arcpy.Append_management(outFS, tableng2, "NO_TEST","","")
								arcpy.Delete_management("cave")
								arcpy.Delete_management(outFS)
							field_names2 = [j.name for j in arcpy.ListFields(tableng2) if j.type != 'OID']
							cursor2 = arcpy.da.SearchCursor(tableng2, field_names2)
							for row2 in cursor2:
								name = row2[1].split('_')[0]
								cat = row2[1].split('_')[1]
								cat = 'Null' if cat=='' else cat
								name = 'Null' if name=='' else name
								frec = row2[2]
								if frec > 1:
									arcpy.AddMessage('En el Featureclass ' +fc+' el elemento con nombre: '+name+', se encuentra repetido '+str(frec) +' veces, junto con la categoria, la cual es: '+str(cat))
									filet.write('En el Featureclass ' +fc+' el elemento con nombre: '+name+', se encuentra repetido '+str(frec) +' veces, junto con la categoria, la cual es: '+str(cat) + "\n")
									i+=1
							arcpy.DeleteField_management(fc, ["ConcNgnc"])
							arcpy.Delete_management(tableng2) '''
							if i == 0:
								arcpy.AddMessage('--- Ningún problema (RuleID)')
							else:
								arcpy.AddMessage('En el Featureclass ' +fc+' el numero de errores encontrados son: '+ str(i))
								filet.write('En el Featureclass ' +fc+' el numero de errores encontrados son: '+ str(i) + "\n")
						else:
							arcpy.AddMessage('El FeatureClass '+fc +' se encuentra vacio')
							filet.write('El FeatureClass '+fc +' se encuentra vacio' + "\n")
					except Exception as ex:
						arcpy.AddMessage("Error..."+ex.message)
			if(dataset=="Transporte"):
				fcList = arcpy.ListFeatureClasses()
				#arcpy.AddMessage('fcList: ' + str(fcList)) #
				for fc in fcList:
					arcpy.AddMessage('---Analizando FeatureClass '+fc)
					#arcpy.AddMessage('-------------------------------------------------')
					# Checking that feature class is not empty
					result = int(arcpy.GetCount_management(fc).getOutput(0))
					if result == 0:
						arcpy.AddMessage('> Feature Class ' + str(fc) + ' está vacía. No se controla.')
						arcpy.AddMessage(' ')
						continue
					else:
						arcpy.AddMessage('> Feature Class ' + str(fc) + ' tiene ' + str(result) + ' entidade(s) para controlar')
					arcpy.AddMessage('> Buscar campos vacíos') #
					vacios(fc)
					arcpy.AddMessage(' ') #
					arcpy.AddMessage('> Buscar repetido') #
					repetido(fc)
					arcpy.AddMessage(' ') #
					arcpy.AddMessage('> Verificación del identificador y del RuleID') #
					try:
						if result>0:
							arcpy.AddMessage('-conse_field funcion')
							conse_field(fc)
							aliasn = arcpy.Describe(fc).aliasName
							#filet.write("\n \n")
							#arcpy.AddMessage('-Analizando FeatureClass '+fc)
							#filet.write('Analizando FeatureClass '+fc + "\n")
							field_names = [i.name for i in arcpy.ListFields(fc) if i.type != 'OID']
							cursor = arcpy.da.SearchCursor(fc, field_names)
							i=0
							for field_name in field_names:
								if field_name == 'RuleID':
									#arcpy.AddMessage("-->field_name: " + field_name)
									index_RuleID = findindex(fc,field_name)-1
									#arcpy.AddMessage("index_RuleID: " + str(index_RuleID))
								elif field_name == 'PuFuncion':
									#arcpy.AddMessage("-->field_name: " + field_name)
									index_PuFuncion = findindex(fc,field_name)-1
									#arcpy.AddMessage("index_PuFuncion: " + str(index_PuFuncion))
								elif field_name == 'VTipo':
									#arcpy.AddMessage("-->field_name: " + field_name)
									index_VTipo = findindex(fc,field_name)-1
									#arcpy.AddMessage("index_VTipo: " + str(index_VTipo))
								elif field_name == 'VEstado':
									#arcpy.AddMessage("-->field_name: " + field_name)
									index_VEstado = findindex(fc,field_name)-1
									#arcpy.AddMessage("index_VEstado: " + str(index_VEstado))
								elif field_name == 'VCarril':
									#arcpy.AddMessage("-->field_name: " + field_name)
									index_VCarril = findindex(fc,field_name)-1
									#arcpy.AddMessage("index_VCarril: " + str(index_VCarril))
								elif field_name == 'VAcceso':
									#arcpy.AddMessage("-->field_name: " + field_name)
									index_VAcceso = findindex(fc,field_name)-1
									#arcpy.AddMessage("index_VAcceso: " + str(index_VAcceso))
								elif field_name == 'VFTipo':
									#arcpy.AddMessage("-->field_name: " + field_name)
									index_VFTipo = findindex(fc,field_name)-1
									#arcpy.AddMessage("index_VFTipo: " + str(index_VFTipo))
								elif field_name == 'LVTipo':
									#arcpy.AddMessage("-->field_name: " + field_name)
									index_LVTipo = findindex(fc,field_name)-1
									#arcpy.AddMessage("index_LVTipo: " + str(index_LVTipo))
								#else:
								#	arcpy.AddMessage("-->>" + field_name + " is not used")
							for row in cursor:
								if(fc=='Puente_P'):
									ruleid = row[index_RuleID]
									funcion = row[index_PuFuncion]
									if(ruleid!=funcion):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+', los campos Funcion y RuleId son diferentes, los valores son: '+str(funcion) + ', '+ str(ruleid)+' respectivamente.')
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+', los campos Funcion y RuleId son diferentes, los valores son: '+str(funcion) + ', '+ str(ruleid)+' respectivamente.' + "\n")
										i+=1
								elif(fc=='Puente_L'):
									ruleid = row[index_RuleID]
									funcion = row[index_PuFuncion]
									if(ruleid!=funcion):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+', los campos Funcion y RuleId son diferentes, los valores son: '+str(funcion) + ', '+ str(ruleid)+' respectivamente.')
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+', los campos Funcion y RuleId son diferentes, los valores son: '+str(funcion) + ', '+ str(ruleid)+' respectivamente.' + "\n")
										i+=1
								elif(fc=='Via'):
									#arcpy.AddMessage('En el Featureclass ' +str(row[0]) +' '+ str(row[1]) +' '+str(row[2]) +' '+str(row[3]) +' '+str(row[4]) +' '+str(row[5]) +' '+str(row[6]) +' '+str(row[7]) +' '+str(row[8]))
									ruleid = row[index_RuleID]
									tipo = row[index_VTipo]
									estado = row[index_VEstado]
									carril = row[index_VCarril]
									acceso = row[index_VAcceso]
									if(ruleid!=tipo):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+', los campos Tipo y RuleId son diferentes, los valores son: '+str(tipo) + ', '+ str(ruleid)+' respectivamente.')
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+', los campos Tipo y RuleId son diferentes, los valores son: '+str(tipo) + ', '+ str(ruleid)+' respectivamente.' + "\n")
										i+=1
									if tipo==1 and (int(estado) not in (1,1) or int(carril) not in (1,1) or int(acceso) not in (1,1)):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+', NO cumple la condicion de Tipo: Via-Primaria, Estado: Pavimentada, Carril:Carretera de 2, Acceso: Permanente')
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+', NO cumple la condicion de Tipo: Via-Primaria, Estado: Pavimentada, Carril:Carretera de 2, Acceso: Permanente' + "\n")
										i+=1
									if tipo==2 and (int(estado) not in (1,2) or int(carril) not in (2,2) or int(acceso) not in (1,1)):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+', NO cumple la condicion de Tipo: Via-Secundaria, Estado: Pavimentada o Sin Pavimentar, Carril: Carretera angosta, Acceso: Permanente')
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+', NO cumple la condicion de Tipo: Via-Secundaria, Estado: Pavimentada o Sin Pavimentar, Carril: Carretera angosta, Acceso: Permanente' + "\n")
										i+=1
									if tipo==3 and (int(estado) not in (2,3) or int(carril) not in (0,0) or int(acceso) not in (2,2)):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+', NO cumple la condicion de Tipo: Via-Terciaria, Estado: Sin Pavimentar o Sin Afirmado, Carril: Sin Valor, Acceso: Temporal')
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+', NO cumple la condicion de Tipo: Via-Terciaria, Estado: Sin Pavimentar o Sin Afirmado, Carril: Sin Valor, Acceso: Temporal' + "\n")
										i+=1
									if tipo==4 and (int(estado) not in (4,4) or int(carril) not in (0,0) or int(acceso) not in (2,2)):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+', NO cumple la condicion de Tipo: Placa Huella, Estado: En Construccion, Carril: Sin Valor, Acceso: Temporal')
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+', NO cumple la condicion de Tipo: Placa Huella, Estado: En Construccion, Carril: Sin Valor, Acceso: Temporal' + "\n")
										i+=1
									elif tipo==5 and (int(estado) not in (0,0) or int(carril) not in (0,0) or int(acceso) not in (0,0)):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+', NO cumple la condicion de Tipo: Camino-Sendero, Estado: Sin Valor, Carril: Sin Valor, Acceso: Sin Valor')
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+', NO cumple la condicion de Tipo: Camino-Sendero, Estado: Sin Valor, Carril: Sin Valor, Acceso: Sin Valor' + "\n")
										i+=1
									elif tipo==6 and (int(estado) not in (0,0) or int(carril) not in (0,0) or int(acceso) not in (0,0)):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+', NO cumple la condicion de Tipo: Via-Peatonal, Estado: Sin Valor, Carril: Sin Valor, Acceso: Sin Valor' + estado)
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+', NO cumple la condicion de Tipo: Via-Peatonal, Estado: Sin Valor, Carril: Sin Valor, Acceso: Sin Valor' + "\n")
										i+=1
									#else:
									#    arcpy.AddMessage('En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+', NO tiene diligenciado el campo Tipo')
									#    filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+', NO tiene diligenciado el campo Tipo' + "\n")
									#    i+=1
								elif(fc=='VFerre'):
									ruleid = row[index_RuleID]
									tipo = row[index_VFTipo]
									if(ruleid!=tipo):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+', los campos Tipo y RuleId son diferentes, los valores son: '+str(tipo) + ', '+ str(ruleid)+' respectivamente.')
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+', los campos Tipo y RuleId son diferentes, los valores son: '+str(tipo) + ', '+ str(ruleid)+' respectivamente.' + "\n")
										i+=1
								elif(fc=='LVia'):
									ruleid = row[index_RuleID]
									tipo = row[index_LVTipo]
									if(ruleid!=tipo):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+', los campos Tipo y RuleId son diferentes, los valores son: '+str(tipo) + ', '+ str(ruleid)+' respectivamente.')
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+', los campos Tipo y RuleId son diferentes, los valores son: '+str(tipo) + ', '+ str(ruleid)+' respectivamente.' + "\n")
										i+=1
								elif(fc=='Tunel'):
									ruleid = row[index_RuleID]
									if(ruleid!=1):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+' se encuentra mal diligenciado el Ruleid, el valor diligenciado es: '+str(ruleid))
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+' se encuentra mal diligenciado el Ruleid, el valor diligenciado es: '+str(ruleid) + "\n")
										i+=1
								elif(fc=='SVial'):
									ruleid = row[index_RuleID]
									if(ruleid!=1):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+' se encuentra mal diligenciado el Ruleid, el valor diligenciado es: '+str(ruleid))
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+' se encuentra mal diligenciado el Ruleid, el valor diligenciado es: '+str(ruleid) + "\n")
										i+=1
								elif(fc=='Ciclor'):
									ruleid = row[index_RuleID]
									if(ruleid!=1):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+' se encuentra mal diligenciado el Ruleid, el valor diligenciado es: '+str(ruleid))
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+' se encuentra mal diligenciado el Ruleid, el valor diligenciado es: '+str(ruleid) + "\n")
										i+=1
								elif(fc=='Telefe'):
									ruleid = row[index_RuleID]
									if(ruleid!=1):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+' se encuentra mal diligenciado el Ruleid, el valor diligenciado es: '+str(ruleid))
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+row[1]+' se encuentra mal diligenciado el Ruleid, el valor diligenciado es: '+str(ruleid) + "\n")
										i+=1
							if i == 0:
								arcpy.AddMessage('--- Ningún problema (RuleID)')
							else:
								arcpy.AddMessage('En el Featureclass ' +fc+' el numero de errores encontrados son: '+ str(i))
								filet.write('En el Featureclass ' +fc+' el numero de errores encontrados son: '+ str(i) + "\n")
						else:
							arcpy.AddMessage('El FeatureClass '+fc +' se encuentra vacio')
							filet.write('El FeatureClass '+fc +' se encuentra vacio' + "\n")
					except Exception as ex:
						arcpy.AddMessage("Error...")# +ex.message) #PB with message
			if(dataset=="ViviendaCiudadTerritorio"):
				fcList = arcpy.ListFeatureClasses()
				for fc in fcList:
					arcpy.AddMessage('---Analizando FeatureClass '+fc)
					#arcpy.AddMessage('-------------------------------------------------')
					# Checking that feature class is not empty
					result = int(arcpy.GetCount_management(fc).getOutput(0))
					if result == 0:
						arcpy.AddMessage('> Feature Class ' + str(fc) + ' está vacía. No se controla.')
						arcpy.AddMessage(' ')
						continue
					else:
						arcpy.AddMessage('> Feature Class ' + str(fc) + ' tiene ' + str(result) + ' entidade(s) para controlar')
					arcpy.AddMessage('> Buscar campos vacíos') #
					vacios(fc)
					arcpy.AddMessage(' ') #
					arcpy.AddMessage('> Buscar repetido') #
					repetido(fc)
					arcpy.AddMessage(' ') #
					arcpy.AddMessage('> Verificación del identificador y del RuleID') #
					try:
						if result>0:
							conse_field(fc)
							aliasn = arcpy.Describe(fc).aliasName
							#filet.write("\n \n")
							#arcpy.AddMessage('Analizando FeatureClass '+fc)
							#filet.write('Analizando FeatureClass '+fc + "\n")
							field_names = [i.name for i in arcpy.ListFields(fc) if i.type != 'OID']
							cursor = arcpy.da.SearchCursor(fc, field_names)
							i=0
							for field_name in field_names:
								if field_name == 'RuleID':
									index_RuleID = findindex(fc,field_name)-1
								elif field_name == 'CTipo':
									index_CTipo = findindex(fc,field_name)-1
								elif field_name == 'CIdentif':
									index_CIdentif = findindex(fc,field_name)-1
								elif field_name == 'CCategor':
									index_CCategor = findindex(fc,field_name)-1
								elif field_name == 'CDescrip':
									index_CDescrip = findindex(fc,field_name)-1
								elif field_name == 'CeTipo':
									index_CeTipo = findindex(fc,field_name)-1
								elif field_name == 'MuTipo':
									index_MuTipo = findindex(fc,field_name)-1
								
							for row in cursor:
								
								if(fc=='Constr_P'):
									#arcpy.AddMessage(str(row[0]) + ' ' +str(row[1]) + ' ' +str(row[2]) + ' ' +str(row[3]) + ' ' + str(row[4]) + ' ' + str(row[5]))
									# Security if Identif is NULL
									if row[1] == None:
										row1 = '(NULL)'
									else:
										row1 = row[1]
									#arcpy.AddMessage('row1: ' + row1)
									ruleid = row[index_RuleID]
									tipo = row[index_CTipo]
									identif = row[index_CIdentif]
									categoria = row[index_CCategor]
									descripcion = row[index_CDescrip]
									if(identif=='Null' or identif=='NULO' or identif=='Nulo' or identif=='nulo' or identif=='' or identif=='NULL' or identif=='null' or identif==str('None')):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' contiene elementos con campo identificador vacio')
										filet.write('En el Featureclass ' +fc+' contiene elementos con campo identificador vacio' + "\n")
										i+=1         
									if(ruleid!=tipo):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +', los campos Tipo y RuleId son diferentes, los valores son: '+str(tipo) + ', '+ str(ruleid)+' respectivamente.')
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +', los campos Tipo y RuleId son diferentes, los valores son: '+str(tipo) + ', '+ str(ruleid)+' respectivamente.' + "\n")
										i+=1                                     
									elif ((categoria == 8 or categoria == 9 or categoria == 10 or categoria == 11 or categoria == 12 or categoria == 13 or categoria == 14 or categoria == 15 or categoria == 16) and (tipo==2)):
										arcpy.AddMessage('')
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +', NO cumple la condicion de Tipo: No Convencional, Categoria: "Agropecuario", "Enramada, cobertizo o caney", "Galpón y gallinero", "Establo y pesebrera", "Cochera, marranera y porqueriza", "Tanque", "Secadero", "Minero", "Cementerio o parque cementerio" u " Otra construcción".')
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +', NO cumple la condicion de Tipo: No Convencional, Categoria: "Agropecuario", "Enramada, cobertizo o caney", "Galpón y gallinero", "Establo y pesebrera", "Cochera, marranera y porqueriza", "Tanque", "Secadero", "Minero", "Cementerio o parque cementerio" u " Otra construcción".' + "\n")
										i+=1
									elif ((categoria == 1 or categoria == 2 or categoria == 3 or categoria == 4 or categoria == 5 or categoria == 6 or categoria == 7) and (tipo==1)):
										arcpy.AddMessage('')
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +', NO cumple la condicion de Tipo: Convencional, Categoria: "Residencial", "Comercial", "Industrial", "Educativo", "Institucional", "Recreacional" o "Religioso". u " Otra construcción".')
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +', NO cumple la condicion de Tipo: Convencional, Categoria: "Residencial", "Comercial", "Industrial", "Educativo", "Institucional", "Recreacional" o "Religioso". u " Otra construcción".' + "\n")
										i+=1
									elif(tipo=='Null' or tipo=='NULO' or tipo=='Nulo' or tipo=='nulo' or tipo=='' or tipo=='NULL' or tipo=='null'):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +', NO tiene diligenciado el campo Tipo')
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +', NO tiene diligenciado el campo Tipo' + "\n")
										i+=1
									if(descripcion=='Null' or descripcion=='NULO' or descripcion=='Nulo' or descripcion=='nulo' or descripcion==''):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +' el campo Descripcion, se encuentra mal diligenciado, el valor diligenciado es: '+str(descripcion))
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +' el campo Descripcion, se encuentra mal diligenciado, el valor diligenciado es: '+str(descripcion) + "\n")
										i+=1
								elif(fc=='Cerca'):
									ruleid = row[index_RuleID]
									tipo = row[index_CeTipo]
									if(ruleid!=tipo):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +', los campos Tipo y RuleId son diferentes, los valores son: '+str(tipo) + ', '+ str(ruleid)+' respectivamente.')
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +', los campos Tipo y RuleId son diferentes, los valores son: '+str(tipo) + ', '+ str(ruleid)+' respectivamente.' + "\n")
										i+=1
								elif(fc=='Muro'):
									ruleid = row[index_RuleID]
									tipo = row[index_MuTipo]
									if(ruleid!=1):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +', se encuentra mal diligenciado el Ruleid, el valor diligenciado es: '+str(ruleid))
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +', se encuentra mal diligenciado el Ruleid, el valor diligenciado es: '+str(ruleid) + "\n")
										i+=1
								elif(fc=='Piscin'):
									ruleid = row[index_RuleID]
									if(ruleid!=1):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +' se encuentra mal diligenciado el Ruleid, el valor diligenciado es: '+str(ruleid))
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +' se encuentra mal diligenciado el Ruleid, el valor diligenciado es: '+str(ruleid) + "\n")
										i+=1
								elif(fc=='ZDura'):
									ruleid = row[index_RuleID]
									tipo = row[2]
									if(ruleid!=1):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +' se encuentra mal diligenciado el Ruleid, el valor diligenciado es: '+str(ruleid))
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +' se encuentra mal diligenciado el Ruleid, el valor diligenciado es: '+str(ruleid) + "\n")
										i+=1
								elif(fc=='Constr_R'):
									ruleid = row[index_RuleID]
									descripcion = row[index_CDescrip]
									tipo = row[index_CTipo]
									if(ruleid!=tipo):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +', los campos Tipo y RuleId son diferentes, los valores son: '+str(tipo) + ', '+ str(ruleid)+' respectivamente.')
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +', los campos Tipo y RuleId son diferentes, los valores son: '+str(tipo) + ', '+ str(ruleid)+' respectivamente.' + "\n")
										i+=1
									if(descripcion=='Null' or descripcion=='NULO' or descripcion=='Nulo' or descripcion=='nulo' or descripcion=='' or descripcion=='NULL' or descripcion=='null'):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +' el campo Descripcion, se encuentra mal diligenciado, el valor diligenciado es: '+str(descripcion))
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +' el campo Descripcion, se encuentra mal diligenciado, el valor diligenciado es: '+str(descripcion) + "\n")
										i+=1
								elif(fc=='Terrap'):
									ruleid = row[index_RuleID]
									if(ruleid!=1):
										arcpy.AddMessage('---ERROR - En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +' se encuentra mal diligenciado el Ruleid, el valor diligenciado es: '+str(ruleid))
										filet.write('En el Featureclass ' +fc+' el elemento con identificador: '+ row1 +' se encuentra mal diligenciado el Ruleid, el valor diligenciado es: '+str(ruleid) + "\n")
										i+=1
							if i == 0:
								arcpy.AddMessage('--- Ningún problema (RuleID)')
							else:
								arcpy.AddMessage('En el Featureclass ' +fc+' el numero de errores encontrados son: '+ str(i))
								filet.write('En el Featureclass ' +fc+' el numero de errores encontrados son: '+ str(i) + "\n")
						else:
							arcpy.AddMessage('El FeatureClass '+fc +' se encuentra vacio')
							filet.write('El FeatureClass '+fc +' se encuentra vacio' + "\n")
					except Exception as ex:
						arcpy.AddMessage("Error..."+ex.message)
	arcpy.AddMessage('Analisis Terminado...Revisar el reporte LOG')
	filet.write("\n \n")
	filet.write('Analisis Terminado.\n')
else:
	arcpy.AddMessage("Validacion tablas GDB: NO")
#########################################################################################################

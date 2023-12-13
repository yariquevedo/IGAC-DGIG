import arcpy
import os,re, math


_name_='_main_'

def getworkspacedatset(dtaset):
 try:
    ndataset=""
    wsp=""
    lruta=dtaset.split(os.sep)
    ndataset= lruta[len(lruta)-1]
    wsp=dtaset.replace(os.sep+ndataset,"")
    return wsp, ndataset
 except:
     import traceback
     arcpy.AddError(traceback.format_exc())

def VerificarDrenajeEnds(dstCAgua,gdb):
  try:
    arcpy.AddMessage("---Verificando diredccion drenajes---")
    drSencillo= dstCAgua+ os.sep+ "Drenaj_L"
    tempdrenaje=gdbOut+os.sep+"temp_dreneje"
    ptdrenaje=gdbOut+os.sep+"puntos_drenaje"
    out_Pol="Poligonos"
    rutaPol=gdb + os.sep+out_Pol
    out_Linea="Linea"
    rutaLinea=gdb + os.sep+out_Linea
    puntoerease=gdb + os.sep+"puntos_earease"
    lypterase=gdb + os.sep+"Ly_puntos_earease"
    ptintermedios=gdb + os.sep+"Puntos_intermedios"
    intputosdr=gdb + os.sep+"Int_puntos_dr"
    lypuntos=gdb + os.sep+"ly_Int_puntos_dr"
    lypuntosdef=gdb + os.sep+"ly_puntos_def"
    puntosdef=gdb + os.sep+"Puntos_revision"

    if arcpy.Exists(tempdrenaje )== True:
            arcpy.Delete_management(tempdrenaje)
    if arcpy.Exists(ptdrenaje)== True:
            arcpy.Delete_management(ptdrenaje)
    if arcpy.Exists(rutaLinea)== True:
            arcpy.Delete_management(rutaLinea)
    if arcpy.Exists(rutaPol)== True:
            arcpy.Delete_management(rutaPol)
    if arcpy.Exists(puntoerease)== True:
            arcpy.Delete_management(puntoerease)
    if arcpy.Exists(lypterase)== True:
            arcpy.Delete_management(lypterase)
    if arcpy.Exists(ptintermedios)== True:
            arcpy.Delete_management(ptintermedios)
    if arcpy.Exists(intputosdr)== True:
            arcpy.Delete_management(intputosdr)
    if arcpy.Exists(lypuntos)== True:
            arcpy.Delete_management(lypuntos)
    if arcpy.Exists(lypuntosdef)== True:
            arcpy.Delete_management(lypuntosdef)
    if arcpy.Exists(puntosdef)== True:
            arcpy.Delete_management(puntosdef)

    if arcpy.Exists(drSencillo)== True:
      arcpy.AddMessage("-----Generando vertices---")
      arcpy.CopyFeatures_management(drSencillo, tempdrenaje)
      arcpy.AddField_management(tempdrenaje,"IDDREN","LONG")
      exp= "!OBJECTID!"
      arcpy.CalculateField_management(tempdrenaje, "IDDREN", exp, "PYTHON_9.3")
      arcpy.FeatureVerticesToPoints_management(tempdrenaje, ptdrenaje, "END")
      arcpy.AddMessage("-----Generando Layer linea y poligono intermedios---")
      spr=arcpy.Describe(dstCAgua).spatialReference
      arcpy.CreateFeatureclass_management(gdb, out_Pol, "POLYGON","","","",spr)
      arcpy.CreateFeatureclass_management(gdb, out_Linea, "POLYLINE","","","",spr)
      ws,dtset = getworkspacedatset(dstCAgua)
      arcpy.env.workspace =ws
      fcListPol = arcpy.ListFeatureClasses("*","polygon",dtset)
      fcListLine=arcpy.ListFeatureClasses("*","polyline",dtset)

      for fcPol in fcListPol:
        if arcpy.Exists(fcPol)== True:
           nelementos=int(arcpy.GetCount_management(fcPol).getOutput(0))

           if nelementos>0 :
              arcpy.Append_management([fcPol], rutaPol,"NO_TEST")

      for fcLine in fcListLine:
        if arcpy.Exists(fcLine)== True:
           nelementos=int(arcpy.GetCount_management(fcLine).getOutput(0))
           descf= arcpy.Describe(fcLine)
           if nelementos>0 and descf.name != "Drenaj_L" :
              arcpy.Append_management([fcLine], rutaLinea,"NO_TEST")

      arcpy.AddMessage("-----seleccionando vertices---")
      arcpy.Erase_analysis(ptdrenaje, rutaPol, puntoerease)
      arcpy.MakeFeatureLayer_management(puntoerease, lypterase)
      arcpy.SelectLayerByLocation_management(lypterase, "INTERSECT", rutaLinea, "", "NEW_SELECTION", "INVERT")
      arcpy.CopyFeatures_management(lypterase, ptintermedios)
      if int(arcpy.GetCount_management(ptintermedios).getOutput(0))>0:
        arcpy.Intersect_analysis([ptintermedios,tempdrenaje], intputosdr, "ALL")
        if gdb.find("mdb")!=-1:
         qryrev="[IDDREN]"+ " <> " +"[IDDREN_1]"
        else:
         qryrev="\"" + "IDDREN" +"\""+ " <> " +"\"" + "IDDREN_1" +"\""
        idsdr=[]
        arcpy.MakeFeatureLayer_management(intputosdr,lypuntos, qryrev)
        cursor = arcpy.SearchCursor(lypuntos)
        for row in cursor:
          iddren= row.getValue("IDDREN")
          idsdr.append(iddren)
        del cursor
        qryrev=""
        for nid in idsdr:
          if qryrev=="":
           if gdb.find("mdb")!=-1:
             qryrev="[IDDREN]"+ " NOT IN (" +str(nid)
           else:
            qryrev="\"" + "IDDREN" +"\""+ " NOT IN (" +str(nid)
          else:
           qryrev=qryrev +" , " + str(nid)
        if qryrev!= "":
         qryrev=qryrev +" )"
         arcpy.MakeFeatureLayer_management(ptintermedios, lypuntosdef,qryrev )
         arcpy.CopyFeatures_management(lypuntosdef, puntosdef)
        else:
         arcpy.AddMessage("---No se Encontraron Inconsistencias---")

    else:
        arcpy.AddMessage("---No se Encontro El Feature Class Drenaje Sencillo---")
    if arcpy.Exists(tempdrenaje )== True:
            arcpy.Delete_management(tempdrenaje)
    if arcpy.Exists(ptdrenaje)== True:
            arcpy.Delete_management(ptdrenaje)
    if arcpy.Exists(rutaLinea)== True:
            arcpy.Delete_management(rutaLinea)
    if arcpy.Exists(rutaPol)== True:
            arcpy.Delete_management(rutaPol)
    if arcpy.Exists(puntoerease)== True:
            arcpy.Delete_management(puntoerease)
    if arcpy.Exists(lypterase)== True:
            arcpy.Delete_management(lypterase)
    if arcpy.Exists(ptintermedios)== True:
            arcpy.Delete_management(ptintermedios)
    if arcpy.Exists(intputosdr)== True:
            arcpy.Delete_management(intputosdr)
    if arcpy.Exists(lypuntos)== True:
            arcpy.Delete_management(lypuntos)
    if arcpy.Exists(lypuntosdef)== True:
            arcpy.Delete_management(lypuntosdef)

  except:
     import traceback
     arcpy.AddError(traceback.format_exc())



if _name_=='_main_':
    dstCAgua=arcpy.GetParameterAsText(0)
    gdbOut=arcpy.GetParameterAsText(1)

    VerificarDrenajeEnds(dstCAgua,gdbOut)







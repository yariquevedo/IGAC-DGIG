import arcpy,os,sys, string
from arcpy import env
arcpy.env.workspace = arcpy.GetParameterAsText(0)
path = arcpy.GetParameterAsText(1)
##arcpy.env.workspace = r'D:\IGAC\2022\Carto1000_20750001_20211218.gdb'
##path = r'D:\IGAC\2022'
arcpy.CheckOutExtension("spatial")
file = open(os.path.join(path,'Error_Tablas.txt'), "w")
fdmdb = arcpy.ListDatasets()
try:
    for fds in fdmdb:
        features = arcpy.ListFeatureClasses(feature_dataset=fds)
        for fc in features:
            if arcpy.Exists(fc)== True:
                print('Process.....')
                def feature(fc):
                    feature_ly =arcpy.MakeFeatureLayer_management(fc, fc+'_ly'+'null')
                    fields = ['OBJECTID', 'RuleID']
                    with arcpy.da.SearchCursor(feature_ly , fields) as cursor:
                        for row in cursor:
                            if row[1] is None:
                                file.write(fc + " RuleID Null," + " " + "ObjectID: " + " " +  str(row[0]) + " " + "\n")
                feature('AExtra')
                feature('Bosque')
                feature('ZVerde')
                feature('CNivel')
                feature('LDTerr')
                feature('MRTerr')
                feature('BArena')
                feature('DAgua_P')
                feature('DAgua_R')
                feature('Drenaj_L')
                feature('Humeda')
                feature('Isla')
                feature('Mangla')
                feature('Drenaj_R')
                feature('DAgua_L')
                feature('Indice')
                feature('PDistr')
                feature('Pozo')
                feature('RATens')
                feature('TSPubl')
                feature('Tuberi')
                feature('NGeogr')
                feature('Depart')
                feature('LLimit')
                feature('Fronte')
                feature('MDANMu')
                feature('LVia')
                feature('Puente_L')
                feature('SVial')
                feature('Tunel')
                feature('VFerre')
                feature('Via')
                feature('Ciclor')
                feature('Puente_P')
                feature('Telefe')
                feature('Cerca')
                feature('Constr_P')
                feature('Constr_R')
                feature('Muro')
                feature('Piscin')
                feature('ZDura')
                feature('Terrap')
                feature('LDemar')                 
                
                def CNivel(fc):
                    CNivel_ly = arcpy.MakeFeatureLayer_management("CNivel", "CNivel_ly")
                    fields = ['OBJECTID', 'CNTipo','RuleID']
                    with arcpy.da.SearchCursor(CNivel_ly, fields) as cursor:
                        for row in cursor:
                            if row[1] <> row[2]:
                                print("{}".format(str(row[0])))
                                file.write("Curva Tipo-RuleID," + " " + "ObjectID: " + " " + str(row[0])  + " " + "\n")
                CNivel("CNivel_ly")
                
                def P_Distr(fc):
                    P_Distr_ly =arcpy.MakeFeatureLayer_management("PDistr", "P_Distr_ly")
                    fields = ['OBJECTID', 'PDTipo', 'RuleID']
                    with arcpy.da.SearchCursor(P_Distr_ly, fields) as cursor:
                        for row in cursor:
                            if row[1] == 1 and row[2] <> 1 or row[1] == 2 and row[2] <> 3 or row[1] == 3 and row[2] <> 2:
                                file.write("PDistr Tipo-RuleID," + " " + "ObjectID: " + " " +  str(row[0]) + " " + "\n")
                P_Distr("P_Distr_ly")

                def NGeogr(fc):
                    NGeogr_ly =arcpy.MakeFeatureLayer_management("NGeogr", "NGeogr_ly")
                    fields = ['OBJECTID', 'NGCategori', 'NGSubcateg', 'NGEstado', 'RuleID']
                    with arcpy.da.SearchCursor(NGeogr_ly , fields) as cursor:
                        for row in cursor:
                            if row[1] <> row[4] and row[4] not in [15,16,17,18] or row[1] <> 3 and row[4] in [3,17,18] or row[1] <> 7 and row[4] in [7,15,16] or row[1] <> 14 and row[4] in [14]:
                                file.write("NGeogr Categ-RuleID," + " " + "ObjectID: " + " " +  str(row[0]) + " " + "\n")
                NGeogr("NGeogr_ly")
                
                def Constr_P(fc):
                    Constr_P_ly =arcpy.MakeFeatureLayer_management("Constr_P", "Constr_P_ly")
                    fields = ['OBJECTID', 'CTipo', 'RuleID']
                    with arcpy.da.SearchCursor(Constr_P_ly , fields) as cursor:
                        for row in cursor:
                            if row[1] <> row[2]:
                                file.write("Constr_P Tipo-RuleID," + " " + "ObjectID: " + " " +  str(row[0]) + " " + "\n")
                Constr_P("Constr_P_ly")

                def LDTerr(fc):
                    LDTerr_ly =arcpy.MakeFeatureLayer_management("LDTerr", 'LDTerr_ly')
                    fields = ['OBJECTID', 'LDTTipo', 'LDTFuente']
                    with arcpy.da.SearchCursor(LDTerr_ly , fields) as cursor:
                        for row in cursor:
                            if row[1] is None or row[2] is None:
                                file.write("LDTerr LDTTipo o LDTFuente es Null," + " " + "ObjectID: " + " " +  str(row[0]) + " " + "\n")
                LDTerr('LDTerr')

                def Drenaj_L(fc):
                    Drenaj_L_ly =arcpy.MakeFeatureLayer_management("Drenaj_L", "Drenaj_L_ly")
                    fields = ['OBJECTID', 'DEstado', 'DDisperso','DNombre', 'RuleID']
                    with arcpy.da.SearchCursor(Drenaj_L_ly , fields) as cursor:
                        for row in cursor:
                            if row[1] == 1 and row[2] == '1' and row[4]<> 4 or row[1] == 1 and row[2] == '2' and row[4]<> 3 or row[1] == 2 and row[2] == '1' and row[4]<> 2 or row[1] == 2 and row[2] == '2' and row[4]<> 1 or row[1] == 3 and row[2] not in [None] or row[1] == 3 and row[4]<> 5 or row[2] in ["", " "] or row[3] in ["", " "] or row[4] is [None] or row[1] == 2 and row[3] not in [None]:
                                file.write("Drenaj_L DEstado-RuleID," + " " + "ObjectID: " + " " +  str(row[0]) + " " + "\n")
                            if row[1] == 1 and row[3] in ["", None, " "]:
                                file.write("Drenaj_L DEstado-RuleID," + " " + "ObjectID: " + " " +  str(row[0]) + " " + "\n")
                Drenaj_L("Drenaj_L_ly")
                
                def Drenaj_R(fc):
                    Drenaj_R_ly =arcpy.MakeFeatureLayer_management("Drenaj_R", "Drenaj_R_ly")
                    fields = ['OBJECTID', 'DTipo', 'DNombre', 'RuleID']
                    with arcpy.da.SearchCursor(Drenaj_R_ly, fields) as cursor:
                        for row in cursor:
                            if row[1] <> row[3] or row[1]==2 and row[2] in ["", None, " "] or row[1]==1 and row[2] not in ["", None, " "]:
                                file.write("Drenaj_R DTipo-RuleID," + " " + "ObjectID: " + " " +  str(row[0]) + " " + "\n")
                Drenaj_R("Drenaj_L_ly")

                def Puente_P(fc):
                    Puente_P_ly =arcpy.MakeFeatureLayer_management("Puente_P", "Puente_P_ly")
                    fields = ['OBJECTID', 'PuFuncion', 'RuleID']
                    with arcpy.da.SearchCursor(Puente_P_ly, fields) as cursor:
                        for row in cursor:
                            if row[1] <> row[2]:
                                file.write("Puente_P Funcion-RuleID," + " " + "ObjectID: " + " " +  str(row[0]) + " " + "\n")
                Puente_P("Puente_P_ly")

                def Puente_L(fc):
                    Puente_L_ly =arcpy.MakeFeatureLayer_management("Puente_L", "Puente_L_ly")
                    fields = ['OBJECTID', 'PuFuncion', 'RuleID']
                    with arcpy.da.SearchCursor(Puente_L_ly, fields) as cursor:
                        for row in cursor:
                            if row[1] <> row[2]:
                                file.write("Puente_L Funcion-RuleID," + " " + "ObjectID: " + " " +  str(row[0]) + " " + "\n")
                Puente_L("Puente_L_ly")
                
                def LVia(fc):
                    LVia_ly =arcpy.MakeFeatureLayer_management("LVia", "LVia_ly")
                    fields = ['OBJECTID', 'LVTipo', 'RuleID']
                    with arcpy.da.SearchCursor(LVia_ly , fields) as cursor:
                        for row in cursor:
                            if row[1] <> row[2]:
                                file.write("LVia Tipo-RuleID," + " " + "ObjectID: " + " " +  str(row[0]) + " " + "\n")
                LVia("LVia_ly")

                def Via(fc):
                    Via_ly =arcpy.MakeFeatureLayer_management("Via", "Via_ly")
                    fields = ['OBJECTID', 'VTipo', 'RuleID']
                    with arcpy.da.SearchCursor(Via_ly , fields) as cursor:
                        for row in cursor:
                            if row[1] <> row[2]:
                                file.write("Via Tipo-RuleID," + " " + "ObjectID: " + " " +  str(row[0]) + " " + "\n")
                Via("Via_ly")

                def VFerre(fc):
                    VFerre_ly =arcpy.MakeFeatureLayer_management("VFerre", "VFerre_ly")
                    fields = ['OBJECTID', 'VFTipo', 'RuleID']
                    with arcpy.da.SearchCursor(VFerre_ly , fields) as cursor:
                        for row in cursor:
                            if row[1] <> row[2]
				((row[1] <> row[5])or
                                (row[1] == 6 and row[3] <> '0') or
                                (row[1] == 1 and row[2] <> '1') or
                                (row[1] == 1 and row[3] <> '1') or
                                (row[1] == 1 and row[4] <> '1') or
                                (row[1] == 2 and row[2] not in ['1','2']) or
                                (row[1] == 2 and row[3] <> '2') or
                                (row[1] == 2 and row[4] <> '1') or
                                (row[1] == 3 and row[2] not in ['2','3'])or
                                (row[1] == 3 and row[3] <> '0') or
                                (row[1] == 3 and row[4] <> '2') or
                                (row[1] == 4 and row[2] <> '4') or
                                (row[1] == 4 and row[3] <> '0') or
                                (row[1] == 4 and row[4] <> '2') or
                                (row[1] == 5 and row[2] <> '0') or
                                (row[1] == 5 and row[3] <> '0') or
                                (row[1] == 5 and row[4] <> '0') or
                                (row[1] == 6 and row[2] <> '0') or
                                (row[1] == 6 and row[3] <> '0') or
                                (row[1] == 6 and row[4] <> '0')
                                ):
                                file.write("VFerre Tipo-RuleID," + " " + "ObjectID: " + " " +  str(row[0]) + " " + "\n")
                VFerre("VFerre_ly")
                

                def Cerca(fc):
                    Cerca_ly =arcpy.MakeFeatureLayer_management("Cerca", "Cerca_ly")
                    fields = ['OBJECTID', 'CeTipo', 'RuleID']
                    with arcpy.da.SearchCursor(Cerca_ly , fields) as cursor:
                        for row in cursor:
                            if row[1] <> row[2]:
                                file.write("Cerca Tipo-RuleID," + " " + "ObjectID: " + " " +  str(row[0]) + " " + "\n")
                Cerca("Cerca_ly")
                
                def DAgua_R(fc):
                    DAgua_R_ly =arcpy.MakeFeatureLayer_management("DAgua_R", "DAgua_R_ly")
                    fields = ['OBJECTID','DATipo', 'RuleID']
                    with arcpy.da.SearchCursor(DAgua_R_ly , fields) as cursor:
                        for row in cursor:
                            if row[1] <> row[2]:
                                file.write("DAgua_R Tipo_RuleID," + " " + "ObjectID: " + " " +  str(row[0]) + " " + "\n")
                DAgua_R("DAgua_R_ly")

                def Constr_R(fc):
                    Constr_R_ly =arcpy.MakeFeatureLayer_management("Constr_R", "Constr_R_ly")
                    fields = ['OBJECTID','CTipo', 'RuleID']
                    with arcpy.da.SearchCursor(Constr_R_ly , fields) as cursor:
                        for row in cursor:
                            if row[1] <> row[2]:
                                file.write("Constr_R Tipo_RuleID," + " " + "ObjectID: " + " " +  str(row[0]) + " " + "\n")
                Constr_R("Constr_R_ly")
                print('Lastone Process.....')
                
        file.close()
        break                     
except:
    print(arcpy.GetMessages())




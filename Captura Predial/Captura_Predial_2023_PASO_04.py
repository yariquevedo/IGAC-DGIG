import arcpy 
import os 
gdb = arcpy.GetParameterAsText(0)
salida = arcpy.GetParameterAsText(1)
inspeccion = arcpy.GetParameterAsText(2)
def conteo_lineas(gdb,salida,inspeccion):
    dic_inspeccion = {
                        '1':'PREDIOS_L_INSP1',
                        '2':'PREDIOS_L_INSP2',
                        '3':'PREDIOS_L_INSP3',
                        '4':'None'}
    arcpy.env.workspace = gdb
    file = open(os.path.join(str(salida),'Reporte_Conteo_lineas_INSP{0}.txt'.format(dic_inspeccion[inspeccion])), "w")
    arcpy.AddMessage("Contado lineas en cada estado de validación")
    with arcpy.da.SearchCursor("VALIDACION\{0}".format(dic_inspeccion[inspeccion]), ['ESTADO', 'OID@','SHAPE@LENGTH']) as cursor:
        aprobado = 0
        medida_ap = 0 
        aprobado_no_identificable = 0
        medida_apno = 0
        ajustar_lindero = 0
        medida_ajlin= 0
        capturar_lindero = 0
        medida_caplin = 0
        eliminar_lindero = 0
        medida_ellin = 0
        aprobadas_totales = 0
        ajustar_totales= 0 
        total = 0
        medida_total = 0 
        for estado in cursor:
            if estado[0] == 1:
                aprobado = aprobado +1
                aprobadas_totales = aprobadas_totales +1 
                total = total +1
                medida_ap = medida_ap + cursor[2]
                medida_total =  medida_total +  cursor[2]  
            elif estado[0] ==2:
                aprobado_no_identificable = aprobado_no_identificable + 1 
                total = total +1 
                aprobadas_totales = aprobadas_totales +1
                medida_apno = medida_apno + cursor[2]
                medida_total =  medida_total +  cursor[2]  
            elif estado[0] ==3:
                ajustar_lindero = ajustar_lindero+1
                total = total +1
                ajustar_totales= ajustar_totales +  1  
                medida_ajlin= medida_ajlin + cursor[2]
                medida_total =  medida_total +  cursor[2]  
            elif estado[0] ==4:
                capturar_lindero =  capturar_lindero + 1 
                total = total +1
                ajustar_totales= ajustar_totales +  1  
                medida_caplin = medida_caplin + cursor[2]
                medida_total =  medida_total +  cursor[2]  
            elif estado[0] ==5:
                eliminar_lindero = eliminar_lindero + 1 
                total = total +1
                ajustar_totales= ajustar_totales +  1
                medida_ellin = medida_ellin+ cursor[2]
                medida_total =  medida_total +  cursor[2]  
            else: 
                arcpy.AddMessage("El siguiente ID no tiene asignado estado: " + str(estado[1]))
        file.write('\nConteo Lineas {0}\n'.format(dic_inspeccion[inspeccion]))
        file.write('\nAprobadas = {0} // Medición: {1} m \n'.format(aprobado,medida_ap))
        file.write('\nAprobadas No Identificable = {0}  // Medición: {1} m\n'.format(aprobado_no_identificable,medida_apno))
        file.write('\nAprobados Totales = {0} // Medición: {1} m\n'.format(aprobadas_totales, (medida_ap+medida_apno)))
        file.write('\nAjustar Lindero = {0} // Medición: {1} m\n'.format(ajustar_lindero,medida_ajlin))
        file.write('\nCapturar Lindero = {0}// Medición: {1} m\n'.format(capturar_lindero,medida_caplin))
        file.write('\nEliminar Lindero = {0}// Medición: {1} m\n'.format(eliminar_lindero,medida_ellin))
        file.write('\nAjustar Totales = {0} // Medición: {1} m\n'.format(ajustar_totales, (medida_ellin+medida_caplin+medida_ajlin)))
        file.write('\nTotal lineas = {0} // Medición: {1} m \n'.format(total,(medida_ellin+medida_caplin+medida_ajlin+medida_ap+medida_apno)))
        arcpy.AddMessage("Proceso Terminado")
if __name__ == "__main__":
    conteo_lineas(gdb,salida,inspeccion)
        

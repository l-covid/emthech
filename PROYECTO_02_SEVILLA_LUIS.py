# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 16:42:46 2020

@author: luis
"""


import csv
  
    
def consigna(direccion):
   
    conteo_precios = []
    rutas_contadas = []
    conteo_rutas = []
    ruta_actual = []
    suma = 0
    contador = 0 
    transporte = []
    #direccion =  'Exports'
    for ruta in lista_datos:
        if ruta[1] == direccion:
            ruta_actual = [ruta[2],ruta[3]]
            transporte.append(ruta[7])
            if ruta_actual  not in rutas_contadas:
                for movimiento in lista_datos:
                    if movimiento[1] == direccion: # solo se queda con las exportaciones
                        if ruta_actual == [movimiento[2],movimiento[3]]:
                            contador+=1
                            suma += int(movimiento[9])
                            
                rutas_contadas.append(ruta_actual)                
                conteo_rutas.append([ruta[2],ruta[3],contador])
                conteo_precios.append([ruta[2],ruta[3],suma])
              
                suma = 0
                contador = 0
    conteo_rutas.sort(reverse = True, key=lambda x:x[2])  
    conteo_precios.sort(reverse = True, key=lambda x:x[2]) 
    
    return conteo_rutas, conteo_precios,rutas_contadas 

def transporte(direccion,rutas_contadas):
    transport_mode = []
    vias_precio = []
    vias_ = []
    aux = []
    
    for ruta in rutas_contadas:
        ruta_actual = [ruta[0],ruta[1]]
        if ruta_actual  not in transport_mode:
            for movimiento in lista_datos:
                 if movimiento[1] == direccion:
                    if ruta_actual == [movimiento[2],movimiento[3]]: 
                        aux.append(movimiento[7])
                        vias_.append(movimiento[7])
                        vias_precio.append({movimiento[7]:movimiento[9]})
        transport_mode.append([ruta_actual,set(aux),aux])

        aux=[]
        
    conteo=0
    #aux=[]
    for transporte in transport_mode:
        #print(transporte[1])
        for modo in transporte[1]:#segudo nivel modo de transporte, ej.:{'Sea'}
            for via in transporte[-1]:
                if modo == via:
                    conteo+=1
            aux.append({modo:conteo})
            conteo=0 
        
        transporte.append(aux)
        
        del(transporte[1:3] )
        aux = []
        
    vias={}
    vias_precio_= {}
    for via in set(vias_):
        vias[via] = 0
        for transporte in transport_mode:
            for modo in transporte[1]:
                for key,val in modo.items(): 
                    if via == key:
                        vias[key] += val
    
    vias = sorted(vias.items(), key=lambda x: x[1], reverse=True)  
    vias = dict((key, val) for (key, val) in vias)
    
    vias_precio_= {}
    for via in set(vias_):
        vias_precio_[via] = 0
        for transporte in  vias_precio:  
     #       print(transporte)
            for key,val in transporte.items(): 
                if via == key:
                    vias_precio_[key] += int(val)
    
        
    vias_precio_=sorted(vias_precio_.items(), key=lambda x: x[1], reverse=True)
    vias_precio_ = dict(elemento for elemento in vias_precio_)
 
    return transport_mode,vias, vias_precio_ 

def consigna_3 (lista_precios):
    consigna_3=[]
    
    acumulado = 0
    total = sum([int(valor[-1]) for valor in lista_precios ]) 
   # print(total)
    for export in lista_precios:
        acumulado+=round(export[-1]/total,2)*100
        if acumulado <=80:
            consigna_3.append( export)# + [round(export[-1]/total,2),acumulado])

    return consigna_3                   
def porcentaje_de_variaciones(direccion):
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt
    from datetime import datetime
    import pandas as pd
    df = pd.read_csv('synergy_logistics_database.csv')  
    exp = df[df['direction']== direccion]
    exp['date']=pd.to_datetime(exp['date'])
    exp['total_value_normalized'] = exp['total_value'] *100/ sum(exp['total_value']) 
    data=exp.set_index('date')

    marca = ['-','-.',':','dashdot','solid']
    i = 0
    vias = data["transport_mode"].unique()
    prc_=[]
    for via in vias:
        prc_.append((via,round(data[data["transport_mode"]==via]['total_value'].sum()/sum(data['total_value']),2)))
        i += 1


        plt.figure(figsize=(14,10), dpi=100)
        #ax = fig.add_axes([0.5, 0.5, 1, 1]) # left, bottom, width, height (range 0 to 1)
        lista_de_vias = data[ data[ "transport_mode"] == via ][ 'total_value_normalized' ].resample('M').std()
        ax = plt.subplot(len(vias),2,i)
        ax.plot(lista_de_vias,
        marker='.', linestyle= marca[i], linewidth=0.5, label = via)

        ax.set_ylabel('Vlaor normalizado')
        #fig.autofmt_xdate()
        ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
        ax.set_title(via)
        ax.legend();
        plt.savefig("Gráficas de desvicion estandar " + str(i) +".jpg", bbox_inches='tight')
    for porcentaje in prc_:
        print(porcentaje)

lista_datos = []
with open(r"C:\Users\luis\Desktop\Luis_Ernesto_Sevilla_Sarao\emtech\proyecto_nivel_2\synergy_logistics_database.csv","r") as archivo_csv:

    lector =csv.reader(archivo_csv)
    
    for linea in lector:
        lista_datos.append(linea)





    
exp_rutas,exp_precios,exp_rutas_contadas = consigna('Exports')
imp_rutas,imp_precios,imp_rutas_contadas = consigna('Imports')

exp_transporte,exp_vias, exp_vias_precio = transporte('Exports',exp_rutas_contadas)
imp_transporte,imp_vias,imp_vias_precio = transporte('Imports',imp_rutas_contadas)

exp_mas_valor = consigna_3(exp_precios)
imp_mas_valor = consigna_3(imp_precios)    



def impresion(lista):
    for transporte_ in lista:
        print(transporte_)
opc = input('ingresa 1 para .-  ver las 10 rutas más demandadas \n ingresa 2 para .- ver los medios de transporte \n ingresa 3 para .- ver los países que generan el 80% del valor de lasexportaciones e importaciones\n presione **q** para salir  ')
while opc !='q':
            
    if opc =='q':
        break
    elif opc == '1':
        impresion(exp_transporte)
        impresion(imp_transporte)
    elif opc == '2':
        print(exp_vias_precio)
        print(imp_vias_precio)
    elif opc == '3':
        impresion(exp_mas_valor)
        impresion(imp_mas_valor)
    else:
        print('Vuelve a intentarlo gg ')    
    
    opc = input('ingresa 1 para .-  ver las 10 rutas más demandadas \n ingresa 2 para .- ver los medios de transporte \n ingresa 3 para .- ver los países que generan el 80% del valor de lasexportaciones e importaciones\n presione **q** para salir  ')
        
        
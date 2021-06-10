# ===============================================
# Conversor de formatos
# Autor: Rodrigo Tufiño <rtufino@ups.edu.ec>
# Version: 1.0.1
#
# Historial:
#   v1.0.0  16-01-2020  Aplicación para Jessy
#   v1.0.1  14-07-2020  Aplicación para Esteban y Karen
#   v1.0.2  10-06-2021  Conversión para Kevin
# ===============================================

import os.path
from datetime import datetime, timedelta
from collections import OrderedDict
from calendar import monthrange

FILE_OUTPUT = 'output/resultado.txt'

DATA = {
    'PRECIPITACION': [],
    'TEMP_MAXIMA': [],
    'TEMP_MINIMA': [],
    'VIENTO': [],
    'PRESION': [],
    'HUMEDAD': [],
    'TIEMPO': []
}

def cargar_datos():
    for magnitud in DATA:
        archivo = "input/" + magnitud.lower() + ".txt"
        if os.path.exists(archivo):
            # ----------------------------------------------
            # Cambio: encoding = "ISO-8859-1"
            # ----------------------------------------------
            file = open(archivo, 'r', encoding="ISO-8859-1")
            datos = []
            primera_fila = True
            for linea in file.readlines():
                if primera_fila:
                    primera_fila = False
                    continue
                datos.append(linea.rstrip().split('\t'))
            file.close
            DATA[magnitud] = datos
            print("Datos de",magnitud,"cargados")
        else:
            print("No existe archivo para", magnitud)

def generar_fechas(desde='1960-01-01', hasta='2020-07-01'):
    dates = [desde, hasta]
    start, end = [datetime.strptime(_, "%Y-%m-%d") for _ in dates]
    return OrderedDict(((start + timedelta(_)).strftime(r"%Y-%m"), None) for _ in range((end - start).days)).keys()
    

def consultar(lista, codigo, anio, mes):
    primer = True
    for row in lista:
        if row[0].strip() == codigo and int(row[1]) == anio and int(row[2]) == mes:
            return row
        primer = False
    return None

def obtener_dato(fila, dia):
    dato = '-99.9'
    if fila is not None:
        try:
            dato = fila[dia+2]
        except:
            pass
    return dato

def armar_datos(codigo, anio, mes, row_a, row_b, row_c, row_d, row_e, row_f, row_g):
    filas = []
    ultimo_dia = monthrange(anio,mes)[1]
    for dia in range(1, ultimo_dia + 1):
        a = obtener_dato(row_a, dia)
        b = obtener_dato(row_b, dia)
        c = obtener_dato(row_c, dia)
        d = obtener_dato(row_d, dia)
        e = obtener_dato(row_e, dia)
        f = obtener_dato(row_f, dia)
        g = obtener_dato(row_g, dia)
        filas.append([codigo, anio, mes, dia,a,b,c,d,e,f,g])
    return filas


def imprimir(salida):
    for row in salida:
        for dato in row:
            print(dato, end=';')
        print('')


def guardar(codigo, resultado):
    archivo = 'output/' + codigo + '.txt'
    print("Generando archivo:", archivo)
    file = open(archivo, 'w')
    for row in resultado:
        linea = ''
        for dato in row:
            linea += str(dato) + '\t'
        linea = linea[:-1]+'\n'
        file.write(linea)
    file.close
    
def procesar(codigos, desde, hasta):
    cabecera = ['CODIGO', 'ANIO', 'MES', 'DIA']
    for magnitud in DATA:
        cabecera.append(magnitud)
    salida = [cabecera]
    fechas = generar_fechas(desde, hasta)
    for codigo in codigos:
        for fecha in fechas:
            anio = int(fecha.split("-")[0])
            mes = int(fecha.split("-")[1])
            row_a = consultar(DATA['PRECIPITACION'],codigo,anio,mes)
            row_b = consultar(DATA['TEMP_MAXIMA'], codigo, anio, mes)
            row_c = consultar(DATA['TEMP_MINIMA'], codigo, anio, mes)
            row_d = consultar(DATA['VIENTO'], codigo, anio, mes)
            row_e = consultar(DATA['PRESION'], codigo, anio, mes)
            row_f = consultar(DATA['HUMEDAD'], codigo, anio, mes)
            row_g = consultar(DATA['TIEMPO'], codigo, anio, mes)
            filas = armar_datos(codigo, anio, mes, row_a, row_b, row_c, row_d, row_e, row_f, row_g)
            salida.extend(filas)
        guardar(codigo, salida)


if __name__ == "__main__":
    print("== CONVERSOR DE FORMATOS ==")
    codigos = ['M0470']
    desde = '1982-01-01'
    hasta = '2018-11-01'

    print("\nEstaciones a procesar:", codigos)
    print("Desde:",desde)
    print("Hasta:",hasta)

    print("\nCargando datos:")
    cargar_datos()
    print('\nProcesando:')
    procesar(codigos, desde, hasta)
    
    print("Fin del programa.")

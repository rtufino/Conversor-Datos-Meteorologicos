# ===============================================
# Conversor de formatos
# Autor: Rodrigo Tufiño <rtufino@ups.edu.ec>
# Version: 1.0.0
# Fecha: 16-01-2020
# ===============================================

FILE_PRECIPITACION = 'input/precipitacion.txt'
FILE_TEMP_MAXIMA = 'input/tempmaxima.txt'
FILE_TEMP_MINIMA = 'input/tempminima.txt'

FILE_OUTPUT = 'output/resultado_27012020.txt'


def leer_archivo(archivo):
    file = open(archivo, 'r')
    datos = []
    for linea in file.readlines():
        datos.append(linea.rstrip().split('\t'))
    file.close
    return datos


def consultar(lista, codigo, anio, mes):
    primera_fila = True
    for row in lista:
        if primera_fila:
            primera_fila = False
            continue
        if row[0] == codigo and row[1] == anio and row[2] == mes:
            return row
    return None


def armar_datos(codigo, anio, mes, row_a, row_b, row_c):
    filas = []
    for d in range(1, 32):
        a = row_a[d+2]
        if row_b is not None:
            b = row_b[d+2]
        else:
            b = '-99.9'
        if row_c is not None:
            c = row_c[d+2]
        else:
            c = "-99.9"
        if a == 'NULL':
            a = "-99.9"
        # if a != '-99.9' or b != '-99.9' or c != '-99.9':
        filas.append([codigo, anio, mes, d, a, b, c])
    return filas


def imprimir(salida):
    for row in salida:
        for dato in row:
            print(dato, end=';')
        print('')


def guardar(resultado):
    file = open(FILE_OUTPUT, 'w')
    for row in resultado:
        linea = ''
        for dato in row:
            linea += str(dato) + '\t'
        linea = linea[:-1]+'\n'
        file.write(linea)
    file.close


def procesar():
    precipitaciones = leer_archivo(FILE_PRECIPITACION)
    temp_maxima = leer_archivo(FILE_TEMP_MAXIMA)
    temp_minima = leer_archivo(FILE_TEMP_MINIMA)

    salida = [['codigo', 'anio', 'mes', 'dia',
               'precipitacion', 'temp_maxima', 'temp_minima']]
    primera_fila = True
    for p in precipitaciones:
        if primera_fila:
            primera_fila = False
            continue
        row_a = p
        codigo = row_a[0]
        anio = row_a[1]
        mes = row_a[2]
        row_b = consultar(temp_maxima, codigo, anio, mes)
        row_c = consultar(temp_minima, codigo, anio, mes)
        filas = armar_datos(codigo, anio, mes, row_a, row_b, row_c)
        salida.extend(filas)
    return salida


if __name__ == "__main__":
    print("== CONVERSOR DE FORMATOS ==")
    print("Iniciando procesamiento...")
    resultado = procesar()
    print("Generando archivo de salida...")
    guardar(resultado)
    print("Fin del programa.")

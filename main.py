from funciones import *
import random


while True:
    procesos = int(input('Ingrese la cantidad de procesos que desea realizar: '))
    if procesos > 25:
        print('Número de proceso inválido, por favor ingrese una cantidad menor a 25')
    else:
        break

quantum=int(input('Ingrese el valor del quantum: '))

lista_procesos=[]
procesos_en_memoria=[]
procesos_pendientes=[]

cont = 0
id_auto = 1
keys_validas = list(OPERACIONES.keys())
keys_validas.remove('error')

while cont < procesos:

    info=crear_proceso(keys_validas, cont+1)
    
    lista_procesos.append(info)
    if procesos>5:
        procesos_pendientes=lista_procesos[5:]

    if len(procesos_en_memoria) < 5:
        procesos_en_memoria.append(info)

    cont += 1

print(lista_procesos,'\n')
print(procesos_pendientes,'\n')
print(procesos_en_memoria)

funcion_procesos(procesos_en_memoria,procesos_pendientes, cont, keys_validas, quantum)

input('Presiona Enter para Finalizar...')

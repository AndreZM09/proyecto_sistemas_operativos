import time
import keyboard
from asyncio.windows_events import NULL
import random
import os

contador_global=0
pausado = False
terminar_proceso = False
bloquear_proceso = False
nuevo_proceso = False
mostrar_tabla_bcp = False 

OPERACIONES = {
    'suma': {'simbolos': ['+', 'suma', 'Suma'], 'func': lambda x, y: x + y, 'valid': lambda x, y: True},
    'resta': {'simbolos': ['-', 'resta', 'Resta'], 'func': lambda x, y: x - y, 'valid': lambda x, y: x >= y},
    'multiplicación': {'simbolos': ['*', 'multiplicacion', 'multiplicación', 'Multiplicacion', 'Multiplicación'], 'func': lambda x, y: x * y, 'valid': lambda x, y: True},
    'división': {'simbolos': ['/', 'division', 'división', 'Division', 'División'], 'func': lambda x, y: x / y, 'valid': lambda x, y: y != 0},
    'residuo': {'simbolos': ['residuo', 'Residuo'], 'func': lambda x, y: x % y, 'valid': lambda x, y: y != 0},
    'porcentaje': {'simbolos': ['porcentaje', 'Porcentaje'], 'func': lambda x, y: (x * y) / 100, 'valid': lambda x, y: y != 0},
    'error':'error'
}

def pausar(e):
    global pausado
    pausado = True
    print('\n---- Pausado ----\nPresione "c" para continuar...')

def continuar(e):
    global pausado
    global mostrar_tabla_bcp
    pausado = False
    mostrar_tabla_bcp = False

def terminar(e):
    global terminar_proceso
    terminar_proceso = True
    print("\n\n=======Se pulsó la tecla 'E'=======")


def interrupcion(i):
    global bloquear_proceso
    bloquear_proceso = True
    print("\n\n=======Se pulsó la tecla 'I'=======")

def crear(e):
    global nuevo_proceso
    nuevo_proceso = True
    print('\n\n=======Se creó un proceso=======')

def pausa_tabla_de_procesos(e):
    global mostrar_tabla_bcp
    mostrar_tabla_bcp = True
    print("\n\n=======Se pulsó la tecla 'B'=======")

keyboard.on_press_key('e', terminar)
keyboard.on_press_key('p', pausar)
keyboard.on_press_key('c', continuar)
keyboard.on_press_key('i', interrupcion)
keyboard.on_press_key('n', crear)
keyboard.on_press_key('b', pausa_tabla_de_procesos)

def validar_nombre(op_simbolo):
    for op_name, op_data in OPERACIONES.items():
        if op_simbolo in op_data['simbolos']:
            return op_name
    print('Operación no válida, inténtalo de nuevo')
    return None

def validacion(op,a,b):
    if op=='+' or op=='suma' or op == 'Suma':
        return True
    elif op=='*' or op=='multiplicacion' or op == 'multiplicación' or op=='Multiplicacion' or op=='Multiplicación':
        return True
    elif op=='-' or op=='resta' or op == 'Resta':
        if a<b:
            return False
        else:
            return True
    elif op=='/' or op=='division' or op == 'división' or op=='Division' or op=='División':
        if b==0:
            return False
        else:
            return True
    elif op=='residuo' or op=='Residuo':
        if b==0:
            return False
        else:
            return True
    elif op=='porcentaje' or op=='Porcentaje':
        if b==0:
            return False
        else:
            return True

def operacion_resultado(op, a, b):
    return OPERACIONES[op]['func'](a, b)

def crear_proceso(keys_validas, cont):
    operacion = random.choice(keys_validas)

    max_intentos = 1000
    intentos = 0

    while True:
        a = random.randint(1, 100)
        b = random.randint(1, 100)
        if validacion(operacion, a, b):
            break

        intentos += 1
        if intentos >= max_intentos:
            a, b = 5, 5
            break

    tiempo = random.randint(6,16)

    id=cont

    info = {"operacion": operacion, "tiempo_maximo": tiempo, "num1": a, "num2": b, "id": id, "tiempo_restante":tiempo, "bloqueado":False, "tt":0, "tiempo_de_llegada":0, "tiempo_de_finalizacion":0, "tiempo_de_espera":0, "tiempo_de_servicio":0, "tiempo_de_retorno":0, "tiempo_de_respuesta":0}
    return info

def funcion_procesos(procesos_en_memoria, procesos_pendientes, contador_proesos, keys_validas, quantum):
    global contador_global
    global pausado
    global terminar_proceso
    global bloquear_proceso
    global nuevo_proceso
    global mostrar_tabla_bcp

    procesos_terminados = []
    procesos_bloqueados = []
    proceso_actual = None
    proceso_fue_interrumpido = False
    quantum_copia=quantum
    quantum_copia+=1

    while True:
        contador = 0
        decrementar_tiempo = True
        print("\033[H\033[J", end="")

        print('Procesos pendientes:', len(procesos_pendientes),'\tValor del quantum:',quantum,'\n')

        if proceso_actual:
            if not proceso_fue_interrumpido or ('error' in proceso_actual and proceso_actual['error']):
                if 'error' in proceso_actual and proceso_actual['error']:
                    proceso_actual['resultado'] = 'ERROR'
                else:
                    proceso_actual['resultado'] = operacion_resultado(proceso_actual["operacion"], proceso_actual["num1"], proceso_actual["num2"])
                if proceso_actual['tiempo_restante']==0 or proceso_actual['resultado'] == 'ERROR':
                    proceso_actual['tiempo_de_finalizacion']=contador_global
                    proceso_actual['tiempo_de_retorno']=proceso_actual['tiempo_de_finalizacion'] - proceso_actual['tiempo_de_llegada']
                    proceso_actual['tiempo_de_servicio']=proceso_actual['tt']
                    proceso_actual['tiempo_de_espera']=proceso_actual['tiempo_de_retorno']-proceso_actual['tiempo_de_servicio']
                    if proceso_actual['tiempo_de_espera']==-1:
                        proceso_actual['tiempo_de_espera']=0
                    procesos_terminados+=[proceso_actual]
                if procesos_pendientes:
                    if len(procesos_bloqueados) + len(procesos_en_memoria) <5:
                        procesos_pendientes[0]['tiempo_de_llegada']=contador_global
                        procesos_en_memoria.append(procesos_pendientes.pop(0))
                proceso_actual = None

        proceso_fue_interrumpido = False
        print('----Procesos en ejecución----')
        num_procesos_a_mostrar = min(4, len(procesos_en_memoria) - 1)
        for i in range(1, 1 + num_procesos_a_mostrar):
            proceso = procesos_en_memoria[i]
            print('ID:', proceso['id'], ' || ', 'tiempo maximo estimado:', proceso['tiempo_maximo'], 'segundos',' || ', 'tiempo restante:', proceso['tiempo_restante'], 'segundos')

        print('\n----Procesos terminados----\n')
        for proceso_terminado in procesos_terminados:
            print(f'{proceso_terminado["id"]}, {proceso_terminado["operacion"]}, {proceso_terminado["num1"]}, {proceso_terminado["num2"]}, {proceso_terminado["resultado"]}, tiempo de llegada: {proceso_terminado["tiempo_de_llegada"]}, tiempo de respuesta: {proceso_terminado["tiempo_de_respuesta"]}, tiempo de servicio: {proceso_terminado["tiempo_de_servicio"]}, tiempo de espera: {proceso_terminado["tiempo_de_espera"]}, tiempo de retorno: {proceso_terminado["tiempo_de_retorno"]}, tiempo de finalizacion: {proceso_terminado["tiempo_de_finalizacion"]}')

        if not procesos_en_memoria and not procesos_bloqueados:
            print ('\n----Contador global----')
            print('\ncontador global:', contador_global, 'segundos\n')
            break

        if procesos_en_memoria or procesos_bloqueados:
            if procesos_en_memoria:
                proceso_actual = procesos_en_memoria[0]
                proceso_actual['tt']-=1
                proceso_actual['tiempo_restante']+=1
                if proceso_actual['tiempo_de_respuesta'] == 0 and not proceso_actual['bloqueado']:
                    proceso_actual['tiempo_de_respuesta']=contador_global-proceso_actual['tiempo_de_llegada']
                print ('\n----Proceso en ejecución----                                             ----Procesos bloqueados----')
                print('operación: ', proceso_actual['operacion'])
                print('tiempo máximo estimado: ', proceso_actual['tiempo_maximo'])
                print('Número de programa: ', proceso_actual['id'])

        if procesos_bloqueados and not procesos_en_memoria:
            print ('\n                                                                    ----Procesos bloqueados----')

        while True:

            if len(procesos_en_memoria)==0 and len(procesos_bloqueados)==0:
                break

            while pausado:
                time.sleep(1)

            if mostrar_tabla_bcp:
                os.system('cls')
                copia_procesos_pendientes=procesos_pendientes.copy()
                for proceso_nuevo in copia_procesos_pendientes:
                    print(f"ID: {proceso_nuevo['id']}, Estado: Nuevo")
                for proceso_en_memoria in procesos_en_memoria[1:]:
                    print(f"ID: {proceso_en_memoria['id']}, Estado: Listo, Operacion: {proceso_en_memoria['operacion']}, Num1: {proceso_en_memoria['num1']}, num2: {proceso_en_memoria['num2']}, tiempo de llegada: {proceso_en_memoria['tiempo_de_llegada']}, tiempo de espera: {proceso_en_memoria['tiempo_de_espera']}, tiempo de servicio: {proceso_en_memoria['tiempo_de_servicio']}, tiempo restante en CPU: {proceso_en_memoria['tiempo_restante']}, tiempo de respuesta: {proceso_en_memoria['tiempo_de_respuesta']}")
                if proceso_actual:
                    print(f"ID: {proceso_actual['id']}, Estado: En ejecución, Operacion: {proceso_actual['operacion']}, Num1: {proceso_actual['num1']}, num2: {proceso_actual['num2']}, tiempo de llegada: {proceso_actual['tiempo_de_llegada']}, tiempo de espera: {proceso_actual['tiempo_de_espera']}, tiempo de servicio: {proceso_actual['tiempo_de_servicio']}, tiempo restante en CPU: {proceso_actual['tiempo_restante']}, tiempo de respuesta: {proceso_actual['tiempo_de_respuesta']}")
                for proceso_bloqueado in procesos_bloqueados:
                    proceso_bloqueado['tiempo_bloqueado']+=1
                    print(f"ID: {proceso_bloqueado['id']}, Estado: Bloqueado, Tiempo bloqueado: {proceso_bloqueado['tiempo_bloqueado']}, Operacion: {proceso_bloqueado['operacion']}, Num1: {proceso_bloqueado['num1']}, num2: {proceso_bloqueado['num2']}, tiempo de llegada: {proceso_bloqueado['tiempo_de_llegada']}, , tiempo de espera: {proceso_bloqueado['tiempo_de_espera']}, tiempo de servicio: {proceso_bloqueado['tiempo_de_servicio']}, tiempo restante en CPU: {proceso_bloqueado['tiempo_restante']}, tiempo de respuesta: {proceso_bloqueado['tiempo_de_respuesta']}")
                for proceso_terminado in procesos_terminados:
                    print(f"ID: {proceso_terminado['id']}, Estado: Terminado, Operacion: {proceso_terminado['operacion']}, Num1: {proceso_terminado['num1']}, num2: {proceso_terminado['num2']}, Resultado: {proceso_terminado['resultado']}, tiempo de llegada: {proceso_terminado['tiempo_de_llegada']}, tiempo de finalización: {proceso_terminado['tiempo_de_finalizacion']}, tiempo de retorno: {proceso_terminado['tiempo_de_retorno']}, tiempo de espera: {proceso_terminado['tiempo_de_espera']}, tiempo de servicio: {proceso_terminado['tiempo_de_servicio']}, tiempo de respuesta: {proceso_terminado['tiempo_de_respuesta']}")
                print('Presione c para continuar...')
                while mostrar_tabla_bcp:
                    time.sleep(1)
                break

            if procesos_en_memoria and decrementar_tiempo:
                proceso_actual['tt'] += 1
                proceso_actual['tiempo_restante'] -= 1
                print(f'\rTiempo transcurrido: {proceso_actual["tt"]}  Tiempo restante por ejecutar: {proceso_actual["tiempo_restante"]}\033[K', end='')
                if proceso_actual['tiempo_restante'] == 0 and procesos_en_memoria:
                    procesos_en_memoria.pop(0)
                    break
                elif contador==quantum_copia:
                    procesos_en_memoria.pop(0)
                    procesos_en_memoria.append(proceso_actual)
                    proceso_actual['tt'] -= 1
                    proceso_actual['tiempo_restante'] += 1
                    break

            if bloquear_proceso:
                bloquear_proceso = False
                proceso_fue_interrumpido = True
                proceso_actual['bloqueado'] = True
                proceso_actual['tt'] -= 1
                proceso_actual['tiempo_restante'] +=1
                proceso_actual['tiempo_bloqueado'] = 8
                procesos_bloqueados.append(proceso_actual)
                procesos_en_memoria.pop(0)
                proceso_actual = None
                break

            if terminar_proceso:
                proceso_actual['tt'] -= 1
                terminar_proceso = False
                proceso_actual['error'] = True
                procesos_en_memoria.pop(0)
                break

            if nuevo_proceso:
                nuevo_proceso = False
                contador_proesos+=1
                if len(procesos_bloqueados) + len(procesos_en_memoria) <5:
                    procesos_en_memoria.append(crear_proceso(keys_validas, contador_proesos))
                else:
                    procesos_pendientes.append(crear_proceso(keys_validas, contador_proesos))

                if proceso_actual:
                    proceso_actual['tt']=proceso_actual['tt']-1
                    proceso_actual['tiempo_restante']=proceso_actual['tiempo_restante']+1
                break


            if procesos_bloqueados:
                bloqueados_str = ' || '.join(f"ID: {pb['id']} - Tiempo restante: {pb['tiempo_bloqueado']}" for pb in procesos_bloqueados)
                print(f'\t\t\t\t|| {bloqueados_str}\r', end='')
            else:
                    print('\r', end='')


            if procesos_bloqueados and procesos_bloqueados[0]['tiempo_bloqueado'] == 0:
                procesos_en_memoria.append(procesos_bloqueados[0])
                procesos_bloqueados.pop(0)
                if len(procesos_en_memoria)==1 and len(procesos_bloqueados)==0:
                    proceso_actual = procesos_en_memoria[0]
                if proceso_actual:
                    proceso_actual['tt']=proceso_actual['tt']-1
                    proceso_actual['tiempo_restante']=proceso_actual['tiempo_restante']+1
                if procesos_bloqueados:
                    proceso_actual = procesos_bloqueados[0]
                decrementar_tiempo = False
                break

            for proceso_bloqueado in procesos_bloqueados:
                proceso_bloqueado['tiempo_bloqueado'] -= 1

            time.sleep(1)
            contador += 1

        contador_global += contador





#Nombre: Hoja de Trabajo 5 - Algoritmos y Estructuras de Datos
#Autor: Adrian Fulladolsa Palma
#Proposito: Simular un procesador utilizando el modulo SimPy y sus recursos de colas con las clases Resources y Container
#Fecha: 13/03/2022
#

import simpy
import random

def revisarInput(mensaje):
    while True:
        try:
            valor = int(input(mensaje))
        except ValueError:
            print("No es un valor aceptado")
            continue
        if valor == 0:
            print('Valor no puede ser cero')
            continue
        elif valor < 0:
            print('Valor no puede ser menor a cero')
            continue
        else:
            break
    return valor   
    
    
    
def proceso(nombre, env, memoria, cpu, llegada, cantidad_instrucciones, cantidad_ram):
    yield env.timeout(llegada)

    tiempo_llegada = env.now

    print(nombre, ' en cola New, esperando asignacion en memoria')
    
    yield memoria.get(cantidad_ram)  

    while cantidad_instrucciones > 3:
        
        SiWaiting = random.randint(1,2)
        if SiWaiting == 1:
            print(nombre, ' en cola Waiting, esperando operaciones I/O')
            yield env.timeout(1)

        print(nombre, ' en cola Ready, instrucciones seran realizadas por CPU')
        
        with cpu.request() as req:  
            yield req


            cantidad_instrucciones = cantidad_instrucciones - 3    
            yield env.timeout(1)  

            print(nombre, ' en cola Running, realizando instruccion en CPU')

    yield memoria.put(cantidad_ram)
    
    print(nombre, ' en cola Terminated, proceso no tiene mas instrucciones por realizar y saldra de sistema')
    
    tiempo_proceso = env.now - tiempo_llegada
    global tiempo_total
    tiempo_total = tiempo_total + tiempo_proceso
    print('Tiempo total del proceso ', tiempo_proceso)

print('Bienvenido al simulador de procesador')
print('')

random.seed(10)

env = simpy.Environment()

canRam = revisarInput("Ingrese la cantidad de RAM: ")
initial_ram = simpy.Container(env, canRam, init=canRam)

canCPU = revisarInput('Ingrese la cantidad de CPU en el sistema : ')
initial_cpu = simpy.Resource(env, capacity=1)


initial_procesos = revisarInput('Ingrese la cantidad de procesos: ') 
tiempo_total = 0


random.seed(30)
for i in range(initial_procesos):
    llegada = 5*i  
    cantidad_instrucciones = random.randint(1, 10) 
    UsoRam = random.randint(1, 10)  
    env.process(proceso('Proceso %d' % i, env, initial_ram, initial_cpu, llegada, cantidad_instrucciones, UsoRam))


env.run()
print('')
print('Tiempo total ', tiempo_total)
print('Tiempo promedio %d ' % (tiempo_total / initial_procesos))
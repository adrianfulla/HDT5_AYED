#Nombre: Hoja de Trabajo 5 - Algoritmos y Estructuras de Datos
#Autor: Adrian Fulladolsa Palma
#Proposito: Simular un procesador utilizando el modulo SimPy y sus recursos de colas con las clases Resources y Container
#Fecha: 13/03/2022
#

#Modulos a usar en el programa
import simpy #Modulos que permite realizar simulaciones de evento-discreto a base de procesos
import random #Modulo que permite la creación de numeros aleatorios

#Funcion que toma una entrada del usuario y verifica si esta es de tipo int y si es mayor a 0
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
#Fin de funcion revisarInput
    
 #Funcion que permite realizar la simulación del procesador   
def proceso(nombre, env, memoria, cpu, llegada, cantidad_instrucciones, cantidad_ram): 
    yield env.timeout(llegada) #Al iniciar función se espera a que el CPU realize el ciclo donde el proceso entra en este

    tiempo_llegada = env.now #Se guarda la unidad de tiempo en el que el proceso entro a cola

    print(nombre, ' en cola New, esperando asignacion en memoria') #Se le muestra al usuario que el proceso entro a cola New y esta esperando asignación en memoria
    
    yield memoria.get(cantidad_ram)  #Se realiza una iteración sobre la memoria para obtener la cantidad de ram que se encuentra disponible

    #Mientras que existan más de 3 instrucciones sin realizar se pasaran a colas de espera o de listo para ser introducidas al procesador
    while cantidad_instrucciones > 3: 
        
        SiWaiting = random.randint(1,2) #Valor aleatorio 1 o 2 que representá si el proceso debe esperar a una operación de entrada/salida o si se encuentra listo para entrar al procesador
        if SiWaiting == 1: #Si el valor aleatorio es 1, el proceso entra a cola de espera. Ya que en realidad esto interrumpe el flujo de los procesos se decidio simularlo con un ciclo del reloj del procesador.
            print(nombre, ' en cola Waiting, esperando operaciones I/O')
            yield env.timeout(1)

        #Si el valor aleatorio es 2 o el proceso deja cola de espera se pasa a cola de listo para entrar al procesador
        print(nombre, ' en cola Ready, instrucciones seran realizadas por CPU') 
        
        #Se busca si el procesador esta disponible para realizar instrucciones
        with cpu.request() as req:  
            yield req

            #Cuando exista disponibilidad en el procesador se procedera a realizar las instrucciones, para esto se resta de la cantidad de instrucciones la velocidad de instrucciones por unidad de tiempo que puede realizar el procesador.
            cantidad_instrucciones = cantidad_instrucciones - 3   
            yield env.timeout(1)  #Se realiza un ciclo de reloj

            print(nombre, ' en cola Running, realizando instruccion en CPU') #Se le muestra al usuario que el proceso esta corriendo en el procesador

    #Cuando termina el procesador de realizar todas las instrucciones el proceso sale de este y la memoria ocupada retorna a memoria
    yield memoria.put(cantidad_ram) 
    
    print(nombre, ' en cola Terminated, proceso no tiene mas instrucciones por realizar y saldra de sistema') #Se muestra al usuario que el proceso termino y salio del procesador
    
    tiempo_proceso = env.now - tiempo_llegada #Se calcula el tiempo que tardo el proceso
    global tiempo_total
    tiempo_total = tiempo_total + tiempo_proceso #Se suma el valor del tiempo que tardo el proceso al tiempo total 
    print('Tiempo total del proceso ', tiempo_proceso) #Se le indica al usuario la cantidad de tiempo que tardo el proceso en realizarse.
#Fin de función Proceso


#Inicia el programa
print('Bienvenido al simulador de procesador') 
print('')

env = simpy.Environment() #Se crea el ambiente de SimPy que se utilizará

canRam = revisarInput("Ingrese la cantidad de RAM: ") #se le pide al usuario la cantidad de RAM en el sistema
initial_ram = simpy.Container(env, canRam, init=canRam) #Se crea el contenedor que representará la memoria RAM

canCPU = revisarInput('Ingrese la cantidad de CPU en el sistema : ') #Se le pide al usuario la cantidad de procesadores en el sistema
initial_cpu = simpy.Resource(env, capacity=canCPU) #Se crea el resource que representará el procesador


initial_procesos = revisarInput('Ingrese la cantidad de procesos: ')  #Se le pide al usuario la cantidad de procesos a realizar

tiempo_total = 0 #Se inicia el tiempo de simulación en 0


random.seed(30) #Se utiliza la semilla 30 para el modulo random de manera que la secuencia de numeros siempre sea la misma y exista consistencia entre corridas de la simulación 

for i in range(initial_procesos): #Se realiza la funcion proceso para cada proceso
    llegada = 0*i #Indica el intervalo de tiempo en el que los procesos entran al procesador   
    cantidad_instrucciones = random.randint(1, 10)  #Se genera la cantidad de instrucciones que tendra cada proceso
    UsoRam = random.randint(1, 10)  #Se genera la cantidad de espacio en memoria necesitado por cada proceso
    env.process(proceso('Proceso %d' % i, env, initial_ram, initial_cpu, llegada, cantidad_instrucciones, UsoRam)) #Se realiza la funcion proceso con los datos obtenidos 


env.run() #Inicia el proceso

#Al terminar simulación se le muestra al usuario el tiempo total que tomo la simulación y el tiempo promedio de todos los procesos realizados
print('')
print('Tiempo total ', tiempo_total)
print('Tiempo promedio %d ' % (tiempo_total / initial_procesos))
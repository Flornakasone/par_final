#GESTION DE FACTURACION

#debe cumplir con los siguientes requisitos:
    # Deberá tener un menú principal con las acciones disponibles ***
    #1. Permitir la búsqueda de un cliente por su nombre (parcial o total) , mostrando todos sus datos. 
    #2. Permitir obtener el total de usuarios por empresa, y todos sus datos. 
    #3. Permitir obtener el total de dinero en viajes por nombre de empresa
    #4. Permitir obtener cantidad total de viajes realizados y monto total por documento, y mostrar los datos del empleado y los viajes.
    #5. Además se requiere que el sistema guarde las consultas en un archivo .log.
    # El csv que se cargue se considerará válido si: ***
        # Documento tiene entre 7 y 8 caracteres numéricos de largo
        # No hay campos vacios
        # Email contiene un @ y un .
        # Precio contiene dos decimales

import csv
import os.path
import re #regex validar email


""" VALIDA SI ES UN INT """
def es_int(num):
    try:
        entero = int(num)
        return True
    except ValueError:
        return False

""" VALIDA SI ES FLOAT """
def es_float(num):
    try:
        flotante = float(num)
        return True
    except:
        return False

""" VALIDA ARCHIVO DATOS.CSV """
def validar_csvDatos(archivo):
    with open(archivo) as file:  
        csvReader = csv.reader(file, delimiter=',')  
        next(csvReader) #salteo encabezado
        
         #validacion de campo vacio
        for linea in csvReader: #iteramos sobre cada linea del archivo
            for i in linea: #volvemos a iterar sobre cada campo de la linea
                if i == None:
                    print(f"ERROR || Hay un campo vacio, no se puede proceder")
                    return False

            #validacion de documento entre 7 y 8 caracteres
            if len(linea[2]) < 7 or len(linea[2]) > 8 or es_int(linea[2]) == False: #lo comparamos con el largo del documento
                print(f"ERROR || Los caracteres del documento no son correctos, no se puede proceder")
                return False 

            #validacion de email con regex 
            #elif "@" not in linea[4] and "." not in linea[4]:
            if not re.match("^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", linea[4]):
                return False
        
        return True
                                      


""" VALIDA ARCHIVO VIAJES.CSV """
def validar_csvViajes(archivo):
    with open(archivo, "r") as file:
        csvReader = csv.reader(file, delimiter=',')  
        next(csvReader)

        for linea in csvReader:
            for i in linea:
                #validar si hay campos vacios
                if i == None:
                        print(f"ERROR || Hay un campo vacio, no se puede proceder")
                        return False

                #validar cantidad de digitos del documento
                if len(linea[0]) < 7 or len(linea[0]) > 8 or es_int(linea[0]) == False: #si se cumple alguna ya va a tirar error
                    print(f"ERROR || Un documento del archivo es invalido, no se puede proceder")
                    return False

                #validamos numeros flotantes
                elif es_float(linea[2]) == False: #usamos la funcion creada arriba
                    print(f"ERROR || Un precio del documento {i} tiene que tener decimales, no se puede proceder")
                    return False

                #validar si precio tiene 2 decimales 
                elif len(linea[2].rsplit('.')[-1]) != 2: #con rsplit marcamos el delimitador y que se cuente 2 digitos enpezando de atras
                    print(f"ERROR || Un precio del documento {i} es invalido, no se puede proceder")
                    return False

validar_csvViajes("viajes.csv")


""" 1) búsqueda de un cliente por su nombre (parcial o total) """
def buscarCliente(campos): #le paso como parametro los campos
    try:    
        archivo_clientes = input("Ingrese nombre del archivo en el que desea buscar: ")+".csv" #el usuario elige el nombre del archivo a consultar

        if validar_csvDatos(archivo_clientes) == False: #si las validaciones no se cumplen 
            print("El archivo no es valido")

        else:
            cliente_buscado = input("Ingrese el nombre que desea buscar:\n>")
            #abrimos archivo de lectura
            with open (archivo_clientes) as f:
                clientes_csv = csv.DictReader(f, fieldnames= campos) 
                contador = 0 #use un contador para validar si hay datos o no del input ingresado
                print("----------------------------------------------")
                print(f"Resultados para '{(cliente_buscado).upper()}'")
                print("----------------------------------------------")
                print(f"[{campos[0]}, {campos[1]}, {campos[2]}, {campos[3]}, {campos[4]}, {campos[5]}]\n") 
                for row in clientes_csv: #recorremos el archivo para ver si esta el dato
                    if cliente_buscado.lower() in row['Nombre'].lower():
                        contador += 1 # si esta, sumamos un acierto al contador
                        print(f"[{row['Nombre']},{row['Dirección']},{row['Documento']},{row['Fecha Alta']},{row['Correo Electrónico']},{row['Empresa']}]")
                        
                
                if contador == 0: # si da 0 es pq no hubo coincidencias
                    print("No se encontró ningún cliente con el nombre ingresado")

    except IOError:
        print("Hubo un error, no se puede visualizar el archivo")




""" 2) obtener el total de usuarios por empresa, y todos sus datos """
def cantidadUsuarios(campos):

    try:  
        archivo_clientes = input("Ingrese nombre del archivo en el que desea buscar: ")+".csv"

        if validar_csvDatos(archivo_clientes) == False:
            print("El archivo no es valido")

        else:
            empresa_buscado = input("Ingrese la empresa que desea buscar:\n>")
            with open (archivo_clientes) as f:
                empresas_csv = csv.DictReader(f, fieldnames=campos)
                contador = 0 #para ver si se encontraron datos
                lista_empleados = [] #lista para almacenar las coincidencias obtenidas
                #print(campos)
                for linea in empresas_csv: #recorremos el archivo
                    if empresa_buscado.lower() in linea['Empresa'].lower(): 
                        contador += 1
                        lista_empleados.append(linea) #se agrega la linea a la lista vacia
                
                print("-----------------------------------------------------------------------------------")
                print("Empresa: " + empresa_buscado.upper())
                print("Total Usuarios: " , contador)
                print("-----------------------------------------------------------------------------------")
                print(f"[{campos[0]}, {campos[1]}, {campos[2]}, {campos[3]}, {campos[4]}, {campos[5]}]\n")
                for i in lista_empleados: #recorremos la lista para imprimir cada dato en ella
                    print(f"[{i['Nombre']},{i['Dirección']},{i['Documento']},{i['Fecha Alta']},{i['Correo Electrónico']},{i['Empresa']}]") 

                
                if contador == 0:
                    print("No se encontró ninguna empresa con el nombre ingresado")    


    except IOError:
        print("Hubo un error, no se puede visualizar el archivo")


#3) obtener el total de dinero en viajes por nombre de empresa
def totalDinero(cDatos, cViajes):
    try:
        archivo_clientes = input("Ingrese nombre del archivo de clientes en el que desea buscar: ")+".csv"
        archivo_viajes = input("Ingrese nombre del archivo de viajes en el que desea buscar: ")+".csv"

        if validar_csvDatos(archivo_clientes) == False or validar_csvViajes(archivo_viajes) == False:
            print("El archivo no es valido")
        else: 
            empresa_buscada = input("Ingrese la empresa que desea buscar:\n>")
            #abrimos primero el archivo de datos
            with open(archivo_clientes, "r") as file1:
                empresas_csv = csv.DictReader(file1, fieldnames=cDatos)
                next(empresas_csv) #salteamos el encabezado
                empresas = next(empresas_csv, None) #empezamos a leer los datos

                total_viajes = 0 #contador para ir sumando los viajes
                contador = 0 #para comprobar si se encontraron datos
                for usuario in empresas_csv:
                    if empresa_buscada.lower() in usuario['Empresa'].lower():
                        #print(usuario['Empresa'])
                        #abrimos el archivo de viajes aca, pq fuera de clientes una vez que llega al final no regresa para seguir comparando
                        with open(archivo_viajes, "r") as file2:
                            viajes_csv = csv.DictReader(file2, fieldnames=cViajes)
                            #next(viajes_csv)
                            #viajes = next(viajes_csv, None) 

                            for registro in viajes_csv:
                                if usuario['Documento'] == registro['Documento']: #validamos que el campo de clientes coincida con viajes
                                    total_viajes +=  float(registro['monto']) #se suma el monto
                                    contador += 1
                if contador == 0:
                    print("No se encontró ninguna empresa con el nombre ingresado")
                else:
                    print("-----------------------------------------------------------------------------------")
                    print(f"{empresa_buscada.upper()}: ${total_viajes:.2f}") #redondear a 2 decimales
                    print("-----------------------------------------------------------------------------------")


    
    except IOError:
        print("Hubo un error, no se puede visualizar el archivo")

       

#4) obtener cantidad total de viajes realizados y monto total por documento, y mostrar los datos del empleado y los viajes.
def totalViajes(cDatos, cViajes):
    try:
        archivo_clientes = input("Ingrese nombre del archivo de clientes en el que desea buscar: ")+".csv"
        archivo_viajes = input("Ingrese nombre del archivo de viajes en el que desea buscar: ")+".csv"

        if validar_csvDatos(archivo_clientes) == False or validar_csvViajes(archivo_viajes) == False:
            print("El archivo no es valido")
        else: 
            documento_buscado = int(input("Ingrese el documento que desea consultar:\n>"))

            with open(archivo_clientes, "r") as file1:
                empresas_csv = csv.DictReader(file1, fieldnames=cDatos)
                next(empresas_csv)
                empresas = next(empresas_csv, None)

                total_viajes = 0 #para sumar cantidad de viajes
                monto_total = 0 #para sumar montos
                contador = 0
                lista_viajes = [] #para ir guardando los datos de clientes

                for cliente in empresas_csv:
                    if int(cliente['Documento']) == documento_buscado: #si el buscado esta en el archivo
                        print("")
                        print("-----------------------------------------------------------------------------------")
                        print("Documento: " , documento_buscado)
                        print("-----------------------------------------------------------------------------------")
                        print(f"[{cDatos[0]}, {cDatos[1]}, {cDatos[2]}, {cDatos[3]}, {cDatos[4]}, {cDatos[5]}]\n")
                        print(f"[{cliente['Nombre']}, {cliente['Dirección']}, {cliente['Documento']}, {cliente['Fecha Alta']}, {cliente['Correo Electrónico']}, {cliente['Empresa']}]")
                        #abrimos el archivo de viajes, para poder recorrerlo junto con el de clientes
                        with open(archivo_viajes, "r") as file2:
                            viajes_csv = csv.DictReader(file2, fieldnames=cViajes)

                            for registro in viajes_csv: 
                                if cliente['Documento'] == registro['Documento']: #validamos si coinciden los datos de ambos archivos
                                    total_viajes += 1
                                    monto_total += float(registro['monto'])
                                    lista_viajes.append(registro)
                                    contador += 1

                if contador == 0:
                    print("No se encontró ningun documento con el valor ingresado")
                else:
                    print("-----------------------------------------------------------------------------------")
                    print(f"Total viajes: {total_viajes}, Monto: ${monto_total}")
                    print("-----------------------------------------------------------------------------------")
                    print(f"[{cViajes[0]},{cViajes[1]},{cViajes[2]}]\n")
                    for dato in lista_viajes:
                        print(f"[{dato['Documento']}, {dato['fecha']}, {dato['monto']}]")
                

    except IOError:
        print("Hubo un error, no se puede visualizar el archivo")


#5) se requiere que el sistema guarde las consultas en un archivo .log
def crearLog(accion):
    try:
        with open("archivo.txt", "a") as f: #creo el archivo para poder escribir en el
            f.write(f"{accion}\n") #escribo la accion que pase por parametro en cada opcion del menu
        
    except IOError:
        print("Hubo un error, no se puede visualizar el archivo")


def imprimir():
        print("\n------------------------------------------")
        print("GESTIÓN DE FACTURACIÓN DE TAXIS - EMPRESAS")
        print("------------------------------------------\n")
        print("Que desea hacer?\n")
        print("\t1. Búsqueda de un cliente")
        print("\t2. Total de usuarios por empresa")
        print("\t3. Total de dinero en viajes por empresa")
        print("\t4. Total de viajes realizados y montos por DNI ")
        print("\t0. Salir\n")


def menu():
    CAMPOS_DATOS = ["Nombre", "Dirección", "Documento", "Fecha Alta", "Correo Electrónico", "Empresa"]
    CAMPOS_VIAJES = ["Documento" ,"fecha" ,"monto"]
    
    while True:
        imprimir()
        crearLog("Acciones")
        crearLog("Menu")
        
        entrada_usuario = input("Seleccione una opcion\n> ")      
        if entrada_usuario == "1":
            buscarCliente(CAMPOS_DATOS)
            crearLog("Busqueda de un cliente")
        elif entrada_usuario == "2":
            cantidadUsuarios(CAMPOS_DATOS)
            crearLog("Obtener total de usuarios por empresa")
        elif entrada_usuario == "3":
            totalDinero(CAMPOS_DATOS, CAMPOS_VIAJES)
            crearLog("Obtener monto por empresa")
        elif entrada_usuario == "4":
            totalViajes(CAMPOS_DATOS, CAMPOS_VIAJES)
            crearLog("Obtener datos por Documento")
        elif entrada_usuario == "0":
            print("Ha salido del programa")
            crearLog("Salir del programa")
            exit()        
        else:
            print('Error no es una opcion válida, intente otra vez')

menu()
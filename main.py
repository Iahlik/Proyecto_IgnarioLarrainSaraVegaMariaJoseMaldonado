import os
import json
import random
from datetime import datetime, timedelta
from tabulate import tabulate

from DAO.CRUDReserva import agregarReserva

import DAO.CRUDUsuario as usuarioCRUD
import DAO.CRUDReserva as reservaCRUD
import DAO.CRUDDestino as destinoCRUD
import DAO.CRUDPaquete as paqueteCRUD

from DTO.Paquete import Paquete
from DTO.Reserva import Reserva
from DTO.Usuario import Usuario
from DTO.Destino import Destino

def registrarUsuario():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Título utilizando tabulate
    titulo = [["REGISTRAR USUARIO"]]
    print(tabulate(titulo, tablefmt="fancy_grid", stralign="center"))
    
    while True:
        # Captura de entradas del usuario con validación individual
        while True:
            nombre = input("Ingrese Usuario: ").strip()
            if nombre:
                break
            print(tabulate([["[Error]"], ["El nombre de usuario no puede estar vacío."]], tablefmt="fancy_grid"))

        while True:
            correo = input("Ingrese Correo: ").strip()
            if correo:
                break
            print(tabulate([["[Error]"], ["El correo no puede estar vacío."]], tablefmt="fancy_grid"))

        while True:
            password = input("Ingrese Contraseña: ").strip()
            if password:
                break
            print(tabulate([["[Error]"], ["La contraseña no puede estar vacía."]], tablefmt="fancy_grid"))

        while True:
            tipoUsuario = input("Ingrese tipo Usuario (administrador/cliente): ").strip().lower()
            if tipoUsuario in ["administrador", "cliente"]:
                break
            print(tabulate([["[Error]"], ["El tipo de usuario debe ser 'administrador' o 'cliente'."]], tablefmt="fancy_grid"))
        
        # Intento de registro del usuario
        try:
            nuevoUsuario = Usuario.registrarUsuario(nombre, correo, password, tipoUsuario)
        except Exception as e:
            error_msg = [
                ["[Error]"],
                [f"Se produjo un error al registrar el usuario: {e}"]
            ]
            print("\n" + tabulate(error_msg, tablefmt="fancy_grid", stralign="center") + "\n")
            retry = input("¿Desea intentarlo de nuevo? [SI/NO]: ").strip().lower()
            if retry != "si":
                return None
            continue
        
        if nuevoUsuario:
            exito_msg = [
                ["¡Éxito!"],
                [f"Usuario '{nombre}' registrado con éxito."]
            ]
            print("\n" + tabulate(exito_msg, tablefmt="fancy_grid", stralign="center") + "\n")
            return nuevoUsuario
        else:
            error_msg = [
                ["[Error]"],
                ["No se pudo registrar el usuario. Intente de nuevo."]
            ]
            print("\n" + tabulate(error_msg, tablefmt="fancy_grid", stralign="center") + "\n")
            retry = input("¿Intentar de nuevo? [SI/NO]: ").strip().lower()
            if retry != "si":
                return None



def login():
    # Limpiar la pantalla
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Título utilizando tabulate
    titulo = [["LOGIN"]]
    print(tabulate(titulo, tablefmt="fancy_grid", stralign="center"))
    
    while True:
        # Campos de entrada organizados en una tabla
        campos = [
            ["Ingrese Correo:", ""],
            ["Ingrese Contraseña:", ""]
        ]
        print(tabulate(campos, tablefmt="plain", colalign=("left", "left")))
        
        # Captura de entradas del usuario
        correo = input(">> ").strip()
        password = input(">> ").strip()
        
        # Validación de campos vacíos
        if not correo or not password:
            error_msg = [
                ["[Error]"],
                ["Los campos de correo y contraseña no pueden estar vacíos. Intente nuevamente."]
            ]
            print("\n" + tabulate(error_msg, tablefmt="fancy_grid", stralign="center") + "\n")
            retry = input("¿Desea intentarlo de nuevo? [SI/NO]: ").strip().lower()
            if retry != "si":
                return None
            # Limpiar la pantalla y mostrar el título nuevamente
            os.system('cls' if os.name == 'nt' else 'clear')
            print(tabulate(titulo, tablefmt="fancy_grid", stralign="center"))
            continue
        
        # Intento de autenticación del usuario
        resultado_login = Usuario.login(correo, password)
        
        if resultado_login.get("autenticado"):
            exito_msg = [
                ["¡Éxito!"],
               # [f"Bienvenido, {resultado_login.get('nombre')}."]
            ]
            print("\n" + tabulate(exito_msg, tablefmt="fancy_grid", stralign="center") + "\n")
            return {
                "tipo_usuario": resultado_login.get("tipo_usuario"),
                "nombre": resultado_login.get("nombre"),
                "correo": correo,
                "id_usuario": resultado_login.get("id_usuario"),
                "autenticado": True
            }
        else:
            error_msg = [
                ["[Error]"],
                ["Correo o contraseña incorrectos."]
            ]
            print("\n" + tabulate(error_msg, tablefmt="fancy_grid", stralign="center") + "\n")
            retry = input("¿Desea intentarlo de nuevo? [SI/NO]: ").strip().lower()
            if retry != "si":
                cancel_msg = [
                    ["Cancelando inicio de sesión."]
                ]
                print("\n" + tabulate(cancel_msg, tablefmt="fancy_grid", stralign="center") + "\n")
                return None
            # Limpiar la pantalla y mostrar el título nuevamente
            os.system('cls' if os.name == 'nt' else 'clear')
            print(tabulate(titulo, tablefmt="fancy_grid", stralign="center"))

def menuDestinos():
    while True:
        # Limpiar la pantalla
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Título del menú utilizando tabulate
        titulo = [["MENÚ DESTINOS"]]
        print(tabulate(titulo, tablefmt="fancy_grid", stralign="center"))
        
        # Opciones del menú organizadas en una tabla
        opciones = [
            ["1", "Registrar un nuevo destino"],
            ["2", "Mostrar todos los destinos"],
            ["3", "Mostrar un destino"],
            ["4", "Mostrar destinos parciales"],
            ["5", "Actualizar destino"],
            ["6", "Eliminar destino"],
            ["7", "Salir"]
        ]
        headers = ["Opción", "Descripción"]
        print(tabulate(opciones, headers=headers, tablefmt="fancy_grid", stralign="left"))
        print()  # Espacio adicional para mejor visualización
        
        # Captura de la opción seleccionada por el usuario
        opcion = input("Por favor, selecciona una opción (1-7): ").strip()
        
        if opcion == "1":
            # Registrar un nuevo destino
            os.system('cls' if os.name == 'nt' else 'clear')
            titulo_submenu = [["REGISTRAR UN NUEVO DESTINO"]]
            print(tabulate(titulo_submenu, tablefmt="fancy_grid", stralign="center"))
            
            # Captura de entradas del usuario con validación
            while True:
                nombre = input("Ingrese Nombre del destino: ").strip()
                if nombre:
                    break
                print(tabulate([["[Error]"], ["El nombre del destino no puede estar vacío."]], tablefmt="fancy_grid"))

            while True:
                descripcion = input("Ingrese Descripción: ").strip()
                if descripcion:
                    break
                print(tabulate([["[Error]"], ["La descripción no puede estar vacía."]], tablefmt="fancy_grid"))

            while True:
                actividades = input("Ingrese Actividades: ").strip()
                if actividades:
                    break
                print(tabulate([["[Error]"], ["Las actividades no pueden estar vacías."]], tablefmt="fancy_grid"))

            # Validación del costo
            while True:
                costo_str = input("Ingrese Costo: ").strip()
                if not costo_str:
                    print(tabulate([["[Error]"], ["El costo no puede estar vacío."]], tablefmt="fancy_grid"))
                    continue
                try:
                    costo = int(costo_str)
                    if costo >= 0:  # Validar que el costo sea positivo
                        break
                    else:
                        print(tabulate([["[Error]"], ["El costo debe ser un número positivo."]], tablefmt="fancy_grid"))
                except ValueError:
                    print(tabulate([["[Error]"], ["El costo debe ser numérico."]], tablefmt="fancy_grid"))
            
            # Crear objeto Destino y agregarlo mediante CRUD
            destino = Destino(nombre, descripcion, actividades, costo)
            if destinoCRUD.agregarDestino(destino):
                exito_msg = [
                    ["¡Éxito!"],
                    [f"Destino '{nombre}' registrado con éxito."]
                ]
                print("\n" + tabulate(exito_msg, tablefmt="fancy_grid", stralign="center") + "\n")
            else:
                error_msg = [
                    ["[Error]"],
                    ["Error al registrar el destino. Verifique la conexión o los datos."]
                ]
                print("\n" + tabulate(error_msg, tablefmt="fancy_grid", stralign="center") + "\n")
            
            input("Presione Enter para continuar...")
        
        elif opcion == "2":
            # Mostrar todos los destinos
            os.system('cls' if os.name == 'nt' else 'clear')
            titulo_submenu = [["MOSTRAR TODOS LOS DESTINOS"]]
            print(tabulate(titulo_submenu, tablefmt="fancy_grid", stralign="center"))
            
            destinos = destinoCRUD.mostrarTodos()
            if destinos:
                table_data = [
                    [d['id_destino'], d['nombre'], d['descripcion'], d['actividades'], d['costo']] 
                    for d in destinos
                ]
                headers = ["ID", "Nombre", "Descripción", "Actividades", "Costo"]
                print(tabulate(table_data, headers=headers, tablefmt="fancy_grid", stralign="left"))
            else:
                mensaje = [["No hay destinos disponibles."]]
                print(tabulate(mensaje, tablefmt="fancy_grid", stralign="center"))
            
            input("Presione Enter para continuar...")
        
        elif opcion == "3":
            # Mostrar un destino específico
            os.system('cls' if os.name == 'nt' else 'clear')
            titulo_submenu = [["MOSTRAR UN DESTINO"]]
            print(tabulate(titulo_submenu, tablefmt="fancy_grid", stralign="center"))
            
            id_destino = input("Ingrese el ID del destino: ").strip()
            if not id_destino.isdigit():
                error_msg = [
                    ["[Error]"],
                    ["El ID debe ser numérico."]
                ]
                print("\n" + tabulate(error_msg, tablefmt="fancy_grid", stralign="center") + "\n")
                input("Presione Enter para continuar...")
                continue
            
            destino = destinoCRUD.mostrarUno(id_destino)
            if destino:
                table_data = [
                    [destino['id_destino'], destino['nombre'], destino['descripcion'], destino['actividades'], destino['costo']]
                ]
                headers = ["ID", "Nombre", "Descripción", "Actividades", "Costo"]
                print(tabulate(table_data, headers=headers, tablefmt="fancy_grid", stralign="left"))
            else:
                mensaje = [["Destino no encontrado."]]
                print(tabulate(mensaje, tablefmt="fancy_grid", stralign="center"))
            
            input("Presione Enter para continuar...")
        
        elif opcion == "4":
            # Mostrar destinos parciales
            os.system('cls' if os.name == 'nt' else 'clear')
            titulo_submenu = [["MOSTRAR DESTINOS PARCIALES"]]
            print(tabulate(titulo_submenu, tablefmt="fancy_grid", stralign="center"))
            
            cantidad_input = input("Cantidad de destinos a mostrar: ").strip()
            if not cantidad_input.isdigit():
                error_msg = [
                    ["[Error]"],
                    ["La cantidad debe ser numérica."]
                ]
                print("\n" + tabulate(error_msg, tablefmt="fancy_grid", stralign="center") + "\n")
                input("Presione Enter para continuar...")
                continue
            
            cantidad = int(cantidad_input)
            destinos = destinoCRUD.mostrarParcial(cantidad)
            if destinos:
                table_data = [
                    [d['id_destino'], d['nombre'], d['descripcion'], d['actividades'], d['costo']] 
                    for d in destinos
                ]
                headers = ["ID", "Nombre", "Descripción", "Actividades", "Costo"]
                print(tabulate(table_data, headers=headers, tablefmt="fancy_grid", stralign="left"))
            else:
                mensaje = [["No hay destinos disponibles."]]
                print(tabulate(mensaje, tablefmt="fancy_grid", stralign="center"))
            
            input("Presione Enter para continuar...")
        
        elif opcion == "5":
            # Actualizar destino
            os.system('cls' if os.name == 'nt' else 'clear')
            titulo_submenu = [["ACTUALIZAR DESTINO"]]
            print(tabulate(titulo_submenu, tablefmt="fancy_grid", stralign="center"))
            
            destinos = destinoCRUD.mostrarTodos()
            if not destinos:
                mensaje = [["No hay destinos disponibles para actualizar."]]
                print(tabulate(mensaje, tablefmt="fancy_grid", stralign="center"))
                input("Presione Enter para continuar...")
                continue
            
            # Mostrar los destinos en una tabla
            table_data = [
                [d['id_destino'], d['nombre'], d['descripcion'], d['actividades'], d['costo']] 
                for d in destinos
            ]
            headers = ["ID", "Nombre", "Descripción", "Actividades", "Costo"]
            print(tabulate(table_data, headers=headers, tablefmt="fancy_grid", stralign="left"))
            
            # Validar el ID de destino a actualizar
            id_destino_str = input("Ingrese el ID del destino a actualizar: ").strip()
            if not id_destino_str.isdigit():
                error_msg = [
                    ["[Error]"],
                    ["Debes ingresar un número válido."]
                ]
                print("\n" + tabulate(error_msg, tablefmt="fancy_grid", stralign="center") + "\n")
                input("Presione Enter para continuar...")
                continue
            id_destino = int(id_destino_str)
            destino_existente = next((d for d in destinos if d['id_destino'] == id_destino), None)
            if not destino_existente:
                mensaje = [["No se encontró un destino con ese ID."]]
                print(tabulate(mensaje, tablefmt="fancy_grid", stralign="center"))
                input("Presione Enter para continuar...")
                continue
            
            # Solicitar nuevos datos, asegurando que no estén vacíos
            campos_actualizacion = [
                ["Nuevo nombre:", destino_existente['nombre']],
                ["Nueva descripción:", destino_existente['descripcion']],
                ["Nuevas actividades:", destino_existente['actividades']],
                ["Nuevo costo:", destino_existente['costo']]
            ]
            print("\n" + tabulate(campos_actualizacion, tablefmt="plain", colalign=("left", "left")) + "\n")
            
            nuevo_nombre = input("Nuevo nombre: ").strip()
            if not nuevo_nombre:
                error_msg = [
                    ["[Error]"],
                    ["El nombre no puede estar vacío."]
                ]
                print("\n" + tabulate(error_msg, tablefmt="fancy_grid", stralign="center") + "\n")
                input("Presione Enter para continuar...")
                continue
            
            nueva_descripcion = input("Nueva descripción: ").strip()
            if not nueva_descripcion:
                error_msg = [
                    ["[Error]"],
                    ["La descripción no puede estar vacía."]
                ]
                print("\n" + tabulate(error_msg, tablefmt="fancy_grid", stralign="center") + "\n")
                input("Presione Enter para continuar...")
                continue
            
            nuevas_actividades = input("Nuevas actividades: ").strip()
            if not nuevas_actividades:
                error_msg = [
                    ["[Error]"],
                    ["Las actividades no pueden estar vacías."]
                ]
                print("\n" + tabulate(error_msg, tablefmt="fancy_grid", stralign="center") + "\n")
                input("Presione Enter para continuar...")
                continue
            
            # Validar el nuevo costo
            while True:
                nuevo_costo_str = input("Nuevo costo: ").strip()
                if not nuevo_costo_str:
                    error_msg = [
                        ["[Error]"],
                        ["El costo no puede estar vacío."]
                    ]
                    print("\n" + tabulate(error_msg, tablefmt="fancy_grid", stralign="center") + "\n")
                    continue
                try:
                    nuevo_costo = int(nuevo_costo_str)
                    break
                except ValueError:
                    error_msg = [
                        ["[Error]"],
                        ["El costo debe ser numérico."]
                    ]
                    print("\n" + tabulate(error_msg, tablefmt="fancy_grid", stralign="center") + "\n")
            
            # Mostrar resumen de cambios antes de confirmar
            resumen = [
                ["Resumen de cambios:"],
                [f"Nombre: {destino_existente['nombre']} -> {nuevo_nombre}"],
                [f"Descripción: {destino_existente['descripcion']} -> {nueva_descripcion}"],
                [f"Actividades: {destino_existente['actividades']} -> {nuevas_actividades}"],
                [f"Costo: {destino_existente['costo']} -> {nuevo_costo}"]
            ]
            print("\n" + tabulate(resumen, tablefmt="fancy_grid", stralign="left") + "\n")
            
            # Confirmar cambios
            confirmar = input("¿Confirmar cambios? [SI/NO]: ").strip().lower()
            if confirmar == "si":
                if destinoCRUD.modificarDestino(id_destino, nuevo_nombre, nueva_descripcion, nuevas_actividades, nuevo_costo):
                    exito_msg = [
                        ["¡Éxito!"],
                        ["Cambios guardados con éxito."]
                    ]
                    print("\n" + tabulate(exito_msg, tablefmt="fancy_grid", stralign="center") + "\n")
                else:
                    error_msg = [
                        ["[Error]"],
                        ["No se pudieron guardar los cambios. Verifique el ID o la conexión."]
                    ]
                    print("\n" + tabulate(error_msg, tablefmt="fancy_grid", stralign="center") + "\n")
            elif confirmar == "no":
                mensaje = [["Cambios descartados."]]
                print("\n" + tabulate(mensaje, tablefmt="fancy_grid", stralign="center") + "\n")
            else:
                error_msg = [
                    ["[Error]"],
                    ["Entrada no válida. Debes responder 'SI' o 'NO'."]
                ]
                print("\n" + tabulate(error_msg, tablefmt="fancy_grid", stralign="center") + "\n")
            
            input("Presione Enter para continuar...")
        
        elif opcion == "6":
            # Eliminar destino
            os.system('cls' if os.name == 'nt' else 'clear')
            titulo_submenu = [["ELIMINAR DESTINO"]]
            print(tabulate(titulo_submenu, tablefmt="fancy_grid", stralign="center"))
            
            destinos = destinoCRUD.mostrarTodos()
            if not destinos:
                mensaje = [["No hay destinos disponibles para eliminar."]]
                print(tabulate(mensaje, tablefmt="fancy_grid", stralign="center"))
                input("Presione Enter para continuar...")
                continue
            
            # Mostrar los destinos en una tabla
            table_data = [
                [d['id_destino'], d['nombre'], d['descripcion'], d['actividades'], d['costo']] 
                for d in destinos
            ]
            headers = ["ID", "Nombre", "Descripción", "Actividades", "Costo"]
            print(tabulate(table_data, headers=headers, tablefmt="fancy_grid", stralign="left"))
            
            # Validar el ID del destino a eliminar
            id_destino_str = input("Ingrese el ID del destino a eliminar: ").strip()
            if not id_destino_str.isdigit():
                error_msg = [
                    ["[Error]"],
                    ["Debe ingresar un número válido."]
                ]
                print("\n" + tabulate(error_msg, tablefmt="fancy_grid", stralign="center") + "\n")
                input("Presione Enter para continuar...")
                continue
            id_destino = int(id_destino_str)
            destino_existente = next((d for d in destinos if d['id_destino'] == id_destino), None)
            if not destino_existente:
                mensaje = [["No se encontró un destino con ese ID."]]
                print(tabulate(mensaje, tablefmt="fancy_grid", stralign="center") + "\n")
                input("Presione Enter para continuar...")
                continue
            
            # Mostrar resumen antes de confirmar
            resumen = [
                ["Resumen del destino a eliminar:"],
                [f"ID: {destino_existente['id_destino']}"],
                [f"Nombre: {destino_existente['nombre']}"],
                [f"Descripción: {destino_existente['descripcion']}"],
                [f"Actividades: {destino_existente['actividades']}"],
                [f"Costo: {destino_existente['costo']}"]
            ]
            print("\n" + tabulate(resumen, tablefmt="fancy_grid", stralign="left") + "\n")
            
            # Confirmar eliminación
            confirmar = input("¿Confirmar eliminación? [SI/NO]: ").strip().lower()
            if confirmar == "si":
                if destinoCRUD.eliminarDestino(id_destino):
                    exito_msg = [
                        ["¡Éxito!"],
                        ["Destino eliminado con éxito."]
                    ]
                    print("\n" + tabulate(exito_msg, tablefmt="fancy_grid", stralign="center") + "\n")
                else:
                    error_msg = [
                        ["[Error]"],
                        ["No se pudo eliminar el destino. Verifique el ID o la conexión."]
                    ]
                    print("\n" + tabulate(error_msg, tablefmt="fancy_grid", stralign="center") + "\n")
            elif confirmar == "no":
                mensaje = [["Eliminación descartada."]]
                print("\n" + tabulate(mensaje, tablefmt="fancy_grid", stralign="center") + "\n")
            else:
                error_msg = [
                    ["[Error]"],
                    ["Entrada no válida. Debes responder 'SI' o 'NO'."]
                ]
                print("\n" + tabulate(error_msg, tablefmt="fancy_grid", stralign="center") + "\n")
            
            input("Presione Enter para continuar...")
        
        elif opcion == "7":
            # Salir del menú de destinos
            os.system('cls' if os.name == 'nt' else 'clear')
            mensaje = [["Saliendo del menú de destinos..."]]
            print(tabulate(mensaje, tablefmt="fancy_grid", stralign="center"))
            input("Presione Enter para continuar...")
            break
        else:
            # Opción no válida
            os.system('cls' if os.name == 'nt' else 'clear')
            error_msg = [
                ["[Error]"],
                ["Opción no válida. Inténtalo de nuevo."]
            ]
            print(tabulate(error_msg, tablefmt="fancy_grid", stralign="center"))
            input("Presione Enter para continuar...")

def agregarPaqueteConDestino(paquete, destinos):
    """
    Inserta un paquete turístico y agrega los destinos relacionados en detalle_paquete.
    - paquete: Objeto con atributos nombre_paquete, descripcion, precio_total, fecha_inicio, fecha_fin.
    - destinos: Lista de diccionarios con id_destino.
    """
    con = None
    try:
        con = Conexion(host, user, password, db)
        if not con:
            print("Error al conectar con la base de datos.")
            return False

        # Verificar si el nombre del paquete ya existe en la base de datos
        sql_check = "SELECT COUNT(*) FROM paquete_turistico WHERE nombre_paquete = %s"
        cursor = con.ejecutaQuery(sql_check, (paquete.nombre_paquete,))
        count = cursor.fetchone()[0]
        if count > 0:
            print(f"El paquete '{paquete.nombre_paquete}' ya existe en la base de datos.")
            return False

        # 1. Insertar el paquete turístico
        sql_paquete = """
        INSERT INTO paquete_turistico (nombre_paquete, descripcion, precio_total, fecha_inicio, fecha_fin)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor = con.ejecutaQuery(sql_paquete, (
            paquete.nombre_paquete,
            paquete.descripcion,
            paquete.precio_total,
            paquete.fecha_inicio,
            paquete.fecha_fin
        ))

        if cursor is None:
            print("Error al ejecutar la consulta de paquete turístico.")
            return False
        
        con.commit()

        # Verificar si se obtuvo un ID válido para el paquete
        if cursor.lastrowid is None:
            print("No se pudo obtener el ID del paquete insertado.")
            return False

        paquete.id_paquete = cursor.lastrowid  # Capturar el ID del paquete

        # 2. Insertar los destinos relacionados
        sql_detalle = "INSERT INTO detalle_paquete (id_paquete, id_destino) VALUES (%s, %s)"
        for destino in destinos:
            con.ejecutaQuery(sql_detalle, (paquete.id_paquete, destino['id_destino']))

        con.commit()
        return True
    except Exception as e:
        if con:
            con.rollback()
        print(f"Error al agregar paquete con destinos: {e}")
        return False
    finally:
        if con:
            con.desconectar()

def menuPaquetes(nombre):
    while True:
        # Limpiar la pantalla
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Título del menú utilizando tabulate
        titulo = [["MENÚ PAQUETES TURÍSTICOS"]]
        print(tabulate(titulo, tablefmt="fancy_grid", stralign="center"))
        
        # Opciones del menú organizadas en una tabla
        opciones = [
            ["1", "Mostrar todos los paquetes"],
            ["2", "Mostrar un paquete específico"],
            ["3", "Mostrar paquetes parciales"],
            ["4", "Eliminar paquete"],
            ["5", "Actualizar paquete"],
            ["6", "Generar paquetes aleatorios"],
            ["7", "Salir"]
        ]
        headers = ["Opción", "Descripción"]
        print(tabulate(opciones, headers=headers, tablefmt="fancy_grid", stralign="left"))
        print()  # Espacio adicional para mejor visualización
        
        # Captura de la opción seleccionada por el usuario
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            # Mostrar todos los paquetes
            os.system('cls' if os.name == 'nt' else 'clear')
            titulo_submenu = [["MOSTRAR TODOS LOS PAQUETES"]]
            print(tabulate(titulo_submenu, tablefmt="fancy_grid", stralign="center"))
            
            paquetes = paqueteCRUD.obtenerPaquetesConDestinos()
            if paquetes:
                table_data = [
                    [
                        p['id_paquete'], 
                        p['nombre_paquete'], 
                        p['descripcion'], 
                        p['precio_total'], 
                        p['fecha_inicio'], 
                        p['fecha_fin'], 
                        p['destinos'] if p['destinos'] else "No tiene destinos"
                    ] 
                    for p in paquetes
                ]
                headers_paquetes = ["ID", "Nombre", "Descripción", "Precio", "Inicio", "Fin", "Destinos"]
                print(tabulate(table_data, headers=headers_paquetes, tablefmt="fancy_grid", stralign="left"))
            else:
                mensaje = [["No hay paquetes turísticos registrados."]]
                print(tabulate(mensaje, tablefmt="fancy_grid", stralign="center"))
            
            input("Presione Enter para continuar...")
        
        elif opcion == "2":
            # Mostrar un paquete específico
            os.system('cls' if os.name == 'nt' else 'clear')
            titulo_submenu = [["MOSTRAR UN PAQUETE ESPECÍFICO"]]
            print(tabulate(titulo_submenu, tablefmt="fancy_grid", stralign="center"))
            
            idPaquete = input("Ingrese el ID del paquete: ").strip()
            if not idPaquete.isdigit():
                error_msg = [
                    ["[Error]"],
                    ["El ID debe ser numérico."]
                ]
                print("\n" + tabulate(error_msg, tablefmt="fancy_grid", stralign="center") + "\n")
                input("Presione Enter para continuar...")
                continue
            
            paquete = paqueteCRUD.mostrarUno(idPaquete)
            if paquete and paquete['fecha_inicio'] != "0000-00-00":
                table_data = [
                    [
                        paquete['id_paquete'], 
                        paquete['nombre_paquete'], 
                        paquete['descripcion'],
                        paquete['precio_total'], 
                        paquete['fecha_inicio'], 
                        paquete['fecha_fin']
                    ]
                ]
                headers_paquete = ["ID", "Nombre", "Descripción", "Precio", "Inicio", "Fin"]
                print(tabulate(table_data, headers=headers_paquete, tablefmt="fancy_grid", stralign="left"))
            else:
                mensaje = [["No se encontró un paquete válido con ese ID."]]
                print(tabulate(mensaje, tablefmt="fancy_grid", stralign="center"))
            
            input("Presione Enter para continuar...")
        
        elif opcion == "3":
            # Mostrar paquetes parciales
            os.system('cls' if os.name == 'nt' else 'clear')
            titulo_submenu = [["MOSTRAR PAQUETES PARCIALES"]]
            print(tabulate(titulo_submenu, tablefmt="fancy_grid", stralign="center"))
            
            cantidad_input = input("¿Cuántos paquetes desea mostrar?: ").strip()
            if not cantidad_input.isdigit():
                error_msg = [
                    ["[Error]"],
                    ["Debe ingresar un número válido."]
                ]
                print("\n" + tabulate(error_msg, tablefmt="fancy_grid", stralign="center") + "\n")
                input("Presione Enter para continuar...")
                continue
            
            cantidad = int(cantidad_input)
            paquetes = paqueteCRUD.mostrarParcial(cantidad)
            paquetes_validos = [p for p in paquetes if p['fecha_inicio'] != "0000-00-00"]
            if paquetes_validos:
                table_data = [
                    [p['id_paquete'], p['nombre_paquete'], p['descripcion'], p['precio_total'],
                     p['fecha_inicio'], p['fecha_fin']] 
                    for p in paquetes_validos
                ]
                headers_paquetes = ["ID", "Nombre", "Descripción", "Precio", "Inicio", "Fin"]
                print(tabulate(table_data, headers=headers_paquetes, tablefmt="fancy_grid", stralign="left"))
            else:
                mensaje = [["No hay paquetes turísticos disponibles para mostrar."]]
                print(tabulate(mensaje, tablefmt="fancy_grid", stralign="center"))
            
            input("Presione Enter para continuar...")
        
        elif opcion == "4":
            # Eliminar paquete
            os.system('cls' if os.name == 'nt' else 'clear')
            titulo_submenu = [["ELIMINAR PAQUETE"]]
            print(tabulate(titulo_submenu, tablefmt="fancy_grid", stralign="center"))
            
            paquetes = paqueteCRUD.mostrarTodos()
            if not paquetes:
                mensaje = [["No hay paquetes disponibles para eliminar."]]
                print(tabulate(mensaje, tablefmt="fancy_grid", stralign="center"))
                input("Presione Enter para continuar...")
                continue
            
            # Filtrar paquetes con fechas válidas
            paquetes_validos = [p for p in paquetes if p['fecha_inicio'] != "0000-00-00" and p['fecha_fin'] != "0000-00-00"]
            if not paquetes_validos:
                mensaje = [["No hay paquetes válidos para eliminar."]]
                print(tabulate(mensaje, tablefmt="fancy_grid", stralign="center"))
                input("Presione Enter para continuar...")
                continue
            
            # Mostrar los paquetes en una tabla
            table_data = [
                [p['id_paquete'], p['nombre_paquete'], p['descripcion'], p['precio_total'], p['fecha_inicio'], p['fecha_fin']] 
                for p in paquetes_validos
            ]
            headers_paquetes = ["ID", "Nombre", "Descripción", "Precio", "Inicio", "Fin"]
            print(tabulate(table_data, headers=headers_paquetes, tablefmt="fancy_grid", stralign="left"))
            
            # Validar el ID del paquete a eliminar
            id_paquete_str = input("Ingrese el ID del paquete a eliminar: ").strip()
            if not id_paquete_str.isdigit():
                error_msg = [
                    ["[Error]"],
                    ["Debe ingresar un número válido."]
                ]
                print("\n" + tabulate(error_msg, tablefmt="fancy_grid", stralign="center") + "\n")
                input("Presione Enter para continuar...")
                continue
            id_paquete = int(id_paquete_str)
            paquete_existente = next((p for p in paquetes_validos if p['id_paquete'] == id_paquete), None)
            if not paquete_existente:
                mensaje = [["No se encontró un paquete con ese ID."]]
                print(tabulate(mensaje, tablefmt="fancy_grid", stralign="center"))
                input("Presione Enter para continuar...")
                continue
            
            # Mostrar resumen antes de confirmar
            resumen = [
                ["Resumen del paquete a eliminar:"],
                [f"ID: {paquete_existente['id_paquete']}"],
                [f"Nombre: {paquete_existente['nombre_paquete']}"],
                [f"Descripción: {paquete_existente['descripcion']}"],
                [f"Precio: {paquete_existente['precio_total']}"],
                [f"Fecha Inicio: {paquete_existente['fecha_inicio']}"],
                [f"Fecha Fin: {paquete_existente['fecha_fin']}"]
            ]
            print("\n" + tabulate(resumen, tablefmt="fancy_grid", stralign="left") + "\n")
            
            # Confirmar eliminación
            confirmar = input("¿Confirmar eliminación? [SI/NO]: ").strip().lower()
            if confirmar == "si":
                if paqueteCRUD.eliminarPaquete(id_paquete):
                    exito_msg = [
                        ["¡Éxito!"],
                        ["Paquete eliminado con éxito."]
                    ]
                    print("\n" + tabulate(exito_msg, tablefmt="fancy_grid", stralign="center") + "\n")
                else:
                    error_msg = [
                        ["[Error]"],
                        ["No se pudo eliminar el paquete. Verifique el ID o la conexión."]
                    ]
                    print("\n" + tabulate(error_msg, tablefmt="fancy_grid", stralign="center") + "\n")
            elif confirmar == "no":
                mensaje = [["Eliminación descartada."]]
                print("\n" + tabulate(mensaje, tablefmt="fancy_grid", stralign="center") + "\n")
            else:
                error_msg = [
                    ["[Error]"],
                    ["Entrada no válida. Debes responder 'SI' o 'NO'."]
                ]
                print("\n" + tabulate(error_msg, tablefmt="fancy_grid", stralign="center") + "\n")
            
            input("Presione Enter para continuar...")
        
        elif opcion == "5":
            # Actualizar paquete
            os.system('cls' if os.name == 'nt' else 'clear')
            titulo_submenu = [["ACTUALIZAR PAQUETE"]]
            print(tabulate(titulo_submenu, tablefmt="fancy_grid", stralign="center"))
            
            paquetes = paqueteCRUD.mostrarTodos()
            paquetes_validos = [p for p in paquetes if p['fecha_inicio'] != "0000-00-00"]
            if not paquetes_validos:
                mensaje = [["No hay paquetes válidos para actualizar."]]
                print(tabulate(mensaje, tablefmt="fancy_grid", stralign="center"))
                input("Presione Enter para continuar...")
                continue
            
            # Mostrar los paquetes en una tabla
            table_data = [
                [p['id_paquete'], p['nombre_paquete'], p['descripcion'], p['precio_total'],
                 p['fecha_inicio'], p['fecha_fin']] 
                for p in paquetes_validos
            ]
            headers_paquetes = ["ID", "Nombre", "Descripción", "Precio", "Inicio", "Fin"]
            print(tabulate(table_data, headers=headers_paquetes, tablefmt="fancy_grid", stralign="left"))
            
            # Capturar ID del paquete a actualizar
            idPaquete = input("Ingrese el ID del paquete a actualizar: ").strip()
            if not idPaquete.isdigit():
                error_msg = [
                    ["[Error]"],
                    ["El ID debe ser numérico."]
                ]
                print("\n" + tabulate(error_msg, tablefmt="fancy_grid", stralign="center") + "\n")
                input("Presione Enter para continuar...")
                continue
            idPaquete = int(idPaquete)
            paquete_existente = next((p for p in paquetes_validos if p['id_paquete'] == idPaquete), None)
            if not paquete_existente:
                mensaje = [["No se encontró un paquete con ese ID."]]
                print(tabulate(mensaje, tablefmt="fancy_grid", stralign="center"))
                input("Presione Enter para continuar...")
                continue
            
            # Capturar nuevos datos
            campos_actualizacion = [
                ["Nuevo nombre:", paquete_existente['nombre_paquete']],
                ["Nueva descripción:", paquete_existente['descripcion']],
                ["Nuevo precio:", paquete_existente['precio_total']],
                ["Nueva fecha de inicio (YYYY-MM-DD):", paquete_existente['fecha_inicio']],
                ["Nueva fecha de fin (YYYY-MM-DD):", paquete_existente['fecha_fin']]
            ]
            print("\n" + tabulate(campos_actualizacion, tablefmt="plain", colalign=("left", "left")) + "\n")
            
            nuevo_nombre = input("Nuevo nombre del paquete: ").strip()
            if not nuevo_nombre:
                error_msg = [
                    ["[Error]"],
                    ["El nombre no puede estar vacío."]
                ]
                print("\n" + tabulate(error_msg, tablefmt="fancy_grid", stralign="center") + "\n")
                input("Presione Enter para continuar...")
                continue
            
            nueva_descripcion = input("Nueva descripción: ").strip()
            if not nueva_descripcion:
                error_msg = [
                    ["[Error]"],
                    ["La descripción no puede estar vacía."]
                ]
                print("\n" + tabulate(error_msg, tablefmt="fancy_grid", stralign="center") + "\n")
                input("Presione Enter para continuar...")
                continue
            
            nuevo_precio_input = input("Nuevo precio: ").strip()
            try:
                nuevo_precio = float(nuevo_precio_input)
            except ValueError:
                error_msg = [
                    ["[Error]"],
                    ["El precio debe ser numérico."]
                ]
                print("\n" + tabulate(error_msg, tablefmt="fancy_grid", stralign="center") + "\n")
                input("Presione Enter para continuar...")
                continue
            
            nueva_fecha_inicio = input("Nueva fecha de inicio (YYYY-MM-DD): ").strip()
            nueva_fecha_fin = input("Nueva fecha de fin (YYYY-MM-DD): ").strip()
            
            # Validar fechas (opcional, dependiendo de tus necesidades)
            # Puedes agregar validaciones de formato de fecha aquí si es necesario
            
            # Intentar actualizar el paquete
            if paqueteCRUD.modificarPaquete(idPaquete, nuevo_nombre, nueva_descripcion, nuevo_precio,
                                            nueva_fecha_inicio, nueva_fecha_fin):
                exito_msg = [
                    ["¡Éxito!"],
                    ["Paquete actualizado correctamente."]
                ]
                print("\n" + tabulate(exito_msg, tablefmt="fancy_grid", stralign="center") + "\n")
            else:
                error_msg = [
                    ["[Error]"],
                    ["Error al actualizar el paquete."]
                ]
                print("\n" + tabulate(error_msg, tablefmt="fancy_grid", stralign="center") + "\n")
            
            input("Presione Enter para continuar...")
        
        elif opcion == "6":
            # Generar paquetes aleatorios
            os.system('cls' if os.name == 'nt' else 'clear')
            titulo_submenu = [["GENERAR PAQUETES ALEATORIOS"]]
            print(tabulate(titulo_submenu, tablefmt="fancy_grid", stralign="center"))
            
            print("\n¿Cuántos paquetes aleatorios desea generar?\n")
            cantidad_input = input(">> ").strip()
            if not cantidad_input.isdigit():
                error_msg = [
                    ["[Error]"],
                    ["Debe ingresar un número válido."]
                ]
                print("\n" + tabulate(error_msg, tablefmt="fancy_grid", stralign="center") + "\n")
                input("Presione Enter para continuar...")
                continue
            
            cantidad = int(cantidad_input)
            if cantidad <= 0:
                error_msg = [
                    ["[Error]"],
                    ["La cantidad debe ser mayor a 0."]
                ]
                print("\n" + tabulate(error_msg, tablefmt="fancy_grid", stralign="center") + "\n")
                input("Presione Enter para continuar...")
                continue
            
            # Generar paquetes aleatorios
            for i in range(cantidad):
                paquete, destinos = Paquete.generarPaqueteAleatorio()  # Generar paquete y destinos
                if paquete and destinos:
                    if paqueteCRUD.agregarPaqueteConDestino(paquete, destinos):
                        exito_msg = [
                            ["¡Éxito!"],
                            [f"Paquete '{paquete.nombre_paquete}' generado y registrado con éxito."]
                        ]
                        print("\n" + tabulate(exito_msg, tablefmt="fancy_grid", stralign="center") + "\n")
                    else:
                        error_msg = [
                            ["[Error]"],
                            [f"Error al registrar el paquete '{paquete.nombre_paquete}'."]
                        ]
                        print("\n" + tabulate(error_msg, tablefmt="fancy_grid", stralign="center") + "\n")
                else:
                    error_msg = [
                        ["[Error]"],
                        ["No se pudo generar el paquete debido a un error o falta de destinos."]
                    ]
                    print("\n" + tabulate(error_msg, tablefmt="fancy_grid", stralign="center") + "\n")
            
            input("Presione Enter para continuar...")
        
        elif opcion == "7":
            # Salir del menú de paquetes
            os.system('cls' if os.name == 'nt' else 'clear')
            mensaje = [["Regresando al menú principal..."]]
            print(tabulate(mensaje, tablefmt="fancy_grid", stralign="center"))
            input("Presione Enter para continuar...")
            break
        
        else:
            # Opción no válida
            os.system('cls' if os.name == 'nt' else 'clear')
            error_msg = [
                ["[Error]"],
                ["Opción no válida. Inténtalo de nuevo."]
            ]
            print(tabulate(error_msg, tablefmt="fancy_grid", stralign="center"))
            input("Presione Enter para continuar...")

def menuReservas(id_usuario):
    while True:
        try:
            # Limpiar la pantalla
            os.system('cls' if os.name == 'nt' else 'clear')
            
            # Título del menú utilizando tabulate
            titulo = [["MENÚ RESERVAS"]]
            print(tabulate(titulo, tablefmt="fancy_grid", stralign="center"))
            
            # Opciones del menú organizadas en una tabla
            opciones = [
                ["1", "Mostrar todas las reservas"],
                ["2", "Mostrar una reserva específica"],
                ["3", "Mostrar reservas por estado"],
                ["4", "Realizar una nueva reserva"],
                ["5", "Cancelar una reserva"],
                ["6", "Salir"]
            ]
            headers = ["Opción", "Descripción"]
            print(tabulate(opciones, headers=headers, tablefmt="fancy_grid", stralign="left"))
            print()  # Espacio adicional para mejor visualización
            
            # Captura de la opción seleccionada por el usuario
            opcion = input("Seleccione una opción (1-6): ").strip()
            
            if opcion == "1":
                # Mostrar todas las reservas
                os.system('cls' if os.name == 'nt' else 'clear')
                titulo_submenu = [["MOSTRAR TODAS LAS RESERVAS"]]
                print(tabulate(titulo_submenu, tablefmt="fancy_grid", stralign="center"))
                
                reservas = reservaCRUD.mostrarTodos()
                if reservas:
                    table_data = [
                        [r['id_reserva'], r['id_usuario'], r['id_paquete'], r['fecha_reserva'], r['estado']] 
                        for r in reservas
                    ]
                    headers_reservas = ["ID Reserva", "ID Usuario", "ID Paquete", "Fecha Reserva", "Estado"]
                    print(tabulate(table_data, headers=headers_reservas, tablefmt="fancy_grid", stralign="left"))
                else:
                    print(tabulate([["No hay reservas registradas."]], tablefmt="fancy_grid", stralign="center"))
                
                input("Presione Enter para continuar...")
            
            elif opcion == "2":
                # Mostrar una reserva específica
                os.system('cls' if os.name == 'nt' else 'clear')
                titulo_submenu = [["MOSTRAR UNA RESERVA ESPECÍFICA"]]
                print(tabulate(titulo_submenu, tablefmt="fancy_grid", stralign="center"))
                
                while True:
                    id_reserva = input("Ingrese el ID de la reserva: ").strip()
                    if id_reserva.isdigit():
                        reserva = reservaCRUD.mostrarUno(id_reserva)
                        if reserva:
                            table_data = [
                                [reserva['id_reserva'], reserva['id_usuario'], reserva['id_paquete'], reserva['fecha_reserva'], reserva['estado']]
                            ]
                            headers_reserva = ["ID Reserva", "ID Usuario", "ID Paquete", "Fecha Reserva", "Estado"]
                            print(tabulate(table_data, headers=headers_reserva, tablefmt="fancy_grid", stralign="left"))
                        else:
                            print(tabulate([["Reserva no encontrada."]], tablefmt="fancy_grid", stralign="center"))
                        break
                    else:
                        print(tabulate([["[Error]"], ["Debe ingresar un ID válido (numérico)."]], tablefmt="fancy_grid", stralign="center"))
                
                input("Presione Enter para continuar...")
            
            elif opcion == "3":
                # Mostrar reservas por estado
                os.system('cls' if os.name == 'nt' else 'clear')
                titulo_submenu = [["MOSTRAR RESERVAS POR ESTADO"]]
                print(tabulate(titulo_submenu, tablefmt="fancy_grid", stralign="center"))
                
                estados_opciones = [
                    ["1", "Pendiente"],
                    ["2", "Confirmada"],
                    ["3", "Cancelada"]
                ]
                print(tabulate(estados_opciones, headers=["Opción", "Estado"], tablefmt="fancy_grid", stralign="left"))
                
                estado_opcion = input("Seleccione el número del estado: ").strip()
                estados_validos = {"1": "pendiente", "2": "confirmada", "3": "cancelada"}
                
                if estado_opcion in estados_validos:
                    estado = estados_validos[estado_opcion]
                    reservas = reservaCRUD.mostrarParcial(estado)
                    if reservas:
                        table_data = [[r['id_reserva'], r['id_usuario'], r['id_paquete'], r['fecha_reserva'], r['estado']] for r in reservas]
                        print(tabulate(table_data, headers=["ID Reserva", "ID Usuario", "ID Paquete", "Fecha Reserva", "Estado"], tablefmt="fancy_grid"))
                    else:
                        print(tabulate([["No hay reservas con ese estado."]], tablefmt="fancy_grid", stralign="center"))
                else:
                    print(tabulate([["[Error]"], ["Opción no válida."]], tablefmt="fancy_grid", stralign="center"))
                
                input("Presione Enter para continuar...")

            elif opcion == "4":
                # Realizar una nueva reserva
                os.system('cls' if os.name == 'nt' else 'clear')
                titulo_submenu = [["REALIZAR UNA NUEVA RESERVA"]]
                print(tabulate(titulo_submenu, tablefmt="fancy_grid", stralign="center"))

                # Mostrar paquetes disponibles
                paquetes = paqueteCRUD.mostrarTodos()
                if not paquetes:
                    print(tabulate([["No hay paquetes disponibles."]], tablefmt="fancy_grid", stralign="center"))
                    input("Presione Enter para continuar...")
                    continue

                table_data_paquetes = [[p['id_paquete'], p['nombre_paquete'], f"${p['precio_total']:.2f}"] for p in paquetes]
                print(tabulate(table_data_paquetes, headers=["ID Paquete", "Nombre", "Precio"], tablefmt="fancy_grid"))
                id_paquete = input("Ingrese el ID del paquete: ").strip()

                # Mostrar usuarios disponibles
                print("\nUsuarios disponibles:")
                usuarios = usuarioCRUD.mostrarTodos()  # Se asume que existe una función para mostrar usuarios
                if not usuarios:
                    print(tabulate([["No hay usuarios disponibles."]], tablefmt="fancy_grid", stralign="center"))
                    input("Presione Enter para continuar...")
                    continue

                table_data_usuarios = [[u['id_usuario'], u['nombre']] for u in usuarios]
                print(tabulate(table_data_usuarios, headers=["ID Usuario", "Nombre"], tablefmt="fancy_grid"))
                id_usuario = input("Ingrese el ID del usuario: ").strip()

                # Mostrar resumen de la reserva
                paquete_seleccionado = next((p for p in paquetes if str(p['id_paquete']) == id_paquete), None)
                usuario_seleccionado = next((u for u in usuarios if str(u['id_usuario']) == id_usuario), None)

                if not paquete_seleccionado or not usuario_seleccionado:
                    print(tabulate([["[Error]"], ["ID de paquete o usuario no válido."]], tablefmt="fancy_grid", stralign="center"))
                    input("Presione Enter para continuar...")
                    continue

                resumen_reserva = [
                    ["Usuario:", f"{usuario_seleccionado['nombre']} (ID: {id_usuario})"],
                    ["Paquete:", f"{paquete_seleccionado['nombre_paquete']} (ID: {id_paquete})"],
                    ["Precio:", f"${paquete_seleccionado['precio_total']:.2f}"],
                    ["Fecha de Reserva:", datetime.now().strftime("%d-%m-%Y")],
                ]
                print("\nResumen de la reserva:")
                print(tabulate(resumen_reserva, tablefmt="fancy_grid"))

                while True:
                    confirmacion = input("¿Confirmar la reserva? (s/n): ").strip().lower()
                    if confirmacion == 's':
                        fecha_reserva = datetime.now().strftime("%d-%m-%Y")
                        nueva_reserva = Reserva(id_usuario, id_paquete, fecha_reserva)

                        if reservaCRUD.agregarReserva(nueva_reserva):
                            print(tabulate([["¡Éxito!"], ["Reserva confirmada con éxito."]], tablefmt="fancy_grid", stralign="center"))
                        else:
                            print(tabulate([["[Error]"], ["No se pudo realizar la reserva."]], tablefmt="fancy_grid", stralign="center"))
                        break  # Sale del bucle después de una respuesta válida ('s')
                    elif confirmacion == 'n':
                        print(tabulate([["Operación cancelada."]], tablefmt="fancy_grid"))
                        break  # Sale del bucle después de una respuesta válida ('n')
                    else:
                        print(tabulate([["Opción inválida."], ["Por favor ingrese 's' para sí o 'n' para no."]], tablefmt="fancy_grid"))

            
            elif opcion == "5":
                # Cancelar una reserva
                os.system('cls' if os.name == 'nt' else 'clear')
                titulo_submenu = [["CANCELAR UNA RESERVA"]]
                print(tabulate(titulo_submenu, tablefmt="fancy_grid", stralign="center"))

                reservas = reservaCRUD.mostrarTodos()
                if not reservas:
                    print(tabulate([["No hay reservas disponibles."]], tablefmt="fancy_grid", stralign="center"))
                    input("Presione Enter para continuar...")
                    continue
                
                table_data = [[r['id_reserva'], r['estado']] for r in reservas]
                print(tabulate(table_data, headers=["ID Reserva", "Estado"], tablefmt="fancy_grid"))
                
                id_reserva = input("Ingrese el ID de la reserva a cancelar: ").strip()
                if reservaCRUD.cambiarEstadoReserva(id_reserva, "cancelada"):
                    print(tabulate([["¡Éxito!"], ["Reserva cancelada con éxito."]], tablefmt="fancy_grid", stralign="center"))
                else:
                    print(tabulate([["[Error]"], ["No se pudo cancelar la reserva."]], tablefmt="fancy_grid", stralign="center"))
                
                input("Presione Enter para continuar...")

            elif opcion == "6":
                # Salir del menú
                print(tabulate([["Saliendo al menú principal..."]], tablefmt="fancy_grid", stralign="center"))
                input("Presione Enter para continuar...")
                break

            else:
                print(tabulate([["[Error]"], ["Opción no válida. Intente de nuevo."]], tablefmt="fancy_grid", stralign="center"))
                input("Presione Enter para continuar...")

        except Exception as e:
            print(tabulate([["[Error]"], [f"Ocurrió un error inesperado: {e}"]], tablefmt="fancy_grid", stralign="center"))
            input("Presione Enter para continuar...")

def menuAdmin(nombre, idUsuario):
    while True:
        # Limpiar la pantalla
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Título del menú utilizando tabulate
        titulo = [["MENÚ ADMIN"]]
        print(tabulate(titulo, tablefmt="fancy_grid", stralign="center"))
        
        # Opciones del menú organizadas en una tabla
        opciones = [
            ["1", "Gestionar Destinos"],
            ["2", "Gestionar Paquetes"],
            ["3", "Gestionar Reservas"],
            ["4", "Salir"]
        ]
        headers = ["Opción", "Descripción"]
        print(tabulate(opciones, headers=headers, tablefmt="fancy_grid", stralign="left"))
        print()  # Espacio adicional para mejor visualización
        
        # Captura de la opción seleccionada por el usuario
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            # Gestionar Destinos
            menuDestinos()
        
        elif opcion == "2":
            # Gestionar Paquetes
            menuPaquetes(nombre)
        
        elif opcion == "3":
            # Gestionar Reservas
            menuReservas(idUsuario)
        
        elif opcion == "4":
            # Salir del menú Admin
            os.system('cls' if os.name == 'nt' else 'clear')
            mensaje = [["Saliendo del menú Admin..."]]
            print(tabulate(mensaje, tablefmt="fancy_grid", stralign="center"))
            input("Presione Enter para continuar...")
            break
        
        else:
            # Opción no válida
            os.system('cls' if os.name == 'nt' else 'clear')
            error_msg = [
                ["[Error]"],
                ["Opción no válida. Intente nuevamente."]
            ]
            print(tabulate(error_msg, tablefmt="fancy_grid", stralign="center"))
            input("Presione Enter para continuar...")

def menuClientes(nombre, idUsuario):
    while True:
        # Limpiar la pantalla
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Título del menú utilizando tabulate
        titulo = [["MENÚ CLIENTE"]]
        print(tabulate(titulo, tablefmt="fancy_grid", stralign="center"))
        
        # Opciones del menú organizadas en una tabla
        opciones = [
            ["1", "Consultar Paquetes Turísticos"],
            ["2", "Realizar Reserva"],
            ["3", "Mostrar Reservas"],
            ["4", "Cancelar Reserva"],
            ["5", "Salir"]
        ]
        headers = ["Opción", "Descripción"]
        print(tabulate(opciones, headers=headers, tablefmt="fancy_grid", stralign="left"))
        print()  # Espacio adicional para mejor visualización
        
        # Captura de la opción seleccionada por el usuario
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            # Consultar Paquetes Turísticos
            os.system('cls' if os.name == 'nt' else 'clear')
            titulo_submenu = [["CONSULTAR PAQUETES TURÍSTICOS"]]
            print(tabulate(titulo_submenu, tablefmt="fancy_grid", stralign="center"))
            
            paquetes = paqueteCRUD.mostrarTodos()
            if paquetes:
                table_data = [
                    [
                        p['id_paquete'], 
                        p['nombre_paquete'], 
                        p['descripcion'], 
                        p['precio_total'], 
                        p['fecha_inicio'], 
                        p['fecha_fin']
                    ] 
                    for p in paquetes
                ]
                headers_paquetes = ["ID", "Nombre", "Descripción", "Precio", "Fecha Inicio", "Fecha Fin"]
                print(tabulate(table_data, headers=headers_paquetes, tablefmt="fancy_grid", stralign="left"))
            else:
                mensaje = [["No hay paquetes disponibles."]]
                print(tabulate(mensaje, tablefmt="fancy_grid", stralign="center"))
            
            input("Presione Enter para continuar...")
        
        elif opcion == "2":
            # Realizar Reserva
            os.system('cls' if os.name == 'nt' else 'clear')
            titulo_submenu = [["REALIZAR RESERVA"]]
            print(tabulate(titulo_submenu, tablefmt="fancy_grid", stralign="center"))
            
            try:
                paquetes = paqueteCRUD.mostrarTodos()
                if paquetes:
                    table_data_paquetes = [
                        [p['id_paquete'], p['nombre_paquete'], p['descripcion'], p['precio_total'], p['fecha_inicio'], p['fecha_fin']]
                        for p in paquetes
                    ]
                    headers_paquetes = ["ID", "Nombre", "Descripción", "Precio", "Fecha Inicio", "Fecha Fin"]
                    print("\nPaquetes disponibles:\n")
                    print(tabulate(table_data_paquetes, headers=headers_paquetes, tablefmt="fancy_grid", stralign="left"))
                else:
                    mensaje = [["No hay paquetes disponibles."]]
                    print(tabulate(mensaje, tablefmt="fancy_grid", stralign="center"))
                    input("Presione Enter para continuar...")
                    continue

                # Solicitar y validar el ID del paquete
                while True:
                    idPaquete_input = input("Ingrese el ID del paquete turístico que desea reservar: ").strip()
                    if idPaquete_input.isdigit():
                        idPaquete = int(idPaquete_input)
                        if any(idPaquete == p['id_paquete'] for p in paquetes):
                            break
                        else:
                            error_msg = [
                                ["[Error]"],
                                ["El ID del paquete no existe en la lista. Intente nuevamente."]
                            ]
                            print("\n" + tabulate(error_msg, tablefmt="fancy_grid", stralign="center") + "\n")
                    else:
                        error_msg = [
                            ["[Error]"],
                            ["El ID del paquete debe ser numérico."]
                        ]
                        print("\n" + tabulate(error_msg, tablefmt="fancy_grid", stralign="center") + "\n")

                # Solicitar y validar la fecha de reserva
                while True:
                    fecha_reserva_input = input("Por favor, ingrese la fecha de reserva (DD-MM-YYYY): ").strip()
                    try:
                        # Validar el formato de la fecha
                        datetime.strptime(fecha_reserva_input, "%d-%m-%Y")
                        break
                    except ValueError:
                        print("Error: La fecha debe estar en el formato DD-MM-YYYY. Intente nuevamente.")

                # Crear reserva usando el ID del usuario autenticado
                nueva_reserva = Reserva(idUsuario, idPaquete, fecha_reserva_input)
                if agregarReserva(nueva_reserva):
                    print("¡Reserva creada con éxito!")
                else:
                    print("No pudimos registrar tu reserva. Intenta nuevamente.")
                            
            except Exception as e:
                error_msg = [
                    ["[Error]"],
                    [f"Hubo un error al intentar registrar la reserva: {e}"]
                ]
                print("\n" + tabulate(error_msg, tablefmt="fancy_grid", stralign="center") + "\n")
            
            input("Presione Enter para continuar...")
        
        elif opcion == "3":
            # Mostrar Reservas
            os.system('cls' if os.name == 'nt' else 'clear')
            titulo_submenu = [["MOSTRAR TUS RESERVAS"]]
            print(tabulate(titulo_submenu, tablefmt="fancy_grid", stralign="center"))
            
            try:
                reservas = reservaCRUD.mostrarReservaPorId(idUsuario)
                if reservas:
                    table_data = [
                        [r['id_reserva'], r['id_paquete'], r['fecha_reserva'], r['estado']] 
                        for r in reservas
                    ]
                    headers_reservas = ["ID Reserva", "ID Paquete", "Fecha Reserva", "Estado"]
                    print(tabulate(table_data, headers=headers_reservas, tablefmt="fancy_grid", stralign="left"))
                else:
                    mensaje = [["No tienes reservas registradas."]]
                    print(tabulate(mensaje, tablefmt="fancy_grid", stralign="center"))
            
            except Exception as e:
                error_msg = [
                    ["[Error]"],
                    [f"Hubo un error al intentar mostrar las reservas: {e}"]
                ]
                print("\n" + tabulate(error_msg, tablefmt="fancy_grid", stralign="center") + "\n")
            
            input("Presione Enter para continuar...")
        
        elif opcion == "4":
            # Cancelar Reserva
            os.system('cls' if os.name == 'nt' else 'clear')
            titulo_submenu = [["CANCELAR RESERVA"]]
            print(tabulate(titulo_submenu, tablefmt="fancy_grid", stralign="center"))
            
            try:
                reservas = reservaCRUD.mostrarReservaPorId(idUsuario)
                if reservas:
                    table_data = [
                        [r['id_reserva'], r['id_paquete'], r['fecha_reserva'], r['estado']] 
                        for r in reservas
                    ]
                    headers_reservas = ["ID Reserva", "ID Paquete", "Fecha Reserva", "Estado"]
                    print(tabulate(table_data, headers=headers_reservas, tablefmt="fancy_grid", stralign="left"))
                    
                    # Solicitar y validar el ID de la reserva a cancelar
                    while True:
                        idReserva_input = input("Ingrese el ID de la reserva que desea cancelar: ").strip()
                        if idReserva_input.isdigit():
                            idReserva = int(idReserva_input)
                            reservaSeleccionada = next((res for res in reservas if res['id_reserva'] == idReserva), None)
                            if reservaSeleccionada:
                                break
                            else:
                                error_msg = [
                                    ["[Error]"],
                                    ["No se encontró una reserva con ese ID. Intente nuevamente."]
                                ]
                                print("\n" + tabulate(error_msg, tablefmt="fancy_grid", stralign="center") + "\n")
                        else:
                            error_msg = [
                                ["[Error]"],
                                ["Debe ingresar un ID válido (numérico)."]
                            ]
                            print("\n" + tabulate(error_msg, tablefmt="fancy_grid", stralign="center") + "\n")
                    
                    # Confirmar cancelación
                    confirmar = input("\n¿Está seguro de que desea cancelar esta reserva? [SI/NO]: ").strip().upper()
                    if confirmar == "SI":
                        reservaACancelar = Reserva(idUsuario, reservaSeleccionada['id_paquete'], reservaSeleccionada['fecha_reserva'], idReserva=idReserva)
                        if reservaACancelar.cancelarReserva():
                            exito_msg = [
                                ["¡Éxito!"],
                                ["Tu reserva ha sido cancelada con éxito."]
                            ]
                            print("\n" + tabulate(exito_msg, tablefmt="fancy_grid", stralign="center") + "\n")
                        else:
                            error_msg = [
                                ["[Error]"],
                                ["No pudimos cancelar tu reserva en este momento."]
                            ]
                            print("\n" + tabulate(error_msg, tablefmt="fancy_grid", stralign="center") + "\n")
                    elif confirmar == "NO":
                        mensaje = [["Cancelación de reserva descartada."]]
                        print("\n" + tabulate(mensaje, tablefmt="fancy_grid", stralign="center") + "\n")
                    else:
                        error_msg = [
                            ["[Error]"],
                            ["Opción inválida. Debes responder 'SI' o 'NO'."]
                        ]
                        print("\n" + tabulate(error_msg, tablefmt="fancy_grid", stralign="center") + "\n")
                else:
                    mensaje = [["No tienes reservas registradas para cancelar."]]
                    print(tabulate(mensaje, tablefmt="fancy_grid", stralign="center"))
            
            except Exception as e:
                error_msg = [
                    ["[Error]"],
                    [f"Hubo un error al intentar cancelar la reserva: {e}"]
                ]
                print("\n" + tabulate(error_msg, tablefmt="fancy_grid", stralign="center") + "\n")
            
            input("Presione Enter para continuar...")
        
        elif opcion == "5":
            # Salir del menú Cliente
            os.system('cls' if os.name == 'nt' else 'clear')
            mensaje = [["Saliendo del menú Cliente..."]]
            print(tabulate(mensaje, tablefmt="fancy_grid", stralign="center"))
            input("Presione Enter para continuar...")
            break
        
        else:
            # Opción no válida
            os.system('cls' if os.name == 'nt' else 'clear')
            error_msg = [
                ["[Error]"],
                ["Opción no válida. Intente nuevamente."]
            ]
            print(tabulate(error_msg, tablefmt="fancy_grid", stralign="center"))
            input("Presione Enter para continuar...")

def main():
    while True:
        # Limpiar la pantalla
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Título del menú utilizando tabulate
        titulo = [["BIENVENIDO AL SISTEMA DE RESERVAS TURÍSTICAS"]]
        print(tabulate(titulo, tablefmt="fancy_grid", stralign="center"))
        
        # Opciones del menú organizadas en una tabla
        opciones = [
            ["1", "Login"],
            ["2", "Registro"],
            ["3", "Salir"]
        ]
        headers = ["Opción", "Descripción"]
        print(tabulate(opciones, headers=headers, tablefmt="fancy_grid", stralign="left"))
        print()  # Espacio adicional para mejor visualización
        
        # Captura de la opción seleccionada por el usuario
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            # Opción 1: Login
            os.system('cls' if os.name == 'nt' else 'clear')
            titulo_login = [["INICIAR SESIÓN"]]
            print(tabulate(titulo_login, tablefmt="fancy_grid", stralign="center"))
            
            try:
                # Llamada a la función login (asegúrate de tenerla definida)
                datos_usuario = login()
                
                # Validar si el login fue exitoso
                if datos_usuario and datos_usuario.get("autenticado"):
                    nombre = datos_usuario.get("nombre", "Usuario")
                    tipo_usuario = datos_usuario.get("tipo_usuario")
                    id_usuario = datos_usuario.get("id_usuario")

                    if not tipo_usuario or not id_usuario:
                        raise ValueError("Faltan datos necesarios del usuario.")

                    # Mensaje de bienvenida en tabla
                    mensaje_bienvenida = [[f"¡Bienvenido, {nombre}!"]]
                    print("\n" + tabulate(mensaje_bienvenida, tablefmt="fancy_grid", stralign="center") + "\n")
                    input("Presione Enter para continuar...")
                    
                    # Redirigir al menú correspondiente según el tipo de usuario
                    if tipo_usuario == "administrador":
                        menuAdmin(nombre, id_usuario)
                    elif tipo_usuario == "cliente":
                        menuClientes(nombre, id_usuario)
                    else:
                        print(tabulate([["[Error]"], ["Tipo de usuario no reconocido."]], tablefmt="fancy_grid", stralign="center"))
                        input("Presione Enter para continuar...")
                else:
                    # Mensaje de error en tabla
                    mensaje_error = [["[Error]"], ["Credenciales inválidas. Por favor, inténtelo de nuevo."]]
                    print("\n" + tabulate(mensaje_error, tablefmt="fancy_grid", stralign="center") + "\n")
                    input("Presione Enter para continuar...")
            
            except Exception as e:
                # Captura de cualquier error inesperado
                mensaje_error = [["[Error]"], [f"Ocurrió un error: {e}"]]
                print("\n" + tabulate(mensaje_error, tablefmt="fancy_grid", stralign="center") + "\n")
                input("Presione Enter para continuar...")
        
        elif opcion == "2":
            # Opción 2: Registro
            os.system('cls' if os.name == 'nt' else 'clear')
            titulo_registro = [["REGISTRO DE NUEVO USUARIO"]]
            print(tabulate(titulo_registro, tablefmt="fancy_grid", stralign="center"))
            
            # Llamada a la función registrarUsuario (asegúrate de tenerla definida)
            registrarUsuario()
            
            # Mensaje de éxito en tabla
            mensaje_exito = [["¡Éxito!"]]
            print("\n" + tabulate(mensaje_exito, tablefmt="fancy_grid", stralign="center") + "\n")
            input("Presione Enter para continuar...")
        
        elif opcion == "3":
            # Opción 3: Salir
            os.system('cls' if os.name == 'nt' else 'clear')
            mensaje_salida = [["Gracias por usar el sistema. ¡Hasta pronto!"]]
            print(tabulate(mensaje_salida, tablefmt="fancy_grid", stralign="center"))
            break
        
        else:
            # Opción no válida
            mensaje_error = [["[Error]"], ["Opción no válida. Intente nuevamente."]]
            print("\n" + tabulate(mensaje_error, tablefmt="fancy_grid", stralign="center") + "\n")
            input("Presione Enter para continuar...")
if __name__ == "__main__":
    main()

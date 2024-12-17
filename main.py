import os
import json
import random
from datetime import datetime, timedelta
from tabulate import tabulate

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
    print("---------------------------")
    print("     REGISTRAR USUARIO     ")
    print("---------------------------")
    while True:
        nombre = input("Ingrese Usuario: ").strip()
        correo = input("Ingrese Correo: ").strip()
        password = input("Ingrese Contraseña: ").strip()
        tipoUsuario = input("Ingrese tipo Usuario (administrador/cliente): ").strip().lower()
        if not nombre or not password or not correo or not tipoUsuario:
            print("Usuario, contraseña, correo y/o tipo Usuario no pueden estar vacíos.")
            continue
        if tipoUsuario not in ["administrador", "cliente"]:
            print("El tipo de usuario debe ser 'administrador' o 'cliente'.")
            continue
        nuevoUsuario = Usuario.registrarUsuario(nombre, correo, password, tipoUsuario)
        if nuevoUsuario:
            print(f"Usuario {nombre} registrado con éxito.")
            input("Presione Enter para continuar...")
            return nuevoUsuario
        else:
            retry = input("¿Intentar de nuevo? [SI/NO]: ").strip().lower()
            if retry != "si":
                return None


def login():
    print("---------------------------")
    print("          LOGIN            ")
    print("---------------------------")
    while True:
        correo = input("Ingrese Correo: ").strip()
        password = input("Ingrese Contraseña: ").strip()

        if not correo or not password:
            print("Los campos de correo y contraseña no pueden estar vacíos. Intente nuevamente.")
            continue
        resultado_login = Usuario.login(correo, password)
        if resultado_login["autenticado"]:
            print("\n¡Inicio de sesión exitoso!")
            input("Presione Enter para continuar...")
            return {
                "tipo_usuario": resultado_login["tipo_usuario"],
                "nombre": resultado_login["nombre"],
                "correo": correo,
                "id_usuario": resultado_login["id_usuario"],
                "autenticado": True
            }
        else:
            print("\nCorreo o contraseña incorrectos.")
            retry = input("¿Desea intentarlo de nuevo? [SI/NO]: ").strip().lower()
            if retry != "si":
                print("Cancelando inicio de sesión.")
                return None


def menuDestinos():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("--------------------------")
        print("       MENÚ DESTINOS      ")
        print("--------------------------")
        print("1. Registrar un nuevo destino")
        print("2. Mostrar todos los destinos")
        print("3. Mostrar un destino")
        print("4. Mostrar destinos parciales")
        print("5. Actualizar destino")
        print("6. Eliminar destino")
        print("7. Salir")
        opcion = input("Por favor, selecciona una opción (1-7): ").strip()

        if opcion == "1":
            print("\n--- REGISTRAR UN NUEVO DESTINO ---")
            nombre = input("Nombre: ").strip()
            descripcion = input("Descripción: ").strip()
            actividades = input("Actividades: ").strip()

            # Validar el costo
            while True:
                costo_str = input("Costo: ").strip()
                if not costo_str:
                    print("El costo no puede estar vacío.")
                    continue
                try:
                    costo = int(costo_str)
                    break
                except ValueError:
                    print("Error: El costo debe ser numérico.")

            destino = Destino(nombre, descripcion, actividades, costo)
            if destinoCRUD.agregarDestino(destino):
                print("Destino registrado con éxito.")
            else:
                print("Error al registrar el destino. Verifique la conexión o los datos.")

            input("Presione Enter para continuar...")


        elif opcion == "2":
            print("\n--- MOSTRAR TODOS LOS DESTINOS ---")
            destinos = destinoCRUD.mostrarTodos()
            if destinos:
                table_data = [[d['id_destino'], d['nombre'], d['descripcion'], d['actividades'], d['costo']] 
                              for d in destinos]
                print(tabulate(table_data, headers=["ID", "Nombre", "Descripción", "Actividades", "Costo"], tablefmt="fancy_grid"))
            else:
                print("No hay destinos disponibles.")
            input("Presione Enter para continuar...")

        elif opcion == "3":
            print("\n--- MOSTRAR UN DESTINO ---")
            id_destino = input("Ingrese el ID del destino: ").strip()
            destino = destinoCRUD.mostrarUno(id_destino)
            if destino:
                table_data = [[destino['id_destino'], destino['nombre'], destino['descripcion'], destino['actividades'], destino['costo']]]
                print(tabulate(table_data, headers=["ID", "Nombre", "Descripción", "Actividades", "Costo"], tablefmt="fancy_grid"))
            else:
                print("Destino no encontrado.")
            input("Presione Enter para continuar...")

        elif opcion == "4":
            print("\n--- MOSTRAR DESTINOS PARCIALES ---")
            try:
                cantidad = int(input("Cantidad de destinos a mostrar: ").strip())
                destinos = destinoCRUD.mostrarParcial(cantidad)
                if destinos:
                    table_data = [[d['id_destino'], d['nombre'], d['descripcion'], d['actividades'], d['costo']] 
                                  for d in destinos]
                    print(tabulate(table_data, headers=["ID", "Nombre", "Descripción", "Actividades", "Costo"], tablefmt="fancy_grid"))
                else:
                    print("No hay destinos disponibles.")
            except ValueError:
                print("Error: La cantidad debe ser numérica.")
            input("Presione Enter para continuar...")

        elif opcion == "5":
            print("\n--- ACTUALIZAR DESTINO ---")
            destinos = destinoCRUD.mostrarTodos()
            
            # Si no hay destinos, no podemos actualizar nada
            if not destinos:
                print("No hay destinos disponibles para actualizar.")
                input("Presione Enter para continuar...")
                continue
            
            # Mostrar los destinos en una tabla
            table_data = [[d['id_destino'], d['nombre'], d['descripcion'], d['actividades'], d['costo']] for d in destinos]
            print(tabulate(table_data, headers=["ID", "Nombre", "Descripción", "Actividades", "Costo"], tablefmt="fancy_grid"))

            # Validar el ID de destino a actualizar
            while True:
                id_destino_str = input("Ingrese el ID del destino a actualizar: ").strip()
                if not id_destino_str.isdigit():
                    print("Debes ingresar un número válido.")
                    continue
                id_destino = int(id_destino_str)
                # Verificar que el ID exista en la lista de destinos
                destino_existente = next((d for d in destinos if d['id_destino'] == id_destino), None)
                if destino_existente:
                    break
                else:
                    print("No se encontró un destino con ese ID. Intente nuevamente.")

            # Solicitar nuevos datos, asegurando que no estén vacíos
            while True:
                nuevo_nombre = input("Nuevo nombre: ").strip()
                if nuevo_nombre:
                    break
                else:
                    print("El nombre no puede estar vacío.")

            while True:
                nueva_descripcion = input("Nueva descripción: ").strip()
                if nueva_descripcion:
                    break
                else:
                    print("La descripción no puede estar vacía.")

            while True:
                nuevas_actividades = input("Nuevas actividades: ").strip()
                if nuevas_actividades:
                    break
                else:
                    print("Las actividades no pueden estar vacías.")

            while True:
                nuevo_costo_str = input("Nuevo costo: ").strip()
                if not nuevo_costo_str:
                    print("El costo no puede estar vacío.")
                    continue
                try:
                    nuevo_costo = int(nuevo_costo_str)
                    break
                except ValueError:
                    print("Error: El costo debe ser numérico.")

            # Mostrar resumen de cambios antes de confirmar
            print("\nResumen de cambios:")
            print(f"Nombre: {destino_existente['nombre']} -> {nuevo_nombre}")
            print(f"Descripción: {destino_existente['descripcion']} -> {nueva_descripcion}")
            print(f"Actividades: {destino_existente['actividades']} -> {nuevas_actividades}")
            print(f"Costo: {destino_existente['costo']} -> {nuevo_costo}")

            # Confirmar cambios
            while True:
                confirmar = input("¿Confirmar cambios? [SI/NO]: ").strip().lower()
                if not confirmar:
                    print("La respuesta no puede estar vacía. Debes responder SI o NO.")
                    continue
                if confirmar == "si":
                    if destinoCRUD.modificarDestino(id_destino, nuevo_nombre, nueva_descripcion, nuevas_actividades, nuevo_costo):
                        print("Cambios guardados con éxito.")
                    else:
                        print("No se pudieron guardar los cambios. Verifique el ID o la conexión.")
                    break
                elif confirmar == "no":
                    print("Cambios descartados.")
                    break
                else:
                    print("Entrada no válida. Debes responder 'SI' o 'NO'.")

            input("Presione Enter para continuar...")

        elif opcion == "6":
            print("\n--- ELIMINAR DESTINO ---")
            destinos = destinoCRUD.mostrarTodos()

            # Si no hay destinos, no se puede eliminar nada.
            if not destinos:
                print("No hay destinos disponibles para eliminar.")
                input("Presione Enter para continuar...")
                continue

            # Mostrar los destinos en una tabla
            table_data = [[d['id_destino'], d['nombre'], d['descripcion'], d['actividades'], d['costo']] for d in destinos]
            print(tabulate(table_data, headers=["ID", "Nombre", "Descripción", "Actividades", "Costo"], tablefmt="fancy_grid"))

            # Validar el ID del destino a eliminar
            while True:
                id_destino_str = input("Ingrese el ID del destino a eliminar: ").strip()
                if not id_destino_str.isdigit():
                    print("Debe ingresar un número válido.")
                    continue
                id_destino = int(id_destino_str)
                destino_existente = next((d for d in destinos if d['id_destino'] == id_destino), None)
                if destino_existente:
                    break
                else:
                    print("No se encontró un destino con ese ID. Intente nuevamente.")

            # Mostrar resumen antes de confirmar
            print("\nResumen del destino a eliminar:")
            print(f"ID: {destino_existente['id_destino']}")
            print(f"Nombre: {destino_existente['nombre']}")
            print(f"Descripción: {destino_existente['descripcion']}")
            print(f"Actividades: {destino_existente['actividades']}")
            print(f"Costo: {destino_existente['costo']}")

            # Confirmar eliminación
            while True:
                confirmar = input("¿Confirmar eliminación? [SI/NO]: ").strip().lower()
                if not confirmar:
                    print("La respuesta no puede estar vacía. Debes responder SI o NO.")
                    continue
                if confirmar == "si":
                    if destinoCRUD.eliminarDestino(id_destino):
                        print("Destino eliminado con éxito.")
                    else:
                        print("No se pudo eliminar el destino. Verifique el ID o la conexión.")
                    break
                elif confirmar == "no":
                    print("Eliminación descartada.")
                    break
                else:
                    print("Entrada no válida. Debes responder 'SI' o 'NO'.")

            input("Presione Enter para continuar...")

        elif opcion == "7":
            print("Saliendo del menú de destinos...")
            input("Presione Enter para continuar...")
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.")
            input("Presione Enter para continuar...")

def generarPaquetesAleatorios():
    """
    Genera una cantidad especificada de paquetes aleatorios con datos ficticios.
    Pide al usuario la cantidad de paquetes a generar, y los inserta en la BD.
    """
    while True:
        try:
            cantidad = int(input("¿Cuántos paquetes aleatorios desea generar?: ").strip())
            if cantidad <= 0:
                print("La cantidad debe ser mayor a 0.")
                continue
            break
        except ValueError:
            print("Debe ingresar un número válido.")

    # Generar paquetes usando el método generarPaqueteAleatorio
    for i in range(cantidad):
        paquete, destinos = Paquete.generarPaqueteAleatorio()  # Generar paquete y destinos
        if paquete and destinos:
            if paqueteCRUD.agregarPaqueteConDestino(paquete, destinos):
                print(f"Paquete '{paquete.nombre_paquete}' generado y registrado con éxito.")
            else:
                print(f"Error al registrar el paquete '{paquete.nombre_paquete}'.")
        else:
            print("No se pudo generar el paquete debido a un error o falta de destinos.")

    input("Presione Enter para continuar...")

from tabulate import tabulate
import os
import DAO.CRUDPaquete as paqueteCRUD
from DTO.Paquete import Paquete
from datetime import datetime


def menuPaquetes(nombre):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n============================")
        print("    MENÚ PAQUETES TURÍSTICOS")
        print("============================")
        print("1. Mostrar todos los paquetes")
        print("2. Mostrar un paquete específico")
        print("3. Mostrar paquetes parciales")
        print("4. Eliminar paquete")
        print("5. Actualizar paquete")
        print("6. Generar paquetes aleatorios")
        print("7. Salir")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            print("\n--- MOSTRAR TODOS LOS PAQUETES ---")
            paquetes = paqueteCRUD.obtenerPaquetesConDestinos()
            if paquetes:
                table_data = [[
                    p['id_paquete'], 
                    p['nombre_paquete'], 
                    p['descripcion'], 
                    p['precio_total'], 
                    p['fecha_inicio'], 
                    p['fecha_fin'], 
                    p['destinos'] if p['destinos'] else "No tiene destinos"
                ] for p in paquetes]

                print(tabulate(
                    table_data, 
                    headers=["ID", "Nombre", "Descripción", "Precio", "Inicio", "Fin", "Destinos"], 
                    tablefmt="fancy_grid"
                ))
            else:
                print("No hay paquetes turísticos registrados.")
            input("Presione Enter para continuar...")

        elif opcion == "2":
            print("\n--- MOSTRAR UN PAQUETE ---")
            idPaquete = input("Ingrese el ID del paquete: ").strip()
            paquete = paqueteCRUD.mostrarUno(idPaquete)
            if paquete and paquete['fecha_inicio'] != "0000-00-00":
                table_data = [[paquete['id_paquete'], paquete['nombre_paquete'], paquete['descripcion'],
                               paquete['precio_total'], paquete['fecha_inicio'], paquete['fecha_fin']]]
                print(tabulate(table_data, headers=["ID", "Nombre", "Descripción", "Precio", "Inicio", "Fin"],
                               tablefmt="fancy_grid"))
            else:
                print("No se encontró un paquete válido con ese ID.")
            input("Presione Enter para continuar...")

        elif opcion == "3":
            print("\n--- MOSTRAR PAQUETES PARCIALES ---")
            try:
                cantidad = int(input("¿Cuántos paquetes desea mostrar?: ").strip())
                paquetes = paqueteCRUD.mostrarParcial(cantidad)
                paquetes_validos = [p for p in paquetes if p['fecha_inicio'] != "0000-00-00"]
                table_data = [[p['id_paquete'], p['nombre_paquete'], p['descripcion'], p['precio_total'],
                               p['fecha_inicio'], p['fecha_fin']] for p in paquetes_validos]
                print(tabulate(table_data, headers=["ID", "Nombre", "Descripción", "Precio", "Inicio", "Fin"],
                               tablefmt="fancy_grid"))
            except ValueError:
                print("Debe ingresar un número válido.")
            input("Presione Enter para continuar...")

        elif opcion == "4":
            print("\n--- ELIMINAR PAQUETE ---")
            paquetes = paqueteCRUD.mostrarTodos()

            # Si no hay paquetes, no se puede eliminar nada
            if not paquetes:
                print("No hay paquetes disponibles para eliminar.")
                input("Presione Enter para continuar...")
                continue

            # Filtrar paquetes con fechas válidas
            paquetes_validos = [p for p in paquetes if p['fecha_inicio'] != "0000-00-00" and p['fecha_fin'] != "0000-00-00"]

            if not paquetes_validos:
                print("No hay paquetes válidos para eliminar.")
                input("Presione Enter para continuar...")
                continue

            # Mostrar los paquetes en una tabla
            table_data = [[p['id_paquete'], p['nombre_paquete'], p['descripcion'], p['precio_total'], p['fecha_inicio'], p['fecha_fin']] 
                        for p in paquetes_validos]
            print(tabulate(table_data, headers=["ID", "Nombre", "Descripción", "Precio", "Inicio", "Fin"], tablefmt="fancy_grid"))

            # Validar el ID del paquete a eliminar
            while True:
                id_paquete_str = input("Ingrese el ID del paquete a eliminar: ").strip()
                if not id_paquete_str.isdigit():
                    print("Debe ingresar un número válido.")
                    continue
                id_paquete = int(id_paquete_str)
                paquete_existente = next((p for p in paquetes_validos if p['id_paquete'] == id_paquete), None)
                if paquete_existente:
                    break
                else:
                    print("No se encontró un paquete con ese ID. Intente nuevamente.")

            # Mostrar resumen antes de confirmar
            print("\nResumen del paquete a eliminar:")
            print(f"ID: {paquete_existente['id_paquete']}")
            print(f"Nombre: {paquete_existente['nombre_paquete']}")
            print(f"Descripción: {paquete_existente['descripcion']}")
            print(f"Precio: {paquete_existente['precio_total']}")
            print(f"Fecha Inicio: {paquete_existente['fecha_inicio']}")
            print(f"Fecha Fin: {paquete_existente['fecha_fin']}")

            # Confirmar eliminación
            while True:
                confirmar = input("¿Confirmar eliminación? [SI/NO]: ").strip().lower()
                if not confirmar:
                    print("La respuesta no puede estar vacía. Debes responder SI o NO.")
                    continue
                if confirmar == "si":
                    if paqueteCRUD.eliminarPaquete(id_paquete):
                        print("Paquete eliminado con éxito.")
                    else:
                        print("No se pudo eliminar el paquete. Verifique el ID o la conexión.")
                    break
                elif confirmar == "no":
                    print("Eliminación descartada.")
                    break
                else:
                    print("Entrada no válida. Debes responder 'SI' o 'NO'.")

            input("Presione Enter para continuar...")


        elif opcion == "5":
            print("\n--- ACTUALIZAR PAQUETE ---")
            paquetes = paqueteCRUD.mostrarTodos()
            paquetes_validos = [p for p in paquetes if p['fecha_inicio'] != "0000-00-00"]

            if not paquetes_validos:
                print("No hay paquetes válidos para actualizar.")
                input("Presione Enter para continuar...")
                continue

            table_data = [[p['id_paquete'], p['nombre_paquete'], p['descripcion'], p['precio_total'],
                           p['fecha_inicio'], p['fecha_fin']] for p in paquetes_validos]
            print(tabulate(table_data, headers=["ID", "Nombre", "Descripción", "Precio", "Inicio", "Fin"],
                           tablefmt="fancy_grid"))

            idPaquete = input("Ingrese el ID del paquete a actualizar: ").strip()
            nuevo_nombre = input("Nuevo nombre del paquete: ").strip()
            nueva_descripcion = input("Nueva descripción: ").strip()
            nuevo_precio = float(input("Nuevo precio: ").strip())
            nueva_fecha_inicio = input("Nueva fecha de inicio (YYYY-MM-DD): ").strip()
            nueva_fecha_fin = input("Nueva fecha de fin (YYYY-MM-DD): ").strip()

            if paqueteCRUD.modificarPaquete(idPaquete, nuevo_nombre, nueva_descripcion, nuevo_precio,
                                            nueva_fecha_inicio, nueva_fecha_fin):
                print("Paquete actualizado correctamente.")
            else:
                print("Error al actualizar el paquete.")
            input("Presione Enter para continuar...")

        elif opcion == "6":
            print("\n--- GENERAR PAQUETES ALEATORIOS ---")
            generarPaquetesAleatorios()

        elif opcion == "7":
            print("\nRegresando al menú principal...")
            input("Presione Enter para continuar...")
            break

        else:
            print("Opción no válida. Intente nuevamente.")
            input("Presione Enter para continuar...")

def menuReservas(id_usuario):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n==========================")
        print("      MENÚ RESERVAS       ")
        print("==========================")
        print("1. Mostrar todas las reservas")
        print("2. Mostrar una reserva específica")
        print("3. Mostrar reservas por estado")
        print("4. Realizar una nueva reserva")
        print("5. Cancelar una reserva")
        print("6. Salir")
        opcion = input("Seleccione una opción (1-6): ").strip()

        # 1. Mostrar todas las reservas
        if opcion == "1":
            print("\n--- MOSTRAR TODAS LAS RESERVAS ---")
            reservas = reservaCRUD.mostrarTodos()
            if reservas:
                table_data = [[r['id_reserva'], r['id_usuario'], r['id_paquete'], r['fecha_reserva'], r['estado']] for r in reservas]
                print(tabulate(table_data, headers=["ID Reserva", "ID Usuario", "ID Paquete", "Fecha Reserva", "Estado"], tablefmt="fancy_grid"))
            else:
                print("No hay reservas registradas.")
            input("Presione Enter para continuar...")

        # 2. Mostrar una reserva específica
        elif opcion == "2":
            print("\n--- MOSTRAR UNA RESERVA ESPECÍFICA ---")
            while True:
                id_reserva = input("Ingrese el ID de la reserva: ").strip()
                if id_reserva.isdigit():
                    reserva = reservaCRUD.mostrarUno(id_reserva)
                    if reserva:
                        table_data = [[reserva['id_reserva'], reserva['id_usuario'], reserva['id_paquete'], reserva['fecha_reserva'], reserva['estado']]]
                        print(tabulate(table_data, headers=["ID Reserva", "ID Usuario", "ID Paquete", "Fecha Reserva", "Estado"], tablefmt="fancy_grid"))
                    else:
                        print("Reserva no encontrada.")
                    break
                else:
                    print("Debe ingresar un ID válido.")
            input("Presione Enter para continuar...")

        # 3. Mostrar reservas por estado
        elif opcion == "3":
            print("\n--- MOSTRAR RESERVAS POR ESTADO ---")
            while True:
                print("\nSeleccione el estado:")
                print("1. Pendiente")
                print("2. Confirmada")
                print("3. Cancelada")
                estado_opcion = input("Ingrese el número del estado: ").strip()

                estados_validos = {"1": "pendiente", "2": "confirmada", "3": "cancelada"}
                if estado_opcion in estados_validos:
                    estado = estados_validos[estado_opcion]
                    reservas = reservaCRUD.mostrarParcial(estado)
                    if reservas:
                        table_data = [[r['id_reserva'], r['id_usuario'], r['id_paquete'], r['fecha_reserva'], r['estado']] for r in reservas]
                        print(tabulate(table_data, headers=["ID Reserva", "ID Usuario", "ID Paquete", "Fecha Reserva", "Estado"], tablefmt="fancy_grid"))
                    else:
                        print(f"No hay reservas con el estado '{estado}'.")
                    break
                else:
                    print("Opción inválida. Seleccione 1, 2 o 3.")
            input("Presione Enter para continuar...")

        # 4. Realizar una nueva reserva
        elif opcion == "4":
            print("\n--- REALIZAR UNA NUEVA RESERVA ---")
            paquetes = paqueteCRUD.mostrarTodos()

            if not paquetes:
                print("No hay paquetes turísticos disponibles para reservar.")
                input("Presione Enter para continuar...")
                continue

            # Mostrar paquetes disponibles
            table_data = [[p['id_paquete'], p['nombre_paquete'], p['descripcion'], p['precio_total'], p['fecha_inicio'], p['fecha_fin']]
                          for p in paquetes]
            print(tabulate(table_data, headers=["ID Paquete", "Nombre", "Descripción", "Precio", "Inicio", "Fin"], tablefmt="fancy_grid"))

            # Solicitar y validar el ID del paquete
            while True:
                id_paquete = input("Ingrese el ID del paquete a reservar: ").strip()
                if id_paquete.isdigit() and any(int(id_paquete) == p['id_paquete'] for p in paquetes):
                    id_paquete = int(id_paquete)
                    break
                else:
                    print("El ID del paquete debe ser válido y existir en la lista.")

            # Mostrar usuarios disponibles y validar el ID del usuario
            while True:
                print("\n--- LISTA DE USUARIOS DISPONIBLES ---")
                usuarios = usuarioCRUD.mostrarTodos()  # Obtener todos los usuarios
                if not usuarios:
                    print("No hay usuarios disponibles.")
                    break
                table_data = [[u['id_usuario'], u['nombre'], u['correo'], u['tipo_usuario']] for u in usuarios]
                print(tabulate(table_data, headers=["ID Usuario", "Nombre", "Correo", "Tipo Usuario"], tablefmt="fancy_grid"))
                
                id_usuario_reserva = input("Ingrese el ID del usuario al que se asignará la reserva: ").strip()
                if id_usuario_reserva.isdigit():
                    id_usuario_reserva = int(id_usuario_reserva)
                    if any(u['id_usuario'] == id_usuario_reserva for u in usuarios):
                        break
                    else:
                        print("Error: El ID del usuario no existe. Intente nuevamente.")
                else:
                    print("El ID del usuario debe ser numérico.")

            # Fecha de reserva
            fecha_reserva = datetime.now().date()

            # Confirmar reserva con validación estricta
            while True:
                confirmar = input("\n¿Confirmar reserva? [SI/NO]: ").strip().upper()
                if confirmar == "SI":
                    nueva_reserva = Reserva(id_usuario_reserva, id_paquete, fecha_reserva)
                    if nueva_reserva.realizarReserva():
                        print("\nReserva realizada con éxito y asignada al usuario.")
                    else:
                        print("\nError: No se pudo realizar la reserva.")
                    break
                elif confirmar == "NO":
                    print("\nReserva cancelada.")
                    break
                else:
                    print("\nOpción inválida. Por favor, escriba 'SI' o 'NO'.")

            input("Presione Enter para continuar...")

        # 5. Cancelar una reserva
        elif opcion == "5":
            print("\n--- CANCELAR UNA RESERVA ---")
            reservas = reservaCRUD.mostrarTodos()
            if not reservas:
                print("No hay reservas para cancelar.")
                input("Presione Enter para continuar...")
                continue

            table_data = [[r['id_reserva'], r['id_usuario'], r['id_paquete'], r['fecha_reserva'], r['estado']] for r in reservas]
            print(tabulate(table_data, headers=["ID Reserva", "ID Usuario", "ID Paquete", "Fecha Reserva", "Estado"], tablefmt="fancy_grid"))

            while True:
                id_reserva = input("Ingrese el ID de la reserva a cancelar: ").strip()
                if id_reserva.isdigit():
                    if reservaCRUD.cancelarReserva(id_reserva):
                        print("Reserva cancelada con éxito.")
                    else:
                        print("No se pudo cancelar la reserva. Verifique el ID.")
                    break
                else:
                    print("Debe ingresar un ID válido.")
            input("Presione Enter para continuar...")

        # 6. Salir
        elif opcion == "6":
            print("Regresando al menú principal...")
            input("Presione Enter para continuar...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")
            input("Presione Enter para continuar...")


def menuAdmin(nombre, idUsuario):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("---------------------------")
        print("       MENÚ ADMIN         ")
        print("---------------------------")
        print("1. Gestionar Destinos     ")
        print("2. Gestionar Paquetes     ")
        print("3. Gestionar Reservas     ")
        print("4. Salir                  ")
        print("---------------------------")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            menuDestinos()
        elif opcion == "2":
            menuPaquetes(nombre)
        elif opcion == "3":
            menuReservas(nombre)
        elif opcion == "4":
            print("Saliendo del menú Admin...")
            input("Presione Enter para continuar...")
            break
        else:
            print("Opción no válida.")
            input("Presione Enter para continuar...")


def menuClientes(nombre, idUsuario):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("--------------------------")
        print(f"       MENÚ CLIENTE")
        print("--------------------------")
        print("1. Consultar Paquetes Turísticos")
        print("2. Realizar Reserva")
        print("3. Mostrar Reservas")
        print("4. Cancelar Reserva")
        print("5. Salir")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            paquetes = paqueteCRUD.mostrarTodos()
            if paquetes:
                table_data = [[p['id_paquete'], p['nombre_paquete'], p['descripcion'], p['precio_total'], p['fecha_inicio'], p['fecha_fin']] 
                              for p in paquetes]
                print(tabulate(table_data, headers=["ID", "Nombre", "Descripción", "Precio", "Fecha Inicio", "Fecha Fin"], tablefmt="fancy_grid"))
            else:
                print("No hay paquetes disponibles.")
            input("Presione Enter para continuar...")

        elif opcion == "2":
            try:
                paquetes = paqueteCRUD.mostrarTodos()
                if paquetes:
                    table_data = [[p['id_paquete'], p['nombre_paquete'], p['descripcion'], p['precio_total'], p['fecha_inicio'], p['fecha_fin']] 
                                for p in paquetes]
                    print(tabulate(table_data, headers=["ID", "Nombre", "Descripción", "Precio", "Fecha Inicio", "Fecha Fin"], tablefmt="fancy_grid"))
                else:
                    print("No hay paquetes disponibles.")
                    input("Presione Enter para continuar...")
                    continue

                # Solicitar y validar el ID del paquete
                while True:
                    idPaquete = input("Ingrese el ID del paquete turístico que desea reservar: ").strip()
                    if idPaquete.isdigit() and any(int(idPaquete) == p['id_paquete'] for p in paquetes):
                        idPaquete = int(idPaquete)
                        break
                    else:
                        print("El ID del paquete debe ser válido y existir en la lista.")

                # Solicitar y validar la fecha de reserva
                while True:
                    fecha_reserva_input = input("Por favor, ingrese la fecha de reserva (DD-MM-YYYY): ").strip()
                    try:
                        # Validar y convertir la fecha al formato YYYY-MM-DD
                        fecha_reserva = datetime.strptime(fecha_reserva_input, "%d-%m-%Y").date()
                        break
                    except ValueError:
                        print("Error: La fecha debe estar en el formato DD-MM-YYYY. Inténtalo de nuevo.")

                # Crear reserva usando el ID del usuario autenticado
                nuevaReserva = Reserva(idUsuario, idPaquete, fecha_reserva)
                if nuevaReserva.realizarReserva():
                    print("¡Tu reserva ha sido registrada con éxito!")
                else:
                    print("No pudimos registrar tu reserva en este momento. Intenta nuevamente.")

            except Exception as e:
                print(f"Hubo un error al intentar registrar la reserva: {e}")
            input("Presione Enter para continuar...")

        elif opcion == "3":
            try:
                reservas = reservaCRUD.mostrarReservaPorId(idUsuario)
                if reservas:
                    table_data = [[r['id_reserva'], r['id_paquete'], r['fecha_reserva'], r['estado']] for r in reservas]
                    print(tabulate(table_data, headers=["ID Reserva", "ID Paquete", "Fecha Reserva", "Estado"], tablefmt="fancy_grid"))
                else:
                    print("No tienes reservas registradas.")
            except Exception as e:
                print(f"Hubo un error al intentar mostrar las reservas: {e}")
            input("Presione Enter para continuar...")

        elif opcion == "4":
            try:
                reservas = reservaCRUD.mostrarReservaPorId(idUsuario)
                if reservas:
                    table_data = [[r['id_reserva'], r['id_paquete'], r['fecha_reserva'], r['estado']] for r in reservas]
                    print(tabulate(table_data, headers=["ID Reserva", "ID Paquete", "Fecha Reserva", "Estado"], tablefmt="fancy_grid"))

                    idReserva = int(input("Ingrese el ID de la reserva que desea cancelar: "))
                    reservaSeleccionada = next((res for res in reservas if res['id_reserva'] == idReserva), None)
                    if reservaSeleccionada:
                        idPaquete = reservaSeleccionada['id_paquete']
                        fechaReserva = reservaSeleccionada['fecha_reserva']
                        reservaACancelar = Reserva(idUsuario, idPaquete, fechaReserva, idReserva=idReserva)
                        if reservaACancelar.cancelarReserva():
                            print("¡Tu reserva ha sido cancelada con éxito!")
                        else:
                            print("No pudimos cancelar tu reserva en este momento.")
                    else:
                        print("No se encontró una reserva con ese ID.")
                else:
                    print("No tienes reservas registradas para cancelar.")
            except Exception as e:
                print(f"Hubo un error al intentar cancelar la reserva: {e}")
            input("Presione Enter para continuar...")

        elif opcion == "5":
            print("Saliendo del menú cliente...")
            input("Presione Enter para continuar...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")
            input("Presione Enter para continuar...")


def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n---------------------------")
        print("     1. Login             ")
        print("     2. Registro          ")
        print("     3. Salir             ")
        print("---------------------------")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            datos_usuario = login()
            if datos_usuario and datos_usuario.get("autenticado"):
                print(f"\n¡Bienvenido, {datos_usuario['nombre']}!\n")
                input("Presione Enter para continuar...")
                if datos_usuario["tipo_usuario"] == "administrador":
                    menuAdmin(datos_usuario["nombre"], datos_usuario["id_usuario"])
                elif datos_usuario["tipo_usuario"] == "cliente":
                    menuClientes(datos_usuario["nombre"], datos_usuario["id_usuario"])
        elif opcion == "2":
            registrarUsuario()
        elif opcion == "3":
            print("\nGracias por usar el sistema. ¡Hasta pronto!\n")
            break
        else:
            print("\nOpción no válida. Intente de nuevo.\n")
            input("Presione Enter para continuar...")


if __name__ == "__main__":
    main()

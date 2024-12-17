from DAO.Conexion import Conexion
from datetime import datetime

# Datos de conexión
host = 'localhost'
user = 'adminagencia'
password = 'adminagencia'
db = 'agencia_de_viajes'

# Agregar paquete turístico
def agregarPaquete(paquete):
    """
    Inserta un paquete en la base de datos.
    paquete: Objeto con atributos nombre_paquete, descripcion, precio_total, fecha_inicio, fecha_fin.
    """
    try:
        con = Conexion(host, user, password, db)
        sql = """
        INSERT INTO paquete_turistico (nombre_paquete, descripcion, precio_total, fecha_inicio, fecha_fin)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor = con.ejecutaQuery(sql, (
            paquete.nombre_paquete,
            paquete.descripcion,
            paquete.precio_total,
            paquete.fecha_inicio,
            paquete.fecha_fin
        ))
        con.commit()
        # Capturar el ID del paquete recién insertado
        paquete.id_paquete = cursor.lastrowid
        return True
    except Exception as e:
        con.rollback()
        print(f"Error al agregar el paquete: {e}")
        return False
    finally:
        con.desconectar()

# Agregar paquete con destinos relacionados
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

def obtenerPaquetesConDestinos():
    """
    Devuelve una lista de paquetes junto con sus destinos asociados.
    """
    try:
        con = Conexion(host, user, password, db)
        sql = """
        SELECT 
            pt.id_paquete, 
            pt.nombre_paquete, 
            pt.descripcion, 
            pt.precio_total, 
            pt.fecha_inicio, 
            pt.fecha_fin,
            GROUP_CONCAT(d.nombre SEPARATOR ', ') AS destinos
        FROM paquete_turistico pt
        LEFT JOIN detalle_paquete dp ON pt.id_paquete = dp.id_paquete
        LEFT JOIN destino d ON dp.id_destino = d.id_destino
        GROUP BY pt.id_paquete
        ORDER BY pt.id_paquete;
        """
        cursor = con.ejecutaQuery(sql)
        paquetes = cursor.fetchall()
        return paquetes
    except Exception as e:
        print(f"Error al obtener paquetes con destinos: {e}")
        return []
    finally:
        con.desconectar()

# Eliminar paquete turístico
def eliminarPaquete(idPaquete):
    """
    Elimina un paquete turístico por su ID.
    """
    try:
        con = Conexion(host, user, password, db)
        sql = "DELETE FROM paquete_turistico WHERE id_paquete = %s"
        con.ejecutaQuery(sql, (idPaquete,))
        con.commit()
        return True
    except Exception as e:
        con.rollback()
        print(f"Error al eliminar el paquete: {e}")
        return False
    finally:
        con.desconectar()

# Mostrar un paquete por ID
def mostrarUno(idPaquete):
    """
    Consulta y retorna un paquete turístico por su ID.
    """
    try:
        con = Conexion(host, user, password, db)
        sql = """
        SELECT id_paquete, nombre_paquete, descripcion, precio_total, fecha_inicio, fecha_fin 
        FROM paquete_turistico 
        WHERE id_paquete = %s
        """
        cursor = con.ejecutaQuery(sql, (idPaquete,))
        paquete = cursor.fetchone()
        return paquete
    except Exception as e:
        print(f"Error al consultar paquete: {e}")
        return None
    finally:
        con.desconectar()

# Mostrar paquetes parciales
def mostrarParcial(cant_reg):
    """
    Consulta y retorna una cantidad limitada de paquetes turísticos.
    """
    try:
        con = Conexion(host, user, password, db)
        sql = """
        SELECT id_paquete, nombre_paquete, descripcion, precio_total, fecha_inicio, fecha_fin 
        FROM paquete_turistico 
        LIMIT %s
        """
        cursor = con.ejecutaQuery(sql, (cant_reg,))
        paquetes = cursor.fetchall()
        return paquetes
    except Exception as e:
        print(f"Error al consultar paquetes parciales: {e}")
        return []
    finally:
        con.desconectar()

# Mostrar todos los paquetes turísticos
def mostrarTodos():
    """
    Consulta y retorna todos los paquetes turísticos.
    """
    try:
        con = Conexion(host, user, password, db)
        sql = """
        SELECT id_paquete, nombre_paquete, descripcion, precio_total, fecha_inicio, fecha_fin 
        FROM paquete_turistico
        """
        cursor = con.ejecutaQuery(sql)
        paquetes = cursor.fetchall()
        return paquetes
    except Exception as e:
        print(f"Error al consultar todos los paquetes: {e}")
        return []
    finally:
        con.desconectar()

# Modificar paquete turístico
def modificarPaquete(idPaquete, nuevo_nombre, nueva_descripcion, nuevo_precio, nueva_fecha_inicio, nueva_fecha_fin):
    """
    Modifica un paquete turístico por su ID.
    - idPaquete: ID del paquete a modificar.
    - nuevo_nombre: Nuevo nombre del paquete.
    - nueva_descripcion: Nueva descripción del paquete.
    - nuevo_precio: Nuevo precio total del paquete.
    - nueva_fecha_inicio: Nueva fecha de inicio del paquete.
    - nueva_fecha_fin: Nueva fecha de fin del paquete.
    """
    try:
        con = Conexion(host, user, password, db)
        sql = """
        UPDATE paquete_turistico
        SET nombre_paquete = %s,
            descripcion = %s,
            precio_total = %s,
            fecha_inicio = %s,
            fecha_fin = %s
        WHERE id_paquete = %s
        """
        con.ejecutaQuery(sql, (nuevo_nombre, nueva_descripcion, nuevo_precio, nueva_fecha_inicio, nueva_fecha_fin, idPaquete))
        con.commit()
        return True
    except Exception as e:
        con.rollback()
        print(f"Error al modificar el paquete: {e}")
        return False
    finally:
        con.desconectar()
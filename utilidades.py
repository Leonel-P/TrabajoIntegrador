#FUNCIONES AUXILIARES
import os, csv, json

ARCHIVO_ESTRUCTURA = "estructura.json"

#FUNCIONES DE ENTRADA DE DATOS
def pedir_opcion(mensaje,rango_maximo):
    while True:
        try:
            opcion = int(input(mensaje))
        except ValueError:
            print("Error: debe indicar la opcion con un numero entero.")
            continue
        if 0<= opcion <= rango_maximo:
            return opcion
        else:
            print("Error: opcion fuera de rango.")
            continue
def pedir_nombre():
    nombre = input("Ingrese el nombre del nuevo producto: ").strip()
    if nombre == "":
        print("El nombre no puede estar vacío.")
        return pedir_nombre()
    return nombre
def pedir_precio():
    while True:
        try:
            precio = float(input("Ingrese el precio del producto: "))
        except ValueError:
            print("Error: ingrese un número válido para el precio.")
            continue
        if precio > 0:
            return precio
        else:
            print("El precio no puede ser negativo. Intente de nuevo.")
            continue
def pedir_marca():
    marca = input("Ingrese la marca del producto: ").strip()
    if marca == "":
        print("La marca no puede estar vacía.")
        return pedir_marca()
    return marca
def pedir_stock():
    while True:
        try:
            stock = int(input("Ingrese la cantidad en stock del producto: "))
        except ValueError:
            print("Error: ingrese un número entero válido para el stock.")
            continue
        if stock >= 0:
            return stock
        else:
            print("Error: el stock no puede ser negativo.")
            continue

#FUNCIONES DE SELECCION DE CATEGORIA Y SUBCATEGORIA
def pedir_categoria():
    # Permite al susuario elegir una categoria desde una estructura.json
    if not os.path.exists(ARCHIVO_ESTRUCTURA):
        print("No hay categorias disponibles.")
        return None
    
    with open(ARCHIVO_ESTRUCTURA, "r", encoding="utf-8") as f:
        estructura = json.load(f)
    categorias = list(estructura.keys())
    if not categorias:
        print("No hay categorias disponibles.")
        return None
    
    print("Categorías disponibles:")
    for i, cat in enumerate(categorias, 1):
        print(f"{i}. {cat}")
    while True:
        try:
            eleccion = int(input("Seleccione una categoría por número: "))
            if 1 <= eleccion <= len(categorias):
                return categorias[eleccion - 1]
            else:
                print("Selección inválida. Intente de nuevo.")
        except ValueError:
            print("Entrada inválida. Por favor ingrese un número.")
def pedir_subcategoria(categoria, SUBCATEGORIAS=None):
    """Permite al usuario elegir una subcategoría desde estructura.json (dinámico)."""
    ARCHIVO_ESTRUCTURA = "estructura.json"

    # Verificamos que exista el archivo de estructura
    if not os.path.exists(ARCHIVO_ESTRUCTURA):
        print("⚠️ No hay estructura registrada. Cree categorías primero.")
        return None

    # Cargamos la estructura actualizada
    with open(ARCHIVO_ESTRUCTURA, "r", encoding="utf-8") as f:
        estructura = json.load(f)

    # Obtenemos las subcategorías de la categoría seleccionada
    opciones = estructura.get(categoria, [])

    # Si no hay subcategorías, avisamos
    if not opciones:
        print(f"⚠️ La categoría '{categoria}' no tiene subcategorías. Cree una primero.")
        return None

    # Mostramos las opciones
    print(f"Subcategorías disponibles para {categoria}:")
    for i, sub in enumerate(opciones, 1):
        print(f"{i}. {sub}")

    # Pedimos elección al usuario
    while True:
        try:
            eleccion = int(input("Seleccione una subcategoría por número: "))
            if 1 <= eleccion <= len(opciones):
                return opciones[eleccion - 1]
            else:
                print("Selección inválida. Intente de nuevo.")
        except ValueError:
            print("Error: por favor ingrese un número.")

#FUNCION DE BUSQUEDA DE PRODUCTOS POR NOMBRE
def buscar_productos_por_nombre(base, termino, incluir_inactivos=False):
    resultados = []
    for ruta, _, archivos in os.walk(base):
        for archivo in archivos:
            if archivo.endswith(".csv"):
                ruta_csv = os.path.join(ruta, archivo)
                with open(ruta_csv, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for idx, fila in enumerate(reader):
                        if not incluir_inactivos and fila.get("activo", "si") != "si":
                            continue
                        if termino.lower() in fila["nombre"].lower():
                            resultados.append((ruta_csv, idx, fila))
    return resultados

#FUNCION DE ANALISIS DE PRODUCTOS
def obtener_todos_los_productos_activos(base):
    """
    Recorre todas las categorías y subcategorías y devuelve
    una lista de diccionarios con los productos activos.
    """
    productos = []
    for carpeta, _, archivos in os.walk(base):
        for archivo in archivos:
            if archivo.endswith(".csv"):
                ruta_csv = os.path.join(carpeta, archivo)
                with open(ruta_csv, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for fila in reader:
                        # Si tiene el campo 'activo' y está en 'si' o no tiene el campo (viejo)
                        if fila.get("activo", "si").lower() == "si":
                            fila["ruta_csv"] = ruta_csv
                            productos.append(fila)
    return productos

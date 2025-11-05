# crud.py
import csv, os
from utilidades import buscar_productos_por_nombre,pedir_opcion,pedir_categoria, pedir_subcategoria, pedir_nombre, pedir_precio, pedir_marca, pedir_stock
from estructura import HEADER

#OPCION 2 ALTA PRODUCTO
def alta_producto(base,SUBCATEGORIAS):
    # Permite agregar un nuevo producto en la jerarquía: categoría -> subcategoría -> productos.csv
    print("\n--- ALTA DE PRODUCTO ---")

    # Pedimos datos al usuario
    categoria = pedir_categoria()
    subcategoria = pedir_subcategoria(categoria,SUBCATEGORIAS)
    if not categoria or not subcategoria:
        print("No se pudo completar el alta del producto debido a categoría o subcategoría inválida.\n")
        return
    nombre = pedir_nombre()
    precio = pedir_precio()
    marca = pedir_marca()
    stock = pedir_stock()


    # Crear ruta del archivo
    ruta_csv = os.path.join(base, categoria, subcategoria, "productos.csv")

    # Crear carpetas si no existen
    os.makedirs(os.path.dirname(ruta_csv), exist_ok=True)

    # Guardar producto en el CSV
    
    with open(ruta_csv, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADER)
        writer.writerow({
            "nombre": nombre,
            "precio": precio,
            "marca": marca,
            "stock": stock,
            "activo": "si"
        })
    print(f"Producto '{nombre}' agregado correctamente en {categoria}/{subcategoria}.\n")

#OPCION 4 MODIFICAR PRODUCTO
def modificar_producto(base):
    print("\n=== MODIFICAR PRODUCTO ===")

    nombre_busqueda = input("Ingrese el nombre (o parte del nombre) del producto a modificar: ").strip()
    encontrados = buscar_productos_por_nombre(base, nombre_busqueda)

    if not encontrados:
        print("No se encontró ningún producto con ese nombre.")
        return

    # Mostrar coincidencias
    print("\nProductos encontrados:")
    for idx, (_, _, prod) in enumerate(encontrados, 1):
        print(f"{idx}. {prod['nombre']} | Precio: ${prod['precio']} | Marca: {prod['marca']} | Stock: {prod['stock']}")

    # Elegir cuál modificar
    while True:
        try:
            eleccion = int(input("\nSeleccione el número del producto a modificar (0 para cancelar): "))
            if eleccion == 0:
                print("Operación cancelada.")
                return
            if 1 <= eleccion <= len(encontrados):
                break
            else:
                print("Opción fuera de rango.")
        except ValueError:
            print("Error: debe ingresar un número.")

    # Datos del producto seleccionado
    ruta_csv, indice, producto = encontrados[eleccion - 1]

    print(f"\nEditando producto: {producto['nombre']}")
    print("Deje vacío un campo si no desea modificarlo.\n")

    # Solicitar nuevos valores
    nuevo_nombre = input(f"Nuevo nombre [{producto['nombre']}]: ").strip() or producto['nombre']
    nuevo_precio = input(f"Nuevo precio [{producto['precio']}]: ").strip() or producto['precio']
    nueva_marca  = input(f"Nueva marca [{producto['marca']}]: ").strip() or producto['marca']
    nuevo_stock  = input(f"Nuevo stock [{producto['stock']}]: ").strip() or producto['stock']

    # Validaciones básicas
    try:
        nuevo_precio = float(nuevo_precio)
        nuevo_stock = int(nuevo_stock)
    except ValueError:
        print("Error: precio o stock con formato inválido. No se aplicaron los cambios.")
        return

    # Cargar todos los productos del CSV
    with open(ruta_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        productos = list(reader)

    # Actualizar el producto
    productos[indice] = {
        "nombre": nuevo_nombre,
        "precio": nuevo_precio,
        "marca": nueva_marca,
        "stock": nuevo_stock
    }

    # Sobrescribir archivo
    with open(ruta_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["nombre", "precio", "marca", "stock"])
        writer.writeheader()
        writer.writerows(productos)

    print(f"\n✅ Producto '{nuevo_nombre}' modificado correctamente.\n")

#OPCION 5 ELIMINAR PRODUCTO _ ELIMINACION LOGICA
def eliminar_producto(base):
    print("\n=== ELIMINAR PRODUCTO ===")

    # Mostrar todos los productos activos antes de pedir búsqueda
    print("\nListado de productos actuales (activos):")
    productos_totales = buscar_productos_por_nombre(base, "", incluir_inactivos=False)
    if not productos_totales:
        print("No hay productos activos cargados.")
        return

    for idx, (_, _, prod) in enumerate(productos_totales, 1):
        print(f"{idx}. {prod['nombre']} | Precio: ${prod['precio']} | Marca: {prod['marca']} | Stock: {prod['stock']}")

    nombre_busqueda = input("\nIngrese el nombre (o parte del nombre) del producto a eliminar: ").strip()
    encontrados = buscar_productos_por_nombre(base, nombre_busqueda, incluir_inactivos=False)

    if not encontrados:
        print("No se encontró ningún producto activo con ese nombre.")
        return

    # Mostrar resultados filtrados
    print("\nProductos encontrados:")
    for idx, (_, _, prod) in enumerate(encontrados, 1):
        print(f"{idx}. {prod['nombre']} | Precio: ${prod['precio']} | Marca: {prod['marca']} | Stock: {prod['stock']}")

    # Elegir cuál marcar como inactivo
    while True:
        try:
            eleccion = int(input("\nSeleccione el número del producto a eliminar (0 para cancelar): "))
            if eleccion == 0:
                print("Operación cancelada.")
                return
            if 1 <= eleccion <= len(encontrados):
                break
            else:
                print("Opción fuera de rango.")
        except ValueError:
            print("Error: debe ingresar un número.")

    # Confirmación
    ruta_csv, indice, producto = encontrados[eleccion - 1]
    confirmar = input(f"¿Está seguro que desea marcar '{producto['nombre']}' como eliminado? (s/n): ").strip().lower()
    if confirmar != "s":
        print("Operación cancelada.")
        return

    # Marcar el producto como inactivo
    with open(ruta_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        productos = list(reader)

    productos[indice]["activo"] = "no"

    with open(ruta_csv, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["nombre", "precio", "marca", "stock", "activo"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(productos)

    print(f"\n✅ Producto '{producto['nombre']}' marcado como inactivo (eliminación lógica).")
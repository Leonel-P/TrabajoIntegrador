import os
from utilidades import obtener_todos_los_productos_activos,pedir_opcion

#OPCION 6 ESTADISTICAS Y ORDENAMIENTO

def ver_estadisticas(base):
    productos = obtener_todos_los_productos_activos(base)
    if not productos:
        print("No hay productos activos registrados.")
        return

    cantidad_total = len(productos)
    precio_total = sum(float(p["precio"]) * float(p["stock"]) for p in productos)
    promedio_precio = sum(float(p["precio"]) for p in productos) / cantidad_total

    categorias = {}
    for p in productos:
        ruta_relativa = os.path.relpath(p["ruta_csv"], base)
        categoria_principal = ruta_relativa.split(os.sep)[0]
        categorias[categoria_principal] = categorias.get(categoria_principal, 0) + 1

    print("\n--- ESTADÍSTICAS ---")
    print(f"Cantidad total de productos activos: {cantidad_total}")
    print(f"Precio total de stock: ${precio_total:.2f}")
    print(f"Promedio de precios: ${promedio_precio:.2f}")
    print("Cantidad de productos por categoría principal:")
    for cat, cant in categorias.items():
        print(f"  - {cat}: {cant}")

def ordenar_productos(base):
    productos = obtener_todos_los_productos_activos(base)
    if not productos:
        print("No hay productos activos para ordenar.")
        return

    print("\n=== ORDENAR PRODUCTOS ===\n1. Por nombre (A-Z)\n2. Por precio\n3. Por stock\n0. Volver")
    opcion = pedir_opcion("Seleccione una opción: ",3)

    if opcion == "0":
        return

    reverso = False
    if opcion in (2, 3):
        print("\n1. Mayor a menor\n2. Menor a mayor")
        orden = input("Seleccione una opción: ")
        reverso = (orden == 1)

    match opcion:
        case 1:
            productos.sort(key=lambda x: x["nombre"].lower())
        case 2:
            productos.sort(key=lambda x: float(x["precio"]), reverse=reverso)
        case 3:
            productos.sort(key=lambda x: float(x["stock"]), reverse=reverso)
        case _:
            print("Opción inválida.")
            return

    print("\n--- PRODUCTOS ORDENADOS ---")
    # Anchos de columna
    widths = {
        "nombre": 30,
        "precio": 12,
        "marca": 18,
        "stock": 6,
        "categoria": 15,
        "subcategoria": 15
    }

    # Mostrar tabla simplificada: Nombre | Precio | Marca | Stock
    name_w = 24
    price_w = 11
    marca_w = 9
    stock_w = 5

    header = f"{'Nombre':{name_w}} | {'Precio':>{price_w}} | {'Marca':{marca_w}} | {'Stock':>{stock_w}}"
    print(header)
    print(f"{'-'*name_w} | {'-'*price_w} | {'-'*marca_w} | {'-'*stock_w}")

    for p in productos:
        nombre = str(p.get('nombre', ''))[:name_w]
        try:
            precio_val = float(p.get('precio', 0))
            precio = f"${precio_val:.1f}"
        except Exception:
            precio = f"${p.get('precio', '0')}"
        marca = str(p.get('marca', ''))[:marca_w]
        try:
            stock = str(int(float(p.get('stock', 0))))
        except Exception:
            stock = str(p.get('stock', '0'))

        print(f"{nombre:{name_w}} | {precio:>{price_w}} | {marca:{marca_w}} | {stock:>{stock_w}}")

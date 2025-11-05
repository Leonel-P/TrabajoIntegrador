import os
from utilidades import obtener_todos_los_productos_activos

#OPCION 6 ESTADISTICAS Y ORDENAMIENTO

def estadisticas_y_ordenamiento(base):
    while True:
        print("\n=== ESTADÍSTICAS Y ORDENAMIENTO ===")
        print("1. Ver estadísticas")
        print("2. Ordenar productos")
        print("0. Volver")
        opcion = input("Ingrese una opción: ")

        match opcion:
            case "1":
                ver_estadisticas(base)
            case "2":
                ordenar_productos(base)
            case "0":
                break
            case _:
                print("Opción inválida.")

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

    print("\n=== ORDENAR PRODUCTOS ===")
    print("1. Por nombre (A-Z)")
    print("2. Por precio")
    print("3. Por stock")
    print("0. Volver")
    opcion = input("Seleccione una opción: ")

    if opcion == "0":
        return

    reverso = False
    if opcion in ("2", "3"):
        print("\n1. Mayor a menor\n2. Menor a mayor")
        orden = input("Seleccione una opción: ")
        reverso = (orden == "1")

    match opcion:
        case "1":
            productos.sort(key=lambda x: x["nombre"].lower())
        case "2":
            productos.sort(key=lambda x: float(x["precio"]), reverse=reverso)
        case "3":
            productos.sort(key=lambda x: float(x["stock"]), reverse=reverso)
        case _:
            print("Opción inválida.")
            return

    print("\n--- PRODUCTOS ORDENADOS ---")
    for p in productos:
        ruta_relativa = os.path.relpath(p["ruta_csv"], base)
        partes = ruta_relativa.split(os.sep)
        categoria = partes[0] if len(partes) > 0 else "-"
        subcategoria = partes[1].replace(".csv", "") if len(partes) > 1 else "-"
        print(f"Nombre: {p['nombre']} | Precio: ${p['precio']} | Marca: {p['marca']} | Stock: {p['stock']} | Categoría: {categoria} | Subcategoría: {subcategoria}")

import os,csv
from estadisticas import ordenar_productos
#VISTA DE PRODUCTOS

def leer_productos_csv(ruta_base):
    productos = []
    for elemento in os.listdir(ruta_base):
        ruta_completa = os.path.join(ruta_base, elemento)

        if os.path.isdir(ruta_completa):
            # Si es un directorio, recorrer recursivamente
            productos.extend(leer_productos_csv(ruta_completa))
        
        elif elemento == "productos.csv":
            # Si es el archivo CSV, leer los productos
            with open(ruta_completa, "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for fila in reader:
                    #guardar la ruta del archivo para referencia futura
                    fila["ruta_csv"] = ruta_completa
                    productos.append(fila)
    return productos

def mostrar_productos(base,mostrar_ordenar):
    print("\n--- LISTA DE PRODUCTOS ---\n")

    # Recolectar filas de todos los CSV (solo activos)
    filas = []  # cada elemento: (nombre, precio_str, marca, stock_str)
    for ruta, _, archivos in os.walk(base):
        for archivo in archivos:
            if archivo.endswith(".csv"):
                ruta_csv = os.path.join(ruta, archivo)
                with open(ruta_csv, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for fila in reader:
                        if fila.get("activo", "si").lower() == "no":
                            continue
                        nombre = fila.get("nombre", "")
                        precio = fila.get("precio", "")
                        # Asegurar formato de precio sin romper si ya es número
                        precio_str = f"${precio}" if precio != "" else ""
                        marca = fila.get("marca", "")
                        stock = fila.get("stock", "")
                        stock_str = str(stock)
                        filas.append((nombre, precio_str, marca, stock_str))

    if not filas:
        print("No hay productos activos registrados.")
        return

    # Encabezados
    headers = ["Nombre", "Precio", "Marca", "Stock"]

    # Calcular ancho máximo por columna
    anchos = []
    for i in range(len(headers)):
        max_celda = max(len(headers[i]), max((len(f[i]) for f in filas), default=0))
        anchos.append(max_celda)

    # Formato: Nombre y Marca alineados a la izquierda; Precio y Stock a la derecha
    formato = f"{{:<{anchos[0]}}} | {{:>{anchos[1]}}} | {{:<{anchos[2]}}} | {{:>{anchos[3]}}}"

    # Imprimir encabezado y separador
    print(formato.format(*headers))
    print("-" * anchos[0] + " | " + "-" * anchos[1] + " | " + "-" * anchos[2] + " | " + "-" * anchos[3])

    # Imprimir filas alineadas
    for nombre, precio, marca, stock in filas:
        print(formato.format(nombre, precio, marca, stock))

    if mostrar_ordenar:
        ordenar_productos(base)


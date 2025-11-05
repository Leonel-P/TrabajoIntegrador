import os
import csv
from utilidades import (pedir_categoria, pedir_subcategoria, pedir_nombre, pedir_precio, pedir_marca, pedir_stock)

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

def mostrar_productos(base):
    print("\n--- LISTA DE PRODUCTOS ---\n")

    hay_productos = False  # bandera para saber si se mostró alguno

    for ruta, _, archivos in os.walk(base):
        for archivo in archivos:
            if archivo.endswith(".csv"):
                ruta_csv = os.path.join(ruta, archivo)
                with open(ruta_csv, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for fila in reader:
                        # Mostrar solo productos activos
                        if fila.get("activo", "si").lower() == "no":
                            continue

                        print(
                            f"Nombre: {fila['nombre']} | Precio: ${fila['precio']} | Marca: {fila['marca']} | Stock: {fila['stock']}"
                        )
                        hay_productos = True

    if not hay_productos:
        print("No hay productos activos registrados.")


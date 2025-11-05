import os, json, csv
from utilidades import pedir_opcion

HEADER = ["nombre", "precio", "marca", "stock","activo"]
ARCHIVO_ESTRUCTURA = "estructura.json"

# === ESTRUCTURA INICIAL POR DEFECTO === #
ESTRUCTURA_INICIAL = {
    "Computadoras": ["Notebooks", "PCs de escritorio", "Tablets"],
    "Celulares": ["Gama alta", "Gama media", "Gama baja"],
    "Consolas": ["PlayStation", "Xbox", "Nintendo"]
}

# === FUNCIONES DE ESTRUCTURA === #

def cargar_estructura():
    """Carga la estructura desde el JSON o crea una por defecto."""
    if not os.path.exists(ARCHIVO_ESTRUCTURA):
        guardar_estructura(ESTRUCTURA_INICIAL)
        return ESTRUCTURA_INICIAL
    with open(ARCHIVO_ESTRUCTURA, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_estructura(estructura):
    """Guarda la estructura actualizada en el archivo JSON."""
    with open(ARCHIVO_ESTRUCTURA, "w", encoding="utf-8") as f:
        json.dump(estructura, f, indent=4, ensure_ascii=False)

def crear_estructura_base():
    """Crea la carpeta raíz si no existe."""
    carpeta_base = "productos_tecnologicos"
    os.makedirs(carpeta_base, exist_ok=True)
    return carpeta_base

def crear_estructura_jerarquica():
    """Crea toda la estructura inicial de carpetas y archivos CSV."""
    base = crear_estructura_base()
    estructura = cargar_estructura()

    for categoria, subcategorias in estructura.items():
        for sub in subcategorias:
            ruta_sub = os.path.join(base, categoria, sub)
            os.makedirs(ruta_sub, exist_ok=True)

            ruta_csv = os.path.join(ruta_sub, "productos.csv")
            if not os.path.exists(ruta_csv):
                with open(ruta_csv, "w", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=HEADER)
                    writer.writeheader()

    print("Estructura jerárquica creada exitosamente.\n")

# === OPCION 1.1 CREAR NUEVA CATEGORÍA === #
def crear_categoria(base):
    estructura = cargar_estructura()

    print("\n=== CREAR NUEVA CATEGORÍA ===")
    nombre_categoria = input("Ingrese el nombre de la nueva categoría (deje vacío para cancelar): ").strip().capitalize()
    if not nombre_categoria:
        print("Operación cancelada.\n")
        return

    if nombre_categoria in estructura:
        print("⚠️ Esa categoría ya existe.\n")
        return

    estructura[nombre_categoria] = []
    ruta_categoria = os.path.join(base, nombre_categoria)
    os.makedirs(ruta_categoria, exist_ok=True)

    # Pedir cantidad de subcategorías
    try:
        cant_sub = int(input("¿Cuántas subcategorías desea crear?: "))
    except ValueError:
        print("Entrada inválida. No se crearán subcategorías.\n")
        guardar_estructura(estructura)
        return

    for i in range(cant_sub):
        sub = input(f"Nombre de la subcategoría {i+1}: ").strip().capitalize()
        if not sub:
            print("⚠️ Subcategoría omitida (nombre vacío).")
            continue

        if sub in estructura[nombre_categoria]:
            print(f"⚠️ La subcategoría '{sub}' ya existe, se omite.")
            continue

        estructura[nombre_categoria].append(sub)
        ruta_sub = os.path.join(ruta_categoria, sub)
        os.makedirs(ruta_sub, exist_ok=True)

        ruta_csv = os.path.join(ruta_sub, "productos.csv")
        with open(ruta_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=HEADER)
            writer.writeheader()

    guardar_estructura(estructura)
    print(f"\n✅ Categoría '{nombre_categoria}' creada correctamente.\n")

# === OPCION 1.2 CREAR NUEVA SUBCATEGORÍA === #
def crear_subcategoria(base):
    print("\n=== CREAR NUEVA SUBCATEGORÍA ===")

    estructura = cargar_estructura()
    categorias = list(estructura.keys())

    if not categorias:
        print("⚠️ No hay categorías existentes. Cree una primero.\n")
        return

    print("Categorías disponibles:")
    for i, cat in enumerate(categorias, 1):
        print(f"{i}. {cat}")

    eleccion = pedir_opcion("Seleccione una categoría por número: ", len(categorias))
    categoria = categorias[eleccion - 1]

    sub = input("Ingrese el nombre de la nueva subcategoría: ").strip().capitalize()
    if not sub:
        print("⚠️ Subcategoría no puede estar vacía.\n")
        return

    if sub in estructura[categoria]:
        print(f"⚠️ La subcategoría '{sub}' ya existe en '{categoria}'.\n")
        return

    estructura[categoria].append(sub)
    guardar_estructura(estructura)

    ruta_sub = os.path.join(base, categoria, sub)
    os.makedirs(ruta_sub, exist_ok=True)
    ruta_csv = os.path.join(ruta_sub, "productos.csv")

    with open(ruta_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADER)
        writer.writeheader()

    print(f"✅ Subcategoría '{sub}' creada correctamente dentro de '{categoria}'.\n")


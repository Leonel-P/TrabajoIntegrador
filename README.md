# Gestión Jerárquica de Productos Tecnológicos  
**Parcial 2 – Programación 1 | UTN FRM Mendoza**

## Resumen de la Estructura de Datos
- Dominio: Productos tecnológicos (Computadoras, Celulares, Consolas).
- Ítem: Diccionario con claves:
  - nombre: str
  - precio: float (> 0)
  - marca: str
  - stock: int (>= 0)
  - activo: "si" | "no"
- Eliminación lógica: activo = "no".

## Estructura Jerárquica (3 Niveles)
- Nivel 0: productos_tecnologicos/ (raíz)
- Nivel 1: [Categoría] → ej. "Consolas"
- Nivel 2: [Subcategoría] → ej. "PlayStation"
- Nivel 3: productos.csv → archivo final con ítems

## Lógica de Almacenamiento
- Alta: usuario elige categoría → subcategoría → datos → se guarda en CSV correspondiente (modo append).
- Creación de carpetas: os.makedirs(..., exist_ok=True).
- Persistencia de jerarquía: estructura.json define categorías/subcategorías iniciales.
- Modificación: sobrescribe solo el CSV del producto.
- Eliminación: marca activo = "no" (no borra archivo).

## Lógica de Filtrado
- Recursividad: recorre toda la jerarquía y lee todos los productos.csv.
- Filtro global: solo ítems con activo = "si".
- Búsqueda: por nombre (insensible a mayúsculas) en todos los CSVs.
- Mostrado: tabla alineada con nombre, precio, marca, stock.

## Instrucciones de Uso
1. Ejecutar: python main.py
2. Menú:
   - 1 → Crear categoría / subcategoría
   - 2 → Alta de producto (pide categoría → subcategoría → datos)
   - 3 → Mostrar catálogo completo (recursividad)
   - 4 → Modificar producto
   - 5 → Eliminar (lógico)
   - 6 → Estadísticas y ordenamiento
   - 0 → Salir
3. Ejemplo de alta:
   - Opción 2 → Consolas → PlayStation → PS5 → 850000 → Sony → 5
   - Guardado en: productos_tecnologicos/Consolas/PlayStation/productos.csv
4. Ver catálogo: Opción 3 → recorre toda la jerarquía y muestra tabla.

## Requisitos
- Python 3.x
- Librerías estándar: os, csv, json
- Datos de prueba: PS5 en Consolas/PlayStation/productos.csv

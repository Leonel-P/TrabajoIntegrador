from estructura import crear_estructura_base, crear_categoria,crear_subcategoria, crear_estructura_jerarquica, cargar_estructura
from crud import alta_producto, modificar_producto, eliminar_producto
from recorrer import mostrar_productos
from estadisticas import ver_estadisticas
from utilidades import pedir_opcion

#---------------------
#  Funcion Principal   
#---------------------

def main():
    base= "datos/base"
    crear_estructura_base()
    base = crear_estructura_base()
    crear_estructura_jerarquica()
    estructura = cargar_estructura()

    while True:
        print("\n===== MENU PRINCIPAL =====\n1. Gestion de categorias\n2. Alta de producto\n3. Mostrar productos\n4. Modificar producto\n5. Eliminar producto\n6. Estadísticas\n0. Salir\n")

        opcion= pedir_opcion("Ingrese una opcion: ",6)

        match opcion:
            case 1:
                print("\n--- GESTION DE CATEGORIAS ---")
                opc = pedir_opcion("\n1. Crear nueva categoría\n2. Crear nueva subcategoría\n0. Volver\nIngrese una opción: ",2)
                match opc:
                    case 1:
                        crear_categoria(base)
                    case 2:
                        crear_subcategoria(base)
            case 2:
                alta_producto(base,estructura)
            case 3:
                mostrar_productos(base,True)
            case 4:
                modificar_producto(base)
            case 5:
                eliminar_producto(base)
            case 6:
                ver_estadisticas(base)
            case 0:
                print("Saliendo...")
                break


if __name__ == "__main__":
    main()


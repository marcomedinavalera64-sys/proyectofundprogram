# =====================================================
# SISTEMA DE PEDIDOS - QUESERÍA LOS ALPES
# Curso: Fundamentos de Programación
# Proyecto académico - Examen parcial
# =====================================================

# LISTAS PARA EL CATÁLOGO DE PRODUCTOS
productos = [
    "Queso fresco",
    "Queso mantecoso",
    "Queso suizo",
    "Mantequilla"
]

precios = [18.0, 22.0, 28.0, 25.0]
stock = [20.0, 15.0, 12.0, 25.0]

# LISTA DONDE SE ALMACENAN LOS PEDIDOS
pedidos = []


# FUNCIÓN PARA MOSTRAR EL MENÚ
def mostrar_menu():
    print("\n" + "=" * 48)
    print("      SISTEMA DE PEDIDOS - QUESERÍA LOS ALPES")
    print("=" * 48)
    print("1. Registrar nuevo pedido")
    print("2. Buscar pedido por código")
    print("3. Listar pedidos ordenados")
    print("4. Ver inventario actual")
    print("5. Mostrar resumen del día")
    print("0. Salir")
    print("=" * 48)


# FUNCIÓN PARA MOSTRAR LOS PRODUCTOS
def mostrar_productos():
    print("\n--- CATÁLOGO DE PRODUCTOS ---")

    for i in range(len(productos)):
        print(
            f"{i + 1}. {productos[i]} "
            f"| S/ {precios[i]:.2f}/kg "
            f"| Stock: {stock[i]:.2f} kg"
        )


# FUNCIÓN PARA REGISTRAR UN PEDIDO
def registrar_pedido():
    print("\n--- REGISTRO DE PEDIDO ---")

    cliente = input("Nombre del cliente: ").strip()

    if len(cliente) < 2:
        print("Error: Ingrese un nombre válido.")
        return

    canal = input(
        "Canal de atención (Presencial/Telefónico): "
    ).strip()

    if canal.lower() not in ["presencial", "telefónico", "telefonico"]:
        print("Error: Canal de atención no válido.")
        return

    mostrar_productos()

    try:
        opcion = int(input("Seleccione un producto: "))

        if opcion < 1 or opcion > len(productos):
            print("Error: Producto no válido.")
            return

        indice = opcion - 1

        cantidad = float(
            input("Cantidad solicitada en kg: ")
        )

        if cantidad <= 0:
            print("Error: La cantidad debe ser mayor a cero.")
            return

        if cantidad > stock[indice]:
            print("Error: Stock insuficiente.")
            print(
                f"Disponible: {stock[indice]:.2f} kg"
            )
            return

        # CALCULAR EL IMPORTE
        total = cantidad * precios[indice]

        # GENERAR CÓDIGO CONSECUTIVO
        codigo = f"PED-{len(pedidos) + 1:06d}"

        # GUARDAR EL PEDIDO EN UNA LISTA
        pedido = {
            "codigo": codigo,
            "cliente": cliente,
            "canal": canal,
            "producto": productos[indice],
            "cantidad": cantidad,
            "precio": precios[indice],
            "total": total
        }

        pedidos.append(pedido)

        # ACTUALIZAR INVENTARIO
        stock[indice] -= cantidad

        print("\n¡PEDIDO REGISTRADO CORRECTAMENTE!")
        print(f"Código: {codigo}")
        print(f"Cliente: {cliente}")
        print(f"Producto: {productos[indice]}")
        print(f"Cantidad: {cantidad:.2f} kg")
        print(f"Total: S/ {total:.2f}")

    except ValueError:
        print("Error: Debe ingresar valores numéricos válidos.")


# FUNCIÓN DE BÚSQUEDA SECUENCIAL
def buscar_pedido():
    print("\n--- BUSCAR PEDIDO ---")

    codigo = input(
        "Ingrese el código del pedido: "
    ).strip().upper()

    encontrado = False

    for pedido in pedidos:
        if pedido["codigo"] == codigo:
            print("\nPEDIDO ENCONTRADO")
            print(f"Código: {pedido['codigo']}")
            print(f"Cliente: {pedido['cliente']}")
            print(f"Canal: {pedido['canal']}")
            print(f"Producto: {pedido['producto']}")
            print(f"Cantidad: {pedido['cantidad']:.2f} kg")
            print(f"Total: S/ {pedido['total']:.2f}")

            encontrado = True
            break

    if not encontrado:
        print("No se encontró el pedido solicitado.")


# FUNCIÓN DE ORDENAMIENTO POR BURBUJA
def ordenar_pedidos():
    print("\n--- PEDIDOS ORDENADOS POR CLIENTE ---")

    if len(pedidos) == 0:
        print("No existen pedidos registrados.")
        return

    # COPIAR LA LISTA PARA NO MODIFICAR EL ORIGINAL
    ordenados = pedidos.copy()

    n = len(ordenados)

    # ALGORITMO DE ORDENAMIENTO BURBUJA
    for i in range(n - 1):
        for j in range(n - 1 - i):
            nombre1 = ordenados[j]["cliente"].lower()
            nombre2 = ordenados[j + 1]["cliente"].lower()

            if nombre1 > nombre2:
                ordenados[j], ordenados[j + 1] = (
                    ordenados[j + 1],
                    ordenados[j]
                )

    # MOSTRAR RESULTADOS
    for pedido in ordenados:
        print(
            f"{pedido['codigo']} | "
            f"{pedido['cliente']} | "
            f"{pedido['producto']} | "
            f"S/ {pedido['total']:.2f}"
        )


# FUNCIÓN PARA CONSULTAR INVENTARIO
def consultar_inventario():
    print("\n--- INVENTARIO ACTUAL ---")

    for i in range(len(productos)):
        print(
            f"{productos[i]} | "
            f"Stock: {stock[i]:.2f} kg | "
            f"Precio: S/ {precios[i]:.2f}/kg"
        )


# FUNCIÓN PARA MOSTRAR RESUMEN
def mostrar_resumen():
    print("\n--- RESUMEN DE PEDIDOS ---")

    cantidad_pedidos = len(pedidos)
    total_acumulado = 0

    for pedido in pedidos:
        total_acumulado += pedido["total"]

    print(f"Pedidos registrados: {cantidad_pedidos}")
    print(f"Importe acumulado: S/ {total_acumulado:.2f}")


# PROGRAMA PRINCIPAL
def main():

    while True:
        mostrar_menu()

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_pedido()

        elif opcion == "2":
            buscar_pedido()

        elif opcion == "3":
            ordenar_pedidos()

        elif opcion == "4":
            consultar_inventario()

        elif opcion == "5":
            mostrar_resumen()

        elif opcion == "0":
            print("\nGracias por utilizar el sistema.")
            print("Quesería Los Alpes")
            break

        else:
            print("Error: Seleccione una opción entre 0 y 5.")


# INICIO DEL PROGRAMA
if __name__ == "__main__":
    main()

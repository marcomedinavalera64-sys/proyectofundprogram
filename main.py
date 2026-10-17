"""Ejecutar: py main.py. Prototipo en memoria para gestionar pedidos."""
from datos import inicial
from negocio import (crear_generador, registrar, buscar, modificar, eliminar,
                     burbuja, seleccion, buscar_texto, mostrar, ejemplo_parametros)

def leer_lineas(estado):
    for i in range(len(estado["ids"])):
        print(estado["ids"][i], estado["nombres"][i],
              "S/", estado["precios"][i], "Disponible:", estado["stock"][i], "kg")
    lineas = []
    while True:
        producto = input("Producto (Enter termina): ").strip()
        if not producto:
            return lineas
        lineas.append([int(producto), input("Cantidad en kg: ")])

def main():
    estado = inicial()
    generar = crear_generador()
    print("DESAFÍO DE PROGRAMACIÓN — QUESERÍA LOS ALPES")
    print("Pedidos borrador. Datos de demostración; se pierden al salir.")
    while True:
        print("1 Registrar | 2 Buscar código | 3 Modificar | 4 Eliminar")
        print("5 Burbuja por código | 6 Selección por cliente | 7 Buscar texto")
        print("8 Stock | 9 Ejemplo de parámetros | 0 Salir")
        opcion = input("Opción: ").strip()
        try:
            if opcion == "0":
                break
            elif opcion in ("1", "3"):
                codigo = input("Código: ") if opcion == "3" else None
                cliente = input("Cliente: ")
                canal = input("Canal (presencial/telefónico): ")
                lineas = leer_lineas(estado)
                if opcion == "1":
                    pedido = registrar(estado, generar, cliente, canal, lineas)
                else:
                    pedido = modificar(estado, codigo, cliente, canal, lineas)
                mostrar(pedido)
            elif opcion == "2":
                pedido = buscar(estado["pedidos"], input("Código: "))
                if pedido is None:
                    print("No encontrado.")
                else:
                    mostrar(pedido)
            elif opcion == "4":
                codigo = input("Código del borrador: ")
                if input("¿Eliminar y liberar reserva? (s/n): ").strip().casefold() == "s":
                    eliminar(estado, codigo)
                    print("Borrador eliminado y stock liberado.")
            elif opcion in ("5", "6", "7"):
                if opcion == "5":
                    resultado = burbuja(estado["pedidos"])
                elif opcion == "6":
                    resultado = seleccion(estado["pedidos"])
                else:
                    resultado = buscar_texto(estado["pedidos"], input("Nombre o parte: "))
                for pedido in resultado:
                    mostrar(pedido)
                if not resultado:
                    print("Sin resultados.")
            elif opcion == "8":
                for i in range(len(estado["ids"])):
                    print(estado["nombres"][i], estado["stock"][i], "kg disponibles")
            elif opcion == "9":
                print(ejemplo_parametros())
            else:
                print("Opción inválida.")
        except ValueError as error:
            print("Operación rechazada:", error)
        except (EOFError, KeyboardInterrupt):
            print("Entrada interrumpida.")
            break

if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nFin del programa.")

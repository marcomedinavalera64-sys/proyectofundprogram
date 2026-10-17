
from datos import inicial
from negocio import (
    crear_generador, registrar, buscar, modificar, eliminar,
    mostrar, ejemplo_parametros,
)


def main():
    estado = inicial()
    generar = crear_generador()

    pedido = registrar(estado, generar, "Daniel", "presencial", [[1, "15"]])
    print("1 REGISTRAR")
    mostrar(pedido)
    print("Stock fresco:", estado["stock"][0])

    encontrado = buscar(estado["pedidos"], "PED-000001")
    print("2 BUSCAR:", encontrado["cliente"])

    actualizado = modificar(
        estado, "PED-000001", "Daniel", "presencial", [[1, "10"]]
    )
    print("3 MODIFICAR A 10 KG")
    mostrar(actualizado)
    print("Stock fresco:", estado["stock"][0])

    eliminar(estado, "PED-000001")
    print("4 ELIMINAR: pedidos", len(estado["pedidos"]), "stock", estado["stock"][0])
    print("PARÁMETROS:", ejemplo_parametros())


if __name__ == "__main__":
    main()

def burbuja(pedidos):
    copia = list(pedidos)

    for limite in range(len(copia) - 1, 0, -1):
        cambio = False

        for j in range(limite):
            if copia[j]["codigo"] > copia[j + 1]["codigo"]:
                copia[j], copia[j + 1] = copia[j + 1], copia[j]
                cambio = True

        if not cambio:
            break

    return copia


def seleccion(pedidos):
    copia = list(pedidos)

    for i in range(len(copia) - 1):
        menor = i

        for j in range(i + 1, len(copia)):
            if copia[j]["cliente"].casefold() < copia[menor]["cliente"].casefold():
                menor = j

        copia[i], copia[menor] = copia[menor], copia[i]

    return copia
pedidos = [
    {"codigo": 3, "cliente": "Luis"},
    {"codigo": 1, "cliente": "Ana"},
    {"codigo": 2, "cliente": "María"}
]

print("Por código:", burbuja(pedidos))
print("Por cliente:", seleccion(pedidos))
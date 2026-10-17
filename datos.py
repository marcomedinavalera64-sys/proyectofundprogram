"""Catálogo de demostración y validación del prototipo del desafío."""
from decimal import Decimal, InvalidOperation

CANALES = ("presencial", "telefónico")  # Constante de alcance global al módulo.

def numero(valor):
    try:
        n = Decimal(str(valor).strip().replace(",", "."))
    except InvalidOperation:
        raise ValueError("Cantidad inválida.") from None
    if not n.is_finite() or n <= 0 or n > 999999 or n.as_tuple().exponent < -3:
        raise ValueError("Use una cantidad positiva con hasta tres decimales.")
    return n

def limpiar_nombre(texto):
    limpio = " ".join(texto.strip().split())
    if not 2 <= len(limpio) <= 80 or not all(c.isalpha() or c in " '-" for c in limpio):
        raise ValueError("Nombre inválido: use de 2 a 80 caracteres.")
    return limpio

def inicial():
    # Arreglos paralelos: el índice relaciona los datos de un producto.
    return {"ids": [1, 2, 3, 4],
            "nombres": ["Queso fresco", "Queso mantecoso", "Queso suizo", "Mantequilla"],
            "precios": [Decimal(x) for x in ("18", "22", "28", "25")],
            "stock": [Decimal(x) for x in ("20", "15", "12", "25")],
            "pedidos": []}

"""Persistencia en JSON UTF-8 para una sola instancia de la aplicación."""
import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from decimal import Decimal
from negocio import inicial, numero


def validar(datos):
    if not isinstance(datos, dict) or set(datos) != {'productos', 'pedidos'}:
        raise ValueError('Estructura de archivo inválida.')
    if not isinstance(datos['productos'], list) or not isinstance(datos['pedidos'], list):
        raise ValueError('Se requieren listas de productos y pedidos.')
    if len(datos['productos']) != 4:
        raise ValueError('Catálogo incompleto.')
    ids = []
    for p in datos['productos']:
        ids.append(p['id'])
        if type(p['id']) is not int or not isinstance(p['nombre'], str) or not p['nombre'].strip():
            raise ValueError('Producto inválido.')
        numero(p['stock'], cero=True)
        numero(p['precio'])
    if set(ids) != {1, 2, 3, 4}:
        raise ValueError('Identificadores de producto inválidos.')
    import re
    from datetime import datetime
    codigos = set()
    for p in datos['pedidos']:
        if not re.fullmatch(r'PED-[0-9]{6}', p['codigo']) or p['codigo'] in codigos:
            raise ValueError('Código inválido o duplicado.')
        codigos.add(p['codigo'])
        datetime.fromisoformat(p['fecha'])
        if not isinstance(p['cliente'], str) or not p['cliente'].strip() or p['canal'] not in ('presencial', 'telefónico'):
            raise ValueError('Datos de pedido inválidos.')
        if not isinstance(p['detalle'], list) or not p['detalle']:
            raise ValueError('Pedido sin detalle.')
        from decimal import ROUND_HALF_UP
        total = Decimal('0')
        for linea in p['detalle']:
            if linea['producto'] not in ids:
                raise ValueError('Producto desconocido en pedido.')
            esperado = (numero(linea['kg']) * numero(linea['precio'])).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
            if not isinstance(linea['nombre'], str) or Decimal(linea['subtotal']) != esperado:
                raise ValueError('Subtotal inválido.')
            total += esperado
        if Decimal(p['total']) != total:
            raise ValueError('Total inconsistente.')


def cargar(ruta):
    ruta = Path(ruta)
    if not ruta.exists():
        return inicial()
    try:
        with ruta.open(encoding='utf-8') as f:
            datos = json.load(f)
        validar(datos)
        return datos
    except (ValueError, KeyError, TypeError, ArithmeticError) as error:
        raise ValueError('Archivo inválido. Se conserva sin cambios; revise una copia de respaldo.') from error


def guardar(ruta, datos):
    ruta = Path(ruta)
    validar(datos)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    temporal = None
    try:
        with NamedTemporaryFile('w', encoding='utf-8', dir=ruta.parent, delete=False, suffix='.tmp') as f:
            temporal = f.name
            json.dump(datos, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temporal, ruta)
    finally:
        if temporal and os.path.exists(temporal):
            os.unlink(temporal)

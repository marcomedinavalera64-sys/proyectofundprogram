"""Ejecutar con python main.py. No requiere paquetes externos."""
from datetime import date
from pathlib import Path
from archivos import cargar, guardar
from negocio import registrar, buscar, ordenar, resumen

RUTA = Path(__file__).parent / 'datos' / 'queseria.json'


def mostrar(p):
    print(f"{p['codigo']} | {p['cliente']} | {p['fecha']} | S/ {p['total']}")
    for linea in p['detalle']:
        print(f"  {linea['nombre']}: {linea['kg']} kg x S/ {linea['precio']} = S/ {linea['subtotal']}")
    print('Constancia interna de venta. No es comprobante tributario.')


def main():
    try:
        estado = cargar(RUTA)
    except (OSError, ValueError) as e:
        print('No se puede iniciar:', e)
        return
    print('QUESERÍA LOS ALPES - PROTOTIPO ACADÉMICO')
    print('Catálogo inicial de demostración. Usar una sola instancia.')
    while True:
        try:
            print('\n1 Registrar  2 Buscar  3 Ordenar  4 Inventario  5 Resumen de hoy  0 Salir')
            opcion = input('Opción: ').strip()
            if opcion == '0':
                break
            if opcion == '1':
                cliente = input('Cliente: ')
                canal = input('Canal (presencial/telefónico): ')
                lineas = []
                while True:
                    producto = input('Producto 1 fresco, 2 mantecoso, 3 suizo, 4 mantequilla; 0 terminar: ')
                    if producto.strip() == '0':
                        break
                    lineas.append((int(producto), input('Cantidad en kg: ')))
                pedido = registrar(estado, cliente, canal, lineas, lambda d: guardar(RUTA, d))
                mostrar(pedido)
            elif opcion == '2':
                pedido = buscar(estado['pedidos'], input('Código: '))
                mostrar(pedido) if pedido else print('Pedido no encontrado.')
            elif opcion == '3':
                for p in ordenar(estado['pedidos']):
                    mostrar(p)
                if not estado['pedidos']:
                    print('No hay pedidos.')
            elif opcion == '4':
                for p in estado['productos']:
                    print(f"{p['id']} {p['nombre']}: {p['stock']} kg | S/ {p['precio']}/kg")
            elif opcion == '5':
                n, total = resumen(estado, date.today().isoformat())
                print(f'Hoy: {n} pedidos | Recaudación: S/ {total:.2f}')
            else:
                print('Opción inválida.')
        except (ValueError, OSError) as e:
            print('Operación rechazada:', e)
        except (EOFError, KeyboardInterrupt):
            print('\nCierre solicitado. Los pedidos confirmados ya están guardados.')
            break


if __name__ == '__main__':
    main()

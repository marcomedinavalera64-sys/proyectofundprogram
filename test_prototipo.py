import unittest
import tempfile
from pathlib import Path
from copy import deepcopy
from negocio import inicial, registrar, buscar, ordenar, numero, resumen
from archivos import cargar, guardar


class Pruebas(unittest.TestCase):
    def setUp(self):
        self.e = inicial()
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.ruta = Path(self.tmp.name) / 'datos.json'

    def venta(self, lineas, nombre='Daniel', canal='presencial'):
        return registrar(self.e, nombre, canal, lineas, lambda d: guardar(self.ruta, d))

    def test_01_venta_normal(self):
        p = self.venta([(1, '15')])
        self.assertEqual(p['total'], '270.00')
        self.assertEqual(self.e['productos'][0]['stock'], '5')

    def test_02_stock_insuficiente(self):
        anterior = deepcopy(self.e)
        with self.assertRaises(ValueError): self.venta([(2, '20')], 'María')
        self.assertEqual(self.e, anterior)

    def test_03_compra_multiple(self):
        p = self.venta([(3, '5'), (4, '5')], 'Yandel')
        self.assertEqual(p['total'], '265.00')

    def test_04_nombre_vacio(self):
        with self.assertRaises(ValueError): self.venta([(1, '1')], ' ')

    def test_05_cantidad_negativa(self):
        with self.assertRaises(ValueError): self.venta([(1, '-5')])

    def test_06_stock_cero(self):
        self.e['productos'][2]['stock'] = '0'
        with self.assertRaises(ValueError): self.venta([(3, '3')], 'Luis')

    def test_07_stock_exacto(self):
        self.venta([(1, '20')])
        self.assertEqual(self.e['productos'][0]['stock'], '0')

    def test_08_numeros_invalidos(self):
        for x in ['0', 'abc', 'NaN', 'Infinity', '1.0001']:
            with self.subTest(x=x):
                with self.assertRaises(ValueError): numero(x)

    def test_09_busqueda(self):
        p = self.venta([(1, '1')])
        self.assertEqual(buscar(self.e['pedidos'], ' ped-000001 '), p)
        self.assertIsNone(buscar(self.e['pedidos'], 'PED-999999'))

    def test_10_ordenamiento(self):
        for i in range(3): self.venta([(1, '1')])
        invertida = self.e['pedidos'][::-1]
        ordenada = ordenar(invertida)
        self.assertEqual([p['codigo'] for p in ordenada], ['PED-000001', 'PED-000002', 'PED-000003'])
        self.assertEqual(invertida[0]['codigo'], 'PED-000003')

    def test_11_persistencia(self):
        self.venta([(1, '15')])
        self.assertEqual(cargar(self.ruta), self.e)

    def test_12_archivo_corrupto(self):
        self.ruta.write_text('{mal', encoding='utf-8')
        with self.assertRaises(ValueError): cargar(self.ruta)
        self.assertEqual(self.ruta.read_text(encoding='utf-8'), '{mal')

    def test_13_fallo_guardado(self):
        anterior = deepcopy(self.e)
        def falla(d): raise OSError('Disco no disponible')
        with self.assertRaises(OSError): registrar(self.e, 'Ana', 'presencial', [(1, '2')], falla)
        self.assertEqual(self.e, anterior)

    def test_14_producto_repetido(self):
        with self.assertRaises(ValueError): self.venta([(1, '15'), (1, '10')])
        self.assertEqual(self.e['productos'][0]['stock'], '20')

    def test_15_coma_decimal(self):
        self.assertEqual(self.venta([(1, '0,125')])['total'], '2.25')

    def test_16_resumen_por_fecha(self):
        p = self.venta([(1, '1')])
        self.assertEqual(str(resumen(self.e, p['fecha'][:10])[1]), '18.00')
        self.assertEqual(resumen(self.e, '2000-01-01')[0], 0)

    def test_17_canal_producto_pedido(self):
        for lineas, canal in [([], 'presencial'), ([(99, '1')], 'presencial'), ([(1, '1')], 'web')]:
            with self.subTest(lineas=lineas, canal=canal):
                with self.assertRaises(ValueError): self.venta(lineas, canal=canal)

    def test_18_archivo_semanticamente_invalido(self):
        self.venta([(1, '1')])
        import json
        datos = json.loads(self.ruta.read_text(encoding='utf-8'))
        datos['pedidos'][0]['total'] = '999'
        self.ruta.write_text(json.dumps(datos), encoding='utf-8')
        with self.assertRaises(ValueError): cargar(self.ruta)


if __name__ == '__main__':
    unittest.main(verbosity=2)

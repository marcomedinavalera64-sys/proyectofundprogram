import unittest
from copy import deepcopy
from decimal import Decimal
from contextlib import redirect_stdout
from io import StringIO
from datos import inicial, numero, limpiar_nombre
from negocio import *

class PruebasDesafio(unittest.TestCase):
    def setUp(self):
        self.e = inicial()
        self.g = crear_generador()

    def alta(self, nombre='Daniel', lineas=None):
        return registrar(self.e, self.g, nombre, 'presencial', lineas or [[1, '2']])

    def test_01_registro_y_matriz(self):
        p=self.alta(lineas=[[1,'15']])
        self.assertEqual(p['total'],Decimal('270.00'))
        self.assertEqual(self.e['stock'][0],Decimal('5'))
        self.assertEqual(p['detalle'],[[1,Decimal('15'),Decimal('18'),Decimal('270.00')]])

    def test_02_busqueda_codigo(self):
        p=self.alta()
        self.assertIs(buscar(self.e['pedidos'],' ped-000001 '),p)
        self.assertIsNone(buscar(self.e['pedidos'],'PED-999999'))

    def test_03_modificar_recalcula_reserva(self):
        self.alta()
        p=modificar(self.e,'PED-000001','María','telefónico',[[1,'5']])
        self.assertEqual(p['total'],Decimal('90'))
        self.assertEqual(self.e['stock'][0],Decimal('15'))
        self.assertEqual(len(self.e['pedidos']),1)

    def test_04_modificacion_fallida_atomica(self):
        self.alta()
        antes=deepcopy(self.e)
        with self.assertRaises(ValueError):
            modificar(self.e,'PED-000001','María','presencial',[[1,'21']])
        self.assertEqual(self.e,antes)

    def test_05_eliminar_libera_stock(self):
        self.alta()
        self.assertIsNone(eliminar(self.e,'PED-000001'))
        self.assertEqual(self.e,inicial())

    def test_06_eliminar_inexistente(self):
        antes=deepcopy(self.e)
        with self.assertRaises(ValueError): eliminar(self.e,'OTRO')
        self.assertEqual(self.e,antes)

    def test_07_burbuja_copia(self):
        datos=[{'codigo':x} for x in ['C','A','B','A']]
        antes=deepcopy(datos)
        self.assertEqual([x['codigo'] for x in burbuja(datos)],['A','A','B','C'])
        self.assertEqual(datos,antes)

    def test_08_seleccion_textual(self):
        datos=[{'cliente':x} for x in ['Zoe','ana','Luis']]
        antes=deepcopy(datos)
        self.assertEqual([x['cliente'] for x in seleccion(datos)],['ana','Luis','Zoe'])
        self.assertEqual(datos,antes)

    def test_09_busqueda_parcial(self):
        p=self.alta('María Pérez')
        self.assertEqual(buscar_texto(self.e['pedidos'],' PÉR '),[p])
        self.assertEqual(buscar_texto(self.e['pedidos'],'maria'),[])
        with self.assertRaises(ValueError): buscar_texto(self.e['pedidos'],'  ')

    def test_10_parametros(self):
        self.assertEqual(ejemplo_parametros(),(10,['pedido']))

    def test_11_nonlocal_independiente(self):
        otro=crear_generador()
        self.assertEqual(self.g(),'PED-000001')
        self.assertEqual(self.g(),'PED-000002')
        self.assertEqual(otro(),'PED-000001')

    def test_12_validaciones_numericas(self):
        for valor in ['0','-1','NaN','Infinity','x','1.0001','1000000']:
            with self.subTest(valor=valor), self.assertRaises(ValueError): numero(valor)
        self.assertEqual(numero(' 0,125 '),Decimal('0.125'))

    def test_13_agrupar_repetidos(self):
        p=self.alta(lineas=[[1,'2'],[1,'3']])
        self.assertEqual(len(p['detalle']),1)
        self.assertEqual(self.e['stock'][0],Decimal('15'))

    def test_14_stock_insuficiente_sin_consumir_codigo(self):
        antes=deepcopy(self.e)
        with self.assertRaises(ValueError): self.alta(lineas=[[1,'21']])
        self.assertEqual(self.e,antes)
        self.assertEqual(self.alta()['codigo'],'PED-000001')

    def test_15_nombre_y_canal(self):
        self.assertEqual(limpiar_nombre('  Ana   Pérez '),'Ana Pérez')
        for nombre in ['', '123', 'A']:
            with self.assertRaises(ValueError): self.alta(nombre)
        with self.assertRaises(ValueError): registrar(self.e,self.g,'Ana','web',[[1,'1']])

    def test_16_rechazo_multilinea_sin_descuento_parcial(self):
        antes=deepcopy(self.e)
        with self.assertRaises(ValueError): self.alta(lineas=[[1,'2'],[2,'16']])
        self.assertEqual(self.e,antes)

    def test_17_producto_y_carrito(self):
        for lineas in [[],[[99,'1']],[[True,'1']]]:
            with self.assertRaises(ValueError): registrar(self.e,self.g,'Ana','presencial',lineas)

    def test_18_sin_retorno_y_matriz(self):
        p=self.alta()
        salida=StringIO()
        with redirect_stdout(salida): resultado=mostrar(p)
        self.assertIsNone(resultado)
        self.assertIn('PED-000001',salida.getvalue())
        self.assertIn('36.00',salida.getvalue())

    def test_19_listas_vacias_unitarias(self):
        self.assertEqual(burbuja([]),[])
        self.assertEqual(seleccion([]),[])
        p=self.alta()
        self.assertEqual(burbuja([p]),[p])
        self.assertEqual(seleccion([p]),[p])

    def test_20_modificar_producto(self):
        self.alta()
        modificar(self.e,'PED-000001','Ana','presencial',[[2,'3']])
        self.assertEqual(self.e['stock'][:2],[Decimal('20'),Decimal('12')])

if __name__=='__main__': unittest.main(verbosity=2)

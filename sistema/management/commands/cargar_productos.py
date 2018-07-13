import csv

from django.core import management
from django.core.management.base import BaseCommand


from ...models import Producto, Existencia, Presentacion, UnidadMedida


fields = ['codigo', 'desc', 'unidad', 'cantidad', 'precio']


class Command(BaseCommand):

    def handle(self, *args, **options):
        Producto.objects.all().delete()
        unidad_medida, _ = UnidadMedida.objects.get_or_create(nombre='mg')
        with open('productos.csv', 'r', encoding='latin-1') as f:
            reader = csv.DictReader(f, fieldnames=fields, dialect='excel')
            for fila in reader:
                presentacion, _ = Presentacion.objects.get_or_create(nombre=fila['unidad'].strip().upper())
                producto = Producto.objects.create(
                    nombre=fila['desc'],
                    dosis=0,
                    unidad_medida=unidad_medida,
                    unidad=presentacion,
                    codigo=fila['codigo'].strip().upper(),
                    precio=round(float(fila['precio']), 2),
                )
                todo = int(float(fila['cantidad']))
                Existencia.objects.create(
                    producto=producto,
                    todo=todo,
                    fondo_fijo=todo,
                    porciento=100,
                )



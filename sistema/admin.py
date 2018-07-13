from django.contrib import admin
from sistema.models import PedidoCama, Producto, DevueltoCama, Existencia, Sala, Cama, PedidoSala, \
    DevueltoSala, PedidoSalaDetalle, DevueltoSalaDetalle, Presentacion, UnidadMedida, Justificacion, DevueltoFarmacia,\
    DevueltoAlmacen, DevueltoAlmacenDetalle, PedidoAlmacen, PedidoAlmacenDetalle, PermisoGlobal
# Register your models here.
admin.site.register(PedidoCama)
admin.site.register(PedidoSala)
admin.site.register(DevueltoCama)
admin.site.register(DevueltoSala)
admin.site.register(Existencia)
admin.site.register(PedidoSalaDetalle)
admin.site.register(DevueltoSalaDetalle)
admin.site.register(Producto)
admin.site.register(Cama)
admin.site.register(Sala)
admin.site.register(Presentacion)
admin.site.register(UnidadMedida)
admin.site.register(Justificacion)
admin.site.register(DevueltoFarmacia)
admin.site.register(DevueltoAlmacenDetalle)
admin.site.register(DevueltoAlmacen)
admin.site.register(PedidoAlmacen)
admin.site.register(PedidoAlmacenDetalle)
admin.site.register(PermisoGlobal)

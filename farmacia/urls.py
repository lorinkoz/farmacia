"""farmacia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from sistema.views import inicio, logear, deslogear, agregar_cantidad_medicamentos, \
    agregar_pedido_cama, editar_pedido_cama, pedidosCama, cama_unico, agregar_cama, editar_cama, cama, eliminar_cama, \
    existencia, sala, agregar_sala, eliminar_sala, eliminar_pedido_cama, agregar_devuelto_cama, editar_devuelto_cama, \
    eliminar_devuelto_cama, devueltosCama, devolucionesSala, agregar_producto, editar_producto, eliminar_producto, \
    producto, solicitar_pedido_sala, solicitar_devuelto_sala, buscar, pedidosSala, eliminar_pedido_sala, editar_sala, \
    despachar_pedido_sala, despachar_devuelto_sala, eliminar_devolucion_sala, pedidos_cama_relacionados, \
    devueltos_cama_relacionados, baja_cobertura, filtro_importe, agregar_presentacion, editar_presentacion, \
    agregar_unidad_medida, editar_unidad_medida, solicitar_pedido_farmacia, agregar_justificacion, editar_justificacion, \
    agregar_producto_almacen, editar_producto_almacen, eliminar_producto_almacen, devolucionesFarmacia, \
    solicitar_devuelto_farmacia, despachar_devuelto_farmacia, devolucionesAlmacen, eliminar_devolucion_farmacia, \
    despachar_pedido_farmacia, pedidosAlmacen, editar_cantidad_medicamentos, eliminar_pedido_farmacia, \
    ver_despacho_devuelto_farmacia, ver_despacho_pedido_farmacia, ReporteProductoPDF, ReporteSalaPDF, \
    ver_despacho_pedido_sala, ver_despacho_devuelto_sala, ReportePedidoCamaPDF, ReporteDevueltoCamaPDF, \
    ReporteBajaCoberturaPDF, ReporteDevueltoSalaPDF, ReportePedidoSalaPDF, \
    ReporteDevueltoAlmacenPDF, ReportePedidoAlmacenPDF, eliminar_cantidad_medicamentos, permisoGlobal, ayuda

urlpatterns = [

    # farmacia y servicios
    url(r'^$', logear, name='logear'),
    url(r'^inicio/$', inicio, name='inicio'),
    url(r'^deslogear/$', deslogear, name='deslogear'),
    url(r'^existencia/', existencia, name='existencia'),
    url(r'^buscar/$', buscar, name='buscar'),
    url(r'^ayuda/$', ayuda, name='ayuda'),
    url(r'^filtro-importe/$', filtro_importe, name='filtro_importe'),
    url(r'^baja-cobertura/$', baja_cobertura, name='baja_cobertura'),
    url(r'^agregar-presentacion/$', agregar_presentacion, name='agregar_presentacion'),
    url(r'^agregar-justificacion/(?P<id_c>\w+)/$', agregar_justificacion, name='agregar_justificacion'),
    url(r'^agregar-unidad-medida/$', agregar_unidad_medida, name='agregar_unidad_medida'),
    url(r'^editar-presentacion/(?P<id_pre>\w+)/$', editar_presentacion, name='editar_presentacion'),
    url(r'^editar-unidad-medida/(?P<id_um>\w+)/$', editar_unidad_medida, name='editar_unidad_medida'),
    url(r'^editar-justificacion/(?P<id_jus>\w+)/(?P<id_c>\w+)/$', editar_justificacion, name='editar_justificacion'),
    url(r'^pedidos-cama-relacionados/(?P<id_ps>\w+)/$', pedidos_cama_relacionados, name='pedidos_cama_relacionados'),
    url(r'^devueltos-cama-relacionados/(?P<id_ds>\w+)/$', devueltos_cama_relacionados,
        name='devueltos_cama_relacionados'),
    # farmacia
    url(r'^agregar-producto/$', agregar_producto, name='agregar_producto'),
    url(r'^editar-producto/(?P<id_p>\w+)/$', editar_producto, name='editar_producto'),
    url(r'^eliminar-producto/(?P<id_p>\w+)/$', eliminar_producto, name='eliminar_producto'),
    url(r'^producto/$', producto, name='producto'),
    url(r'^agregar-producto-almacen/$', agregar_producto_almacen, name='agregar_producto_almacen'),
    url(r'^editar-producto-almacen/(?P<id_df>\w+)/$', editar_producto_almacen, name='editar_producto_almacen'),
    url(r'^eliminar-producto-almacen/(?P<id_df>\w+)/$', eliminar_producto_almacen, name='eliminar_producto_almacen'),
    url(r'^devolucionesFarmacia/$', devolucionesFarmacia, name='devolucionesFarmacia'),
    url(r'^agregar-cantidad-medicamentos/$', agregar_cantidad_medicamentos, name='agregar_cantidad_medicamentos'),
    url(r'^editar-cantidad-medicamentos/(?P<id_e>\w+)/$', editar_cantidad_medicamentos,
        name='editar_cantidad_medicamentos'),
    url(r'^eliminar-cantidad-medicamentos/(?P<id_e>\w+)/$', eliminar_cantidad_medicamentos,
        name='eliminar_cantidad_medicamentos'),
    url(r'^devolucionesSala/$', devolucionesSala, name='devolucionesSala'),
    url(r'^devolucionesAlmacen/$', devolucionesAlmacen, name='devolucionesAlmacen'),
    url(r'^pedidosAlmacen/$', pedidosAlmacen, name='pedidosAlmacen'),
    url(r'^despachar-pedido-sala/(?P<id_ps>\w+)/$', despachar_pedido_sala, name='despachar_pedido_sala'),
    url(r'^despachar-devuelto-sala/(?P<id_ds>\w+)/$', despachar_devuelto_sala, name='despachar_devuelto_sala'),
    url(r'^despachar-devuelto-farmacia/(?P<id_df>\w+)/$', despachar_devuelto_farmacia,
        name='despachar_devuelto_farmacia'),
    url(r'^despachar-pedido-farmacia/(?P<id_pf>\w+)/$', despachar_pedido_farmacia, name='despachar_pedido_farmacia'),
    url(r'^eliminar-pedido-sala/(?P<id_peds>\w+)/$', eliminar_pedido_sala, name='eliminar_pedido_sala'),
    url(r'^eliminar-devolucion-sala/(?P<id_devs>\w+)/$', eliminar_devolucion_sala, name='eliminar_devolucion_sala'),
    url(r'^eliminar-devolucion-farmacia/(?P<id_devf>\w+)/$', eliminar_devolucion_farmacia,
        name='eliminar_devolucion_farmacia'),
    url(r'^eliminar-pedido-farmacia/(?P<id_pedf>\w+)/$', eliminar_pedido_farmacia, name='eliminar_pedido_farmacia'),
    url(r'^pedidosSala/$', pedidosSala, name='pedidosSala'),
    url(r'^permisoGlobal/$', permisoGlobal, name='permisoGlobal'),
    # sala
    url(r'^sala/$', sala, name='sala'),
    url(r'^eliminar-sala/(?P<id_s>\w+)/$', eliminar_sala, name='eliminar_sala'),
    url(r'^editar-sala/(?P<id_s>\w+)/$', editar_sala, name='editar_sala'),
    url(r'^agregar-sala/$', agregar_sala, name='agregar_sala'),
    # cama
    url(r'^agregar-pedido-cama/(?P<id_c>\w+)/$', agregar_pedido_cama, name='agregar_pedido_cama'),
    url(r'^editar-pedido-cama/(?P<id_pc>\w+)/$', editar_pedido_cama, name='editar_pedido_cama'),
    url(r'^eliminar-pedido-cama/(?P<id_pc>\w+)/$', eliminar_pedido_cama, name='eliminar_pedido_cama'),
    url(r'^pedidosCama/$', pedidosCama, name='pedidosCama'),
    url(r'^cama/$', cama, name='cama'),
    url(r'^cama-unico/(?P<id_c>\w+)/$', cama_unico, name='cama_unico'),
    url(r'^agregar-cama/$', agregar_cama, name='agregar_cama'),
    url(r'^eliminar-cama/$', eliminar_cama, name='eliminar_cama'),
    url(r'^editar-cama/(?P<id_c>\w+)/$', editar_cama, name='editar_cama'),
    url(r'^agregar-devuelto-cama/(?P<id_c>\w+)/$', agregar_devuelto_cama, name='agregar_devuelto_cama'),
    url(r'^editar-devuelto-cama/(?P<id_d>\w+)/$', editar_devuelto_cama, name='editar_devuelto_cama'),
    url(r'^eliminar-devuelto-cama/(?P<id_d>\w+)/$', eliminar_devuelto_cama, name='eliminar_devuelto_cama'),
    url(r'^devueltosCama/$', devueltosCama, name='devueltosCama'),
    url(r'^solicitar_pedido_sala/$', solicitar_pedido_sala, name='solicitar_pedido_sala'),
    url(r'^solicitar_devuelto_sala/$', solicitar_devuelto_sala, name='solicitar_devuelto_sala'),
    url(r'^solicitar_pedido_farmacia/$', solicitar_pedido_farmacia, name='solicitar_pedido_farmacia'),
    url(r'^solicitar_devuelto_farmacia/$', solicitar_devuelto_farmacia, name='solicitar_devuelto_farmacia'),
    url(r'^ver-despacho-pedido-sala/(?P<id_ps>\w+)/$', ver_despacho_pedido_sala, name='ver_despacho_pedido_sala'),
    url(r'^ver-despacho-devuelto-sala/(?P<id_ds>\w+)/$', ver_despacho_devuelto_sala, name='ver_despacho_devuelto_sala'),
    url(r'^ver-despacho-pedido-farmacia/(?P<id_pf>\w+)/$', ver_despacho_pedido_farmacia, name='ver_despacho_pedido_farmacia'),
    url(r'^ver-despacho-devuelto-farmacia/(?P<id_df>\w+)/$', ver_despacho_devuelto_farmacia, name='ver_despacho_devuelto_farmacia'),
    # reportes
    url(r'^ReporteProductoPDF/$', ReporteProductoPDF.as_view(), name='ReporteProductoPDF'),
    url(r'^ReporteSalaPDF/$', ReporteSalaPDF.as_view(), name='ReporteSalaPDF'),
    url(r'^ReportePedidoCamaPDF/(?P<id_ps>\w+)/$', ReportePedidoCamaPDF.as_view(), name='ReportePedidoCamaPDF'),
    url(r'^ReporteDevueltoCamaPDF/(?P<id_ds>\w+)/$', ReporteDevueltoCamaPDF.as_view(), name='ReporteDevueltoCamaPDF'),
    url(r'^ReportePedidoSalaPDF/(?P<id_ps>\w+)/$', ReportePedidoSalaPDF.as_view(), name='ReportePedidoSalaPDF'),
    url(r'^ReporteDevueltoSalaPDF/(?P<id_ds>\w+)/$', ReporteDevueltoSalaPDF.as_view(), name='ReporteDevueltoSalaPDF'),
    url(r'^ReportePedidoAlmacenPDF/(?P<id_pf>\w+)/$', ReportePedidoAlmacenPDF.as_view(), name='ReportePedidoAlmacenPDF'),
    url(r'^ReporteDevueltoAlmacenPDF/(?P<id_df>\w+)/$', ReporteDevueltoAlmacenPDF.as_view(), name='ReporteDevueltoAlmacenPDF'),
    url(r'^ReporteBajaCoberturaPDF/$', ReporteBajaCoberturaPDF.as_view(), name='ReporteBajaCoberturaPDF'),
    url(r'^admin/', admin.site.urls),
]

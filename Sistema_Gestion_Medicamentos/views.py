from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout as logout_dj, login as login_dj
import math
from django.conf import settings
from django.utils.dateformat import format as date_format
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.http import HttpResponse
from reportlab.platypus import TableStyle, SimpleDocTemplate, Table
from reportlab.lib import colors, pagesizes
from django.views.generic import View
from .form import AutenticarForm, CamaForm, PedidoCamaForm, ExistenciaMedicamentosForm, SalaForm, \
    DevueltoCamaForm, ProductoForm, PedidoSalaEntregadoFormSet, DevueltoSalaEntregadoFormSet, \
    DespachoFirmaDevueltoForm, DespachoFirmaPedidoForm, FiltrarImporteForm, PresentacionForm, \
    FiltrarSolicitudSalaForm, UnidadMedidaForm, JustificacionForm, DevueltoFarmaciaForm, DevueltoAlmacenEntregadoFormSet,\
    DespachoFirmaDevueltoAlmacenForm, DespachoFirmaPedidoAlmacenForm, PedidoAlmacenEntregadoFormSet, PermisoGlobalForm
from .models import Sala, Cama, PedidoCama, Existencia, PedidoSala, DevueltoCama, Producto, DevueltoSala, \
    PedidoSalaDetalle, DevueltoSalaDetalle, Presentacion, UnidadMedida, Justificacion, DevueltoFarmacia, DevueltoAlmacen,\
    DevueltoAlmacenDetalle, PedidoAlmacen, PedidoAlmacenDetalle, PermisoGlobal
from datetime import datetime
from django.utils import timezone

# Create your views here.


def logear(request):
    form = AutenticarForm()
    if request.user.is_authenticated():
        return redirect('inicio')
        form = AutenticarForm()
    if request.method == "POST":
        form = AutenticarForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user and user.is_active:
                login_dj(request, user)
                return redirect('inicio')
            else:
                form.add_error('username', 'Usuario incorrecto')
    return render(request, 'autenticar.html', locals())


def deslogear(request):
    logout_dj(request)
    return redirect(reverse('logear'))


@login_required
def permisoGlobal(request):
    pg = PermisoGlobal.objects.first()
    form = PermisoGlobalForm(instance=pg)
    if request.method == "POST":
        form = PermisoGlobalForm(request.POST, instance=pg)
        if form.is_valid():
            form.save()
            return redirect('permisoGlobal')
    return render(request, 'permisoGlobal.html', locals())


@login_required
def agregar_cantidad_medicamentos(request):
    pg = PermisoGlobal.objects.first()
    if pg.jefe_farmacia != request.user:
        raise PermissionDenied
    else:
        productos = Producto.objects.exclude(existencia__todo__gte=0)
        form = ExistenciaMedicamentosForm()
        if request.method == "POST":
            form = ExistenciaMedicamentosForm(request.POST)
            if form.is_valid():
               add_ex = form.save(commit=False)
               add_ex.porciento = (add_ex.todo * 100)/add_ex.fondo_fijo
               add_ex.save()
               return redirect('existencia')
    return render(request, 'agregar-cantidad-medicamentos.html', locals())


@login_required
def editar_cantidad_medicamentos(request, id_e):
    pg = PermisoGlobal.objects.first()
    if pg.jefe_farmacia != request.user:
        raise PermissionDenied
    else:
        ex = get_object_or_404(Existencia, id=id_e)
        form = ExistenciaMedicamentosForm(instance=ex)
        if request.method == "POST":
            form = ExistenciaMedicamentosForm(request.POST, instance=ex)
            if form.is_valid():
                edit_ex = form.save(commit=False)
                edit_ex.porciento = (edit_ex.todo * 100)/edit_ex.fondo_fijo
                edit_ex.save()
                return redirect('existencia')
    return render(request, 'editar-cantidad-medicamentos.html', locals())


@login_required
def eliminar_cantidad_medicamentos(request, id_e):
    pg = PermisoGlobal.objects.first()
    if pg.jefe_farmacia != request.user:
        raise PermissionDenied
    else:
        ex = Existencia.objects.get(id=id_e)
        ex.delete()
    return redirect('existencia')


@login_required
def buscar(request):
    sala = Sala.objects.all()
    form = FiltrarSolicitudSalaForm()
    if "sala" in request.GET:
            form = FiltrarSolicitudSalaForm(request.GET)
            if form.is_valid():
                ini_fecha = form.cleaned_data['inicio_fecha']
                fin_fecha = form.cleaned_data['final_fecha']
                if form.cleaned_data['tipo_solicitud'] == 'Pedidos de sala':
                    peds = PedidoSala.objects.filter(fecha_hora__range=(ini_fecha, fin_fecha))
                    peds = peds.filter(sala=form.cleaned_data['sala'])
                    peds = peds.exclude(despachado_por="")
                elif form.cleaned_data['tipo_solicitud'] == 'Devoluciones de sala':
                    devs = DevueltoSala.objects.filter(fecha_hora__range=(ini_fecha, fin_fecha))
                    devs = devs.filter(sala=form.cleaned_data['sala'])
                    devs = devs.exclude(recibida_por="")
    if form.is_valid():
            ini_fecha = form.cleaned_data['inicio_fecha']
            fin_fecha = form.cleaned_data['final_fecha']
            if form.cleaned_data['tipo_solicitud'] == 'Reposiciones a farmacia':
                    pedf = PedidoAlmacen.objects.filter(fecha_hora__range=(ini_fecha, fin_fecha))
                    pedf = pedf.exclude(recibido_por="")
            elif form.cleaned_data['tipo_solicitud'] == 'Devoluciones de farmacia':
                    devf = DevueltoAlmacen.objects.filter(fecha_hora__range=(ini_fecha, fin_fecha))
                    devf = devf.exclude(recibido_por="")
    return render(request, "buscar.html", locals())


@login_required
def filtro_importe(request):
    pg = PermisoGlobal.objects.first()
    if not request.user in pg.contabilidad.all():
        raise PermissionDenied
    else:
        detalles = {}
        form = FiltrarImporteForm(request.GET)
        if form.is_valid():
            ini_fecha = form.cleaned_data['inicio_fecha']
            fin_fecha = form.cleaned_data['final_fecha']
            centro_costo = form.cleaned_data['centro_costo']
            peds = PedidoSala.objects.filter(sala__centro_costo=centro_costo)
            peds = peds.filter(fecha_hora__range=(ini_fecha, fin_fecha))
            peds = peds.exclude(despachado_por="")
            psd = PedidoSalaDetalle.objects.select_related().filter(pedido_sala__in=peds)
            devs = DevueltoSala.objects.filter(sala__centro_costo=centro_costo)
            devs = devs.filter(fecha_hora__range=(ini_fecha, fin_fecha))
            devs = devs.exclude(despachado_por="")
            dsd = DevueltoSalaDetalle.objects.select_related().filter(devuelto_sala__in=devs)
            for p in psd:
                detalles.setdefault(p.producto, [0, 0])
                detalles[p.producto][0] += p.cantidad_entregada
            for d in dsd:
                detalles.setdefault(d.producto, [0, 0])
                detalles[d.producto][1] += d.cantidad_confirmada
    return render(request, 'filtro-importe.html', locals())


@login_required
def ayuda(request):
    return render(request, 'ayuda.html', locals())


@login_required
def inicio(request):
    info_ps = len(PedidoSala.objects.all())
    info_ds = len(DevueltoSala.objects.all())
    info_p = len(Producto.objects.all())
    return render(request, 'inicio.html', locals())


@login_required
def existencia(request):
    ex = Existencia.objects.all()
    return render(request, 'existencia.html', locals())


@login_required
def sala(request):
    s = Sala.objects.all()
    return render(request, 'sala.html', locals())


@login_required
def agregar_sala(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    else:
        form = SalaForm()
        if request.method == "POST":
            form = SalaForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('sala')
    return render(request, 'agregar-sala.html', locals())


@login_required
def editar_sala(request, id_s):
    if not request.user.is_superuser:
        raise PermissionDenied
    else:
        sala = get_object_or_404(Sala, id=id_s)
        form = SalaForm(instance=sala)
        if request.method == "POST":
            form = SalaForm(request.POST, instance=sala)
            if form.is_valid():
                form.save()
                return redirect('sala')
    return render(request, 'editar-sala.html', locals())


@login_required
def eliminar_sala(request, id_s):
    if not request.user.is_superuser:
        raise PermissionDenied
    else:
        sala_temp = Sala.objects.get(id=id_s)
        sala_temp.delete()
    return redirect('sala')


@login_required
def solicitar_pedido_sala(request):
    pg = PermisoGlobal.objects.first()
    if not request.user in pg.secretaria_sala.all():
        raise PermissionDenied
    else:
        sala = Sala.objects.get(secretaria=request.user)
        ca = Cama.objects.filter(sala__secretaria=request.user)
        pc = PedidoCama.objects.select_related().filter(cama__in=ca)
        pedidos_cama_pendientes = pc.filter(pedido_sala_detalle=None)
        detalles = {}
        for pedido_cama in pedidos_cama_pendientes:
            detalles.setdefault(pedido_cama.producto, [0, []])
            detalles[pedido_cama.producto][0] += pedido_cama.cantidad_solicitada
            detalles[pedido_cama.producto][1].append(pedido_cama)
        pedido_sala = PedidoSala.objects.create(fecha_hora=datetime.now(), solicitado_por=sala.secretaria.first_name + " " + sala.secretaria.last_name, sala=sala)
        for producto, data in detalles.items():
            cantidad, pedidos_cama = data
            pedido_sala_detalle = PedidoSalaDetalle.objects.create(
                pedido_sala=pedido_sala,
                producto=producto,
                cantidad_solicitada=cantidad,
            )
            for pedido_cama in pedidos_cama:
                pedido_cama.pedido_sala_detalle = pedido_sala_detalle
                pedido_cama.save()
    return redirect('cama')


@login_required
def solicitar_devuelto_sala(request):
    pg = PermisoGlobal.objects.first()
    if not request.user in pg.secretaria_sala.all():
        raise PermissionDenied
    else:
        sala = Sala.objects.get(secretaria=request.user)
        ca = Cama.objects.filter(sala__secretaria=request.user)
        dc = DevueltoCama.objects.select_related().filter(cama__in=ca)
        devueltos_cama_pendientes = dc.filter(devuelto_sala_detalle=None)
        detalles = {}
        for devuelto_cama in devueltos_cama_pendientes:
            detalles.setdefault(devuelto_cama.producto, [0, []])
            detalles[devuelto_cama.producto][0] += devuelto_cama.cantidad_devuelta
            detalles[devuelto_cama.producto][1].append(devuelto_cama)
        devuelto_sala = DevueltoSala.objects.create(fecha_hora=datetime.now(), devuelta_por=sala.secretaria.first_name + " " + sala.secretaria.last_name, sala=sala)
        for producto, data in detalles.items():
            cantidad, devueltos_cama = data
            devuelto_sala_detalle = DevueltoSalaDetalle.objects.create(
                devuelto_sala=devuelto_sala,
                producto=producto,
                cantidad_devuelta=cantidad,
            )
            for devuelto_cama in devueltos_cama:
                devuelto_cama.devuelto_sala_detalle = devuelto_sala_detalle
                devuelto_cama.save()
    return redirect('cama')


@login_required
def despachar_pedido_sala(request, id_ps):
    pedido_sala = PedidoSala.objects.get(id=id_ps)
    if pedido_sala.despachado_por != "":
        return redirect('ver_despacho_pedido_sala', pedido_sala.pk)
    pg = PermisoGlobal.objects.first()
    if not request.user in pg.farmacia.all():
        raise PermissionDenied
    else:
        redondeo = 0
        existencia = Existencia.objects.all()
        pedido_sala = PedidoSala.objects.get(id=id_ps)
        detalles = PedidoSalaDetalle.objects.filter(pedido_sala__id=id_ps)
        form = DespachoFirmaPedidoForm(instance=pedido_sala)
        formset = PedidoSalaEntregadoFormSet(queryset=detalles)
        if request.method == "POST":
            form = DespachoFirmaPedidoForm(request.POST, instance=pedido_sala)
            formset = PedidoSalaEntregadoFormSet(request.POST, queryset=detalles)
            if formset.is_valid() and form.is_valid():
                formset.save()
                firma = form.save(commit=False)
                for psd in detalles:
                    for exist in existencia:
                            if psd.producto.codigo == exist.producto.codigo:
                                rex = (psd.cantidad_entregada / exist.fondo_fijo) * 100
                                exist.porciento = math.fabs(rex - exist.porciento)
                                exist.todo -= psd.cantidad_entregada
                                exist.save()
                                psd.importe = psd.cantidad_entregada * psd.producto.precio
                                psd.saldo = int(exist.todo)
                                redondeo += psd.importe
                                psd.save()
                firma.importe_total = redondeo.__round__(2)
                firma.fecha_hora = datetime.now()
                firma.save()
                return redirect('pedidosSala')
    return render(request, 'despachar-pedido-sala.html', {'formset': formset, 'form': form})


@login_required
def despachar_devuelto_sala(request, id_ds):
    devuelto_sala = DevueltoSala.objects.get(id=id_ds)
    if devuelto_sala.recibida_por != "":
        return redirect('ver_despacho_devuelto_sala', devuelto_sala.pk)
    pg = PermisoGlobal.objects.first()
    if not request.user in pg.farmacia.all():
        raise PermissionDenied
    else:
        redondeo = 0
        existencia = Existencia.objects.all()
        devuelto_sala = DevueltoSala.objects.get(id=id_ds)
        detalles = DevueltoSalaDetalle.objects.filter(devuelto_sala__id=id_ds)
        form = DespachoFirmaDevueltoForm(instance=devuelto_sala)
        formset = DevueltoSalaEntregadoFormSet(queryset=detalles)
        if request.method == "POST":
            form = DespachoFirmaDevueltoForm(request.POST, instance=devuelto_sala)
            formset = DevueltoSalaEntregadoFormSet(request.POST, queryset=detalles)
            if formset.is_valid() and form.is_valid():
                formset.save()
                firma = form.save(commit=False)
                for dsd in detalles:
                        for exist in existencia:
                            if dsd.producto.codigo == exist.producto.codigo:
                                suma = dsd.cantidad_confirmada + exist.todo
                                if suma > exist.fondo_fijo:
                                    exist.todo = suma
                                    exist.fondo_fijo = suma
                                    exist.porciento = 100
                                    exist.save()
                                    dsd.importe = dsd.cantidad_confirmada * dsd.producto.precio
                                    dsd.saldo = int(exist.todo)
                                    redondeo += dsd.importe
                                    dsd.save()
                                else:
                                    rex = (dsd.cantidad_confirmada / exist.fondo_fijo) * 100
                                    exist.porciento = math.fabs(rex + exist.porciento)
                                    exist.todo += dsd.cantidad_confirmada
                                    exist.save()
                                    dsd.importe = dsd.cantidad_confirmada * dsd.producto.precio
                                    dsd.saldo = int(exist.todo)
                                    redondeo += dsd.importe
                                    dsd.save()
                firma.importe_total = redondeo.__round__(2)
                firma.fecha_hora = datetime.now()
                firma.save()
                return redirect('devolucionesSala')
    return render(request, 'despachar-devuelto-sala.html', {'formset': formset, 'form': form})


@login_required
def pedidos_cama_relacionados(request, id_ps):
    psd = PedidoSalaDetalle.objects.select_related().filter(pedido_sala=id_ps)
    pc = PedidoCama.objects.select_related().filter(pedido_sala_detalle__in=psd)
    return render(request, 'pedidos-cama-relacionados.html', locals())


@login_required
def devueltos_cama_relacionados(request, id_ds):
    dsd = DevueltoSalaDetalle.objects.select_related().filter(devuelto_sala=id_ds)
    d = DevueltoCama.objects.select_related().filter(devuelto_sala_detalle__in=dsd)
    return render(request, 'devueltos-cama-relacionados.html', locals())


@login_required
def pedidosSala(request):
    pg = PermisoGlobal.objects.first()
    if not request.user in pg.farmacia.all():
        raise PermissionDenied
    else:
        peds = PedidoSala.objects.filter(despachado_por="")
    return render(request, 'pedidosSala.html', locals())


@login_required
def devolucionesSala(request):
    pg = PermisoGlobal.objects.first()
    if not request.user in pg.farmacia.all():
        raise PermissionDenied
    else:
        devs = DevueltoSala.objects.filter(recibida_por="")
    return render(request, 'devolucionesSala.html', locals())


@login_required
def eliminar_pedido_sala(request, id_peds):
    pg = PermisoGlobal.objects.first()
    if not request.user in pg.farmacia.all():
        raise PermissionDenied
    else:
        peds_temp = PedidoSala.objects.get(id=id_peds)
        peds_temp.delete()
    return redirect('pedidosSala')


@login_required
def eliminar_devolucion_sala(request, id_devs):
    pg = PermisoGlobal.objects.first()
    if not request.user in pg.farmacia.all():
        raise PermissionDenied
    else:
        devs_temp = DevueltoSala.objects.get(id=id_devs)
        devs_temp.delete()
    return redirect('devolucionesSala')


@login_required
def ver_despacho_pedido_sala(request, id_ps):
    peds = PedidoSala.objects.get(id=id_ps)
    psd = PedidoSalaDetalle.objects.select_related().filter(pedido_sala=peds)
    return render(request, 'ver-despacho-pedido-sala.html', locals())


@login_required
def ver_despacho_devuelto_sala(request, id_ds):
    devs = DevueltoSala.objects.get(id=id_ds)
    dsd = DevueltoSalaDetalle.objects.select_related().filter(devuelto_sala=devs)
    return render(request, 'ver-despacho-devuelto-sala.html', locals())


@login_required
def baja_cobertura(request):
    pg = PermisoGlobal.objects.first()
    if pg.jefe_farmacia != request.user:
        raise PermissionDenied
    else:
        detalles = {}
        baja_cobertura = Existencia.objects.filter(porciento__lte=50)
        for bc in baja_cobertura.values('producto', 'fondo_fijo', 'todo'):
            pro = Producto.objects.get(id=bc['producto'])
            faltante = bc['fondo_fijo'] - bc['todo']
            detalles[pro] = faltante
    return render(request, 'baja-cobertura.html', locals())


@login_required
def solicitar_pedido_farmacia(request):
    pg = PermisoGlobal.objects.first()
    if pg.jefe_farmacia != request.user:
        raise PermissionDenied
    else:
        detalles = {}
        nombre_user = request.user
        baja_cobertura = Existencia.objects.filter(porciento__lte=50)
        pa = PedidoAlmacen.objects.filter(recibido_por="")
        if pa:
            pad = PedidoAlmacenDetalle.objects.select_related().filter(pedido_almacen__in=pa)
            for p in pad:
                for b in baja_cobertura:
                    if p.producto.codigo == b.producto.codigo:
                        cantidad_ex = b.fondo_fijo - b.todo
                        resta = p.cantidad_enviada - cantidad_ex
                        resta = math.fabs(resta)
                        if resta != 0:
                             detalles.setdefault(b.producto, [0, []])
                             detalles[b.producto][0] = resta
                             detalles[b.producto][1].append(b)
                            #todo: no mandar planilla vacia
                    else:
                        cantidad_enviada = b.fondo_fijo - b.todo
                        detalles.setdefault(b.producto, [0, []])
                        detalles[b.producto][0] = cantidad_enviada
                        detalles[b.producto][1].append(b)
            pedido_almacen = PedidoAlmacen.objects.create(fecha_hora=datetime.now(), entregado_por=nombre_user.first_name + " " + nombre_user.last_name)
            for producto, data in detalles.items():
                cantidad, pedidos_farmacia = data
                PedidoAlmacenDetalle.objects.create(
                    pedido_almacen=pedido_almacen,
                    producto=producto,
                    cantidad_enviada=cantidad,
            )

        else:
            for pedido_farmacia in baja_cobertura.values('producto', 'fondo_fijo', 'todo'):
                producto = Producto.objects.get(id=pedido_farmacia['producto'])
                cantidad_enviada = pedido_farmacia['fondo_fijo'] - pedido_farmacia['todo']
                detalles.setdefault(producto, [0, []])
                detalles[producto][0] += cantidad_enviada
                detalles[producto][1].append(pedido_farmacia)
            pedido_almacen = PedidoAlmacen.objects.create(fecha_hora=datetime.now(), entregado_por=nombre_user.first_name + " " + nombre_user.last_name)
            for producto, data in detalles.items():
                cantidad, pedidos_farmacia = data
                PedidoAlmacenDetalle.objects.create(
                    pedido_almacen=pedido_almacen,
                    producto=producto,
                    cantidad_enviada=cantidad,
            )
    return redirect('baja_cobertura')


@login_required
def despachar_pedido_farmacia(request, id_pf):
    pedido_almacen = PedidoAlmacen.objects.get(id=id_pf)
    if pedido_almacen.recibido_por != "":
        return redirect('ver_despacho_pedido_farmacia', pedido_almacen.pk)
    pg = PermisoGlobal.objects.first()
    if pg.almacen != request.user:
        raise PermissionDenied
    else:
        redondeo = 0
        redondeo1 = 0
        existencia = Existencia.objects.all()
        pedido_almacen = PedidoAlmacen.objects.get(id=id_pf)
        detalles = PedidoAlmacenDetalle.objects.filter(pedido_almacen__id=id_pf)
        form = DespachoFirmaPedidoAlmacenForm(instance=pedido_almacen)
        formset = PedidoAlmacenEntregadoFormSet(queryset=detalles)
        if request.method == "POST":
            form = DespachoFirmaPedidoAlmacenForm(request.POST, instance=pedido_almacen)
            formset = PedidoAlmacenEntregadoFormSet(request.POST, queryset=detalles)
            if formset.is_valid() and form.is_valid():
                formset.save()
                firma = form.save(commit=False)
                for dsd in detalles:
                        for exist in existencia:
                            if dsd.producto.codigo == exist.producto.codigo:
                                suma = dsd.cantidad_recibida + exist.todo
                                if suma > exist.fondo_fijo:
                                    exist.todo = suma
                                    exist.fondo_fijo = suma
                                    exist.porciento = 100
                                    exist.save()
                                    dsd.importe_recibida = dsd.cantidad_recibida * dsd.producto.precio
                                    dsd.importe_enviada = dsd.cantidad_enviada * dsd.producto.precio
                                    dsd.saldo = int(exist.todo)
                                    redondeo += dsd.importe_recibida
                                    redondeo1 += dsd.importe_enviada
                                    dsd.save()
                                else:
                                    rex = (dsd.cantidad_recibida / exist.fondo_fijo) * 100
                                    exist.porciento = math.fabs(rex + exist.porciento)
                                    exist.todo += dsd.cantidad_recibida
                                    exist.save()
                                    dsd.importe_recibida = dsd.cantidad_recibida * dsd.producto.precio
                                    dsd.importe_enviada = dsd.cantidad_enviada * dsd.producto.precio
                                    dsd.saldo = int(exist.todo)
                                    redondeo += dsd.importe_recibida
                                    redondeo1 += dsd.importe_enviada
                                    dsd.save()
                firma.importe_recibida_total = redondeo.__round__(2)
                firma.importe_enviada_total = redondeo1.__round__(2)
                firma.fecha_hora = datetime.now()
                firma.save()
                return redirect('pedidosAlmacen')
    return render(request, 'despachar-pedido-farmacia.html', {'formset': formset, 'form': form})


@login_required
def pedidosAlmacen(request):
    pg = PermisoGlobal.objects.first()
    if pg.almacen != request.user:
        raise PermissionDenied
    else:
        pedf = PedidoAlmacen.objects.filter(recibido_por="")
    return render(request, 'pedidosAlmacen.html', locals())


@login_required
def eliminar_pedido_farmacia(request, id_pedf):
    pg = PermisoGlobal.objects.first()
    if pg.almacen != request.user:
        raise PermissionDenied
    else:
        pedf_temp = PedidoAlmacen.objects.get(id=id_pedf)
        pedf_temp.delete()
    return redirect('pedidosAlmacen')


@login_required
def agregar_producto_almacen(request):
    pg = PermisoGlobal.objects.first()
    if pg.jefe_farmacia != request.user:
        raise PermissionDenied
    else:
        productos = Producto.objects.filter(existencia__todo__gt=0)
        form = DevueltoFarmaciaForm()
        if request.method == "POST":
            form = DevueltoFarmaciaForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('agregar_producto_almacen')
    return render(request, 'agregar-producto-almacen.html', locals())


@login_required
def editar_producto_almacen(request, id_df):
    pg = PermisoGlobal.objects.first()
    if pg.jefe_farmacia != request.user:
        raise PermissionDenied
    else:
        productos = Producto.objects.filter(existencia__todo__gt=0)
        ddf = get_object_or_404(DevueltoFarmacia, id=id_df)
        form = DevueltoFarmaciaForm(instance=ddf)
        if request.method == "POST":
            form = DevueltoFarmaciaForm(request.POST, instance=ddf)
            if form.is_valid():
                form.save()
                return redirect('devolucionesFarmacia')
    return render(request, 'editar-producto-almacen.html', locals())


@login_required
def devolucionesFarmacia(request):
    pg = PermisoGlobal.objects.first()
    if pg.jefe_farmacia != request.user:
        raise PermissionDenied
    else:
        ddf = DevueltoFarmacia.objects.filter(devuelto_almacen_detalle=None)
    return render(request, 'devolucionesFarmacia.html', locals())


@login_required
def eliminar_producto_almacen(request, id_df):
    pg = PermisoGlobal.objects.first()
    if pg.jefe_farmacia != request.user:
        raise PermissionDenied
    else:
        dev_almacen_temp = DevueltoFarmacia.objects.get(id=id_df)
        dev_almacen_temp.delete()
    return redirect('devolucionesFarmacia')


@login_required
def solicitar_devuelto_farmacia(request):
    pg = PermisoGlobal.objects.first()
    if pg.jefe_farmacia != request.user:
        raise PermissionDenied
    else:
        devueltos_farmacia_pendientes = DevueltoFarmacia.objects.filter(devuelto_almacen_detalle=None)
        detalles = {}
        nombre_user = request.user
        for devuelto_farmacia in devueltos_farmacia_pendientes:
            detalles.setdefault(devuelto_farmacia.producto, [0, []])
            detalles[devuelto_farmacia.producto][0] += devuelto_farmacia.cantidad_enviada
            detalles[devuelto_farmacia.producto][1].append(devuelto_farmacia)
        devuelto_almacen = DevueltoAlmacen.objects.create(fecha_hora=datetime.now(), entregado_por=nombre_user.first_name + " " + nombre_user.last_name)
        for producto, data in detalles.items():
            cantidad, devueltos_farmacia = data
            devuelto_almacen_detalle = DevueltoAlmacenDetalle.objects.create(
                devuelto_almacen=devuelto_almacen,
                producto=producto,
                cantidad_enviada=cantidad,
            )
            for devuelto_farmacia in devueltos_farmacia:
                devuelto_farmacia.devuelto_almacen_detalle = devuelto_almacen_detalle
                devuelto_farmacia.save()
    return redirect('devolucionesFarmacia')


@login_required
def despachar_devuelto_farmacia(request, id_df):
    devuelto_almacen = DevueltoAlmacen.objects.get(id=id_df)
    if devuelto_almacen.recibido_por != "":
        return redirect('ver_despacho_devuelto_farmacia', devuelto_almacen.pk)
    pg = PermisoGlobal.objects.first()
    if pg.almacen != request.user:
        raise PermissionDenied
    else:
        redondeo = 0
        redondeo1 = 0
        existencia = Existencia.objects.all()
        devuelto_almacen = DevueltoAlmacen.objects.get(id=id_df)
        detalles = DevueltoAlmacenDetalle.objects.filter(devuelto_almacen__id=id_df)
        form = DespachoFirmaDevueltoAlmacenForm(instance=devuelto_almacen)
        formset = DevueltoAlmacenEntregadoFormSet(queryset=detalles)
        if request.method == "POST":
            form = DespachoFirmaDevueltoAlmacenForm(request.POST, instance=devuelto_almacen)
            formset = DevueltoAlmacenEntregadoFormSet(request.POST, queryset=detalles)
            if formset.is_valid() and form.is_valid():
                formset.save()
                firma = form.save(commit=False)
                for dsd in detalles:
                        for exist in existencia:
                            if dsd.producto.codigo == exist.producto.codigo:
                                rex = (dsd.cantidad_recibida / exist.fondo_fijo) * 100
                                exist.porciento = math.fabs(rex - exist.porciento)
                                exist.todo -= dsd.cantidad_recibida
                                exist.save()
                                dsd.importe_recibida = dsd.cantidad_recibida * dsd.producto.precio
                                dsd.importe_enviada = dsd.cantidad_enviada * dsd.producto.precio
                                dsd.saldo = int(exist.todo)
                                redondeo += dsd.importe_recibida
                                redondeo1 += dsd.importe_enviada
                                dsd.save()
                firma.importe_recibida_total = redondeo.__round__(2)
                firma.importe_enviada_total = redondeo1.__round__(2)
                firma.fecha_hora = datetime.now()
                firma.save()
                return redirect('devolucionesAlmacen')
    return render(request, 'despachar-devuelto-farmacia.html', {'formset': formset, 'form': form})


@login_required
def devolucionesAlmacen(request):
    pg = PermisoGlobal.objects.first()
    if pg.almacen != request.user:
        raise PermissionDenied
    else:
        devf = DevueltoAlmacen.objects.filter(recibido_por="")
    return render(request, 'devolucionesAlmacen.html', locals())


@login_required
def eliminar_devolucion_farmacia(request, id_devf):
    pg = PermisoGlobal.objects.first()
    if pg.almacen != request.user:
        raise PermissionDenied
    else:
        devf_temp = DevueltoAlmacen.objects.get(id=id_devf)
        devf_temp.delete()
    return redirect('devolucionesAlmacen')


@login_required
def ver_despacho_pedido_farmacia(request, id_pf):
    pedf = PedidoAlmacen.objects.get(id=id_pf)
    pfd = PedidoAlmacenDetalle.objects.select_related().filter(pedido_almacen=pedf)
    return render(request, 'ver-despacho-pedido-farmacia.html', locals())


@login_required
def ver_despacho_devuelto_farmacia(request, id_df):
    devf = DevueltoAlmacen.objects.get(id=id_df)
    dfd = DevueltoAlmacenDetalle.objects.select_related().filter(devuelto_almacen=devf)
    return render(request, 'ver-despacho-devuelto-farmacia.html', locals())


@login_required
def agregar_producto(request):
    pg = PermisoGlobal.objects.first()
    if pg.jefe_farmacia != request.user:
        raise PermissionDenied
    else:
        presentacion = Presentacion.objects.all()
        unidadMed = UnidadMedida.objects.all()
        form = ProductoForm()
        if request.method == "POST":
            form = ProductoForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('agregar_producto')
    return render(request, 'agregar-producto.html', locals())


@login_required
def editar_producto(request, id_p):
    pg = PermisoGlobal.objects.first()
    if pg.jefe_farmacia != request.user and pg.jefe_contabilidad != request.user:
        raise PermissionDenied
    else:
        presentacion = Presentacion.objects.all()
        unidadMed = UnidadMedida.objects.all()
        producto = get_object_or_404(Producto, id=id_p)
        form = ProductoForm(instance=producto)
        if request.method == "POST":
            form = ProductoForm(request.POST, instance=producto)
            if form.is_valid():
                form.save()
                return redirect('producto')
    return render(request, 'editar-producto.html', locals())


@login_required
def eliminar_producto(request, id_p):
    pg = PermisoGlobal.objects.first()
    if pg.jefe_farmacia != request.user:
        raise PermissionDenied
    else:
        p_temp = Producto.objects.get(id=id_p)
        p_temp.delete()
    return redirect('producto')


@login_required
def producto(request):
    pg = PermisoGlobal.objects.first()
    if pg.jefe_farmacia != request.user and pg.jefe_contabilidad != request.user:
        raise PermissionDenied
    else:
        p = Producto.objects.all()
    return render(request, 'productos.html', locals())


@login_required
def agregar_justificacion(request, id_c):
    pg = PermisoGlobal.objects.first()
    if not request.user in pg.secretaria_sala.all():
        raise PermissionDenied
    else:
        form = JustificacionForm()
        if request.method == "POST":
            fkcama = Cama.objects.get(id=id_c)
            form = JustificacionForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('agregar_devuelto_cama', fkcama.pk)
    return render(request, 'agregar-justificacion.html', locals())


@login_required
def editar_justificacion(request, id_jus, id_c):
    pg = PermisoGlobal.objects.first()
    if not request.user in pg.secretaria_sala.all():
        raise PermissionDenied
    else:
        justificacion = get_object_or_404(Justificacion, id=id_jus)
        form = JustificacionForm(instance=justificacion)
        if request.method == "POST":
            fkcama = Cama.objects.get(id=id_c)
            form = JustificacionForm(request.POST, instance=justificacion)
            if form.is_valid():
                form.save()
                return redirect('agregar_devuelto_cama', fkcama.pk)
    return render(request, 'editar-justificacion.html', locals())


@login_required
def agregar_presentacion(request):
    pg = PermisoGlobal.objects.first()
    if not request.user in pg.farmacia.all():
        raise PermissionDenied
    else:
        form = PresentacionForm()
        if request.method == "POST":
            form = PresentacionForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('agregar_producto')
    return render(request, 'agregar-presentacion.html', locals())


@login_required
def editar_presentacion(request, id_pre):
    pg = PermisoGlobal.objects.first()
    if not request.user in pg.farmacia.all():
        raise PermissionDenied
    else:
        presentacion = get_object_or_404(Presentacion, id=id_pre)
        form = PresentacionForm(instance=presentacion)
        if request.method == "POST":
            form = PresentacionForm(request.POST, instance=presentacion)
            if form.is_valid():
                form.save()
                return redirect('agregar_producto')
    return render(request, 'editar-presentacion.html', locals())


@login_required
def agregar_unidad_medida(request):
    pg = PermisoGlobal.objects.first()
    if not request.user in pg.farmacia.all():
        raise PermissionDenied
    else:
        form = UnidadMedidaForm()
        if request.method == "POST":
            form = UnidadMedidaForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('agregar_producto')
    return render(request, 'agregar-unidad-medida.html', locals())


@login_required
def editar_unidad_medida(request, id_um):
    pg = PermisoGlobal.objects.first()
    if not request.user in pg.farmacia.all():
        raise PermissionDenied
    else:
        unid_med = get_object_or_404(UnidadMedida, id=id_um)
        form = UnidadMedidaForm(instance=unid_med)
        if request.method == "POST":
            form = UnidadMedidaForm(request.POST, instance=unid_med)
            if form.is_valid():
                form.save()
                return redirect('agregar_producto')
    return render(request, 'editar-unidad-medida.html', locals())


@login_required
def agregar_cama(request):
    pg = PermisoGlobal.objects.first()
    if not request.user in pg.secretaria_sala.all():
        raise PermissionDenied
    else:
        form = CamaForm()
        if request.method == "POST":
            fksala = Sala.objects.get(secretaria=request.user)
            form = CamaForm(request.POST)
            if form.is_valid():
                add_cama = form.save(commit=False)
                add_cama.sala = fksala
                add_cama.num_cama = Cama.objects.filter(sala__secretaria=request.user).count() + 1
                add_cama.fecha_hora = datetime.now()
                add_cama.save()
                return redirect('cama')
    return render(request, 'agregar-cama.html', locals())


@login_required
def editar_cama(request, id_c):
    pg = PermisoGlobal.objects.first()
    if not request.user in pg.secretaria_sala.all():
        raise PermissionDenied
    else:
        cama = get_object_or_404(Cama, id=id_c)
        form = CamaForm(instance=cama)
        if request.method == "POST":
            form = CamaForm(request.POST, instance=cama)
            if form.is_valid():
                form.save()
                return redirect('cama')
    return render(request, 'editar-cama.html', locals())


@login_required
def eliminar_cama(request):
    pg = PermisoGlobal.objects.first()
    if not request.user in pg.secretaria_sala.all():
        raise PermissionDenied
    else:
        camas = Cama.objects.filter(sala__secretaria=request.user).order_by('num_cama').last()
        camas.delete()
    return redirect('cama')


@login_required
def cama_unico(request, id_c):
    pg = PermisoGlobal.objects.first()
    if not request.user in pg.secretaria_sala.all():
        raise PermissionDenied
    else:
        c = Cama.objects.get(id=id_c)
    return render(request, 'cama-unico.html', locals())


@login_required
def cama(request):
    pg = PermisoGlobal.objects.first()
    if not request.user in pg.secretaria_sala.all():
        raise PermissionDenied
    else:
        s = Sala.objects.get(secretaria=request.user)
        c = Cama.objects.filter(sala__secretaria=request.user)
    return render(request, 'camas.html', locals())


@login_required
def agregar_pedido_cama(request, id_c):
    pg = PermisoGlobal.objects.first()
    if not request.user in pg.secretaria_sala.all():
        raise PermissionDenied
    else:
        cama = Cama.objects.get(id=id_c)
        productos = Producto.objects.filter(existencia__todo__gt=0)
        form = PedidoCamaForm()
        if request.method == "POST":
            fkcama = Cama.objects.get(id=id_c)
            form = PedidoCamaForm(request.POST)
            if form.is_valid():
                add_ped = form.save(commit=False)
                add_ped.cama = fkcama
                add_ped.save()
                return redirect('agregar_pedido_cama', fkcama.pk)
    return render(request, 'agregar-pedido-cama.html', locals())


@login_required
def editar_pedido_cama(request, id_pc):
    pg = PermisoGlobal.objects.first()
    if not request.user in pg.secretaria_sala.all():
        raise PermissionDenied
    else:
        productos = Producto.objects.filter(existencia__todo__gt=0)
        pdc = get_object_or_404(PedidoCama, id=id_pc)
        form = PedidoCamaForm(instance=pdc)
        if request.method == "POST":
            form = PedidoCamaForm(request.POST, instance=pdc)
            if form.is_valid():
                form.save()
                return redirect('pedidosCama')
    return render(request, 'editar-pedido-cama.html', locals())


@login_required
def pedidosCama(request):
    pg = PermisoGlobal.objects.first()
    if not request.user in pg.secretaria_sala.all():
        raise PermissionDenied
    else:
        ca = Cama.objects.filter(sala__secretaria=request.user)
        pc = PedidoCama.objects.select_related().filter(cama__in=ca)
        pc = pc.filter(pedido_sala_detalle=None)
    return render(request, 'pedidosCama.html', locals())


@login_required
def eliminar_pedido_cama(request, id_pc):
    pg = PermisoGlobal.objects.first()
    if not request.user in pg.secretaria_sala.all():
        raise PermissionDenied
    else:
        ped_cama_temp = PedidoCama.objects.get(id=id_pc)
        ped_cama_temp.delete()
    return redirect('pedidosCama')


@login_required
def agregar_devuelto_cama(request, id_c):
    pg = PermisoGlobal.objects.first()
    if not request.user in pg.secretaria_sala.all():
        raise PermissionDenied
    else:
        cama = Cama.objects.get(id=id_c)
        just = Justificacion.objects.all()
        form = DevueltoCamaForm()
        productos = Producto.objects.filter(existencia__todo__gt=0)
        if request.method == "POST":
            fkcama = Cama.objects.get(id=id_c)
            form = DevueltoCamaForm(request.POST)
            if form.is_valid():
                add_dev = form.save(commit=False)
                add_dev.cama = fkcama
                add_dev.save()
                return redirect('agregar_devuelto_cama', fkcama.pk)
    return render(request, 'agregar-devuelto-cama.html', locals())


@login_required
def editar_devuelto_cama(request, id_d):
    pg = PermisoGlobal.objects.first()
    if not request.user in pg.secretaria_sala.all():
        raise PermissionDenied
    else:
        productos = Producto.objects.filter(existencia__todo__gt=0)
        dev = get_object_or_404(DevueltoCama, id=id_d)
        form = DevueltoCamaForm(instance=dev)
        if request.method == "POST":
            form = DevueltoCamaForm(request.POST, instance=dev)
            if form.is_valid():
                form.save()
                return redirect('devueltosCama')
    return render(request, 'editar-devuelto-cama.html', locals())


@login_required
def devueltosCama(request):
    pg = PermisoGlobal.objects.first()
    if not request.user in pg.secretaria_sala.all():
        raise PermissionDenied
    else:
        ca = Cama.objects.filter(sala__secretaria=request.user)
        d = DevueltoCama.objects.select_related().filter(cama__in=ca)
        d = d.filter(devuelto_sala_detalle=None)
    return render(request, 'devueltosCama.html', locals())


@login_required
def eliminar_devuelto_cama(request, id_d):
    pg = PermisoGlobal.objects.first()
    if not request.user in pg.secretaria_sala.all():
        raise PermissionDenied
    else:
        dev_temp = DevueltoCama.objects.get(id=id_d)
        dev_temp.delete()
    return redirect('devueltosCama')


def aa(canvas, doc):
    import os
    canvas.saveState()
    image = os.path.join(settings.STATICFILES_DIRS[0], 'image', 'Artboard 5.jpg')
    canvas.drawImage(image, 0, 710, 90, 90)
    canvas.restoreState()


def bb(canvas, doc):
    import os
    canvas.saveState()
    image = os.path.join(settings.STATICFILES_DIRS[0], 'image', 'Artboard 5.jpg')
    canvas.drawImage(image, 0, 530, 90, 90)
    canvas.restoreState()


class ReporteProductoPDF(View):

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename = productos.pdf'
        document = SimpleDocTemplate(response, pagesize=pagesizes.portrait(pagesizes.LETTER),)
        story =[]
        story.append(self.tabla())
        document.build(story, onFirstPage=aa, onLaterPages=aa)
        return response

    def tabla(self):
        titulo = ['PRODUCTOS', '', '', '', '', '']
        encabezados = ('NOMBRE', 'DOSIS', 'UM', 'UNIDAD', 'CÓDIGO', 'PRECIO')
        detalles = [(producto.nombre, producto.dosis, producto.unidad_medida, producto.unidad, producto.codigo, producto.precio) for producto in Producto.objects.all()]
        detalle_orden = Table([titulo] + [encabezados] + detalles)
        detalle_orden.setStyle(TableStyle([
            ('ALIGN', (0, 0), (3, 0), 'CENTER'),
            ('SPAN', (0, 0), (5, 0)),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
        ]))
        return detalle_orden


class ReporteSalaPDF(View):

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename = servicios.pdf'
        document = SimpleDocTemplate(response, pagesize=pagesizes.portrait(pagesizes.LETTER),)
        story = []

        story.append(self.tabla())
        document.build(story, onFirstPage=aa, onLaterPages=aa)
        return response

    def tabla(self):
        titulo = ['SERVICIOS', '', '', '']
        encabezados = ('SERVICIO', 'SALA', 'CENTRO DE COSTO', 'SECRETARIA')
        detalles = [(sala.servicio, sala.apodo, sala.centro_costo, sala.secretaria) for sala in Sala.objects.all()]
        detalle_orden = Table([titulo] + [encabezados] + detalles)
        detalle_orden.setStyle(TableStyle([
            ('ALIGN', (0, 0), (3, 0), 'CENTER'),
            ('SPAN', (0, 0), (3, 0)),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
        ]))
        return detalle_orden


class ReportePedidoCamaPDF(View):

    def get(self, request, id_ps):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename = pedidos de cama.pdf'
        document = SimpleDocTemplate(response, pagesize=pagesizes.landscape(pagesizes.LETTER),)
        story = []

        story.append(self.tabla(id_ps))
        document.build(story, onFirstPage=bb, onLaterPages=bb)
        return response

    def tabla(self, id_ps):
        titulo = ['PEDIDO', '', '', '', '', '', '']
        encabezados = ('CAMA No.', 'HISTORIA CLÍNICA', 'PRODUCTO', 'DOSIS', 'UNIDAD', 'CANTIDAD', 'MÉDICO')
        psd = PedidoSalaDetalle.objects.select_related().filter(pedido_sala=id_ps)
        p = PedidoCama.objects.select_related().filter(pedido_sala_detalle__in=psd)
        detalles = [(pc.cama.num_cama, pc.cama.historia_clinica, pc.producto, pc.producto.dosis, pc.producto.unidad, pc.cantidad_solicitada, pc.medico) for pc in p]
        detalle_orden = Table([titulo] + [encabezados] + detalles)
        detalle_orden.setStyle(TableStyle([
            ('ALIGN', (0, 0), (3, 0), 'CENTER'),
            ('SPAN', (0, 0), (6, 0)),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
        ]))
        return detalle_orden


class ReporteDevueltoCamaPDF(View):

    def get(self, request, id_ds):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename = devoluciones de cama.pdf'
        document = SimpleDocTemplate(response, pagesize=pagesizes.landscape(pagesizes.LETTER),)
        story = []

        story.append(self.tabla(id_ds))
        document.build(story, onFirstPage=bb, onLaterPages=bb)
        return response

    def tabla(self, id_ds):
        titulo = ['DEVOLUCIÓN', '', '', '', '', '', '', '']
        encabezados = ('CAMA No.', 'HISTORIA CLÍNICA', 'PRODUCTO', 'DOSIS', 'UNIDAD', 'CANTIDAD', 'JUSTIFICACIÓN', 'MÉDICO')
        dsd = DevueltoSalaDetalle.objects.select_related().filter(devuelto_sala=id_ds)
        d = DevueltoCama.objects.select_related().filter(devuelto_sala_detalle__in=dsd)
        detalles = [(dd.cama.num_cama, dd.cama.historia_clinica, dd.producto, dd.producto.dosis, dd.producto.unidad, dd.cantidad_devuelta, dd.justificacion, dd.medico) for dd in d]
        detalle_orden = Table([titulo] + [encabezados] + detalles)
        detalle_orden.setStyle(TableStyle([
            ('ALIGN', (0, 0), (3, 0), 'CENTER'),
            ('SPAN', (0, 0), (7, 0)),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
        ]))
        return detalle_orden


class ReportePedidoSalaPDF(View):

    def get(self, request, id_ps):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename = pedido de sala.pdf'
        document = SimpleDocTemplate(response, pagesize=pagesizes.landscape(pagesizes.LETTER),)
        story = []

        story.append(self.tabla(id_ps))
        document.build(story, onFirstPage=bb, onLaterPages=bb)
        return response

    def tabla(self, id_ps):
        peds = PedidoSala.objects.get(id=id_ps)
        encabezados = [['MOD 17-24 MINISTERIO DE SALUD PÚBLICA. CONTROL', '', 'PEDIDO DE SALA', '', '', '', '', 'FECHA:' + '%s' % date_format(timezone.localtime(peds.fecha_hora), settings.SHORT_DATETIME_FORMAT), '', ''],
                       ['UNIDAD: H.U.C.Q  "Lucía Íñiguez Landín"', '', '', '', '', '', '', 'CENTRO DE COSTO:' + '%s' % peds.sala.centro_costo, '', ''],
                       ['RESUMEN DEL PEDIDO', '', '', '', '', '', '', '', '', ''],
                       ['CÓDIGO', 'PRODUCTO', 'DOSIS', 'UM', 'UNIDAD', 'CANTIDAD', '', 'PRECIO', 'IMPORTE', 'SALDO'],
                       ['', '', '', '', '', 'SOLICIT.', 'ENTREG.', '', '', '']]
        psd = PedidoSalaDetalle.objects.select_related().filter(pedido_sala=peds)
        detalles = [(p.producto.codigo, p.producto.nombre, p.producto.dosis, p.producto.unidad_medida, p.producto.unidad, p.cantidad_solicitada,  p.cantidad_entregada, p.producto.precio, p.importe, p.saldo) for p in psd]
        detalles1 = [['SALA:' + '%s' % peds.sala.servicio, '', 'TOTAL', '', '', '', '', '', peds.importe_total, '']]
        firmas = [['Solicitado por:' + peds.solicitado_por, '', 'Aprobado por:' + peds.aprobado_por, '',  'Despachado por:' + peds.despachado_por, '', 'Recibido por:' + peds.recibido_por, '', 'No.' + '%s' % peds.id, '']]
        detalle_orden = Table(encabezados + detalles + detalles1 + firmas)
        detalle_orden.setStyle(TableStyle([
            ('ALIGN', (0, 0), (3, 0), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('SPAN', (0, 0), (1, 0)),
            ('SPAN', (0, 1), (1, 1)),
            ('SPAN', (2, 0), (6, 1)),
            ('SPAN', (7, 0), (9, 0)),
            ('SPAN', (7, 1), (9, 1)),
            ('SPAN', (0, 2), (9, 2)),
            ('ALIGN', (0, 2), (9, 2), 'CENTER'),
            ('SPAN', (5, 3), (6, 3)),
            ('ALIGN', (5, 3), (6, 3), 'CENTER'),
            ('SPAN', (0, 3), (0, 4)),
            ('ALIGN', (0, 3), (0, 4), 'CENTER'),
            ('SPAN', (1, 3), (1, 4)),
            ('ALIGN', (1, 3), (1, 4), 'CENTER'),
            ('SPAN', (2, 3), (3, 4)),
            ('ALIGN', (2, 3), (3, 4), 'CENTER'),
            ('SPAN', (4, 3), (4, 4)),
            ('ALIGN', (4, 3), (4, 4), 'CENTER'),
            ('SPAN', (7, 3), (7, 4)),
            ('ALIGN', (7, 3), (7, 4), 'CENTER'),
            ('SPAN', (8, 3), (8, 4)),
            ('ALIGN', (8, 3), (8, 4), 'CENTER'),
            ('SPAN', (9, 3), (9, 4)),
            ('ALIGN', (9, 3), (9, 4), 'CENTER'),
            ('SPAN', (-2, -1), (-1, -1)),
            ('SPAN', (-4, -1), (-3, -1)),
            ('SPAN', (-6, -1),  (-5, -1)),
            ('SPAN', (-8, -1), (-7, -1)),
            ('SPAN', (-10, -1), (-9, -1)),
            ('SPAN', (-10, -2), (-9, -2)),
            ('SPAN', (-8, -2), (-3, -2)),
            ('ALIGN', (-8, -2), (-3, -2), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
        ]))
        return detalle_orden


class ReporteDevueltoSalaPDF(View):

    def get(self, request, id_ds):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename = devolución de sala.pdf'
        document = SimpleDocTemplate(response, pagesize=pagesizes.landscape(pagesizes.LETTER),)
        story = []

        story.append(self.tabla(id_ds))
        document.build(story, onFirstPage=bb, onLaterPages=bb)
        return response

    def tabla(self, id_ds):
        devs = DevueltoSala.objects.get(id=id_ds)
        encabezados = [['MOD 17-24 MINISTERIO DE SALUD PÚBLICA. CONTROL', '', 'DEVOLUCIÓN DE SALA', '', '', '', '', 'FECHA:' + '%s' % date_format(timezone.localtime(devs.fecha_hora), settings.SHORT_DATETIME_FORMAT), '', ''],
                       ['UNIDAD: H.U.C.Q  "Lucía Íñiguez Landín"', '', '', '', '', '', '', 'CENTRO DE COSTO:' + '%s' % devs.sala.centro_costo, '', ''],
                       ['RESUMEN DE LA DEVOLUCIÓN', '', '', '', '', '', '', '', '', ''],
                       ['CÓDIGO', 'PRODUCTO', 'DOSIS', 'UM', 'UNIDAD', 'CANTIDAD', '', 'PRECIO', 'IMPORTE', 'SALDO'],
                       ['', '', '', '', '', 'DEVUELT.', 'CONFIRM.', '', '', '']]
        dsd = DevueltoSalaDetalle.objects.select_related().filter(devuelto_sala=devs)
        detalles = [(d.producto.codigo, d.producto.nombre, d.producto.dosis, d.producto.unidad_medida, d.producto.unidad, d.cantidad_devuelta, d.cantidad_confirmada, d.producto.precio, d.importe, d.saldo) for d in dsd]
        detalles1 = [['SALA:' + '%s' % devs.sala.servicio, '', 'TOTAL', '', '', '', '', '', devs.importe_total, '']]
        firmas = [['Devuelto por:' + devs.devuelta_por, '', 'Aprobado por:' + devs.aprobado_por, '', 'Despachado por:' + devs.despachado_por, '', 'Recibido por:' + devs.recibida_por, '', 'No.' + '%s' % devs.id, '']]
        detalle_orden = Table(encabezados + detalles + detalles1 + firmas)
        detalle_orden.setStyle(TableStyle([
            ('ALIGN', (0, 0), (3, 0), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('SPAN', (0, 0), (1, 0)),
            ('SPAN', (0, 1), (1, 1)),
            ('SPAN', (2, 0), (6, 1)),
            ('SPAN', (7, 0), (9, 0)),
            ('SPAN', (7, 1), (9, 1)),
            ('SPAN', (0, 2), (9, 2)),
            ('ALIGN', (0, 2), (9, 2), 'CENTER'),
            ('SPAN', (5, 3), (6, 3)),
            ('ALIGN', (5, 3), (6, 3), 'CENTER'),
            ('SPAN', (0, 3), (0, 4)),
            ('ALIGN', (0, 3), (0, 4), 'CENTER'),
            ('SPAN', (1, 3), (1, 4)),
            ('ALIGN', (1, 3), (1, 4), 'CENTER'),
            ('SPAN', (2, 3), (3, 4)),
            ('ALIGN', (2, 3), (3, 4), 'CENTER'),
            ('SPAN', (4, 3), (4, 4)),
            ('ALIGN', (4, 3), (4, 4), 'CENTER'),
            ('SPAN', (7, 3), (7, 4)),
            ('ALIGN', (7, 3), (7, 4), 'CENTER'),
            ('SPAN', (8, 3), (8, 4)),
            ('ALIGN', (8, 3), (8, 4), 'CENTER'),
            ('SPAN', (9, 3), (9, 4)),
            ('ALIGN', (9, 3), (9, 4), 'CENTER'),
            ('SPAN', (-2, -1), (-1, -1)),
            ('SPAN', (-4, -1), (-3, -1)),
            ('SPAN', (-6, -1),  (-5, -1)),
            ('SPAN', (-8, -1), (-7, -1)),
            ('SPAN', (-10, -1), (-9, -1)),
            ('SPAN', (-10, -2), (-9, -2)),
            ('SPAN', (-8, -2), (-3, -2)),
            ('ALIGN', (-8, -2), (-3, -2), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
        ]))
        return detalle_orden


class ReportePedidoAlmacenPDF(View):

    def get(self, request, id_pf):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename = solicitud de reposición.pdf'
        document = SimpleDocTemplate(response, pagesize=pagesizes.landscape(pagesizes.LETTER),)
        story = []

        story.append(self.tabla(id_pf))
        document.build(story, onFirstPage=bb, onLaterPages=bb)
        return response

    def tabla(self, id_pf):
        pedf = PedidoAlmacen.objects.get(id=id_pf)
        encabezados = [['MINSAP-SC-2-06 Y 9', '', 'TRANSFERENCIA ENTRE ALMACENES', '', '', '', '', 'FECHA:' + '%s' % date_format(timezone.localtime(pedf.fecha_hora), settings.SHORT_DATETIME_FORMAT), ''],
                       ['Entidad: Hospital Universitario Clínico Quirúrgico  "Lucía Íñiguez Landín"', '', '', '', '', 'Código:', '', '', ''],
                       ['Almacén-Recepción:', '', '', 'Código:', '', 'Dirección:', '', '', ''],
                       ['Almacén-Entrega:', '', '', 'Dirección:', '', '', 'Código:', '', 'Lote:'],
                       ['CÓDIGO', 'DESCRIPCIÓN', 'UM', 'CANTIDAD', '', 'PRECIO', 'IMPORTE', '', 'SALDO'],
                       ['', '', '', 'ENVIADA', 'RECIBIDA', '', 'ENVIADA', 'RECIBIDA', '']]
        pfd = PedidoAlmacenDetalle.objects.select_related().filter(pedido_almacen=pedf)
        detalles = [(p.producto.codigo, p.producto.nombre, p.producto.unidad, p.cantidad_enviada, p.cantidad_recibida, p.producto.precio, p.importe_enviada, p.importe_recibida, p.saldo) for p in pfd]
        detalles1 = [['TOTAL', '', '', '', '', '', pedf.importe_enviada_total, pedf.importe_recibida_total, '']]
        firmas = [['Entregado por:' + pedf.entregado_por, '', 'Autorizado por:' + pedf.autorizado_por, '', '', 'Recibido por:' + pedf.recibido_por, '', '', 'No.' + '%s' % pedf.id]]
        detalle_orden = Table(encabezados + detalles + detalles1 + firmas)
        detalle_orden.setStyle(TableStyle([
            ('ALIGN', (0, 0), (3, 0), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('SPAN', (0, 0), (1, 0)),
            ('ALIGN', (0, 0), (1, 0), 'LEFT'),
            ('SPAN', (2, 0), (6, 0)),
            ('SPAN', (7, 0), (8, 1)),
             ('SPAN', (0, 1), (4, 1)),
             ('SPAN', (5, 1), (6, 1)),
             ('SPAN', (0, 2), (2, 2)),
             ('SPAN', (3, 2), (4, 2)),
             ('SPAN', (5, 2), (8, 2)),
             ('SPAN', (0, 3), (2, 3)),
             ('SPAN', (3, 3), (5, 3)),
             ('SPAN', (6, 3), (7, 3)),
             ('SPAN', (0, 4), (0, 5)),
            ('ALIGN', (0, 4), (0, 5), 'CENTER'),
             ('SPAN', (1, 4), (1, 5)),
            ('ALIGN', (1, 4), (1, 5), 'CENTER'),
             ('SPAN', (2, 4), (2, 5)),
            ('ALIGN', (2, 4), (2, 5), 'CENTER'),
             ('SPAN', (3, 4), (4, 4)),
            ('ALIGN', (3, 4), (4, 4), 'CENTER'),
             ('SPAN', (5, 4), (5, 5)),
            ('ALIGN', (5, 4), (5, 5), 'CENTER'),
             ('SPAN', (6, 4), (7, 4)),
            ('ALIGN', (6, 4), (7, 4), 'CENTER'),
             ('SPAN', (8, 4), (8, 5)),
            ('ALIGN', (8, 4), (8, 5), 'CENTER'),
            ('ALIGN', (3, 5), (3, 5), 'CENTER'),
            ('ALIGN', (4, 5), (4, 5), 'CENTER'),
            ('ALIGN', (6, 5), (6, 5), 'CENTER'),
            ('ALIGN', (7, 5), (7, 5), 'CENTER'),
            ('SPAN', (0, -2), (-4, -2)),
            ('ALIGN', (0, -2), (-4, -2), 'CENTER'),
            ('SPAN', (-4, -1), (-2, -1)),
            ('SPAN', (-7, -1), (-5, -1)),
            ('SPAN', (-9, -1), (-8, -1)),
        ]))
        return detalle_orden


class ReporteDevueltoAlmacenPDF(View):

    def get(self, request, id_df):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename = devolución de sala.pdf'
        document = SimpleDocTemplate(response, pagesize=pagesizes.landscape(pagesizes.LETTER),)
        story = []

        story.append(self.tabla(id_df))
        document.build(story, onFirstPage=bb, onLaterPages=bb)
        return response

    def tabla(self, id_df):
        devf = DevueltoAlmacen.objects.get(id=id_df)
        encabezados = [['MINSAP-SC-2-06 Y 9', '', 'TRANSFERENCIA ENTRE ALMACENES', '', '', '', '', 'FECHA:' + '%s' % date_format(timezone.localtime(devf.fecha_hora), settings.SHORT_DATETIME_FORMAT), ''],
                       ['Entidad: Hospital Universitario Clínico Quirúrgico  "Lucía Íñiguez Landín"', '', '', '', '', 'Código:', '', '', ''],
                       ['Almacén-Recepción:', '', '', 'Código:', '', 'Dirección:', '', '', ''],
                       ['Almacén-Entrega:', '', '', 'Dirección:', '', '', 'Código:', '', 'Lote:'],
                       ['CÓDIGO', 'DESCRIPCIÓN', 'UM', 'CANTIDAD', '', 'PRECIO', 'IMPORTE', '', 'SALDO'],
                       ['', '', '', 'ENVIADA', 'RECIBIDA', '', 'ENVIADA', 'RECIBIDA', '']]
        dfd = DevueltoAlmacenDetalle.objects.select_related().filter(devuelto_almacen=devf)
        detalles = [(d.producto.codigo, d.producto.nombre, d.producto.unidad, d.cantidad_enviada, d.cantidad_recibida, d.producto.precio, d.importe_enviada, d.importe_recibida, d.saldo) for d in dfd]
        detalles1 = [['TOTAL', '', '', '', '', '', devf.importe_enviada_total, devf.importe_recibida_total, '']]
        firmas = [['Entregado por:' + devf.entregado_por, '', 'Autorizado por:' + devf.autorizado_por, '', '', 'Recibido por:' + devf.recibido_por, '', '', 'No.' + '%s' % devf.id]]
        detalle_orden = Table(encabezados + detalles + detalles1 + firmas)
        detalle_orden.setStyle(TableStyle([
            ('ALIGN', (0, 0), (3, 0), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('SPAN', (0, 0), (1, 0)),
            ('ALIGN', (0, 0), (1, 0), 'LEFT'),
            ('SPAN', (2, 0), (6, 0)),
            ('SPAN', (7, 0), (8, 1)),
             ('SPAN', (0, 1), (4, 1)),
             ('SPAN', (5, 1), (6, 1)),
             ('SPAN', (0, 2), (2, 2)),
             ('SPAN', (3, 2), (4, 2)),
             ('SPAN', (5, 2), (8, 2)),
             ('SPAN', (0, 3), (2, 3)),
             ('SPAN', (3, 3), (5, 3)),
             ('SPAN', (6, 3), (7, 3)),
             ('SPAN', (0, 4), (0, 5)),
            ('ALIGN', (0, 4), (0, 5), 'CENTER'),
             ('SPAN', (1, 4), (1, 5)),
            ('ALIGN', (1, 4), (1, 5), 'CENTER'),
             ('SPAN', (2, 4), (2, 5)),
            ('ALIGN', (2, 4), (2, 5), 'CENTER'),
             ('SPAN', (3, 4), (4, 4)),
            ('ALIGN', (3, 4), (4, 4), 'CENTER'),
             ('SPAN', (5, 4), (5, 5)),
            ('ALIGN', (5, 4), (5, 5), 'CENTER'),
             ('SPAN', (6, 4), (7, 4)),
            ('ALIGN', (6, 4), (7, 4), 'CENTER'),
             ('SPAN', (8, 4), (8, 5)),
            ('ALIGN', (8, 4), (8, 5), 'CENTER'),
            ('ALIGN', (3, 5), (3, 5), 'CENTER'),
            ('ALIGN', (4, 5), (4, 5), 'CENTER'),
            ('ALIGN', (6, 5), (6, 5), 'CENTER'),
            ('ALIGN', (7, 5), (7, 5), 'CENTER'),
            ('SPAN', (0, -2), (-4, -2)),
            ('ALIGN', (0, -2), (-4, -2), 'CENTER'),
            ('SPAN', (-4, -1), (-2, -1)),
            ('SPAN', (-7, -1), (-5, -1)),
            ('SPAN', (-9, -1), (-8, -1)),
        ]))
        return detalle_orden


class ReporteBajaCoberturaPDF(View):

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename = baja cobertura.pdf'
        document = SimpleDocTemplate(response, pagesize=pagesizes.portrait(pagesizes.LETTER),)
        story = []

        story.append(self.tabla())
        document.build(story, onFirstPage=aa, onLaterPages=aa)
        return response

    def tabla(self):
        titulo = ['PRODUCTOS EN BAJA COBERTURA', '', '', '']
        encabezados = ('CÓDIGO', 'DESCRIPCIÓN', 'UM', 'CANTIDAD FALTANTE')
        existencia = Existencia.objects.filter(porciento__lte=50)
        for bc in existencia:
            cf = bc.fondo_fijo - bc.todo
            detalles = [(bc.producto.codigo, bc.producto.nombre, bc.producto.unidad, cf)]
        detalle_orden = Table([titulo] + [encabezados] + detalles)
        detalle_orden.setStyle(TableStyle([
            ('ALIGN', (0, 0), (3, 0), 'CENTER'),
            ('SPAN', (0, 0), (3, 0)),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
        ]))
        return detalle_orden


class ReporteFiltroImportePDF(View):

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename = salida al centro de costo.pdf'
        document = SimpleDocTemplate(response, pagesize=pagesizes.landscape(pagesizes.LETTER),)
        story = []

        story.append(self.tabla(request))
        document.build(story, onFirstPage=bb, onLaterPages=bb)
        return response

    def tabla(self, request):
        detalles = {}
        titulo = ['SALIDA AL CENTRO DE COSTO', '', '', '', '', '', '', '']
        encabezados = ['CÓDIGO', 'PRODUCTO', 'PRECIO', 'CANT. PEDIDOS', 'IMPORTE', 'CANT. DEVOLUCIONES', 'IMPORTE', 'SALDO']
        form = FiltrarImporteForm(request.GET)
        if form.is_valid():
            ini_fecha = form.cleaned_data['inicio_fecha']
            fin_fecha = form.cleaned_data['final_fecha']
            centro_costo = form.cleaned_data['centro_costo']
            peds = PedidoSala.objects.filter(sala__centro_costo=centro_costo)
            peds = peds.filter(fecha_hora__range=(ini_fecha, fin_fecha))
            peds = peds.exclude(despachado_por="")
            psd = PedidoSalaDetalle.objects.select_related().filter(pedido_sala__in=peds)
            devs = DevueltoSala.objects.filter(sala__centro_costo=centro_costo)
            devs = devs.filter(fecha_hora__range=(ini_fecha, fin_fecha))
            devs = devs.exclude(despachado_por="")
            dsd = DevueltoSalaDetalle.objects.select_related().filter(devuelto_sala__in=devs)
            for p in psd:
                detalles.setdefault(p.producto, [0, 0])
                detalles[p.producto][0] += p.cantidad_entregada
            for d in dsd:
                detalles.setdefault(d.producto, [0, 0])
                detalles[d.producto][1] += d.cantidad_confirmada
            ex = Existencia.objects.all()
            for e in ex:
                if d.producto.nombre == e.producto.nombre:
                    saldo = e.todo
            detalles1 = [[d.producto.codigo, d.producto.nombre, detalles[p.producto][0], d.producto.precio, detalles[d.producto][1], saldo]]
            detalle_orden = Table([titulo] + [encabezados] + detalles1)
            detalle_orden.setStyle(TableStyle([
                ('ALIGN', (0, 0), (3, 0), 'CENTER'),
                ('SPAN', (0, 0), (7, 0)),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
            ]))
        return detalle_orden

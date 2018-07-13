from django import forms
from .models import PedidoCama, Sala, Cama, DevueltoCama, PedidoSala, DevueltoSala, Producto, PedidoSalaDetalle, \
    DevueltoSalaDetalle, Presentacion, UnidadMedida, Justificacion, DevueltoFarmacia, DevueltoAlmacen, \
    DevueltoAlmacenDetalle, PedidoAlmacenDetalle, PedidoAlmacen, Existencia, PermisoGlobal


class AutenticarForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class FiltrarSolicitudSalaForm(forms.Form):
    TIPO_SOLICITUD = (
        ('Pedidos de sala', 'Pedidos de sala'),
        ('Devoluciones de sala', 'Devoluciones de sala'),
        ('Reposiciones a farmacia', 'Reposiciones a farmacia'),
        ('Devoluciones de farmacia', 'Devoluciones de farmacia'),
    )

    inicio_fecha = forms.DateTimeField(required=True)
    final_fecha = forms.DateTimeField(required=True)
    sala = forms.ModelChoiceField(queryset=Sala.objects.all())
    tipo_solicitud = forms.ChoiceField(choices=TIPO_SOLICITUD)


class FiltrarImporteForm(forms.Form):
    centro_costo = forms.IntegerField(required=True)
    inicio_fecha = forms.DateTimeField(required=True)
    final_fecha = forms.DateTimeField(required=True)


class PermisoGlobalForm(forms.ModelForm):
    class Meta:
        model = PermisoGlobal
        fields = ['farmacia', 'almacen', 'jefe_farmacia', 'secretaria_sala', 'contabilidad', 'jefe_contabilidad']


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['unidad', 'nombre', 'codigo', 'precio', 'dosis', 'unidad_medida']


class PresentacionForm(forms.ModelForm):
    class Meta:
        model = Presentacion
        fields = ['nombre']


class UnidadMedidaForm(forms.ModelForm):
    class Meta:
        model = UnidadMedida
        fields = ['nombre']


class JustificacionForm(forms.ModelForm):
    class Meta:
        model = Justificacion
        fields = ['nombre']


class CamaForm(forms.ModelForm):
    class Meta:
        model = Cama
        fields = ['historia_clinica', 'nombre', 'apellido1', 'apellido2']


class SalaForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = ['servicio', 'secretaria', 'apodo', 'centro_costo']


class ExistenciaMedicamentosForm(forms.ModelForm):
    class Meta:
        model = Existencia
        fields = ['producto', 'todo', 'fondo_fijo']

    def clean(self):
        cleaned_data = super(ExistenciaMedicamentosForm, self).clean()
        todo = cleaned_data.get('todo')
        fondo_fijo = cleaned_data.get('fondo_fijo')
        if todo and fondo_fijo:
            if todo > fondo_fijo:
                a = "La cantidad no puede superar el fondo fijo"
                self.add_error('todo', a)


class PedidoCamaForm(forms.ModelForm):
    class Meta:
        model = PedidoCama
        fields = ['producto', 'cantidad_solicitada', 'medico']


class PedidoSalaForm(forms.ModelForm):
    class Meta:
        model = PedidoSala
        fields = ['solicitado_por', 'despachado_por', 'recibido_por', 'aprobado_por']


class PedidoSalaEntregadoForm(forms.ModelForm):
    cantidad_entregada = forms.IntegerField(required=True)

    class Meta:
        model = PedidoSalaDetalle
        fields = ['cantidad_entregada']

    def clean_cantidad_entregada(self):
        cantidad_entregada = self.cleaned_data['cantidad_entregada']
        if self.instance and cantidad_entregada > self.instance.cantidad_solicitada:
            raise forms.ValidationError("La cantidad entregada no puede superar la cantidad solicitada")
        return cantidad_entregada


PedidoSalaEntregadoFormSet = forms.modelformset_factory(PedidoSalaDetalle, form=PedidoSalaEntregadoForm, extra=0)


class DevueltoFarmaciaForm(forms.ModelForm):
    class Meta:
        model = DevueltoFarmacia
        fields = ['producto', 'cantidad_enviada']


class DevueltoCamaForm(forms.ModelForm):
    class Meta:
        model = DevueltoCama
        fields = ['producto', 'cantidad_devuelta', 'medico', 'justificacion']


class DevueltoSalaForm(forms.ModelForm):
    class Meta:
        model = DevueltoSala
        fields = ['devuelta_por', 'recibida_por', 'aprobado_por']


class DevueltoSalaEntregadoForm(forms.ModelForm):
    cantidad_confirmada = forms.IntegerField(required=True)

    class Meta:
        model = DevueltoSalaDetalle
        fields = ['cantidad_confirmada']

    def clean_cantidad_confirmada(self):
        cantidad_confirmada = self.cleaned_data['cantidad_confirmada']
        if self.instance and cantidad_confirmada > self.instance.cantidad_devuelta:
            raise forms.ValidationError("La cantidad confirmada no puede superar la cantidad devuelta")
        return cantidad_confirmada


DevueltoSalaEntregadoFormSet = forms.modelformset_factory(DevueltoSalaDetalle, form=DevueltoSalaEntregadoForm, extra=0)


class DespachoFirmaPedidoForm(forms.ModelForm):
    class Meta:
        model = PedidoSala
        fields = ['aprobado_por', 'despachado_por', 'recibido_por']


class DespachoFirmaDevueltoForm(forms.ModelForm):
    class Meta:
        model = DevueltoSala
        fields = ['aprobado_por', 'recibida_por', 'despachado_por']


class PedidoAlmacenForm(forms.ModelForm):
    class Meta:
        model = PedidoAlmacen
        fields = ['entregado_por', 'recibido_por', 'autorizado_por']


class PedidoAlmacenEntregadoForm(forms.ModelForm):
    cantidad_recibida = forms.IntegerField(required=True)

    class Meta:
        model = PedidoAlmacenDetalle
        fields = ['cantidad_recibida']

    def clean_cantidad_recibida(self):
        cantidad_recibida = self.cleaned_data['cantidad_recibida']
        if self.instance and cantidad_recibida > self.instance.cantidad_enviada:
            raise forms.ValidationError("La cantidad recibida no debe superar la cantidad enviada")
        return cantidad_recibida


PedidoAlmacenEntregadoFormSet = forms.modelformset_factory(PedidoAlmacenDetalle, form=PedidoAlmacenEntregadoForm,
                                                           extra=0)


class DespachoFirmaPedidoAlmacenForm(forms.ModelForm):
    class Meta:
        model = PedidoAlmacen
        fields = ['recibido_por', 'autorizado_por']


class DevueltoAlmacenForm(forms.ModelForm):
    class Meta:
        model = DevueltoAlmacen
        fields = ['entregado_por', 'recibido_por', 'autorizado_por']


class DevueltoAlmacenEntregadoForm(forms.ModelForm):
    cantidad_recibida = forms.IntegerField(required=True)

    class Meta:
        model = DevueltoAlmacenDetalle
        fields = ['cantidad_recibida']


DevueltoAlmacenEntregadoFormSet = forms.modelformset_factory(DevueltoAlmacenDetalle, form=DevueltoAlmacenEntregadoForm,
                                                             extra=0)


class DespachoFirmaDevueltoAlmacenForm(forms.ModelForm):
    class Meta:
        model = DevueltoAlmacen
        fields = ['recibido_por', 'autorizado_por']
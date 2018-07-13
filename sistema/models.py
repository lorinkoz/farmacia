from django.db import models
from django.core.exceptions import ValidationError


def validar(valor):
    if len(valor) != 3:
        raise ValidationError(' el Centro de Costo debe tener 3 caracteres')
    if not valor.isnumeric():
        raise ValidationError(' el valor no es un dígito')


class Sala(models.Model):
    servicio = models.CharField(max_length=40)
    apodo = models.CharField(max_length=20)
    centro_costo = models.CharField(validators=[validar], max_length=3, unique=True)
    secretaria = models.ForeignKey('auth.User', related_name='sala')

    def __str__(self):
        return '%s' % self.servicio

    class Meta:
        ordering = ['centro_costo']


def validar(valor):
    if len(valor) != 11:
        raise ValidationError(' la H.C debe tener 11 caracteres')
    if not valor.isnumeric():
        raise ValidationError(' el valor no es numérico')


class Cama(models.Model):
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    num_cama = models.IntegerField()
    historia_clinica = models.CharField(validators=[validar], max_length=11, unique=True)
    nombre = models.CharField(max_length=30)
    apellido1 = models.CharField(max_length=30)
    apellido2 = models.CharField(max_length=30)
    fecha_hora = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return '%s' % self.sala + " " + '%s' % self.num_cama

    class Meta:
        ordering = ['num_cama']


class PedidoCama(models.Model):
    producto = models.ForeignKey('Producto')
    pedido_sala_detalle = models.ForeignKey('PedidoSalaDetalle', null=True, blank=True)
    cama = models.ForeignKey(Cama)
    cantidad_solicitada = models.PositiveIntegerField()
    medico = models.CharField(max_length=40)

    def __str__(self):
        return '%s' % self.cama + " " + '%s' % self.producto


class PedidoSala(models.Model):
    sala = models.ForeignKey(Sala)
    solicitado_por = models.CharField(max_length=40)
    despachado_por = models.CharField(max_length=40)
    recibido_por = models.CharField(max_length=40)
    aprobado_por = models.CharField(max_length=40)
    importe_total = models.FloatField(default=0)
    fecha_hora = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return '%s' % self.sala + " " + '%s' % self.id


class PedidoSalaDetalle(models.Model):
    pedido_sala = models.ForeignKey('PedidoSala', on_delete=models.CASCADE, related_name="pedido_sala")
    producto = models.ForeignKey('Producto')
    cantidad_solicitada = models.PositiveIntegerField()
    cantidad_entregada = models.PositiveIntegerField(null=True, blank=True)
    importe = models.FloatField(default=0)
    saldo = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return '%s' % self.producto


class DevueltoCama(models.Model):
    cama = models.ForeignKey(Cama)
    producto = models.ForeignKey('Producto')
    devuelto_sala_detalle = models.ForeignKey('DevueltoSalaDetalle', null=True, blank=True)
    cantidad_devuelta = models.PositiveIntegerField()
    justificacion = models.ForeignKey('Justificacion')
    medico = models.CharField(max_length=40)

    def __str__(self):
        return '%s' % self.cama + " " + '%s' % self.producto


class DevueltoSala(models.Model):
    sala = models.ForeignKey(Sala)
    devuelta_por = models.CharField(max_length=40)
    recibida_por = models.CharField(max_length=40)
    aprobado_por = models.CharField(max_length=40)
    despachado_por = models.CharField(max_length=40)
    importe_total = models.FloatField(default=0)
    fecha_hora = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return '%s' % self.sala + " " + '%s' % self.id


class DevueltoSalaDetalle(models.Model):
    devuelto_sala = models.ForeignKey('DevueltoSala', on_delete=models.CASCADE, related_name="devuelto_sala")
    producto = models.ForeignKey('Producto')
    cantidad_devuelta = models.PositiveIntegerField()
    cantidad_confirmada = models.PositiveIntegerField(null=True, blank=True)
    importe = models.FloatField(default=0)
    saldo = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return'%s' % self.producto


class Existencia(models.Model):
    producto = models.OneToOneField('Producto', related_name='existencia')
    porciento = models.IntegerField(null=True, blank=True)
    todo = models.PositiveIntegerField()
    fondo_fijo = models.PositiveIntegerField()

    def __str__(self):
        return '%s' % self.producto


def validar(valor):
    if len(valor) != 8:
        raise ValidationError(' el código debe tener 8 caracteres')


class Producto(models.Model):
    nombre = models.CharField(max_length=60)
    dosis = models.FloatField()
    unidad_medida = models.ForeignKey('UnidadMedida')
    unidad = models.ForeignKey('Presentacion')
    codigo = models.CharField(max_length=8, validators=[validar], unique=True)
    precio = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return '%s' % self.nombre

    class Meta:
        ordering = ['unidad', 'nombre']


class Presentacion(models.Model):
    nombre = models.CharField(max_length=15)

    def __str__(self):
        return '%s' % self.nombre

    class Meta:
        ordering = ['nombre']


class UnidadMedida(models.Model):
    nombre = models.CharField(max_length=10)

    def __str__(self):
        return '%s' % self.nombre

    class Meta:
        ordering = ['nombre']


class Justificacion(models.Model):
    nombre = models.CharField(max_length=30)

    def __str__(self):
        return '%s' % self.nombre

    class Meta:
        ordering = ['nombre']


class PedidoAlmacen(models.Model):
    entregado_por = models.CharField(max_length=40)
    recibido_por = models.CharField(max_length=40)
    autorizado_por = models.CharField(max_length=40)
    importe_enviada_total = models.FloatField(default=0)
    importe_recibida_total = models.FloatField(default=0)
    fecha_hora = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return '%s' % self.entregado_por


class PedidoAlmacenDetalle(models.Model):
    pedido_almacen = models.ForeignKey('PedidoAlmacen', on_delete=models.CASCADE, related_name="pedido_almacen")
    producto = models.ForeignKey('Producto')
    cantidad_enviada = models.IntegerField()
    cantidad_recibida = models.PositiveIntegerField(null=True, blank=True)
    importe_enviada = models.FloatField(default=0)
    importe_recibida = models.FloatField(default=0)
    saldo = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return'%s' % self.producto


class DevueltoFarmacia(models.Model):
    devuelto_almacen_detalle = models.ForeignKey('DevueltoAlmacenDetalle', null=True, blank=True)
    producto = models.ForeignKey('Producto')
    cantidad_enviada = models.PositiveIntegerField()

    def __str__(self):
        return '%s' % self.producto

    class Meta:
        ordering = ['producto']


class DevueltoAlmacen(models.Model):
    entregado_por = models.CharField(max_length=40)
    recibido_por = models.CharField(max_length=40)
    autorizado_por = models.CharField(max_length=40)
    importe_enviada_total = models.FloatField(default=0)
    importe_recibida_total = models.FloatField(default=0)
    fecha_hora = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return '%s' % self.entregado_por


class DevueltoAlmacenDetalle(models.Model):
    devuelto_almacen = models.ForeignKey('DevueltoAlmacen', on_delete=models.CASCADE, related_name="devuelto_almacen")
    producto = models.ForeignKey('Producto')
    cantidad_enviada = models.PositiveIntegerField()
    cantidad_recibida = models.PositiveIntegerField(null=True, blank=True)
    importe_enviada = models.FloatField(default=0)
    importe_recibida = models.FloatField(default=0)
    saldo = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return '%s' % self.producto


class PermisoGlobal(models.Model):
    farmacia = models.ManyToManyField('auth.User', blank=True, related_name="farmacia")# J Dpto. farmacia y farmacia
    almacen = models.ForeignKey('auth.User', blank=True, null=True, related_name="almacen")# almacen
    jefe_farmacia = models.ForeignKey('auth.User', blank=True, null=True, related_name="jefe_farmacia")# J Dpto de farmacia
    secretaria_sala = models.ManyToManyField('auth.User', blank=True, related_name="secretaria_sala")# Secretaria de sala
    jefe_contabilidad = models.ForeignKey('auth.User', blank=True, null=True, related_name="jefe_contabilidad")# Contabilidad
    contabilidad = models.ManyToManyField('auth.User', blank=True, related_name="contabilidad")# J Dpto. Framacia y contabilidad

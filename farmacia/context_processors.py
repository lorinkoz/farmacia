from django.contrib.auth.models import User
from sistema.models import PermisoGlobal


def security(request):
    return {
        'secretarios': User.objects.exclude(sala=None),
        'pglobal': PermisoGlobal.objects.first()
    }

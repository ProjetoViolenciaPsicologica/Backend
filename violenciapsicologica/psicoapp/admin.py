from django.contrib import admin
from .models import Formulario, TipoUsuario, User, AreaUsuario, LocalFormulario, GrauInstrucao
# Registro de models

admin.site.register(Formulario)
admin.site.register(TipoUsuario)
admin.site.register(User)
admin.site.register(AreaUsuario)
admin.site.register(LocalFormulario)
admin.site.register(GrauInstrucao)
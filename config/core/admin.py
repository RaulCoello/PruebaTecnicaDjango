from django.contrib import admin
from .models import Proyecto, Tarea, ProyectoTarea,TareaUsuario

# Register your models here.
admin.site.register(Proyecto)
admin.site.register(Tarea)
admin.site.register(ProyectoTarea)
admin.site.register(TareaUsuario)
from django.urls import path
from . import views

urlpatterns = [
	# Frontend
	path('',views.home),

	# API
	path('api/usuarios/',views.Usuarios),
	path('api/proyectos/',views.proyectos),
	path('api/proyectos/<int:id>/',views.proyectos),
	path('api/tareas/',views.Tareas),
	path('api/tareas/<int:id>/',views.Tareas),
	path('api/proyectostareas/',views.ProyectosTareas),
	path('api/proyectostareas/<int:id>/',views.ProyectosTareas)
]
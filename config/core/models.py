from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Proyecto(models.Model):
	nombre = models.CharField(max_length=150)
	descripcion =  models.TextField(blank=True)
	fecha_creacion = models.DateTimeField(auto_now_add = True)


	# Relacion de muchos a muchos en tabla intermedia
	tareas = models.ManyToManyField(
		'Tarea',
		through = 'ProyectoTarea',
		related_name ='proyectos'
		)


	def __str__(self):
		return self.nombre

class Tarea(models.Model):
	titulo = models.CharField(max_length=200)
	instrucciones = models.TextField(blank=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.titulo

# clases para las transacciones
class ProyectoTarea(models.Model):
	PRIORIDADES =[
		('alta','Alta'),
		('media','Media'),
		('baja','Baja'),
	]
	proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='proyecto_tareas')
	tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name='tarea_proyectos')
	prioridad = models.CharField(max_length=10, choices = PRIORIDADES)
	fecha_creacion = models.DateTimeField(auto_now_add=True)

	class Meta:
		# evitar duplicidad de tareas en el proyecto
		unique_together = ('proyecto','tarea')

	def __str__(self):
		return f"{self.proyecto} - {self.tarea} ({self.prioridad})"

class TareaUsuario(models.Model):
	proyecto_tarea = models.ForeignKey(ProyectoTarea, on_delete=models.CASCADE, related_name='usuarios_tareas')
	usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tareas_usuario')
	tiempo_dedicado = models.DecimalField(max_digits=5, decimal_places=2, default=0)
	completada = models.BooleanField(default=False)
	fecha_creacion = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.usuario.username} - {self.proyecto_tarea}"

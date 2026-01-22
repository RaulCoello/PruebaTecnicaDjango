from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Proyecto, Tarea, ProyectoTarea,TareaUsuario
from django.contrib.auth.models import User
from django.http import JsonResponse
import json

# Create your views here.
# frontend
@csrf_exempt
def home(request):
	return render(request, 'core/index.html')



# API

# Usuarios
@csrf_exempt
def Usuarios(request, id=None):

	#Get all 
	if request.method == 'GET' and id  is None:
		usuarios = list(User.objects.values('id','username'))
		return JsonResponse(usuarios, safe=False)

	# retonar por defecto
	return JsonResponse({'mensaje':'Metodo no permitido'}, status=405)

# Proyectos
@csrf_exempt
def proyectos(request, id=None):

	#Get all
	if request.method == 'GET' and id is None:
		proyectos = list(Proyecto.objects.values())
		return JsonResponse(proyectos, safe = False)

	#get con id 

	if request.method == 'GET' and id is not None:
		try:
			p= Proyecto.objects.get(id=id)
			data={
				'id':p.id,
				'nombre':p.nombre,
				'descripcion': p.descripcion,
				'fecha_creacion': p.fecha_creacion
			}
			return JsonResponse(data)
		except Proyecto.DoesNotExist:
			return JsonResponse({'error':'Proyecto no exisite id'}, status=404)

	# post para guardar datos 
	if request.method == 'POST':
		data = json.loads(request.body)
		p = Proyecto.objects.create(
			nombre= data['nombre'],
			descripcion = data.get('descripcion','')
			)	
		return JsonResponse({'id':p.id,'nombre':p.nombre})

	# PUT para actualizar
	if request.method == 'PUT' and id is not None:
		try:
			p=Proyecto.objects.get(id=id)
			data = json.loads(request.body)

			p.nombre= data.get('nombre',p.nombre)
			p.descripcion = data.get('descripcion',p.descripcion)
			p.save()

			return JsonResponse({'mensaje':'Proyecto actualizado'})
		except Proyecto.DoesNotExist:
			return JsonResponse({'error':'Proyecto no existe'},status=404)

	if request.method == 'DELETE' and id is not None:
		try:
			p= Proyecto.objects.get(id=id)
			p.delete()
			return JsonResponse({'mensaje':'Proyecto eliminado'})
		except Proyecto.DoesNotExist:
			return JsonResponse({'error':'Proyecto no existe'}, status=404)


	# retonar por defecto
	return JsonResponse({'mensaje':'Metodo no permitido'}, status=405)




#Tarea
@csrf_exempt
def Tareas(request, id=None):

	# Get all 
	if request.method == 'GET' and id is None:
		tareas = list(Tarea.objects.values())
		return JsonResponse(tareas, safe=False)

	# Get con id
	if request.method == 'GET' and id is not None:
		try:
			t = Tarea.objects.get(id=id)
			data = {
				'titulo':t.titulo,
				'instrucciones':t.instrucciones,
				'fecha_creacion':t.fecha_creacion
			}
			return JsonResponse(data)
		except Tarea.DoesNotExist:
			return JsonResponse({'error':'Tarea no existe'}, status=404)

	# Post para guardar
	if request.method == 'POST':
		data = json.loads(request.body)
		t = Tarea.objects.create(
				titulo=data['titulo'],
				instrucciones=data.get('instrucciones','')
			)
		return JsonResponse({'id':t.id, 'titulo':t.titulo})

	# Put para editar
	if request.method == 'PUT' and id is not None:
		try:
			t = Tarea.objects.get(id=id)
			data = json.loads(request.body)

			t.titulo = data.get('titulo',t.titulo)
			t.instrucciones = data.get('instrucciones',t.instrucciones)

			t.save()
			return JsonResponse({'mensaje':'Tarea Actualizada'})
		except Tarea.DoesNotExist:
			return JsonResponse({'error':'No existe la tarea'},status=404)


	# Eliminar
	if request.method == 'DELETE' and id is not None:
		try:
			t = Tarea.objects.get(id=id)
			t.delete()
			return JsonResponse({'mensaje':'Tarea eleminada'})
		except Tarea.DoesNotExist:
			return JsonResponse({'error':'Tarea no Existe'})

	# retornar por defecto
	return JsonResponse({'mensaje':'Metodo no permitido'}, status=405)

# para conectar tareas con proyectos
@csrf_exempt
def ProyectosTareas(request, id=None):

	# Get para traer todas las tareas con proyectos
	if request.method == 'GET' and id is None:
		proyecto_tarea = ProyectoTarea.objects.select_related('proyecto','tarea')

		data = []

		for r in proyecto_tarea:
			data.append({
				'id':r.id,
				'proyecto_id':r.proyecto.id,
				'proyecto_nombre':r.proyecto.nombre,
				'tarea_id':r.tarea.id,
				'tarea_titulo':r.tarea.titulo,
				'prioridad':r.prioridad,
				'fecha_creacion':r.fecha_creacion
				})
		return JsonResponse(data, safe=False)


	# Get para filtrar solo las tareas de un proyecto id
	if request.method =='GET' and id is not None:
		proyecto_tarea = ProyectoTarea.objects.select_related('proyecto','tarea').filter(proyecto_id=id)

		data = []

		for r in proyecto_tarea:
			data.append({
				'id':r.id,
				'proyecto_id':r.proyecto.id,
				'proyecto_nombre':r.proyecto.nombre,
				'tarea_id':r.tarea.id,
				'tarea_titulo':r.tarea.titulo,
				'prioridad':r.prioridad,
				'fecha_creacion':r.fecha_creacion
				})
		return JsonResponse(data, safe=False)

	# Post para juntar una tarea a un proyecto
	if request.method == 'POST':
		data = json.loads(request.body)
		proyecto_tarea = ProyectoTarea.objects.create(
				proyecto_id=data['proyecto_id'],
				tarea_id=data['tarea_id'],
				prioridad=data['prioridad']
			)
		return JsonResponse({'id':proyecto_tarea.id})

	# Delete para eliminar 
	if request.method == 'DELETE' and id is not None:
		try:
			t=ProyectoTarea.objects.get(id=id)
			t.delete()
			return JsonResponse({'mensaje':'Tarea eliminada del proyecto'})
		except ProyectoTarea.DoesNotExist:
			return JsonResponse({'error':'Tarea no existe dentro del proyecto'},status=404)

	# defult
	return JsonResponse({'mensaje':'Metodo no permitido'}, status=405)


# para conectar las tareas de los proyectos con usuarios 
@csrf_exempt
def UsuariosTareas(request, id=None):

	# Get ALL
	# TareaUsuario
	if request.method == 'GET' and id is None:
		registros = TareaUsuario.objects.select_related(
			'usuario',
			'proyecto_tarea__proyecto',
			'proyecto_tarea__tarea'
			)

		data = []
		for r in registros:
			data.append({
				'id':r.id,
				'usuario':r.usuario.username,
				'proyecto':r.proyecto_tarea.proyecto.nombre,
				'tarea':r.proyecto_tarea.tarea.titulo,
				'prioridad':r.proyecto_tarea.prioridad,
				'tiempo_dedicado':float(r.tiempo_dedicado),
				'completada':r.completada,
				'fecha_creacion':r.fecha_creacion
				})
		return JsonResponse(data, safe=False)


	# Get con filtro
	if request.method == 'GET' and id is not None:
		registros = TareaUsuario.objects.select_related(
			'usuario',
			'proyecto_tarea__proyecto',
			'proyecto_tarea__tarea'
			).filter(proyecto_tarea_id=id)

		data = []
		for r in registros:
			data.append({
				'id':r.id,
				'usuario':r.usuario.username,
				'proyecto':r.proyecto_tarea.proyecto.nombre,
				'tarea':r.proyecto_tarea.tarea.titulo,
				'prioridad':r.proyecto_tarea.prioridad,
				'tiempo_dedicado':float(r.tiempo_dedicado),
				'completada':r.completada,
				'fecha_creacion':r.fecha_creacion
				})
		return JsonResponse(data, safe=False)	



	# Post para registrar un usuario con una tarea
	if request.method == 'POST':
		data = json.loads(request.body)
		t = TareaUsuario.objects.create(
			proyecto_tarea_id = data['proyecto_tarea'],
			usuario_id=data['usuario'],
			tiempo_dedicado =data.get('tiempo_dedicado',1),
			completada =data.get('completada',False)
			)
		return JsonResponse({'id':t.id})

		# defult
	return JsonResponse({'mensaje':'Metodo no permitido'}, status=405)
const loader = document.getElementById("loader");

function mostrarLoader() {
  loader.style.display = "flex";
}

function ocultarLoader() {
  loader.style.display = "none";
}

// Simular latencia
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// PROYECTOS-------------------------------------------------------------------
// ---- CARGAR PROYECTOS ----
async function cargarProyectos() {
  mostrarLoader();
  await sleep(1000); // efecto visual

  fetch("/api/proyectos/")
    .then((res) => res.json())
    .then((data) => {
      const tbody = document.getElementById("tableproyectos");
      tbody.innerHTML = "";

      data.forEach((p) => {
            const tr= document.createElement("tr");
            tr.innerHTML = `
                <td>${p.id}</td>
                <td class="container">
                        <p class="fw-bold">${p.nombre}</p>
                        <p>${p.descripcion}</p>
                        <p>${p.fecha_creacion}</p>
                </td>
                <td class="d-flex flex-column gap-2">
                    <button class="btn btn-sm btn-warning me-2"
                        onclick="editarProyecto(${p.id},'${p.nombre}','${p.descripcion || ""}')"
                    >
                    Editar
                    </button>
                    <button class="btn btn-sm btn-danger me-2"
                        onclick="eliminarProyecto(${p.id})"
                    >
                    Eliminar
                    </button>
                </td>
            `;
            tr.onclick = () => seleccionProyecto(p.id,p.nombre);
            tbody.appendChild(tr);
      });
    })
    .finally(() => ocultarLoader());
}

// crear proyecto 
document.getElementById("formProyecto").addEventListener("submit",async function(e){
    e.preventDefault();

    const nombre = document.getElementById("nombreProyecto").value;
    const descripcion = document.getElementById("descripcionProyecto").value;

    mostrarLoader();
    await sleep(1000);

    fetch("/api/proyectos/",{
        method: "POST",
        headers:{
            "Content-Type":"application/json",
        },
        body: JSON.stringify({
            nombre:nombre,
            descripcion:descripcion
        }),
    })
    .then((res)=>res.json())
    .then(()=>{
        cargarProyectos();
        document.getElementById("formProyecto").reset();
    })
    .finally(()=>ocultarLoader());
});

//eliminar proyecto
async function eliminarProyecto(id){
    if (!confirm("Eliminar proyecto")) return;

    mostrarLoader();
    await sleep(1000);
    fetch(`/api/proyectos/${id}/`,{
        method:"DELETE",
    })
    .then((res)=>res.json())
    .then((data)=>{
        console.log(data);
        cargarProyectos();
    })
    .catch((err)=>console.error("Error eliminando proyecto: ",err))
    .finally(()=>ocultarLoader());
}

// editar proyecto
async function editarProyecto(id, nombreActual, descripcionActual){
    const nuevoNombre = prompt("Nuevo nombre:", nombreActual);
    if (nuevoNombre===null) return;

    const nuevaDescripcion = prompt("Nueva descripcion:", descripcionActual);
    if (nuevaDescripcion === null) return;

    mostrarLoader();
    await sleep(1000);

    fetch(`/api/proyectos/${id}/`,{
        method: "PUT",
        headers: {
            "Content-Type":"application/json",
        },
        body: JSON.stringify({
            nombre: nuevoNombre,
            descripcion: nuevaDescripcion
        })
    })
    .then((res)=>res.json())
    .then((data)=>{
        console.log("Actualizado: ",data);
        cargarProyectos();
    })
    .catch((err)=>console.error("Error actualizando proyecto:",err))
    .finally(()=>ocultarLoader());
}

// funcion cuando selecciona un proyecto para capturar su id
async function seleccionProyecto(id,Proyecto){
    cargarProyectosTareas(id);
    // crear una nueva funcion que recargue la lista de tareas pero que aparezca un boton para asignalar al proyecto
    cargarTareas_id_proyecto(id);
    const h3 = document.getElementById('titleTareasProyectos');
    h3.textContent = `Tareas: ${Proyecto}`;
}


// TAREAS -----------------------------------------------------------------
async function cargarTareas() {
  mostrarLoader();
  await sleep(1000); // efecto visual

  fetch("/api/tareas/")
    .then((res) => res.json())
    .then((data) => {
      const tbody = document.getElementById("tabletareas");
      tbody.innerHTML = "";

      data.forEach((t) => {
            const tr= document.createElement("tr");
            tr.innerHTML = `
                <td>${t.id}</td>
                <td class="container">
                        <p class="fw-bold">${t.titulo}</p>
                        <p>${t.instrucciones}</p>
                        <p>${t.fecha_creacion}</p>
                </td>
                <td class="d-flex flex-column gap-2">
                    <button class="btn btn-sm btn-warning me-2"
                        onclick="editarTarea(${t.id},'${t.titulo}','${t.instrucciones || ""}')"
                    >
                    Editar
                    </button>
                    <button class="btn btn-sm btn-danger me-2"
                        onclick="eliminarTarea(${t.id})"
                    >
                    Eliminar
                    </button>
                </td>
            `;
            tbody.appendChild(tr);
      });
    })
    .finally(() => ocultarLoader());
}

//crear tarea
document.getElementById("formTarea").addEventListener("submit",async function(e){
    e.preventDefault();

    const titulo = document.getElementById("tituloTarea").value;
    const instrucciones = document.getElementById("instruccionTarea").value;

    mostrarLoader();
    await sleep(1000);

    fetch("/api/tareas/",{
        method: "POST",
        headers:{
            "Content-Type":"application/json",
        },
        body: JSON.stringify({
            titulo:titulo,
            instrucciones:instrucciones
        }),
    })
    .then((res)=>res.json())
    .then(()=>{
        cargarTareas();
        document.getElementById("formTarea").reset();
    })
    .finally(()=>ocultarLoader());
});

//eliminar tarea
async function eliminarTarea(id){
    if (!confirm("Eliminar Tarea")) return;

    mostrarLoader();
    await sleep(1000);
    fetch(`/api/tareas/${id}/`,{
        method:"DELETE",
    })
    .then((res)=>res.json())
    .then((data)=>{
        console.log(data);
        cargarTareas();
    })
    .catch((err)=>console.error("Error eliminando tarea: ",err))
    .finally(()=>ocultarLoader());
}

//editar tarea

async function editarTarea(id, tituloActual, instruccionActual){
    const nuevoTitulo = prompt("Nuevo Titulo:", tituloActual);
    if (nuevoTitulo===null) return;

    const nuevasInstrucciones = prompt("Nueva instruccion:", instruccionActual);
    if (nuevasInstrucciones === null) return;

    mostrarLoader();
    await sleep(1000);

    fetch(`/api/tareas/${id}/`,{
        method: "PUT",
        headers: {
            "Content-Type":"application/json",
        },
        body: JSON.stringify({
            titulo: nuevoTitulo,
            instrucciones: nuevasInstrucciones
        })
    })
    .then((res)=>res.json())
    .then((data)=>{
        console.log("Actualizado: ",data);
        cargarTareas();
    })
    .catch((err)=>console.error("Error actualizando tarea:",err))
    .finally(()=>ocultarLoader());
}

async function cargarTareas_id_proyecto(id) {
  mostrarLoader();
  await sleep(1000); // efecto visual

  fetch("/api/tareas/")
    .then((res) => res.json())
    .then((data) => {
      const tbody = document.getElementById("tabletareas");
      tbody.innerHTML = "";

      data.forEach((t) => {
            const tr= document.createElement("tr");
            tr.innerHTML = `
                <td>${t.id}</td>
                <td class="container">
                        <p class="fw-bold">${t.titulo}</p>
                        <p>${t.instrucciones}</p>
                        <p>${t.fecha_creacion}</p>
                </td>
                <td class="d-flex flex-column gap-2">
                    <button class="btn btn-sm btn-warning me-2"
                        onclick="editarTarea(${t.id},'${t.titulo}','${t.instrucciones || ""}')"
                    >
                    Editar
                    </button>
                    <button class="btn btn-sm btn-danger me-2"
                        onclick="eliminarTarea(${t.id})"
                    >
                    Eliminar
                    </button>
                    <button class="btn btn-sm btn-primary me-2"
                       onclick="asignarTareaProyecto(${t.id},${id})"
                    >
                    Asignar
                    </button>
                </td>
            `;
            tbody.appendChild(tr);
      });
    })
    .finally(() => ocultarLoader());
}

// Tareas Proyectos -------------------------------------------------------------
async function cargarProyectosTareas(id) {

  mostrarLoader();
  await sleep(1000); // efecto visual

  fetch(`/api/proyectostareas/${id}/`)
    .then((res) => res.json())
    .then((data) => {
      const tbody = document.getElementById("tabletareasproyectos");
      tbody.innerHTML = "";

      data.forEach((p) => {
            const tr= document.createElement("tr");
            tr.innerHTML = `
                <td>${p.id}</td>
                <td class="container">
                        <p class="fw-bold">${p.tarea_titulo}</p>
                        <p><span class="fw-bold">Prioridad:</span> ${p.prioridad}</p>
                        <p>${p.fecha_creacion}</p>
                </td>
                <td class="d-flex flex-column gap-2">
                    <button class="btn btn-sm btn-danger me-2"
                        onclick="eliminarTareaProyecto(${p.id},${p.proyecto_id})"
                    >
                    Eliminar
                    </button>
                    <button class="btn btn-sm btn-primary me-2"
                        
                    >
                    Usuarios
                    </button>
                </td>
            `;
            //onclick="eliminarProyecto(${p.id})"
            tbody.appendChild(tr);
      });
    })
    .finally(() => ocultarLoader());
}

// asignar tarea a proyecto 
async function asignarTareaProyecto(idTarea, idProyecto){
 
    const prioridad = prompt("Prioridad:", '');
    if (prioridad === null) return;

    mostrarLoader();
    await sleep(1000);

    fetch(`/api/proyectostareas/`,{
        method: "POST",
        headers: {
            "Content-Type":"application/json",
        },
        body: JSON.stringify({
            proyecto_id: idProyecto,
            tarea_id: idTarea,
            prioridad:prioridad
        })
    })
    .then((res)=>res.json())
    .then((data)=>{
        console.log("Creado: ",data);
        cargarTareas();
    })
    .catch((err)=>console.error("Error asignando tarea:",err))
    .finally(()=>ocultarLoader());

    cargarProyectosTareas(idProyecto);
}

// eliminar tarea de proyecto
async function eliminarTareaProyecto(id, idProyecto){
 
    if (!confirm("Eliminar Tarea del proyecto?")) return;

    mostrarLoader();
    await sleep(1000);

    fetch(`/api/proyectostareas/${id}/`,{
        method: "DELETE"
    })
    .then((res)=>res.json())
    .then((data)=>{
        cargarProyectosTareas(idProyecto);
    })
    .catch((err)=>console.error("Error eliminando tarea del proyecto:",err))
    .finally(()=>ocultarLoader());

    
}

// ---- INICIAL ----
cargarProyectos();
cargarTareas();
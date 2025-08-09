from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Persona, ResultadoProceso
from .forms import FormularioPersona
from django.http import HttpResponse

def inicio_sesion(request):
    if request.method == 'POST':
        usuario = request.POST['username']
        clave = request.POST['password']
        usuario_autenticado = authenticate(request, username=usuario, password=clave)
        if usuario_autenticado:
            login(request, usuario_autenticado)
            return redirect('lista_personas')
    return render(request, 'gestion/inicio_sesion.html')

def cerrar_sesion(request):
    logout(request)
    return redirect('inicio_sesion')

@login_required
def lista_personas(request):
    personas = Persona.objects.all()
    return render(request, 'gestion/lista_personas.html', {'personas': personas})

@login_required
def crear_persona(request):
    if request.method == 'POST':
        formulario = FormularioPersona(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('lista_personas')
    else:
        formulario = FormularioPersona()
    return render(request, 'gestion/crear_persona.html', {'formulario': formulario})

@login_required
def editar_persona(request, id):
    persona = get_object_or_404(Persona, id=id)
    if request.method == 'POST':
        formulario = FormularioPersona(request.POST, instance=persona)
        if formulario.is_valid():
            formulario.save()
            return redirect('lista_personas')
    else:
        formulario = FormularioPersona(instance=persona)
    return render(request, 'gestion/editar_persona.html', {'formulario': formulario})

@login_required
def eliminar_persona(request, id):
    persona = get_object_or_404(Persona, id=id)
    persona.delete()
    return redirect('lista_personas')


@login_required
def reporte_sin_template(request):
    resultados = ResultadoProceso.objects.all()

    html = """
    <html>
    <head>
      <title>Reporte de Resultados</title>
      <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f7f7f7; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
        th { background-color: #007bff; color: white; }
        .exito { background-color: #d4edda; color: #155724; }
        .fallo { background-color: #f8d7da; color: #721c24; }
      </style>
    </head>
    <body>
      <h1>Reporte de Resultados de Procesos Automatizados</h1>
      <table>
        <thead>
          <tr><th>Fecha</th><th>Paso</th><th>Estado</th><th>Mensaje</th></tr>
        </thead>
        <tbody>
    """

    for r in resultados:
        clase = "exito" if r.exito else "fallo"
        estado = "Éxito" if r.exito else "Fallo"
        html += f"""
          <tr class="{clase}">
            <td>{r.fecha}</td>
            <td>{r.paso}</td>
            <td>{estado}</td>
            <td>{r.mensaje}</td>
          </tr>
        """

    html += """
        </tbody>
      </table>
    </body>
    </html>
    """

    return HttpResponse(html)

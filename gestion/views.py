from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Persona
from .forms import FormularioPersona

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

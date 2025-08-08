from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio_sesion, name='inicio_sesion'),
    path('cerrar/', views.cerrar_sesion, name='cerrar_sesion'),
    path('personas/', views.lista_personas, name='lista_personas'),
    path('crear/', views.crear_persona, name='crear_persona'),
    path('editar/<int:id>/', views.editar_persona, name='editar_persona'),
    path('eliminar/<int:id>/', views.eliminar_persona, name='eliminar_persona'),
]

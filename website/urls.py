# Archivo que defina las vistas de cada página

from django.urls import path
from . import views

urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('listETS/', views.ListETSView.as_view(), name='listETS'),
    path('Alumno/', views.AlumnoView.as_view(), name='alumno'),
    path('Docente/', views.DocenteView.as_view(), name='docente'),
    path('PS/', views.PSView.as_view(), name='ps'),
    path('PETS/', views.PETSView.as_view(), name='pets'),
    path('NPETS/', views.NPETSView.as_view(), name='npets'),
    path('NETS/', views.NETSView.as_view(), name='nets'),
    path('NPS/', views.NPSView.as_view(), name='nps'),
    path('NDocente/', views.NDocenteView.as_view(), name='ndocente'),
    path('NAlumno/', views.NAlumnoView.as_view(), name='nalumno'),
    path('NVAlumno/', views.CargarAlumnoView.as_view(), name='nvalumno'),
    path('NDAlumno/', views.CargarDatosView.as_view(), name='ndalumno'),
    path('NInscripciones/', views.NInsView.as_view(), name='ninscripciones'),
    path('Inscripciones/', views.InsView.as_view(), name='inscripciones'),
    path('carreras/', views.carreras, name='carreras'),
    path('api/obtener-imagen/', views.obtener_imagen, name='obtener_imagen'),
]
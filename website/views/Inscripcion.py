import requests
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render, redirect
from .url import url
from ..forms import InscripcionForm
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

class InsView(View):
    """
        Clase que define la vista del listado de las inscripciones registradoa
    """
    def get(self, request, *args, **kwargs):
        """
            Función get de la vista encargada de renderizar la página html
        """
        usuario = request.session.get("usuario")

        api = f"inscripciones/{usuario}"
        
        headers = {"Content-Type": "application/json"}
        
        response = requests.get(url+api, headers=headers)
        
        context = {
            "DetailInscripciones": response.json()
        }
        
        return render(request, 'Inscripcion.html', context)

class NInsView(View):
    """
        Clase que define la vista del formulario de alta de Inscripciones
    """
    def get(self, request, *args, **kwargs):
        """
            Función para cargar la vista de la página html con el formulario
        """
        usuario = request.session.get("usuario")
        
        form = InscripcionForm(user=usuario)
        return render(request, "New_Inscripcion.html", { 'form': form })
        
    def post(self, request, *args, **kwargs):
        """
            Función post para procesar los datos enviados del formulario
        """
        
        usuario = request.session.get("usuario")
        
        api = "nIns"
        form = InscripcionForm(request.POST, user=usuario)
        
        if (form.is_valid()):
            alumno = form.cleaned_data['alumnos']
            ets = form.cleaned_data['ets']
            idPeriodo = form.cleaned_data['idPeriodo']
            turno = form.cleaned_data['turno']
        
            data = {
                "boleta": alumno,
                "ets": ets,
                "periodo": idPeriodo,
                "turno": turno,
                "user": usuario
            }
            
            headers = {"Content-Type": "application/json"}
            response = requests.post(url+api, json=data, headers=headers)
            response_data = response.json()
            
            print(response_data)
            
            if response_data.get("Error"):
                return render(request, 'New_Inscripcion.html', {'form': form, 'message': response_data.get("message"), 'Error': response_data.get("Error") })
            else:
                return render(request, 'New_Inscripcion.html', {'form': form, 'message': response_data.get("message")})
        else:
            print("Error en el formulario:", form.errors)
            return render(request, 'New_Inscripcion.html', {'form': form})
        
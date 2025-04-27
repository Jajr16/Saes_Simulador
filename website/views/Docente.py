import requests
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render, redirect
from .url import url
from ..forms import NDocenteForm

class DocenteView(View):
    """
        Clase que define la vista del listado de los docentes registrados
    """
    def get(self, request, *args, **kwargs):
        """
            Función get de la vista encargada de renderizar la página html
        """

        api = "docentes"
        
        headers = {"Content-Type": "application/json"}
        
        response = requests.get(url+api, headers=headers)
        
        print(response.json())
        
        context = {
            "DetailDocentes": response.json()
        }
        
        return render(request, 'Docente.html', context)
    
class NDocenteView(View):
    """
        Clase que define la vista del formulario de alta de Docentes
    """
    def get(self, request, *args, **kwargs):
        """
            Función para cargar la vista de la página html con el formulario
        """
        form = NDocenteForm()
        return render(request, "New_Docente.html", { 'form': form })
    
    def post(self, request, *args, **kwargs):
        """
            Función post para procesar los datos enviados del formulario
        """
        api = "nd"
        form = NDocenteForm(request.POST)
        
        if (form.is_valid()):
            curp = form.cleaned_data['curp']
            rfc = form.cleaned_data['rfc']
            nombre = form.cleaned_data['nombre']
            apellido_P = form.cleaned_data['apellido_P']
            apellido_M = form.cleaned_data['apellido_M']
            sexo = form.cleaned_data['sexo']
            correo = form.cleaned_data['correo']
            cargo = form.cleaned_data['cargo']
            turno = form.cleaned_data['turno']
            usuario = request.session.get('usuario')  
            
            data = {
                "curp": curp,
                "rfc": rfc,
                "nombre": nombre,
                "apellido_p": apellido_P,
                "apellido_m": apellido_M,
                "sexo": sexo,
                "correo": correo,
                "cargo": cargo,
                "turno": turno,
                "user": usuario
            }
            
            headers = {"Content-Type": "application/json"}
            response = requests.post(url+api, json=data, headers=headers)
            response_data = response.json()
            
            print(response_data)
            
            if response_data.get("Error"):
                return render(request, 'New_Docente.html', {'form': form, 'message': response_data.get("message"), 'Error': response_data.get("Error") })
            else:
                return render(request, 'New_Docente.html', {'form': form, 'message': response_data.get("message")})
        else:
            print("Error en el formulario:", form.errors)
            return render(request, 'New_Docente.html', {'form': form})
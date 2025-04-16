import requests
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render, redirect
from .url import url
from ..forms import NPSForm

class PSView(View):
    """
        Clase que define la vista del listado del personal de seguridad
    """
    def get(self, request, *args, **kwargs):
        """
            Función get de la vista encargada de renderizar la página html
        """
        api = "ps"
        
        headers = {"Content-Type": "application/json"}
        
        response = requests.get(url+api, headers=headers)
        
        context = {
            "DetailPS": response.json()
        }
        
        return render(request, 'PS.html', context)
    
class NPSView(View):
    """
        Clase que define la vista del formulario para la alta de nuevo personal de seguridad
    """
    def get(self, request, *args, **kwargs):
        """
            Función get de la vista encargada de renderizar la página html con el formulario vació para dar de alta personal de seguridad 
        """
        form = NPSForm()
        return render(request, 'New_PersonalSeguridad.html', {'form': form  })
    
    def post(self, request, *args, **kwargs):
        """
            Función post de la vista encargada de la lógica para el envío de la información del formulario
        """
        api = "nps"
        
        form = NPSForm(request.POST)
        
        if form.is_valid():
            rfc = form.cleaned_data['rfc']
            curp = form.cleaned_data['curp']
            nombre = form.cleaned_data['nombre']
            apellido_P = form.cleaned_data['apellido_P']
            apellido_M = form.cleaned_data['apellido_M']
            sexo = form.cleaned_data['sexo']
            cargoPS = form.cleaned_data['cargoPS']
            turno = form.cleaned_data['turno']
            usuario = request.session.get('usuario')  
            
            data = {
                "rfc": rfc,
                "curp": curp,
                "nombre": nombre,
                "apellido_P": apellido_P,
                "apellido_M": apellido_M,
                "sexo": sexo,
                "cargoPS": cargoPS,
                "turno": turno,
                "user": usuario
            }
            
            headers = {"Content-Type": "application/json"}
            response = requests.post(url+api, json=data, headers=headers)
            response_data = response.json()
            
            print(response_data)
            
            if response_data.get("Error"):
                return render(request, 'New_PersonalSeguridad.html', {'form': form, 'message': response_data.get("message"), 'Error': response_data.get("Error") })
            else:
                return render(request, 'New_PersonalSeguridad.html', {'form': form, 'message': response_data.get("message")})
        else:
            print("Error en el formulario:", form.errors)
            return render(request, 'New_PersonalSeguridad.html', {'form': form})
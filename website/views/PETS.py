import requests
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render, redirect
from .url import url
from ..forms import periodoForm

class PETSView(View):
    """
        Clase que define la vista del listado de los periodos de los ETS
    """
    def get(self, request, *args, **kwargs):
        """
            Función get de la vista encargada de renderizar la página html
        """
        
        api = "periodoETS"
        
        headers = {"Content-Type": "application/json"}
        
        response = requests.get(url+api, headers=headers)
        
        context = {
            "DetailPETS": response.json()
        }
        
        return render(request, 'PETS.html', context)
    
class NPETSView(View):
    """
        Clase que define la vista del formulario para la alta de los periodos de ETS 
    """
    def get(self, request, *args, **kwargs):
        """
            Función get de la vista encargada de renderizar la página html con el formulario vació para dar de alta los periodos de ETS 
        """
        form = periodoForm()
        return render(request, 'New_PETS.html', {'form': form  })
    
    def post(self, request, *args, **kwargs):
        """
            Función post de la vista encargada de la lógica para el envío de la información del formulario
        """
        api = "periodoETS"
        
        form = periodoForm(request.POST)
        
        if form.is_valid():
            periodo = form.cleaned_data['periodo']
            tipo = form.cleaned_data['tipo']
            fecha_I = form.cleaned_data['fecha_I'].strftime('%Y-%m-%d')
            fecha_F = form.cleaned_data['fecha_F'].strftime('%Y-%m-%d')
            
            data = {
                "idPeriodo": None,
                "periodo": periodo,
                "tipo": tipo[0],
                "fecha_Inicio": fecha_I,
                "fecha_Fin": fecha_F,
            }
            
            print(data)
            
            headers = {"Content-Type": "application/json"}
            response = requests.post(url+api, json=data, headers=headers)
            response_data = response.json() 
            
            if response_data.get("Error"):
                return render(request, 'New_PETS.html', {'form': form, 'message': response_data.get("message"), 'Error': response_data.get("Error") })
            else:
                return render(request, 'New_PETS.html', {'form': form, 'message': response_data.get("message")})
        else:
            print("Error en el formulario:", form.errors)
            return render(request, 'New_PETS.html', {'form': form})
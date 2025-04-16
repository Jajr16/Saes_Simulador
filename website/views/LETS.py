import requests
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render, redirect
from .url import url
from ..forms import ETSForm

class ListETSView(View):
    """
        Clase que define la vista del listado de los ETS registrados
    """
    def get(self, request, *args, **kwargs):
        """
            Función get de la vista encargada de renderizar la página html
        """
        api = "ets"
        
        headers = {"Content-Type": "application/json"}
        
        response = requests.get(url+api, headers=headers)
        
        context = {
            'DetallesETS': response.json()
        }
        
        return render(request, 'ETS.html', context)
    
class NETSView(View):
    """
        Clase que define la vista del formulario de los ETS 
    """
    def get(self, request, *args, **kwargs):
        """
            Función get de la vista encargada de renderizar la página html con el formulario vació para dar de alta ETS
        """
        form = ETSForm()
        return render(request, 'New_ETS.html', {'form': form  })
    
    def post(self, request, *args, **kwargs):
        """
            Función post de la vista encargada de la lógica para el envío de la información del formulario
        """
        api = "NETS"
        
        form = ETSForm(request.POST)
        
        if form.is_valid():
            idPeriodo = int(form.cleaned_data['idPeriodo'])
            turno = form.cleaned_data['Turno']
            fecha = form.cleaned_data['Fecha'].strftime('%Y-%m-%d')
            hora = form.cleaned_data['hora'].strftime('%H:%M')
            cupo = form.cleaned_data['Cupo']
            idUA = form.cleaned_data['idUA']
            duracion = form.cleaned_data['Duracion']
            
            data = {
                "idPeriodo": idPeriodo,
                "turno": turno,
                "fecha": fecha,
                "hora": hora,
                "cupo": cupo,
                "idUA": idUA,
                "duracion": duracion,
            }
            
            if form.cleaned_data['salon']:
                data["salon"] = int(form.cleaned_data['salon'])
                
            if form.cleaned_data['docente']:
                data["docenteCURP"] = form.cleaned_data['docente']
                data["titular"] = True
            
            headers = {"Content-Type": "application/json"}
            response = requests.post(url+api, json=data, headers=headers)
            response_data = response.json()
            
            print(response_data)
            
            if response_data.get("Error"):
                return render(request, 'New_ETS.html', {'form': form, 'message': response_data.get("message"), 'Error': response_data.get("Error") })
            else:
                return render(request, 'New_ETS.html', {'form': form, 'message': response_data.get("message")})
        else:
            print("Error en el formulario:", form.errors)
            return render(request, 'New_ETS.html', {'form': form})
import requests
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render, redirect
from ..forms import LoginForm

class LoginView(View):
    """
        Clase que define la vista del formulario del Login 
    """
    def get(self, request, *args, **kwargs):
        """
        Muestra la página de login con su respectivo formulario.
        """
        form = LoginForm()
        
        return render(request, 'login.html', {'form': form  })
    
    def post(self, request, *args, **kwargs):
        """
            Función post de la vista encargada de la lógica para el envío de la información del formulario
        """

        # api_url = "https://springboot-java-production-1f4e.up.railway.app/login"
        api_url = "http://localhost:8080/login"
        
        form = LoginForm(request.POST)
        
        if form.is_valid():
            boleta = form.cleaned_data['boleta']
            contraseña = form.cleaned_data['contraseña']
            
            data = {
                "usuario": boleta,
                "password": contraseña,
            }

            headers = {"Content-Type": "application/json"}
            response = requests.post(api_url, json=data, headers=headers)
            response_data = response.json()
            
            if response_data.get("error_Code") == 0:
                request.session['usuario'] = response_data["usuario"]
                request.session['rol'] = response_data["rol"]
                
                return redirect('home')
            else: 
                return render(request, 'login.html', {'form': form, 'error_message': response_data.get("message")})
        else:
            print("Error en el formulario:", form.errors)
            captcha_error = form.errors.get("captcha", ["Captcha incorrecto"])[0]
            
            return render(request, 'login.html', {
                'form': form, 
                'error_message': captcha_error
            })

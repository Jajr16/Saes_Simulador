import requests
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render, redirect

class HomeView(View):
    """
        Clase que define la vista de la página principal
    """
    def get(self, request, *args, **kwargs):
        """
            Función get de la vista encargada de renderizar la página html
        """

        if 'usuario' not in request.session:
            return redirect('login')
        
        user_data = {
            'usuario': request.session.get('usuario'),
            'rol': request.session.get('rol'),
        }
        return render(request, 'home.html', user_data)
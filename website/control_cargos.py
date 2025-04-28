from django.shortcuts import redirect

def rol_cargo_context(request):
    return {
        'rol': request.session.get('rol', None),
        'cargos': request.session.get('cargos', []),
    }
    
def cargo_required(allowed_cargos=None):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            cargos = request.session.get('cargos', [])
            if any(cargo in cargos for cargo in allowed_cargos):
                return view_func(request, *args, **kwargs)
            return redirect('home') 
        return _wrapped_view
    return decorator
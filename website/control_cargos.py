from django.shortcuts import redirect

def rol_cargo_context(request):
    return {
        'rol': request.session.get('rol', None),
        'cargos': request.session.get('cargos', []),
    }

def cargo_required(allowed_roles=None):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            rol = request.session.get('rol', None) 
            
            if rol and (any(allowed_role in rol for allowed_role in allowed_roles) or rol in allowed_roles):
                return view_func(request, *args, **kwargs)
            
            return redirect('home')
        return _wrapped_view
    return decorator

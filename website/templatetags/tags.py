from django import template

register = template.Library()

@register.filter
def contiene_cargo(rol, texto_buscado):
    """Devuelve True si el rol contiene el texto_buscado."""
    if not rol:
        return False
    return texto_buscado in rol

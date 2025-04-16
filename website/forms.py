# Archivo para declarar todos los campos que tendrán los formularios

from django import forms
from captcha.fields import CaptchaField
from django.forms.widgets import DateInput
from datetime import date
from django.core.exceptions import ValidationError
from .views.url import url
import requests

def obtener_opciones(api_endpoint, id_key, label_key, user=None):
    """ Función para crear options de selects con base en los registros de la BD

    Args:
        api_endpoint (str): Endpoint al que se dirigirá para obtener los datos que se insertarán en el select 
        id_key (str): Valor que tendrá cada option del select
        label_key (str): Lo que dirá el option del select
    """
    
    if user:
        api_endpoint = f"{api_endpoint}/{user}"
    
    # Manda la solicitud GET al servidor de Java
    response = requests.get(url + api_endpoint)
    if response.status_code == 200: # Si la respuesta se procesa de manera correcta entra aquí
        
        json_data = response.json() # Convierte la respuesta a json
        print(f"RECIBE: {json_data}")
        
        # Crea los option del select
        opciones = [(str(item[id_key]), str(item[label_key])) for item in json_data if id_key in item and label_key in item] 
        
        print(f"Opciones generadas: {opciones}") 
        
        return [("", "Seleccione una opción...")] + opciones  # Agrega opción vacía al inicio
    
    return [("", "Seleccione una opción...")]

class LoginForm(forms.Form):
    """ 
        Clase que define el formulario de la página de Login
    """
    
    boleta = forms.CharField(max_length=100, label="Boleta", required=True)
    contraseña = forms.CharField(widget=forms.PasswordInput, required=True)
    captcha = CaptchaField()
    
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        
        self.fields['boleta'].widget.attrs.update({
            'class': 'textEntry',
            'style': 'width: 6rem; height: 0.5rem; border: 1px solid black;',
        })
        self.fields['contraseña'].widget.attrs.update({
            'class': 'passwordEntry',
            'style': 'width: 6rem; height: 0.5rem; border: 1px solid black;',
        })
        
        self.fields['captcha'].widget.attrs.update({
            'class': 'textEntry', 
            'id': 'captcha-id',
            'style': 'width: 6rem; height: 0.5rem; border: 1px solid black;',
        })
        
class periodoForm(forms.Form):
    """ 
        Clase que define el formulario de la página de la alta de periodos
    """
    
    OPCIONES = [
        ('', 'Seleccione el tipo de examen'),
        ('O', 'Ordinario'),
        ('E', 'Especial')
    ]
    
    periodo = forms.CharField(max_length=20, required=True)
    tipo = forms.ChoiceField(choices=OPCIONES, required=True)
    fecha_I = forms.DateField(
        widget=DateInput(attrs={'type': 'date', 
                                'class': 'form-control', 
                                'min': date.today().strftime('%Y-%m-%d'),
                                'id': 'fecha_fin'}), 
        input_formats=['%Y-%m-%d'],
        required=True)
    
    fecha_F = forms.DateField(
        widget=DateInput(attrs={'type': 'date', 
                                'class': 'form-control',
                                'min': date.today().strftime('%Y-%m-%d'),
                                'id': 'fecha_fin'}), 
        input_formats=['%Y-%m-%d'],
        required=True)
    
    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_I')
        fecha_fin = cleaned_data.get('fecha_F')

        if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
            raise ValidationError("La fecha de fin no puede ser anterior a la fecha de inicio.")

        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        super(periodoForm, self).__init__(*args, **kwargs)
        
class ETSForm(forms.Form):
    """ 
        Clase que define el formulario de la página de la alta de ETS
    """
    
    def __init__(self, *args, **kwargs):
        super(ETSForm, self).__init__(*args, **kwargs)

        self.fields['idPeriodo'].choices = obtener_opciones("PeriodoToETS", "idPeriodo", "periodo")
        self.fields['idUA'].choices = obtener_opciones("UAprenToETS", "idUA", "nombre")
        self.fields["docente"].choices = obtener_opciones("DocenteToETS", "curp", "nombre")
        self.fields['salon'].choices = obtener_opciones("SalonToETS", "numSalon", "numSalon")

    idPeriodo = forms.ChoiceField(label="Periodo")
    idUA = forms.ChoiceField(label="Unidad de Aprendizaje")
    Turno = forms.ChoiceField(
        choices=[("", "Seleccione un turno..."), ("Matutino", "Matutino"), ("Vespertino", "Vespertino")],
        label="Turno"
    )
    Fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date',
                                                        'min': date.today().strftime('%Y-%m-%d'),}))
    hora = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))  
    Cupo = forms.IntegerField(min_value=1)
    Duracion = forms.IntegerField(min_value=1)
    docente = forms.ChoiceField(label="Docente", required=False)
    salon = forms.ChoiceField(label="Salon", required=False)

class NPSForm(forms.Form):
    """ 
        Clase que define el formulario de la página de la alta de personal de seguridad
    """
    
    def __init__(self, *args, **kwargs):
        super(NPSForm, self).__init__(*args, **kwargs)

        self.fields['cargoPS'].choices = obtener_opciones('CargoToPS', 'nombre', 'nombre')
    
    rfc = forms.CharField(max_length=13, required=True, label='CURP')
    curp = forms.CharField(max_length=18, required=True, label='CURP')
    nombre = forms.CharField(required=True, label='Nombre')
    apellido_P = forms.CharField(required=True, label='apellido_P')
    apellido_M = forms.CharField(required=True, label='apellido_M')
    sexo = forms.ChoiceField(
        choices=[("", "Selecciona una opción..."), ("Masculino", "Masculino"), ("Femenino", "Femenino")],
        label="Sexo"
    )
    cargoPS = forms.ChoiceField(label='Cargo', required=True)
    turno = forms.ChoiceField(
        choices=[("", "Seleccione un turno..."), ("Matutino", "Matutino"), ("Vespertino", "Vespertino")],
        label="Turno"
    )

class NDocenteForm(forms.Form):
    """ 
        Clase que define el formulario de la página de la alta de docentes
    """
    
    def __init__(self, *args, **kwargs):
        super(NDocenteForm, self).__init__(*args, **kwargs)

        self.fields['cargo'].choices = obtener_opciones('CargoToDocente', 'cargo', 'cargo')
    
    curp = forms.CharField(max_length=18, required=True, label='CURP')
    rfc = forms.CharField(max_length=13, required=True, label='RFC')
    nombre = forms.CharField(required=True, label='Nombre')
    apellido_P = forms.CharField(required=True, label='apellido_P')
    apellido_M = forms.CharField(required=True, label='apellido_M')
    sexo = forms.ChoiceField(
        choices=[("", "Selecciona una opción..."), ("Masculino", "Masculino"), ("Femenino", "Femenino")],
        label="Sexo"
    )
    correo = forms.CharField(required=True, label='correo')
    cargo = forms.ChoiceField(label='Cargo', required=True)
    turno = forms.ChoiceField(
        choices=[("", "Seleccione un turno..."), ("Matutino", "Matutino"), ("Vespertino", "Vespertino")],
        label="Turno"
    )

class NAlumnoForm(forms.Form):
    """ 
        Clase que define el formulario de la página de la alta del alumno
    """
    
    def __init__(self, *args, **kwargs):
        super(NAlumnoForm, self).__init__(*args, **kwargs)

        self.fields['escuela'].choices = obtener_opciones('UAcademica', 'idEscuela', 'nombre')
        self.fields['carrera'].choices = obtener_opciones('AllprogramasAcademicos', 'idPA', 'nombre')
    
    curp = forms.CharField(max_length=18, required=True, label='CURP')
    boleta = forms.CharField(max_length=13, required=True, label='Boleta')
    nombre = forms.CharField(required=True, label='Nombre')
    apellido_P = forms.CharField(required=True, label='apellido_P')
    apellido_M = forms.CharField(required=True, label='apellido_M')
    sexo = forms.ChoiceField(
        choices=[("", "Selecciona una opción..."), ("Masculino", "Masculino"), ("Femenino", "Femenino")],
        label="Sexo"
    )
    correo = forms.CharField(required=True, label='correo')
    escuela = forms.ChoiceField(label='Cargo', required=True)
    carrera = forms.ChoiceField(label='carrera', required=True)

class NAlumnoVideoForm(forms.Form):
    """ 
        Clase que define el formulario de la página de la alta del alumno
    """
    
    def __init__(self, *args, **kwargs):
        super(NAlumnoVideoForm, self).__init__(*args, **kwargs)
    
    boleta = forms.CharField(max_length=13, required=True, label='Boleta')
    curp = forms.CharField(max_length=18, required=True, label='CURP')

class InscripcionForm(forms.Form):
    """ 
        Clase que define el formulario de la página que inscribirá alumnos a los ETS
    """
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(InscripcionForm, self).__init__(*args, **kwargs)

        self.fields['ets'].choices = obtener_opciones(f'etsperschool', 'idUA', 'nombre', self.user)
        self.fields['alumnos'].choices = obtener_opciones(f'studentperschool', 'boleta', 'nombre', self.user)
        self.fields['idPeriodo'].choices = obtener_opciones("PeriodoToETS", "idPeriodo", "periodo")
    
    alumnos = forms.ChoiceField(label='Alumno', required=True)
    ets = forms.ChoiceField(label='ETS', required=True)
    turno = forms.ChoiceField(
        choices=[("", "Seleccione un turno..."), ("Matutino", "Matutino"), ("Vespertino", "Vespertino")],
        label="Turno"
    )
    idPeriodo = forms.ChoiceField(label="Periodo")
    

from django.forms import DateInput, ModelForm
from .models import Representante, Alumno

# creando un modelform le colocamos el mismo nombre del models
class RepresentanteForm(ModelForm):
    class Meta:
        model = Representante
        fields = '__all__'

# creando un modelform le colocamos el mismo nombre del models
class AlumnoForm(ModelForm):
    class Meta:
        model = Alumno
        fields = '__all__'
        widgets = {
            'fecha_de_nacimiento': DateInput(attrs={'type' : 'date'}),
        }
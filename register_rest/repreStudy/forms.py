from django.forms import DateInput, ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Representante, Alumno

# creando formulario de registro
class CustomUserCreationForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
	def clean_email(self):
		email = self.cleaned_data['email']

		if User.objects.filter(email=email).exists():
			raise forms.ValidationError('Este correo electrónico ya está registrado')
		return email

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
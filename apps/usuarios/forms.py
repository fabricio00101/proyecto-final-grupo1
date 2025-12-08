from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group

class RegistroForm(UserCreationForm):
    """Formulario personalizado de registro con opción de perfil"""
    
    PERFIL_CHOICES = (
        ('miembro', 'Miembro (Solo comentar)'),
        ('colaborador', 'Colaborador (Crear y publicar artículos)'),
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Correo electrónico'
        })
    )
    
    perfil = forms.ChoiceField(
        choices=PERFIL_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'form-radio'
        }),
        label='¿Qué tipo de usuario deseas ser?',
        required=True
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'perfil')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar campos del formulario
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nombre de usuario'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmar contraseña'
        })
        
        # Agregar ayuda visual a los campos de contraseña
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
    
    def clean_email(self):
        """Validar que el email no esté registrado"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado.')
        return email
    
    def save(self, commit=True):
        """Guardar usuario con email"""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

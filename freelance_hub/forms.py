from django import forms
from .models import Proyecto

class FormularioProyecto(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'cliente': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'presupuesto': forms.TextInput(attrs={
                'class': 'form-control',
                'pattern': '[0-9\.]+',
                'title': 'Ingrese un valor numérico válido, mayor o igual a cero',
                # HTML5 validation para no permitir spinner pero forzar teclado numérico si se desea
                'inputmode': 'decimal'
            }),
            'fecha_inicio': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_limite': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'prioridad': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_presupuesto(self):
        presupuesto = self.cleaned_data.get('presupuesto')
        if presupuesto is None:
            raise forms.ValidationError("Debe ingresar un presupuesto válido.")
        if presupuesto < 0:
            raise forms.ValidationError("El presupuesto no puede ser negativo.")
        return presupuesto

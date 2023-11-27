from django import forms
from .models import DatosEntrega

class DatosEntregaForm(forms.ModelForm):
    class Meta:
        model = DatosEntrega
        fields = ['direccion_entrega', 'ciudad', 'codigo_postal', 'metodo_pago']
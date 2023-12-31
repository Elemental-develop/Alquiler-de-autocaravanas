from django import forms
from .models import DatosPedido, FormaEntrega, FormaPago

class DatosPedidoForm(forms.ModelForm):
    
    FORMAS_ENTREGA = [
        (FormaEntrega.ESTANDAR, 'Estándar'),
        (FormaEntrega.URGENTE, 'Urgente'),
        (FormaEntrega.VEINTICUATRO_HORAS, '24 horas'),
    ]

    forma_entrega = forms.ChoiceField(
        choices=FORMAS_ENTREGA,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Forma de Entrega*'
    )
    class Meta:
        model = DatosPedido
        fields = ['email', 'first_name', 'last_name', 'telefono', 'direccion_envio', 'direccion_facturacion', 'instrucciones_entrega', 'forma_entrega']
        
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        user = self.request.user
        if user.is_authenticated:
                
            # Aqui se autorrellena el formulario con informacion de la db
            db_data = {}
            db_data["email"] = user.email
            db_data["first_name"] = user.first_name
            db_data["last_name"] = user.last_name
            
            
            form_fields = self.fields
            
            for field, value in db_data.items():
                form_fields[field].initial = value
                form_fields[field].required = True
                
            # Campo no requerido
            form_fields["instrucciones_entrega"].required = False


class DatosPagoForm(forms.ModelForm):
    class Meta:
        model = DatosPedido
        fields = ['forma_pago']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agrega las opciones de forma de pago dinámicamente
        self.fields['forma_pago'].widget = forms.RadioSelect(
            choices=self.get_formas_pago_choices(),
            attrs={'class': 'form-check-input'}
        )

    def get_formas_pago_choices(self):
        # Agrega aquí cualquier lógica adicional para obtener opciones de forma de pago
        formas_pago = [
            (FormaPago.CONTRARREEMBOLSO, 'Contrareembolso'),
            (FormaPago.STRIPE, 'Pago con Stripe'),
        ]
        return formas_pago

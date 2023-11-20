from django import forms
from .models import DatosPedido

class DatosPedidoForm(forms.ModelForm):
    class Meta:
        model = DatosPedido
        fields = ['email', 'first_name', 'last_name', 'telefono', 'direccion_envio', 'direccion_facturacion', 'instrucciones_entrega']
        
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        user = self.request.user
        if user.is_authenticated:
            print("===DATOS USER")
            print(user.email)
            # Consultar los datos existentes en la base de datos y autorellenar los campos
                
            # Aqui se autorrellena el formulario con informacion de la db
            db_data = {}
            db_data["email"] = user.email
            db_data["first_name"] = user.first_name
            db_data["last_name"] = user.last_name
            
            
            form_fields = self.fields
            
            for field, value in db_data.items():
                form_fields[field].initial = value
                form_fields[field].required = True
            
            print("="*30)    
            print(form_fields["email"].initial)
                
            # Campo no requerido
            form_fields["instrucciones_entrega"].required = False
                
            
            """ for field_name, field in self.fields.items():
                if field_name != 'instrucciones_entrega' and db_data.get(field_name):
                    field.initial = db_data[field_name]
                    field.required = False  # No es necesario que el campo sea obligatorio si se autorellena """

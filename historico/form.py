from django import forms
from .models import HistorialPagos

# no se utiliza
class HistorialPagoForm(forms.ModelForm):
    class Meta:
        model = HistorialPagos
        fields = ['mesPago','formaPago','valorPago','aportePago','bSocialPago','mascotaPago','repatriacionPago','seguroVidaPago','coohopAporte','coohopBsocial','adicionalesPago']
        widgets = {
            'mesPago': forms.Select(
                attrs={
                    'class':'form-control',
                    'style':'text-transform: uppercase;',
                    # 'readonly':'readonly'
                }
            ),
            'formaPago': forms.Select(
                attrs={ 
                    'class':'form-control'
                }
            ),
            'valorPago': forms.NumberInput(
                attrs={
                    'class':'form-control',
                    'readonly':'readonly'
                }
            ),
            'aportePago': forms.NumberInput(
                attrs={ 
                    'class':'form-control',
                    'readonly':'readonly'
                }
            ),
            'bSocialPago': forms.NumberInput(
                attrs={ 
                    'class':'form-control',
                    'maxlength':'10',
                    'readonly':'readonly'
                }
            ),
            'mascotaPago': forms.NumberInput(
                attrs={
                    'class':'form-control',
                    'readonly':'readonly'
                }
            ),
            'repatriacionPago': forms.NumberInput(   
                attrs={
                    'class':'form-control',
                    'readonly':'readonly'
                }
            ),
            'seguroVidaPago': forms.NumberInput(
                attrs={ 
                    'class':'form-control',
                    'readonly':'readonly'
                }
            ),
            'coohopAporte': forms.NumberInput(
                attrs={ 
                    'class':'form-control',
                    'readonly':'readonly'
                }
            ),
            'coohopBsocial': forms.NumberInput(
                attrs={ 
                    'class':'form-control',
                    'readonly':'readonly'
                }
            ),
            'adicionalesPago': forms.NumberInput(
                attrs={ 
                    'class':'form-control',
                    'readonly':'readonly' 
                }
            ),
        }
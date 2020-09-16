from django import forms
from patients.models import Diagnostic

class DxRequestCreationForm(forms.ModelForm):

    class Meta:
        model = Diagnostic
        fields = ('recomendations',)
    
        

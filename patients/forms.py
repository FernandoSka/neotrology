from django import forms
from .models import User, Patient, DxRequest

class PatientCreationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
    )

    gender = forms.ChoiceField(choices = GENDER_CHOICES)

    password1 = forms.CharField(label=("Password"),
        widget=forms.PasswordInput)

    password2 = forms.CharField(label=("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=("Enter the same password as above, for verification."))
    

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                'Las contraseñas no coinciden',
                code='password_mismatch',
            )
        return password2

    def save(self):
        user = super(PatientCreationForm, self).save(commit = False)
        user.set_password(self.cleaned_data["password1"])
        user.save()
        patient = Patient(user=user, gender=self.cleaned_data["gender"])
        patient.save()


class DxRequestCreationForm(forms.ModelForm):

    class Meta:
        model = DxRequest
        fields = ('weight', 'height')
        labels = {
            "weight": "Peso",
            "height": "Altura",
        }
        help_texts = {
            "weight": "Kg",
            "height": "cm",
        }
    
        

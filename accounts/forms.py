from django import forms
from .models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ["first_name", "last_name",
                  "username", "email", "password", "role"]

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        role = cleaned_data.get('role')
        print(role)

        if password != confirm_password:
            raise forms.ValidationError(
                "Passwords Do Not Match"
            )


class DataUpload(forms.ModelForm):
    profile_picture = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'btn btn-info'}))

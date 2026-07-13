from django import forms
import re

class RegisterForm(forms.Form):

    first_name = forms.CharField(
        max_length=100,
        label="First Name"
    )

    last_name = forms.CharField(
        max_length=100,
        label="Last Name"
    )

    username = forms.CharField(
        max_length=100,
        label="User Name"
    )

    email = forms.EmailField(
        label="Email"
    )

    phone = forms.CharField(
        max_length=10,
        label="Phone Number",
        widget=forms.TextInput(attrs={
            'type': 'tel',
            'maxlength': '10',
            'placeholder': 'Enter 10 Digit Phone Number'
        })
    )

    password = forms.CharField(
        label="Create Password",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Minimum 8 chars, 1 Capital, 1 Number, 1 Symbol'
        })
    )

    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput
    )

    def clean_phone(self):
        phone = self.cleaned_data['phone']

        if not phone.isdigit():
            raise forms.ValidationError(
                "Phone number must contain only numbers"
            )

        if len(phone) != 10:
            raise forms.ValidationError(
                "Phone number must be exactly 10 digits"
            )

        return phone

    def clean_password(self):
        password = self.cleaned_data['password']

        if len(password) < 8:
            raise forms.ValidationError(
                "Password must be at least 8 characters long"
            )

        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError(
                "Password must contain at least one capital letter"
            )

        if not re.search(r'[0-9]', password):
            raise forms.ValidationError(
                "Password must contain at least one number"
            )

        if not re.search(r'[@$!%*?&#]', password):
            raise forms.ValidationError(
                "Password must contain at least one special symbol"
            )

        return password
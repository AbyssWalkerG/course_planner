from django import forms

from .models import *


class Login(forms.Form):
    username = forms.CharField(
        label="User Name",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control required"}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control required"}),
    )


class Edit(forms.ModelForm):
    class Meta:
        model = User
        fields = ["password", "name", "email", "address", "phone"]
        laebls = {
            "password": "Password",
            "name": "Nick Name",
            "email": "Email",
            "address": "Address",
            "phone": "Phone number",
        }
        widgets = {
            "password": forms.PasswordInput(attrs={"class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.NumberInput(attrs={"class": "form-control"}),
        }

        # def clean_name(self):
        #     name = self.cleaned_data.get("name")
        #     result = User.objects.filter(name=name)
        #     if result:
        #         raise form.ValidationError("Name already exists")
        #     return name


class RegisterForm(forms.Form):
    username = forms.CharField(
        label="User Name",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    password1 = forms.CharField(
        label="Password",
        max_length=128,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    name = forms.CharField(
        label="Name",
        max_length=128,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    phone = forms.CharField(
        label="Phone Number",
        max_length=128,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    address = forms.CharField(
        label="Address",
        max_length=128,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")

        if len(username) < 1:
            raise forms.ValidationError(
                "Your username must be at least 6 characters long."
            )
        elif len(username) > 50:
            raise forms.ValidationError("The username is too long!")
        else:
            filter_result = User.objects.filter(username=username)
            if len(filter_result) > 0:
                raise forms.ValidationError("This username has been used!")
        return username

    def clean_name(self):
        name = self.cleaned_data.get("name")
        filter_result = User.objects.filter(name=name)
        if len(filter_result) > 0:
            raise forms.ValidationError("This nickname has been used!")
        return name

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 6:
            raise forms.ValidationError("Password is too short!")
        elif len(password1) > 20:
            raise forms.ValidationError("Password is too long!")
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password is incorrect，please input again!")
        return password2

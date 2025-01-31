from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from taxi.models import Driver, Car
from django.core.exceptions import ValidationError


class DriverCreateForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number"
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    LICENSE_LENGTH = 8

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != DriverLicenseUpdateForm.LICENSE_LENGTH:
            raise ValidationError(
                "License number must be only 8 characters"
            )
        for letter in list(license_number)[:3]:
            if letter != letter.upper():
                raise ValidationError(
                    "First 3 characters must be uppercase"
                )
        for letter in list(license_number)[3:8]:
            if letter.isdigit() is False:
                raise ValidationError(
                    "Last 5 characters must be digits"
                )


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"

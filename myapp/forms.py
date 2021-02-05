from django import forms
from django.forms import ModelForm
from .models import Polinja


class DocumentForm(forms.Form):
    docfile = forms.FileField(label="Select a file")


class PolinjaForm(ModelForm):
    class Meta:
        model = Polinja
        fields = [
            "Available_positions",
            "SKPvsESCO",
            "Languages",
            "Driving_licence",
            "Age_appropriateness",
            "Disability_appropriateness",
            "SKP_Wish",
            "BO_wishes_for_contract_type",
            "Job_contract_type",
            "BO_career_wishes",
            "Job_career_advancement",
            "BO_working_hours_wishes",
            "Job_working_hours",
            "MSO",
            "BO_wish_location",
        ]

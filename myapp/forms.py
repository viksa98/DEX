from django import forms
import pandas as pd
import os
from django.conf import settings


class DocumentForm(forms.Form):
    docfile = forms.FileField(label="Select a file")


class DexForm(forms.Form):
    def __init__(self, dex_attributes={}, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for k in dex_attributes.keys():
            vals = dex_attributes[k]
            vals.insert(0, "*")
            choices = list(zip(vals, vals))
            self.fields[k] = forms.ChoiceField(
                choices=choices, widget=forms.Select(attrs={"class": "form-control"})
            )


class DexForm2(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        occupations = pd.read_excel(os.path.join(settings.DATA_ROOT, "SKP_ESCO.xlsx"))
        vals = occupations["SKP poklic"].drop_duplicates()
        choices = list(zip(vals, vals))
        self.fields["skp_code"] = forms.ChoiceField(
            choices=choices, widget=forms.Select(attrs={"class": "form-control"})
        )

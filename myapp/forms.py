from django import forms

# Vo slucaj da treba file uplaod
# class DocumentForm(forms.Form):
#     docfile = forms.FileField(label="Select a file")

class DexForm(forms.Form):
    def __init__(self, dex_attributes={}, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for k in dex_attributes.keys():
            vals = dex_attributes[k]
            vals.insert(0,'*')
            choices = list(zip(vals,vals))
            self.fields[k] = forms.ChoiceField(choices=choices, widget=forms.Select(attrs={'class':'form-control'}))

from django import forms


class DatasetUploadForm(forms.Form):
    file = forms.FileField(
        label='Select File',
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.csv,.xlsx,.json'}),
    )

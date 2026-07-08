from django import forms
from .models import Pipeline, PipelineStep


class PipelineForm(forms.ModelForm):
    class Meta:
        model = Pipeline
        fields = ['name', 'description', 'output_format']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pipeline Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description (optional)'}),
            'output_format': forms.Select(attrs={'class': 'form-select'}),
        }


class PipelineStepForm(forms.ModelForm):
    class Meta:
        model = PipelineStep
        fields = ['operation', 'config']
        widgets = {
            'operation': forms.Select(attrs={'class': 'form-select'}),
            'config': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Configuration as JSON'}),
        }

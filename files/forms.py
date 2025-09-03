from django import forms
from .models import Document, Tenant, DocumentType

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['tenant', 'doc_type_fk', 'expiry_date', 'file']  # this is correct
        widgets = {
            'doc_type_fk': forms.Select(attrs={'class': 'select2'}),
            'tenant': forms.Select(attrs={'class': 'select2'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'doc_type_fk': 'Document Type',
            'expiry_date': 'Expiry Date',
            'file': 'Upload File',
        }

class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['name', 'email', 'tenant_type_fk']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'tenant_type_fk': forms.Select(attrs={'class': 'select2'}),
        }
        labels = {
            'name' : 'Tenant name',
            'email' : 'Email address',
            'tenant_type_fk' : 'Tenant type',
        }

class DocumentUploadForm(forms.Form):
    tenant = forms.ModelChoiceField(
        queryset=Tenant.objects.all(),
        widget=forms.Select(attrs={'class': 'select2'})
    )

# forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import Tenant, Unit

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['unit_id', 'size_sqm', 'size_sqft']
        widgets = {
            'unit_id': forms.TextInput(attrs={'class': 'form-control'}),
            'size_sqm': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'size_sqft': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

# Inline formset: connects Tenant ↔ Unit
UnitFormSet = inlineformset_factory(
    Tenant, Unit, form=UnitForm,
    extra=1,  # show 1 empty row by default
    can_delete=True
)

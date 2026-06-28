from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    # Honeypot anti-spam (caché côté template)
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'project_type', 'message']

    def clean_website(self):
        if self.cleaned_data.get('website'):
            raise forms.ValidationError('Spam détecté.')
        return ''

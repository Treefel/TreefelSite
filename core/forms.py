from django import forms
from core.models import FeedbackMessage


class FeedbackForm(forms.ModelForm):
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = FeedbackMessage
        fields = ["email", "subject", "body"]
        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": "Email (optional)"}),
            "subject": forms.TextInput(attrs={"placeholder": "Subject"}),
            "body": forms.Textarea(attrs={"placeholder": "Your message...", "rows": 5}),
        }

    def clean_honeypot(self):
        value = self.cleaned_data.get("honeypot")
        if value:
            raise forms.ValidationError("Bot detected.")
        return value

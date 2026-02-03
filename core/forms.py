from django import forms
from tinymce.widgets import TinyMCE
from core.models import FeedbackMessage, BlogPost, BlogCategory


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


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ["title", "body", "category", "tags", "header_image", "published"]
        widgets = {
            "body": TinyMCE(),
            "title": forms.TextInput(attrs={"placeholder": "Post title"}),
            "tags": forms.TextInput(attrs={"placeholder": "tag1, tag2, tag3"}),
            "header_image": forms.URLInput(attrs={"placeholder": "Header image URL (optional)"}),
        }


class BlogCategoryForm(forms.ModelForm):
    class Meta:
        model = BlogCategory
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Category name"}),
        }

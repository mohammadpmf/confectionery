from django import forms

from .models import ProductCustomUserComment, ProductAnanymousUserComment, SuggestionsCritics


class ProductCustomUserCommentForm(forms.ModelForm):
    class Meta:
        model = ProductCustomUserComment
        fields = ['text', 'dont_show_my_name', 'stars']


class ProductAnanymousUserCommentForm(forms.ModelForm):
    class Meta:
        model = ProductAnanymousUserComment
        fields = ['text', 'author']


class SuggestionsCriticsForm(forms.ModelForm):
    class Meta:
        model = SuggestionsCritics
        fields = ['name', 'email', 'subject', 'text']

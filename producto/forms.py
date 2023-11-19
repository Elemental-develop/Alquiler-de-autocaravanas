from django import forms

class OpinionForm(forms.Form):
    opinion = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True)

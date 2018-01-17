from django import forms

class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput, required=False)
    object_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    content = forms.CharField(label='', widget=forms.Textarea)
    # parent_id = forms.CharFiel(widget=forms.Testarea, required=False)

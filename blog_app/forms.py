from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    nombre = forms.CharField(max_length = 25)
    micorreo = forms.EmailField()
    para = forms.EmailField()
    comentario = forms.CharField(required = False,
                               widget = forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']


class SearchForm(forms.Form):
    query = forms.CharField()
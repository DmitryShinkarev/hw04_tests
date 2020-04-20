from django import forms
from posts.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('group', 'text')
        required = {'group': False, }
        widgets = {
            'text': forms.Textarea,
        }
from django import forms
from actualite.models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)
        # image = forms.ImageField()

from django import forms


class ArticlePostForm(forms.ModelForm):
    class Meta:
        fields = ('title', 'body', 'tags','img')

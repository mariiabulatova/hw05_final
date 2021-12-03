from django import forms
from django.forms import ModelForm

from .models import Comment, Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['group', 'text', 'image']
        help_texts = {
            'text': 'Введите текст',
            'group': 'Выберите группу',
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        text = forms.CharField(widget=forms.Textarea)

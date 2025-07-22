from django.forms import ModelForm
from django import forms

from .models import Post, PostAttachment


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ('body', 'is_private',)

    def clean_body(self):
        body = self.cleaned_data.get('body', '')
        if body and len(body.strip()) < 3:
            raise forms.ValidationError("Body must be at least 3 characters long.")
        return body


class AttachmentForm(ModelForm):
    class Meta:
        model = PostAttachment
        fields = ('image',)

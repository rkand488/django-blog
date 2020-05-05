from django import forms
from blog.models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        labels = {"text": "Post Content"}
        exclude = ['author', 'slug', 'updated_at']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        labels = {"text": "Comment"}
        exclude = ['post']
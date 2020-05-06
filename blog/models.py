from django.db import models
import re
from datetime import datetime
from django.utils import timezone
from django.template.defaultfilters import slugify

# Create your models here.
from django.contrib.auth.models import User
from blog.helper import HTMLStripper

STATUS_CHOICES = (
    (0, 'Draft'),
    (1, 'Publish'),
)


class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)

    class Meta:
        ordering = ["-created_at"]

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("view_post", args=[self.slug])

    def get_thumbnail(self):
        p = re.compile('src="(data:image\/[^;]+;base64[^"]+)"')
        matcher = p.findall(self.text)
        if len(matcher) > 0:
            return matcher[0]
        return '/static/images/logo.png'

    def excerpt(self):
        s = HTMLStripper()
        s.feed(self.text)
        no_tags = s.get_data()
        limit = 60
        append_str = "..."
        if len(no_tags) > limit:
            return no_tags[0:limit:]
        return no_tags + append_str

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    name = models.CharField(max_length=42)
    email = models.EmailField(max_length=75)
    website = models.URLField(max_length=200, null=True, blank=True)
    text = models.TextField()
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.text
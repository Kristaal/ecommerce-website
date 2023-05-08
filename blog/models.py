from django.db import models


class Post(models.Model):
    """
    A class to create Post model
    """
    title = models.CharField(max_length=100, unique=True)
    content = models.TextField(blank=False)
    excerpt = models.TextField(max_length=300, blank=False)
    featured_image = models.ImageField(
        'blog_image',
        null=True,
        blank=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return self.title

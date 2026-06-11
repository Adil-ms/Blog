from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


class Author(models.Model):
    name = models.CharField(max_length=128)
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Category(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=255)
    short_description = models.TextField()

    # CKEditor 5 field
    description = CKEditor5Field('Description')

    categories = models.ManyToManyField(Category)
    time_to_read = models.CharField(max_length=128)
    featured_image = models.ImageField(upload_to="posts/")
    is_draft = models.BooleanField(default=False)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    published_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title
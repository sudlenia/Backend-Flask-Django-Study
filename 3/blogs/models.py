from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from transliterate import translit


class Category(models.Model):
    name = models.CharField(max_length=120, verbose_name="Имя")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f"{self.name}"


class Tag(models.Model):
    name = models.CharField(max_length=120, verbose_name="Имя")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f"{self.name}"


class Comment(models.Model):
    body = models.TextField(max_length=255, verbose_name="Текст")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.body}"


class Post(models.Model):
    name = models.CharField(max_length=30, verbose_name="Имя")
    description = RichTextField()
    featured_image = models.ImageField(blank=True, default="default.jpg", upload_to="images/")
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    # def get_absolute_url(self):
    #     return reverse("post_detail", kwargs={"pk": self.pk})

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        slug_name = self.name
        self.slug = slugify(translit(slug_name, 'ru', reversed=True))
        super().save(*args, **kwargs)

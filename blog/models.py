from django.db import models
from django.urls import reverse
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(unique=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Catégorie'
        verbose_name_plural = 'Catégories'

    def get_absolute_url(self):
        return reverse('blog:category', args=[self.slug])

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=220)
    slug = models.SlugField(unique=True, max_length=240)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts',
    )
    author = models.CharField(max_length=120, default='Idohou Augustin')
    excerpt = models.CharField(max_length=300, help_text="Résumé affiché dans la liste.")
    content = models.TextField(help_text="Contenu HTML de l'article.")
    cover = models.ImageField(upload_to='blog/', blank=True)
    reading_time = models.PositiveSmallIntegerField(default=4, help_text="Temps de lecture (min)")
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    published_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-published_at']

    def get_absolute_url(self):
        return reverse('blog:detail', args=[self.slug])

    def __str__(self):
        return self.title


class PublishedPostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)

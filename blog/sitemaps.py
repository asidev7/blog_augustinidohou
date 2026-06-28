from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Category, Post


class PostSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return Post.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class BlogCategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return Category.objects.all()

    def location(self, obj):
        return obj.get_absolute_url()


class BlogIndexSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        return ['blog:list']

    def location(self, item):
        return reverse(item)

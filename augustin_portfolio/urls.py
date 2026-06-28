from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import TemplateView

from blog.sitemaps import BlogCategorySitemap, BlogIndexSitemap, PostSitemap
from core.sitemaps import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'blog': BlogIndexSitemap,
    'posts': PostSitemap,
    'blog_categories': BlogCategorySitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('blog/', include('blog.urls')),
    path(
        'sitemap.xml',
        sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap',
    ),
    path(
        'robots.txt',
        TemplateView.as_view(
            template_name='robots.txt',
            content_type='text/plain',
        ),
        name='robots',
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Category, Post


def post_list(request, category_slug=None):
    posts = Post.objects.filter(is_published=True).select_related('category')
    active_category = None
    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
        posts = posts.filter(category=active_category)

    featured = None
    if not category_slug:
        featured = posts.filter(is_featured=True).first()
        if featured:
            posts = posts.exclude(pk=featured.pk)

    paginator = Paginator(posts, 6)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj,
        'posts': page_obj.object_list,
        'featured': featured,
        'categories': Category.objects.all(),
        'active_category': active_category,
    }
    return render(request, 'blog/list.html', context)


def post_detail(request, slug):
    post = get_object_or_404(
        Post.objects.select_related('category'), slug=slug, is_published=True,
    )
    related = (
        Post.objects.filter(is_published=True, category=post.category)
        .exclude(pk=post.pk)[:2]
        if post.category else Post.objects.none()
    )
    return render(request, 'blog/detail.html', {'post': post, 'related': related})

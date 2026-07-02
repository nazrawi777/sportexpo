from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, render

from .models import BlogPost, HeroSlide, SponsorLogo


def get_category_counts():
    return (
        BlogPost.objects.filter(is_active=True)
        .values('category')
        .annotate(count=Count('id'))
        .order_by('category')
    )


def index(request):
    context = {
        'hero_slides': HeroSlide.objects.filter(is_active=True).order_by('order'),
        'sponsor_logos': SponsorLogo.objects.filter(is_active=True).order_by('order'),
        'latest_blog_posts': BlogPost.objects.filter(is_active=True).order_by('-published_date')[:3],
    }
    return render(request, 'index.html', context)


def blog(request):
    posts = BlogPost.objects.filter(is_active=True).order_by('-published_date')
    paginator = Paginator(posts, 6)
    page_obj = paginator.get_page(request.GET.get('page'))
    context = {
        'posts': page_obj,
        'category_counts': get_category_counts(),
    }
    return render(request, 'blog.html', context)


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_active=True)
    context = {
        'post': post,
        'category_counts': get_category_counts(),
    }
    return render(request, 'blog-single.html', context)

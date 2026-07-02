from django.core.paginator import Paginator
from django.db.models import Count, Prefetch
from django.shortcuts import get_object_or_404, render

from .models import BlogPost, GalleryImage, HeroSlide, ScheduleDay, ScheduleSpeaker, SponsorLogo


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


def simple_page(template_name):
    def view(request):
        return render(request, template_name)
    return view

about = simple_page('about.html')
visitor = simple_page('visitor.html')
media = simple_page('media.html')
sponsor = simple_page('sponsor.html')
hall = simple_page('hall.html')
contact = simple_page('contact.html')
terms_and_conditions = simple_page('terms-and-conditions.html')
not_found = simple_page('not-found.html')


def gallery(request):
    return render(request, 'gallery.html', {
        'gallery_images': GalleryImage.objects.filter(is_active=True).order_by('order', 'created_at'),
    })


def schedule(request):
    speakers = ScheduleSpeaker.objects.order_by('order', 'time_start')
    days = ScheduleDay.objects.prefetch_related(Prefetch('speakers', queryset=speakers)).order_by('order', 'date')
    return render(request, 'schedule.html', {'schedule_days': days})


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

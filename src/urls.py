from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('visitor/', views.visitor, name='visitor'),
    path('media/', views.media, name='media'),
    path('sponsor/', views.sponsor, name='sponsor'),
    path('hall/', views.hall, name='hall'),
    path('schedule/', views.schedule, name='schedule'),
    path('gallery/', views.gallery, name='gallery'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('contact/', views.contact, name='contact'),
    path('terms-and-conditions/', views.terms_and_conditions, name='terms_and_conditions'),
    path('not-found/', views.not_found, name='not_found'),
]

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify


class HeroSlide(models.Model):
    MEDIA_TYPE_IMAGE = 'image'
    MEDIA_TYPE_VIDEO = 'video'
    MEDIA_TYPE_CHOICES = [
        (MEDIA_TYPE_IMAGE, 'Image'),
        (MEDIA_TYPE_VIDEO, 'Video'),
    ]

    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default=MEDIA_TYPE_IMAGE)
    title = models.CharField(max_length=255)
    heading = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    countdown_date = models.DateTimeField()
    image = models.ImageField(upload_to='hero_slides/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    video = models.FileField(upload_to='hero_slides/videos/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return self.heading

    def get_image_url(self):
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        return None

    def get_media_url(self):
        if self.media_type == self.MEDIA_TYPE_VIDEO:
            if self.video:
                return self.video.url
            if self.video_url:
                return self.video_url
            return None
        return self.get_image_url()

    def clean(self):
        super().clean()
        if self.media_type == self.MEDIA_TYPE_IMAGE and not self.image and not self.image_url:
            raise ValidationError('An image or image URL is required for image hero slides.')
        if self.media_type == self.MEDIA_TYPE_VIDEO and not self.video and not self.video_url:
            raise ValidationError('A video or video URL is required for video hero slides.')


class SponsorLogo(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='sponsor_logos/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return self.name

    def get_image_url(self):
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        return None

    def clean(self):
        super().clean()
        if not self.image and not self.image_url:
            raise ValidationError('A logo image or image URL is required.')


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(max_length=100)
    author_name = models.CharField(max_length=255)
    published_date = models.DateField()
    excerpt = models.TextField()
    content = models.TextField()
    image = models.ImageField(upload_to='blog/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    def get_image_url(self):
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        return None

    def clean(self):
        super().clean()
        if not self.image and not self.image_url:
            raise ValidationError('A featured image or image URL is required.')

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while BlogPost.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

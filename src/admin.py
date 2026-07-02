from django.contrib import admin
from django.utils.html import format_html

from .models import BlogPost, GalleryImage, HeroSlide, ScheduleDay, ScheduleSpeaker, SponsorLogo


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ('media_preview', 'title', 'heading', 'media_type', 'countdown_date', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('media_type', 'is_active', 'countdown_date')
    search_fields = ('title', 'heading', 'location')
    ordering = ('order', 'created_at')
    readonly_fields = ('image_preview_large',)
    fieldsets = (
        ('Content', {'fields': ('title', 'heading', 'location', 'countdown_date')}),
        ('Media', {
            'description': 'Only the fields for the selected media type apply. Use image fields for image slides and video fields for video slides.',
            'fields': ('media_type', ('image', 'image_url'), ('video', 'video_url'), 'image_preview_large'),
        }),
        ('Display Settings', {'fields': ('order', 'is_active')}),
    )

    def media_preview(self, obj):
        if obj.media_type == HeroSlide.MEDIA_TYPE_VIDEO:
            return format_html('<span style="font-size: 24px;">🎬</span>')
        image_url = obj.get_image_url()
        if image_url:
            return format_html('<img src="{}" style="width: 60px; height: 40px; object-fit: cover; border-radius: 4px;" />', image_url)
        return 'No image'
    media_preview.short_description = 'Preview'

    def image_preview_large(self, obj):
        image_url = obj.get_image_url()
        if image_url:
            return format_html('<img src="{}" style="max-width: 300px; height: auto; border-radius: 6px;" />', image_url)
        return 'No image preview available'
    image_preview_large.short_description = 'Image Preview'


@admin.register(SponsorLogo)
class SponsorLogoAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'name', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    ordering = ('order', 'created_at')
    readonly_fields = ('image_preview_large',)
    fieldsets = (
        ('Sponsor Info', {'fields': ('name',)}),
        ('Logo Image', {'fields': ('image', 'image_url', 'image_preview_large')}),
        ('Display Settings', {'fields': ('order', 'is_active')}),
    )

    def image_preview(self, obj):
        image_url = obj.get_image_url()
        if image_url:
            return format_html('<img src="{}" style="width: 60px; height: 40px; object-fit: contain; border-radius: 4px;" />', image_url)
        return 'No image'
    image_preview.short_description = 'Preview'

    def image_preview_large(self, obj):
        image_url = obj.get_image_url()
        if image_url:
            return format_html('<img src="{}" style="max-width: 300px; height: auto; border-radius: 6px;" />', image_url)
        return 'No image preview available'
    image_preview_large.short_description = 'Image Preview'


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'title', 'category', 'author_name', 'published_date', 'order', 'is_active', 'created_at')
    list_editable = ('order', 'is_active')
    list_filter = ('category', 'is_active', 'published_date')
    search_fields = ('title', 'category', 'author_name', 'excerpt', 'content')
    ordering = ('-published_date',)
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    readonly_fields = ('image_preview_large',)
    fieldsets = (
        ('Content', {'fields': ('title', 'slug', 'category', 'author_name', 'published_date')}),
        ('Excerpt & Body', {'fields': ('excerpt', 'content')}),
        ('Featured Image', {'fields': ('image', 'image_url', 'image_preview_large')}),
        ('Display Settings', {'fields': ('is_active', 'order')}),
    )

    def image_preview(self, obj):
        image_url = obj.get_image_url()
        if image_url:
            return format_html('<img src="{}" style="width: 60px; height: 40px; object-fit: cover; border-radius: 4px;" />', image_url)
        return 'No image'
    image_preview.short_description = 'Preview'

    def image_preview_large(self, obj):
        image_url = obj.get_image_url()
        if image_url:
            return format_html('<img src="{}" style="max-width: 300px; height: auto; border-radius: 6px;" />', image_url)
        return 'No image preview available'
    image_preview_large.short_description = 'Image Preview'


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'title', 'tagline', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'tagline')
    ordering = ('order', 'created_at')
    readonly_fields = ('image_preview_large',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 60px; height: 40px; object-fit: cover; border-radius: 4px;" />', obj.image.url)
        return 'No image'
    image_preview.short_description = 'Preview'

    def image_preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 300px; height: auto; border-radius: 6px;" />', obj.image.url)
        return 'No image preview available'
    image_preview_large.short_description = 'Image Preview'


class ScheduleSpeakerInline(admin.TabularInline):
    model = ScheduleSpeaker
    extra = 1
    fields = ('image_preview', 'name', 'role', 'session_title', 'image', 'location', 'time_start', 'time_end', 'order')
    readonly_fields = ('image_preview',)
    ordering = ('order', 'time_start')

    def image_preview(self, obj):
        if obj and obj.image:
            return format_html('<img src="{}" style="width: 48px; height: 48px; object-fit: cover; border-radius: 50%;" />', obj.image.url)
        return 'No image'
    image_preview.short_description = 'Preview'


@admin.register(ScheduleDay)
class ScheduleDayAdmin(admin.ModelAdmin):
    list_display = ('date', 'day_label', 'order')
    list_editable = ('day_label', 'order')
    ordering = ('order', 'date')
    inlines = (ScheduleSpeakerInline,)


@admin.register(ScheduleSpeaker)
class ScheduleSpeakerAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'name', 'role', 'session_title', 'day', 'time_start', 'time_end', 'order')
    list_editable = ('order',)
    list_filter = ('day',)
    search_fields = ('name', 'role', 'session_title', 'location')
    ordering = ('day__order', 'order', 'time_start')
    readonly_fields = ('image_preview_large',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 48px; height: 48px; object-fit: cover; border-radius: 50%;" />', obj.image.url)
        return 'No image'
    image_preview.short_description = 'Preview'

    def image_preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 220px; height: auto; border-radius: 6px;" />', obj.image.url)
        return 'No image preview available'
    image_preview_large.short_description = 'Image Preview'


admin.site.site_header = 'Sport Expo ET 2026 Admin'
admin.site.site_title = 'Sport Expo ET 2026'
admin.site.index_title = 'Sport Expo ET 2026 Dashboard'

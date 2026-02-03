from django.contrib import admin
from core.models import BlogCategory, BlogPost, GalleryItem, FeedbackMessage, SiteSetting


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "published", "created_at")
    list_filter = ("published", "category")
    search_fields = ("title", "body")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "media_type", "sort_order")
    list_filter = ("category", "media_type")
    list_editable = ("sort_order",)


@admin.register(FeedbackMessage)
class FeedbackMessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "email", "is_completed", "created_at")
    list_filter = ("is_completed",)
    readonly_fields = ("email", "subject", "body", "created_at")


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ("key", "value")

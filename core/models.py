from django.db import models
from django.utils.text import slugify


class BlogCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "blog categories"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    body = models.TextField()
    category = models.ForeignKey(
        BlogCategory, on_delete=models.SET_NULL, null=True, related_name="posts"
    )
    tags = models.CharField(max_length=500, blank=True)
    header_image = models.URLField(max_length=500, blank=True)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class GalleryItem(models.Model):
    CATEGORY_CHOICES = [("2D", "2D"), ("3D", "3D")]
    MEDIA_TYPE_CHOICES = [("image", "Image"), ("youtube", "YouTube")]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    image = models.URLField(max_length=500, blank=True)
    youtube_url = models.URLField(max_length=500, blank=True)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sort_order"]

    def __str__(self):
        return self.title


class FeedbackMessage(models.Model):
    email = models.EmailField(blank=True, default="")
    subject = models.CharField(max_length=200)
    body = models.TextField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.subject


class SiteSetting(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField(blank=True)

    def __str__(self):
        return self.key

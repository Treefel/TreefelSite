# Treefel.com Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a Django-powered personal website for digital artist Treefel with a blog, art gallery, feedback form, and admin pages.

**Architecture:** Django 5.x monolith with a single `core` app. Tailwind v4 for styling via standalone CLI (`pytailwindcss`). HTMX for interactive filtering and form submissions. TinyMCE for rich text editing. SQLite for now, Cloudflare R2 for media storage.

**Tech Stack:** Django 5.x, Tailwind CSS v4, HTMX, TinyMCE, SQLite, Cloudflare R2 (via django-storages), Pillow, django-ratelimit, pytailwindcss.

**Design doc:** `docs/plans/2026-02-03-treefel-website-design.md`

**Venv:** `C:/Projects/treefel/venv/` (Python 3.14.2, already created)

---

## Task 1: Project Scaffolding & Dependencies

**Files:**
- Create: `requirements.txt`
- Create: `treefel/treefel/settings.py` (via django-admin)
- Create: `treefel/treefel/urls.py` (via django-admin)
- Create: `treefel/core/` (via startapp)
- Create: `.gitignore`

**Step 1: Install Python dependencies**

```
pip install django django-htmx django-tinymce django-storages[s3] django-ratelimit pillow boto3 pytailwindcss gunicorn whitenoise python-dotenv
```

Run: `C:/Projects/treefel/venv/Scripts/pip.exe install django django-htmx django-tinymce "django-storages[s3]" django-ratelimit pillow boto3 pytailwindcss gunicorn whitenoise python-dotenv`

**Step 2: Freeze requirements**

Run: `C:/Projects/treefel/venv/Scripts/pip.exe freeze > C:/Projects/treefel/requirements.txt`

**Step 3: Create Django project**

Run: `cd C:/Projects/treefel && venv/Scripts/django-admin.exe startproject treefel .`

This creates `manage.py` and `treefel/` settings package in `C:/Projects/treefel/`.

Note: The project root IS `C:/Projects/treefel/`, so `manage.py` is at `C:/Projects/treefel/manage.py` and the settings package is at `C:/Projects/treefel/treefel/`.

**Step 4: Create the core app**

Run: `C:/Projects/treefel/venv/Scripts/python.exe C:/Projects/treefel/manage.py startapp core`

This creates `C:/Projects/treefel/core/`.

**Step 5: Create .gitignore**

Create `C:/Projects/treefel/.gitignore`:

```
# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
*.egg

# Virtual environment
venv/

# Django
db.sqlite3
*.log
media/

# Tailwind
node_modules/

# Environment
.env

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

**Step 6: Create .env file for local development**

Create `C:/Projects/treefel/.env`:

```
DJANGO_SECRET_KEY=dev-secret-key-change-in-production
DJANGO_DEBUG=True
```

**Step 7: Configure Django settings**

Modify `C:/Projects/treefel/treefel/settings.py`:

- Add to top: `from dotenv import load_dotenv; import os; load_dotenv()`
- Set `SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'fallback-dev-key')`
- Set `DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'`
- Add to `INSTALLED_APPS`:
  ```python
  'core',
  'django_htmx',
  'tinymce',
  'storages',
  ```
- Add `'django_htmx.middleware.HtmxMiddleware'` to `MIDDLEWARE` (after `SessionMiddleware`)
- Add `'whitenoise.middleware.WhiteNoiseMiddleware'` to `MIDDLEWARE` (after `SecurityMiddleware`)
- Set `STATIC_ROOT = BASE_DIR / 'staticfiles'`
- Set `STATICFILES_DIRS = [BASE_DIR / 'static']`
- Set `LOGIN_URL = '/accounts/login/'`
- Set `LOGIN_REDIRECT_URL = '/admin-blog/'`
- Set `ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')`
- Add TinyMCE config:
  ```python
  TINYMCE_DEFAULT_CONFIG = {
      'height': 400,
      'width': '100%',
      'menubar': False,
      'plugins': 'lists link image code',
      'toolbar': 'undo redo | bold italic underline | bullist numlist | link image | code',
      'content_css': '/static/css/tinymce-content.css',
  }
  ```

**Step 8: Configure project URLs**

Modify `C:/Projects/treefel/treefel/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('', include('core.urls')),
]
```

**Step 9: Create core app URL stub**

Create `C:/Projects/treefel/core/urls.py`:

```python
from django.urls import path

app_name = 'core'

urlpatterns = []
```

**Step 10: Verify server starts**

Run: `C:/Projects/treefel/venv/Scripts/python.exe C:/Projects/treefel/manage.py runserver --noreload`
Expected: Server starts at http://127.0.0.1:8000/ with no errors. Stop it after verifying.

**Step 11: Initialize git and commit**

```bash
cd C:/Projects/treefel
git init
git remote add origin https://github.com/Treefel/TreefelSite.git
git add .gitignore requirements.txt manage.py treefel/ core/ docs/
git commit -m "feat: initial Django project scaffolding with core app"
```

---

## Task 2: Data Models & Tests

**Files:**
- Modify: `C:/Projects/treefel/core/models.py`
- Create: `C:/Projects/treefel/core/tests/__init__.py`
- Create: `C:/Projects/treefel/core/tests/test_models.py`
- Modify: `C:/Projects/treefel/core/admin.py`

**Step 1: Write model tests**

Delete `C:/Projects/treefel/core/tests.py` and create `C:/Projects/treefel/core/tests/` directory.

Create `C:/Projects/treefel/core/tests/__init__.py` (empty).

Create `C:/Projects/treefel/core/tests/test_models.py`:

```python
from django.test import TestCase
from django.utils.text import slugify
from core.models import BlogCategory, BlogPost, GalleryItem, FeedbackMessage, SiteSetting


class BlogCategoryModelTest(TestCase):
    def test_create_category(self):
        cat = BlogCategory.objects.create(name="Dev Log")
        self.assertEqual(cat.name, "Dev Log")
        self.assertEqual(cat.slug, "dev-log")

    def test_str_representation(self):
        cat = BlogCategory.objects.create(name="Personal")
        self.assertEqual(str(cat), "Personal")

    def test_slug_auto_generated(self):
        cat = BlogCategory.objects.create(name="Interesting Finds")
        self.assertEqual(cat.slug, "interesting-finds")


class BlogPostModelTest(TestCase):
    def setUp(self):
        self.category = BlogCategory.objects.create(name="Dev Log")

    def test_create_post(self):
        post = BlogPost.objects.create(
            title="My First Post",
            body="<p>Hello world</p>",
            category=self.category,
        )
        self.assertEqual(post.title, "My First Post")
        self.assertEqual(post.slug, "my-first-post")
        self.assertFalse(post.published)

    def test_str_representation(self):
        post = BlogPost.objects.create(
            title="Test Post", body="body", category=self.category
        )
        self.assertEqual(str(post), "Test Post")

    def test_published_manager(self):
        BlogPost.objects.create(
            title="Draft", body="body", category=self.category, published=False
        )
        BlogPost.objects.create(
            title="Live", body="body", category=self.category, published=True
        )
        self.assertEqual(BlogPost.objects.filter(published=True).count(), 1)

    def test_ordering_by_created_at_desc(self):
        p1 = BlogPost.objects.create(
            title="First", body="body", category=self.category, published=True
        )
        p2 = BlogPost.objects.create(
            title="Second", body="body", category=self.category, published=True
        )
        posts = list(BlogPost.objects.all())
        self.assertEqual(posts[0], p2)


class GalleryItemModelTest(TestCase):
    def test_create_image_item(self):
        item = GalleryItem.objects.create(
            title="Landscape",
            description="A 3D landscape",
            category="3D",
            media_type="image",
            image="https://r2.example.com/landscape.jpg",
            sort_order=1,
        )
        self.assertEqual(item.title, "Landscape")
        self.assertEqual(item.category, "3D")

    def test_create_youtube_item(self):
        item = GalleryItem.objects.create(
            title="Timelapse",
            description="Speed modeling",
            category="3D",
            media_type="youtube",
            youtube_url="https://youtube.com/watch?v=abc123",
            sort_order=2,
        )
        self.assertEqual(item.media_type, "youtube")

    def test_str_representation(self):
        item = GalleryItem.objects.create(
            title="My Art", description="desc", category="2D",
            media_type="image", sort_order=1,
        )
        self.assertEqual(str(item), "My Art")

    def test_ordering_by_sort_order(self):
        i2 = GalleryItem.objects.create(
            title="Second", description="d", category="2D",
            media_type="image", sort_order=2,
        )
        i1 = GalleryItem.objects.create(
            title="First", description="d", category="2D",
            media_type="image", sort_order=1,
        )
        items = list(GalleryItem.objects.all())
        self.assertEqual(items[0], i1)


class FeedbackMessageModelTest(TestCase):
    def test_create_message(self):
        msg = FeedbackMessage.objects.create(
            subject="Hello", body="Nice work!"
        )
        self.assertEqual(msg.subject, "Hello")
        self.assertFalse(msg.is_completed)
        self.assertEqual(msg.email, "")

    def test_create_message_with_email(self):
        msg = FeedbackMessage.objects.create(
            email="test@example.com", subject="Hi", body="Great art"
        )
        self.assertEqual(msg.email, "test@example.com")

    def test_str_representation(self):
        msg = FeedbackMessage.objects.create(subject="Test", body="body")
        self.assertEqual(str(msg), "Test")


class SiteSettingModelTest(TestCase):
    def test_create_setting(self):
        setting = SiteSetting.objects.create(
            key="feedback_welcome", value="Welcome! Leave a message."
        )
        self.assertEqual(setting.key, "feedback_welcome")

    def test_str_representation(self):
        setting = SiteSetting.objects.create(key="test_key", value="val")
        self.assertEqual(str(setting), "test_key")
```

**Step 2: Run tests to verify they fail**

Run: `C:/Projects/treefel/venv/Scripts/python.exe C:/Projects/treefel/manage.py test core.tests.test_models -v 2`
Expected: ImportError -- models don't exist yet.

**Step 3: Implement models**

Write `C:/Projects/treefel/core/models.py`:

```python
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
```

**Step 4: Create and run migrations**

Run: `C:/Projects/treefel/venv/Scripts/python.exe C:/Projects/treefel/manage.py makemigrations core`
Run: `C:/Projects/treefel/venv/Scripts/python.exe C:/Projects/treefel/manage.py migrate`

**Step 5: Run tests to verify they pass**

Run: `C:/Projects/treefel/venv/Scripts/python.exe C:/Projects/treefel/manage.py test core.tests.test_models -v 2`
Expected: All tests pass.

**Step 6: Create seed data command**

Create `C:/Projects/treefel/core/management/__init__.py` (empty).
Create `C:/Projects/treefel/core/management/commands/__init__.py` (empty).
Create `C:/Projects/treefel/core/management/commands/seed_data.py`:

```python
from django.core.management.base import BaseCommand
from core.models import BlogCategory, SiteSetting


class Command(BaseCommand):
    help = "Seed initial data for Treefel site"

    def handle(self, *args, **options):
        categories = ["Dev Log", "Personal", "Interesting Finds"]
        for name in categories:
            BlogCategory.objects.get_or_create(name=name)
            self.stdout.write(f"  Category: {name}")

        SiteSetting.objects.get_or_create(
            key="feedback_welcome",
            defaults={"value": "Have something to share? Drop a message below!"},
        )
        self.stdout.write(self.style.SUCCESS("Seed data created."))
```

**Step 7: Run seed command**

Run: `C:/Projects/treefel/venv/Scripts/python.exe C:/Projects/treefel/manage.py seed_data`
Expected: "Seed data created."

**Step 8: Commit**

```bash
git add core/ treefel/
git commit -m "feat: add data models with tests and seed data command"
```

---

## Task 3: Tailwind Setup & Base Template

**Files:**
- Create: `C:/Projects/treefel/static/css/input.css`
- Create: `C:/Projects/treefel/static/css/output.css` (generated)
- Create: `C:/Projects/treefel/static/css/tinymce-content.css`
- Create: `C:/Projects/treefel/core/templates/core/base.html`
- Create: `C:/Projects/treefel/core/templates/registration/login.html`

**Step 1: Initialize Tailwind**

Run: `C:/Projects/treefel/venv/Scripts/tailwindcss.exe init`

This creates a `tailwind.config.js` if using v3. For Tailwind v4, config is CSS-based. Check which version `pytailwindcss` installed.

Run: `C:/Projects/treefel/venv/Scripts/tailwindcss.exe --help` to verify CLI works.

**Step 2: Create Tailwind input CSS**

Create `C:/Projects/treefel/static/css/input.css`:

```css
@import "tailwindcss";

@theme {
  --color-primary: #87aa6c;
  --color-primary-light: #9dbe85;
  --color-primary-dark: #6e9455;
  --color-secondary: #567e54;
  --color-secondary-light: #6e9a6b;
  --color-secondary-dark: #3f5e3d;
  --color-tertiary: #cfdc7b;
  --color-tertiary-light: #dbe69e;
  --color-tertiary-dark: #b8c55a;
  --color-dark: #1a1a1a;
  --color-light: #f5f5f0;
  --color-light-dim: #e8e8e0;

  --font-heading: "Stick", sans-serif;
  --font-body: "Poor Story", cursive;
}

/* Base styles */
body {
  font-family: var(--font-body);
  color: var(--color-dark);
  background-color: var(--color-light);
}

h1, h2, h3, h4, h5, h6 {
  font-family: var(--font-heading);
}
```

Note: If `pytailwindcss` ships Tailwind v3, use `@tailwind base; @tailwind components; @tailwind utilities;` syntax instead and create a `tailwind.config.js` with the theme. The implementing engineer should check the version and adjust accordingly.

**Step 3: Build Tailwind CSS**

Run: `C:/Projects/treefel/venv/Scripts/tailwindcss.exe -i C:/Projects/treefel/static/css/input.css -o C:/Projects/treefel/static/css/output.css --content "C:/Projects/treefel/core/templates/**/*.html"`

This generates the compiled CSS. During development, run with `--watch` flag.

**Step 4: Create TinyMCE content CSS**

Create `C:/Projects/treefel/static/css/tinymce-content.css`:

```css
@import url('https://fonts.googleapis.com/css2?family=Poor+Story&display=swap');

body {
  font-family: "Poor Story", cursive;
  font-size: 1.1rem;
  line-height: 1.7;
  color: #1a1a1a;
  padding: 0.5rem;
}
```

**Step 5: Create base template**

Create `C:/Projects/treefel/core/templates/core/base.html`.

Use @frontend-design:frontend-design skill for the visual quality. The template must include:

- `<!DOCTYPE html>` with lang="en"
- Google Fonts: Stick and Poor Story via `<link>` in `<head>`
- HTMX via CDN `<script>` tag
- Compiled Tailwind CSS: `{% static 'css/output.css' %}`
- Sticky header with: Treefel branding (far-left, links to `/`), Blog | Gallery (left), About | Feedback (right)
- `{% block content %}` for page content
- Footer with copyright
- Colors: primary `#87aa6c`, secondary `#567e54`, tertiary `#cfdc7b`, dark `#1a1a1a`, light `#f5f5f0`
- Responsive mobile hamburger menu
- `{% block title %}` for page titles
- `{% block extra_head %}` for page-specific CSS/JS

**Step 6: Create login template**

Create `C:/Projects/treefel/core/templates/registration/login.html`:

Extends `core/base.html`. Simple login form with username/password fields styled with Tailwind. No links to this page from public navigation. Shows form errors.

**Step 7: Build CSS and verify**

Run Tailwind build again after templates are created:
`C:/Projects/treefel/venv/Scripts/tailwindcss.exe -i C:/Projects/treefel/static/css/input.css -o C:/Projects/treefel/static/css/output.css --content "C:/Projects/treefel/core/templates/**/*.html"`

Run: `C:/Projects/treefel/venv/Scripts/python.exe C:/Projects/treefel/manage.py runserver`
Verify the base template loads at http://127.0.0.1:8000/ (will 404 but check for CSS/font loading errors in console).

**Step 8: Commit**

```bash
git add static/ core/templates/
git commit -m "feat: add Tailwind setup, base template with nav, and login template"
```

---

## Task 4: Public Blog Pages

**Files:**
- Modify: `C:/Projects/treefel/core/urls.py`
- Modify: `C:/Projects/treefel/core/views.py`
- Create: `C:/Projects/treefel/core/templates/core/blog_list.html`
- Create: `C:/Projects/treefel/core/templates/core/blog_detail.html`
- Create: `C:/Projects/treefel/core/templates/core/partials/blog_list_items.html`
- Create: `C:/Projects/treefel/core/tests/test_views_blog.py`

**Step 1: Write blog view tests**

Create `C:/Projects/treefel/core/tests/test_views_blog.py`:

```python
from django.test import TestCase, Client
from django.urls import reverse
from core.models import BlogCategory, BlogPost


class BlogListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = BlogCategory.objects.create(name="Dev Log")
        self.published_post = BlogPost.objects.create(
            title="Published Post",
            body="<p>Content</p>",
            category=self.category,
            published=True,
        )
        self.draft_post = BlogPost.objects.create(
            title="Draft Post",
            body="<p>Draft</p>",
            category=self.category,
            published=False,
        )

    def test_blog_list_returns_200(self):
        response = self.client.get(reverse("core:blog_list"))
        self.assertEqual(response.status_code, 200)

    def test_blog_list_shows_published_only(self):
        response = self.client.get(reverse("core:blog_list"))
        self.assertContains(response, "Published Post")
        self.assertNotContains(response, "Draft Post")

    def test_blog_list_filter_by_category(self):
        other_cat = BlogCategory.objects.create(name="Personal")
        BlogPost.objects.create(
            title="Other Post", body="body", category=other_cat, published=True
        )
        response = self.client.get(
            reverse("core:blog_list") + f"?category={self.category.slug}"
        )
        self.assertContains(response, "Published Post")
        self.assertNotContains(response, "Other Post")

    def test_blog_list_htmx_returns_partial(self):
        response = self.client.get(
            reverse("core:blog_list"),
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        # HTMX requests return just the partial, not full page
        self.assertNotContains(response, "<!DOCTYPE html>")


class BlogDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = BlogCategory.objects.create(name="Dev Log")
        self.post = BlogPost.objects.create(
            title="Test Post",
            body="<p>Full content here</p>",
            category=self.category,
            published=True,
            tags="django,web",
        )

    def test_blog_detail_returns_200(self):
        response = self.client.get(
            reverse("core:blog_detail", kwargs={"slug": self.post.slug})
        )
        self.assertEqual(response.status_code, 200)

    def test_blog_detail_shows_content(self):
        response = self.client.get(
            reverse("core:blog_detail", kwargs={"slug": self.post.slug})
        )
        self.assertContains(response, "Test Post")
        self.assertContains(response, "Full content here")

    def test_unpublished_post_returns_404(self):
        draft = BlogPost.objects.create(
            title="Draft", body="body", category=self.category, published=False
        )
        response = self.client.get(
            reverse("core:blog_detail", kwargs={"slug": draft.slug})
        )
        self.assertEqual(response.status_code, 404)
```

**Step 2: Run tests to verify they fail**

Run: `C:/Projects/treefel/venv/Scripts/python.exe C:/Projects/treefel/manage.py test core.tests.test_views_blog -v 2`
Expected: Failures (no URL routes or views yet).

**Step 3: Implement blog views**

Add to `C:/Projects/treefel/core/views.py`:

```python
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from core.models import BlogCategory, BlogPost


def blog_list(request):
    posts = BlogPost.objects.filter(published=True).select_related("category")
    categories = BlogCategory.objects.all()

    category_slug = request.GET.get("category")
    if category_slug:
        posts = posts.filter(category__slug=category_slug)

    paginator = Paginator(posts, 9)
    page = request.GET.get("page")
    posts = paginator.get_page(page)

    template = "core/partials/blog_list_items.html" if request.htmx else "core/blog_list.html"
    return render(request, template, {
        "posts": posts,
        "categories": categories,
        "current_category": category_slug,
    })


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, published=True)
    return render(request, "core/blog_detail.html", {"post": post})
```

**Step 4: Add blog URL routes**

Update `C:/Projects/treefel/core/urls.py`:

```python
from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
]
```

**Step 5: Create blog templates**

Create `C:/Projects/treefel/core/templates/core/blog_list.html`:
- Extends `base.html`
- Category filter buttons (All + each BlogCategory), using HTMX `hx-get` with `?category=<slug>` targeting the post list container
- Post card grid (title, date, category badge, body snippet truncated)
- Each card links to blog detail
- Pagination controls
- Uses `{% include "core/partials/blog_list_items.html" %}`

Create `C:/Projects/treefel/core/templates/core/partials/blog_list_items.html`:
- Just the post cards and pagination (the HTMX swappable portion)

Create `C:/Projects/treefel/core/templates/core/blog_detail.html`:
- Extends `base.html`
- Header image if present
- Title, date, category badge, tags
- Full `{{ post.body|safe }}` content
- Back to blog link

Use @frontend-design:frontend-design for visual quality on these templates.

**Step 6: Run tests to verify they pass**

Run: `C:/Projects/treefel/venv/Scripts/python.exe C:/Projects/treefel/manage.py test core.tests.test_views_blog -v 2`
Expected: All pass.

**Step 7: Commit**

```bash
git add core/
git commit -m "feat: add public blog list and detail pages with HTMX category filtering"
```

---

## Task 5: Public Gallery Page

**Files:**
- Modify: `C:/Projects/treefel/core/urls.py`
- Modify: `C:/Projects/treefel/core/views.py`
- Create: `C:/Projects/treefel/core/templates/core/gallery.html`
- Create: `C:/Projects/treefel/core/templates/core/partials/gallery_items.html`
- Create: `C:/Projects/treefel/core/tests/test_views_gallery.py`

**Step 1: Write gallery view tests**

Create `C:/Projects/treefel/core/tests/test_views_gallery.py`:

```python
from django.test import TestCase, Client
from django.urls import reverse
from core.models import GalleryItem


class GalleryViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.item_2d = GalleryItem.objects.create(
            title="Painting", description="A 2D painting",
            category="2D", media_type="image",
            image="https://r2.example.com/painting.jpg", sort_order=1,
        )
        self.item_3d = GalleryItem.objects.create(
            title="Sculpture", description="A 3D model",
            category="3D", media_type="image",
            image="https://r2.example.com/sculpture.jpg", sort_order=2,
        )
        self.item_yt = GalleryItem.objects.create(
            title="Timelapse", description="Speed sculpt",
            category="3D", media_type="youtube",
            youtube_url="https://www.youtube.com/watch?v=abc123", sort_order=3,
        )

    def test_gallery_returns_200(self):
        response = self.client.get(reverse("core:gallery"))
        self.assertEqual(response.status_code, 200)

    def test_gallery_shows_all_items(self):
        response = self.client.get(reverse("core:gallery"))
        self.assertContains(response, "Painting")
        self.assertContains(response, "Sculpture")
        self.assertContains(response, "Timelapse")

    def test_gallery_filter_2d(self):
        response = self.client.get(reverse("core:gallery") + "?category=2D")
        self.assertContains(response, "Painting")
        self.assertNotContains(response, "Sculpture")

    def test_gallery_filter_3d(self):
        response = self.client.get(reverse("core:gallery") + "?category=3D")
        self.assertNotContains(response, "Painting")
        self.assertContains(response, "Sculpture")

    def test_gallery_htmx_returns_partial(self):
        response = self.client.get(
            reverse("core:gallery"), HTTP_HX_REQUEST="true",
        )
        self.assertNotContains(response, "<!DOCTYPE html>")
```

**Step 2: Run tests to verify they fail**

Run: `C:/Projects/treefel/venv/Scripts/python.exe C:/Projects/treefel/manage.py test core.tests.test_views_gallery -v 2`
Expected: Failures.

**Step 3: Implement gallery view**

Add to `C:/Projects/treefel/core/views.py`:

```python
from core.models import GalleryItem

def gallery(request):
    items = GalleryItem.objects.all()

    category = request.GET.get("category")
    if category in ("2D", "3D"):
        items = items.filter(category=category)

    template = "core/partials/gallery_items.html" if request.htmx else "core/gallery.html"
    return render(request, template, {
        "items": items,
        "current_category": category,
    })
```

**Step 4: Add gallery URL route**

Add to `C:/Projects/treefel/core/urls.py`:

```python
path('gallery/', views.gallery, name='gallery'),
```

**Step 5: Create gallery templates**

Create `C:/Projects/treefel/core/templates/core/gallery.html`:
- Extends `base.html`
- All / 2D / 3D toggle tabs with HTMX `hx-get` targeting gallery grid
- Grid of items (uses partial)
- `{% include "core/partials/gallery_items.html" %}`

Create `C:/Projects/treefel/core/templates/core/partials/gallery_items.html`:
- Responsive grid of gallery cards
- For image items: image with CSS overlay for right-click protection, title, description on hover/click
- For YouTube items: thumbnail or embed, title, description
- Right-click protection:
  ```html
  <div class="relative group" oncontextmenu="return false;">
    <img src="{{ item.image }}" alt="{{ item.title }}" class="pointer-events-none ...">
    <div class="absolute inset-0"></div>
  </div>
  ```
- Lightbox/modal for full-size view (can use simple HTMX or Alpine.js -- keep it lightweight)
- YouTube embeds use `<iframe>` with youtube-nocookie.com domain

Use @frontend-design:frontend-design for visual quality.

**Step 6: Run tests to verify they pass**

Run: `C:/Projects/treefel/venv/Scripts/python.exe C:/Projects/treefel/manage.py test core.tests.test_views_gallery -v 2`
Expected: All pass.

**Step 7: Commit**

```bash
git add core/
git commit -m "feat: add gallery page with 2D/3D filtering and right-click protection"
```

---

## Task 6: Public About & Feedback Pages

**Files:**
- Modify: `C:/Projects/treefel/core/urls.py`
- Modify: `C:/Projects/treefel/core/views.py`
- Create: `C:/Projects/treefel/core/forms.py`
- Create: `C:/Projects/treefel/core/templates/core/about.html`
- Create: `C:/Projects/treefel/core/templates/core/feedback.html`
- Create: `C:/Projects/treefel/core/templates/core/partials/feedback_form.html`
- Create: `C:/Projects/treefel/core/tests/test_views_feedback.py`

**Step 1: Write feedback view tests**

Create `C:/Projects/treefel/core/tests/test_views_feedback.py`:

```python
from django.test import TestCase, Client
from django.urls import reverse
from core.models import FeedbackMessage, SiteSetting


class AboutViewTest(TestCase):
    def test_about_returns_200(self):
        response = self.client.get(reverse("core:about"))
        self.assertEqual(response.status_code, 200)


class FeedbackViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        SiteSetting.objects.create(
            key="feedback_welcome", value="Drop a message!"
        )

    def test_feedback_page_returns_200(self):
        response = self.client.get(reverse("core:feedback"))
        self.assertEqual(response.status_code, 200)

    def test_feedback_shows_welcome_message(self):
        response = self.client.get(reverse("core:feedback"))
        self.assertContains(response, "Drop a message!")

    def test_feedback_submit_valid(self):
        response = self.client.post(
            reverse("core:feedback"),
            {"subject": "Hello", "body": "Nice site!", "honeypot": ""},
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(FeedbackMessage.objects.count(), 1)
        self.assertContains(response, "Thank you")

    def test_feedback_submit_with_email(self):
        self.client.post(
            reverse("core:feedback"),
            {"email": "user@example.com", "subject": "Hi", "body": "Great", "honeypot": ""},
        )
        msg = FeedbackMessage.objects.first()
        self.assertEqual(msg.email, "user@example.com")

    def test_feedback_honeypot_rejects_bots(self):
        response = self.client.post(
            reverse("core:feedback"),
            {"subject": "Spam", "body": "Buy stuff", "honeypot": "gotcha"},
        )
        self.assertEqual(FeedbackMessage.objects.count(), 0)

    def test_feedback_submit_invalid(self):
        response = self.client.post(
            reverse("core:feedback"),
            {"subject": "", "body": "", "honeypot": ""},
        )
        self.assertEqual(FeedbackMessage.objects.count(), 0)
```

**Step 2: Run tests to verify they fail**

Run: `C:/Projects/treefel/venv/Scripts/python.exe C:/Projects/treefel/manage.py test core.tests.test_views_feedback -v 2`

**Step 3: Create feedback form**

Write `C:/Projects/treefel/core/forms.py`:

```python
from django import forms
from core.models import FeedbackMessage


class FeedbackForm(forms.ModelForm):
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = FeedbackMessage
        fields = ["email", "subject", "body"]
        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": "Email (optional)"}),
            "subject": forms.TextInput(attrs={"placeholder": "Subject"}),
            "body": forms.Textarea(attrs={"placeholder": "Your message...", "rows": 5}),
        }

    def clean_honeypot(self):
        value = self.cleaned_data.get("honeypot")
        if value:
            raise forms.ValidationError("Bot detected.")
        return value
```

**Step 4: Implement about and feedback views**

Add to `C:/Projects/treefel/core/views.py`:

```python
from django.http import HttpResponse
from django_ratelimit.decorators import ratelimit
from core.forms import FeedbackForm
from core.models import SiteSetting


def about(request):
    return render(request, "core/about.html")


@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def feedback(request):
    welcome = SiteSetting.objects.filter(key="feedback_welcome").first()
    welcome_message = welcome.value if welcome else ""

    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid() and not form.cleaned_data.get("honeypot"):
            form.save()
            template = "core/partials/feedback_form.html" if request.htmx else "core/feedback.html"
            return render(request, template, {
                "form": FeedbackForm(),
                "welcome_message": welcome_message,
                "success": True,
            })
    else:
        form = FeedbackForm()

    return render(request, "core/feedback.html", {
        "form": form,
        "welcome_message": welcome_message,
    })
```

**Step 5: Add URL routes**

Add to `C:/Projects/treefel/core/urls.py`:

```python
path('about/', views.about, name='about'),
path('feedback/', views.feedback, name='feedback'),
```

**Step 6: Create templates**

Create `C:/Projects/treefel/core/templates/core/about.html`:
- Extends `base.html`
- Boilerplate "About Treefel" content
- Placeholder text for the artist to fill in later

Create `C:/Projects/treefel/core/templates/core/feedback.html`:
- Extends `base.html`
- Welcome message from SiteSetting
- Feedback form with HTMX `hx-post` and `hx-swap`
- Success message display
- Hidden honeypot field
- `{% include "core/partials/feedback_form.html" %}`

Create `C:/Projects/treefel/core/templates/core/partials/feedback_form.html`:
- Just the form and success message (HTMX swappable)

Use @frontend-design:frontend-design for visual quality.

**Step 7: Run tests to verify they pass**

Run: `C:/Projects/treefel/venv/Scripts/python.exe C:/Projects/treefel/manage.py test core.tests.test_views_feedback -v 2`
Expected: All pass.

**Step 8: Commit**

```bash
git add core/
git commit -m "feat: add about page and feedback form with honeypot and rate limiting"
```

---

## Task 7: Home Page

**Files:**
- Modify: `C:/Projects/treefel/core/urls.py`
- Modify: `C:/Projects/treefel/core/views.py`
- Create: `C:/Projects/treefel/core/templates/core/home.html`
- Create: `C:/Projects/treefel/core/tests/test_views_home.py`

**Step 1: Write home view tests**

Create `C:/Projects/treefel/core/tests/test_views_home.py`:

```python
from django.test import TestCase, Client
from django.urls import reverse
from core.models import BlogCategory, BlogPost, GalleryItem


class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = BlogCategory.objects.create(name="Dev Log")

    def test_home_returns_200(self):
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)

    def test_home_shows_latest_post(self):
        BlogPost.objects.create(
            title="Latest Post", body="body", category=self.category, published=True
        )
        response = self.client.get(reverse("core:home"))
        self.assertContains(response, "Latest Post")

    def test_home_shows_featured_gallery_item(self):
        GalleryItem.objects.create(
            title="Featured Art", description="desc",
            category="3D", media_type="image",
            image="https://r2.example.com/art.jpg", sort_order=1,
        )
        response = self.client.get(reverse("core:home"))
        self.assertContains(response, "Featured Art")
```

**Step 2: Run tests to verify they fail**

Run: `C:/Projects/treefel/venv/Scripts/python.exe C:/Projects/treefel/manage.py test core.tests.test_views_home -v 2`

**Step 3: Implement home view**

Add to `C:/Projects/treefel/core/views.py`:

```python
def home(request):
    latest_post = BlogPost.objects.filter(published=True).first()
    featured_item = GalleryItem.objects.first()
    return render(request, "core/home.html", {
        "latest_post": latest_post,
        "featured_item": featured_item,
    })
```

**Step 4: Add home URL route**

Add to `C:/Projects/treefel/core/urls.py`:

```python
path('', views.home, name='home'),
```

**Step 5: Create home template**

Create `C:/Projects/treefel/core/templates/core/home.html`:
- Extends `base.html`
- Hero section with Treefel intro/tagline
- Featured artwork (if exists) with right-click protection
- Latest blog post card (if exists)
- CTAs to gallery and blog

Use @frontend-design:frontend-design for visual quality. This is the landing page -- it should be visually striking.

**Step 6: Run tests to verify they pass**

Run: `C:/Projects/treefel/venv/Scripts/python.exe C:/Projects/treefel/manage.py test core.tests.test_views_home -v 2`
Expected: All pass.

**Step 7: Commit**

```bash
git add core/
git commit -m "feat: add home page with featured art and latest blog post"
```

---

## Task 8: Cloudflare R2 Storage & Image Upload Utility

**Files:**
- Modify: `C:/Projects/treefel/treefel/settings.py`
- Create: `C:/Projects/treefel/core/storage.py`
- Create: `C:/Projects/treefel/core/tests/test_storage.py`

**Step 1: Write storage utility tests**

Create `C:/Projects/treefel/core/tests/test_storage.py`:

```python
from unittest.mock import patch, MagicMock
from django.test import TestCase
from io import BytesIO
from PIL import Image
from core.storage import optimize_image


class ImageOptimizationTest(TestCase):
    def _create_test_image(self, width=2000, height=2000, format="PNG"):
        img = Image.new("RGB", (width, height), color="red")
        buffer = BytesIO()
        img.save(buffer, format=format)
        buffer.seek(0)
        return buffer

    def test_optimize_resizes_large_image(self):
        large_image = self._create_test_image(4000, 4000)
        result = optimize_image(large_image, max_dimension=1920)
        img = Image.open(result)
        self.assertLessEqual(max(img.size), 1920)

    def test_optimize_preserves_small_image_dimensions(self):
        small_image = self._create_test_image(800, 600)
        result = optimize_image(small_image, max_dimension=1920)
        img = Image.open(result)
        self.assertEqual(img.size[0], 800)

    def test_optimize_outputs_jpeg(self):
        image = self._create_test_image(1000, 1000, "PNG")
        result = optimize_image(image)
        img = Image.open(result)
        # Result should be JPEG for smaller file size
        self.assertEqual(img.format, "JPEG")
```

**Step 2: Run tests to verify they fail**

Run: `C:/Projects/treefel/venv/Scripts/python.exe C:/Projects/treefel/manage.py test core.tests.test_storage -v 2`

**Step 3: Implement storage utility**

Create `C:/Projects/treefel/core/storage.py`:

```python
from io import BytesIO
from PIL import Image


def optimize_image(file_obj, max_dimension=1920, quality=85):
    """Resize and compress an image. Returns a BytesIO with JPEG data."""
    img = Image.open(file_obj)
    img = img.convert("RGB")

    if max(img.size) > max_dimension:
        img.thumbnail((max_dimension, max_dimension), Image.LANCZOS)

    output = BytesIO()
    img.save(output, format="JPEG", quality=quality, optimize=True)
    output.seek(0)
    return output
```

**Step 4: Run tests to verify they pass**

Run: `C:/Projects/treefel/venv/Scripts/python.exe C:/Projects/treefel/manage.py test core.tests.test_storage -v 2`
Expected: All pass.

**Step 5: Configure R2 storage in settings**

Add to `C:/Projects/treefel/treefel/settings.py`:

```python
# Cloudflare R2 Storage
R2_ACCOUNT_ID = os.getenv("R2_ACCOUNT_ID", "")
R2_ACCESS_KEY_ID = os.getenv("R2_ACCESS_KEY_ID", "")
R2_SECRET_ACCESS_KEY = os.getenv("R2_SECRET_ACCESS_KEY", "")
R2_BUCKET_NAME = os.getenv("R2_BUCKET_NAME", "treefel-media")
R2_CUSTOM_DOMAIN = os.getenv("R2_CUSTOM_DOMAIN", "")  # e.g., media.treefel.com

if R2_ACCOUNT_ID:
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
            "OPTIONS": {
                "access_key": R2_ACCESS_KEY_ID,
                "secret_key": R2_SECRET_ACCESS_KEY,
                "bucket_name": R2_BUCKET_NAME,
                "endpoint_url": f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com",
                "custom_domain": R2_CUSTOM_DOMAIN or None,
                "default_acl": "public-read",
                "signature_version": "s3v4",
            },
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }
```

**Step 6: Add upload helper to storage.py**

Add to `C:/Projects/treefel/core/storage.py`:

```python
import uuid
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


def upload_image(file_obj, folder="uploads"):
    """Optimize and upload an image to storage. Returns the URL."""
    optimized = optimize_image(file_obj)
    filename = f"{folder}/{uuid.uuid4().hex}.jpg"
    path = default_storage.save(filename, ContentFile(optimized.read()))
    return default_storage.url(path)
```

**Step 7: Update .env with placeholder R2 values**

Add to `C:/Projects/treefel/.env`:
```
R2_ACCOUNT_ID=
R2_ACCESS_KEY_ID=
R2_SECRET_ACCESS_KEY=
R2_BUCKET_NAME=treefel-media
R2_CUSTOM_DOMAIN=
```

**Step 8: Commit**

```bash
git add core/storage.py core/tests/test_storage.py treefel/settings.py
git commit -m "feat: add Cloudflare R2 storage integration and image optimization"
```

---

## Task 9: Admin Blog Management

**Files:**
- Modify: `C:/Projects/treefel/core/urls.py`
- Modify: `C:/Projects/treefel/core/views.py`
- Modify: `C:/Projects/treefel/core/forms.py`
- Create: `C:/Projects/treefel/core/templates/core/admin_blog.html`
- Create: `C:/Projects/treefel/core/templates/core/admin_blog_form.html`
- Create: `C:/Projects/treefel/core/tests/test_views_admin_blog.py`

**Step 1: Write admin blog tests**

Create `C:/Projects/treefel/core/tests/test_views_admin_blog.py`:

```python
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import BlogCategory, BlogPost


class AdminBlogViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="treefel", password="testpass123")
        self.category = BlogCategory.objects.create(name="Dev Log")

    def test_admin_blog_requires_login(self):
        response = self.client.get(reverse("core:admin_blog"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_admin_blog_returns_200_when_logged_in(self):
        self.client.login(username="treefel", password="testpass123")
        response = self.client.get(reverse("core:admin_blog"))
        self.assertEqual(response.status_code, 200)

    def test_create_blog_post(self):
        self.client.login(username="treefel", password="testpass123")
        response = self.client.post(reverse("core:admin_blog_create"), {
            "title": "New Post",
            "body": "<p>Content</p>",
            "category": self.category.pk,
            "tags": "test,blog",
            "published": True,
        })
        self.assertEqual(BlogPost.objects.count(), 1)
        post = BlogPost.objects.first()
        self.assertEqual(post.title, "New Post")

    def test_edit_blog_post(self):
        self.client.login(username="treefel", password="testpass123")
        post = BlogPost.objects.create(
            title="Old Title", body="body", category=self.category
        )
        self.client.post(reverse("core:admin_blog_edit", kwargs={"pk": post.pk}), {
            "title": "Updated Title",
            "body": "<p>Updated</p>",
            "category": self.category.pk,
            "tags": "",
            "published": False,
        })
        post.refresh_from_db()
        self.assertEqual(post.title, "Updated Title")

    def test_delete_blog_post(self):
        self.client.login(username="treefel", password="testpass123")
        post = BlogPost.objects.create(
            title="Delete Me", body="body", category=self.category
        )
        self.client.post(reverse("core:admin_blog_delete", kwargs={"pk": post.pk}))
        self.assertEqual(BlogPost.objects.count(), 0)


class AdminBlogCategoryTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="treefel", password="testpass123")
        self.client.login(username="treefel", password="testpass123")

    def test_create_category(self):
        self.client.post(reverse("core:admin_blog_category_create"), {
            "name": "New Category",
        })
        self.assertEqual(BlogCategory.objects.filter(name="New Category").count(), 1)

    def test_delete_category(self):
        cat = BlogCategory.objects.create(name="To Delete")
        self.client.post(reverse("core:admin_blog_category_delete", kwargs={"pk": cat.pk}))
        self.assertEqual(BlogCategory.objects.filter(name="To Delete").count(), 0)
```

**Step 2: Run tests to verify they fail**

Run: `C:/Projects/treefel/venv/Scripts/python.exe C:/Projects/treefel/manage.py test core.tests.test_views_admin_blog -v 2`

**Step 3: Create blog admin forms**

Add to `C:/Projects/treefel/core/forms.py`:

```python
from tinymce.widgets import TinyMCE
from core.models import BlogPost, BlogCategory


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ["title", "body", "category", "tags", "header_image", "published"]
        widgets = {
            "body": TinyMCE(),
            "title": forms.TextInput(attrs={"placeholder": "Post title"}),
            "tags": forms.TextInput(attrs={"placeholder": "tag1, tag2, tag3"}),
            "header_image": forms.URLInput(attrs={"placeholder": "Header image URL (optional)"}),
        }


class BlogCategoryForm(forms.ModelForm):
    class Meta:
        model = BlogCategory
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Category name"}),
        }
```

**Step 4: Implement admin blog views**

Add to `C:/Projects/treefel/core/views.py`:

```python
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from core.forms import BlogPostForm, BlogCategoryForm
from core.storage import upload_image


@login_required
def admin_blog(request):
    posts = BlogPost.objects.select_related("category").all()
    categories = BlogCategory.objects.all()
    return render(request, "core/admin_blog.html", {
        "posts": posts,
        "categories": categories,
        "category_form": BlogCategoryForm(),
    })


@login_required
def admin_blog_create(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            # Handle image upload if file provided
            if "header_image_file" in request.FILES:
                post.header_image = upload_image(
                    request.FILES["header_image_file"], folder="blog"
                )
            post.save()
            return redirect("core:admin_blog")
    else:
        form = BlogPostForm()
    return render(request, "core/admin_blog_form.html", {"form": form, "editing": False})


@login_required
def admin_blog_edit(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == "POST":
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            if "header_image_file" in request.FILES:
                post.header_image = upload_image(
                    request.FILES["header_image_file"], folder="blog"
                )
            post.save()
            return redirect("core:admin_blog")
    else:
        form = BlogPostForm(instance=post)
    return render(request, "core/admin_blog_form.html", {"form": form, "editing": True, "post": post})


@login_required
def admin_blog_delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == "POST":
        post.delete()
    return redirect("core:admin_blog")


@login_required
def admin_blog_category_create(request):
    if request.method == "POST":
        form = BlogCategoryForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect("core:admin_blog")


@login_required
def admin_blog_category_delete(request, pk):
    cat = get_object_or_404(BlogCategory, pk=pk)
    if request.method == "POST":
        cat.delete()
    return redirect("core:admin_blog")
```

**Step 5: Add admin blog URL routes**

Add to `C:/Projects/treefel/core/urls.py`:

```python
path('admin-blog/', views.admin_blog, name='admin_blog'),
path('admin-blog/create/', views.admin_blog_create, name='admin_blog_create'),
path('admin-blog/<int:pk>/edit/', views.admin_blog_edit, name='admin_blog_edit'),
path('admin-blog/<int:pk>/delete/', views.admin_blog_delete, name='admin_blog_delete'),
path('admin-blog/category/create/', views.admin_blog_category_create, name='admin_blog_category_create'),
path('admin-blog/category/<int:pk>/delete/', views.admin_blog_category_delete, name='admin_blog_category_delete'),
```

**Step 6: Create admin blog templates**

Create `C:/Projects/treefel/core/templates/core/admin_blog.html`:
- Extends `base.html`
- Post list table: title, date, category, published badge, edit/delete buttons
- "New Post" button linking to create form
- Category management section: list of categories with delete buttons, add form
- Delete confirmation modals

Create `C:/Projects/treefel/core/templates/core/admin_blog_form.html`:
- Extends `base.html`
- Full form with TinyMCE editor
- File upload field for header image (alongside URL field)
- Category dropdown, tags input, published checkbox
- Save and Cancel buttons
- Include TinyMCE JS: `{{ form.media }}`

Use @frontend-design:frontend-design for visual quality.

**Step 7: Run tests to verify they pass**

Run: `C:/Projects/treefel/venv/Scripts/python.exe C:/Projects/treefel/manage.py test core.tests.test_views_admin_blog -v 2`
Expected: All pass.

**Step 8: Commit**

```bash
git add core/
git commit -m "feat: add blog admin with CRUD, TinyMCE editor, and category management"
```

---

## Task 10: Admin Gallery Management

**Files:**
- Modify: `C:/Projects/treefel/core/urls.py`
- Modify: `C:/Projects/treefel/core/views.py`
- Modify: `C:/Projects/treefel/core/forms.py`
- Create: `C:/Projects/treefel/core/templates/core/admin_gallery.html`
- Create: `C:/Projects/treefel/core/templates/core/admin_gallery_form.html`
- Create: `C:/Projects/treefel/core/tests/test_views_admin_gallery.py`

**Step 1: Write admin gallery tests**

Create `C:/Projects/treefel/core/tests/test_views_admin_gallery.py`:

```python
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import GalleryItem
import json


class AdminGalleryViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="treefel", password="testpass123")

    def test_admin_gallery_requires_login(self):
        response = self.client.get(reverse("core:admin_gallery"))
        self.assertEqual(response.status_code, 302)

    def test_admin_gallery_returns_200(self):
        self.client.login(username="treefel", password="testpass123")
        response = self.client.get(reverse("core:admin_gallery"))
        self.assertEqual(response.status_code, 200)

    def test_create_gallery_item(self):
        self.client.login(username="treefel", password="testpass123")
        self.client.post(reverse("core:admin_gallery_create"), {
            "title": "New Art",
            "description": "Description",
            "category": "2D",
            "media_type": "image",
            "image": "https://r2.example.com/art.jpg",
            "sort_order": 1,
        })
        self.assertEqual(GalleryItem.objects.count(), 1)

    def test_edit_gallery_item(self):
        self.client.login(username="treefel", password="testpass123")
        item = GalleryItem.objects.create(
            title="Old", description="d", category="2D",
            media_type="image", sort_order=1,
        )
        self.client.post(reverse("core:admin_gallery_edit", kwargs={"pk": item.pk}), {
            "title": "Updated",
            "description": "new desc",
            "category": "3D",
            "media_type": "image",
            "image": "",
            "sort_order": 1,
        })
        item.refresh_from_db()
        self.assertEqual(item.title, "Updated")
        self.assertEqual(item.category, "3D")

    def test_delete_gallery_item(self):
        self.client.login(username="treefel", password="testpass123")
        item = GalleryItem.objects.create(
            title="Delete", description="d", category="2D",
            media_type="image", sort_order=1,
        )
        self.client.post(reverse("core:admin_gallery_delete", kwargs={"pk": item.pk}))
        self.assertEqual(GalleryItem.objects.count(), 0)

    def test_reorder_gallery_items(self):
        self.client.login(username="treefel", password="testpass123")
        i1 = GalleryItem.objects.create(
            title="A", description="d", category="2D",
            media_type="image", sort_order=1,
        )
        i2 = GalleryItem.objects.create(
            title="B", description="d", category="2D",
            media_type="image", sort_order=2,
        )
        self.client.post(
            reverse("core:admin_gallery_reorder"),
            data=json.dumps({"order": [i2.pk, i1.pk]}),
            content_type="application/json",
        )
        i1.refresh_from_db()
        i2.refresh_from_db()
        self.assertEqual(i2.sort_order, 0)
        self.assertEqual(i1.sort_order, 1)
```

**Step 2: Run tests to verify they fail**

Run: `C:/Projects/treefel/venv/Scripts/python.exe C:/Projects/treefel/manage.py test core.tests.test_views_admin_gallery -v 2`

**Step 3: Create gallery admin form**

Add to `C:/Projects/treefel/core/forms.py`:

```python
from core.models import GalleryItem

class GalleryItemForm(forms.ModelForm):
    image_file = forms.ImageField(required=False, help_text="Upload an image file")

    class Meta:
        model = GalleryItem
        fields = ["title", "description", "category", "media_type", "image", "youtube_url", "sort_order"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Title"}),
            "description": forms.Textarea(attrs={"placeholder": "Description / context", "rows": 3}),
            "image": forms.URLInput(attrs={"placeholder": "Image URL (or upload below)"}),
            "youtube_url": forms.URLInput(attrs={"placeholder": "YouTube URL"}),
        }
```

**Step 4: Implement admin gallery views**

Add to `C:/Projects/treefel/core/views.py`:

```python
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from core.forms import GalleryItemForm


@login_required
def admin_gallery(request):
    items = GalleryItem.objects.all()
    return render(request, "core/admin_gallery.html", {"items": items})


@login_required
def admin_gallery_create(request):
    if request.method == "POST":
        form = GalleryItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            if "image_file" in request.FILES:
                item.image = upload_image(
                    request.FILES["image_file"], folder="gallery"
                )
            item.save()
            return redirect("core:admin_gallery")
    else:
        form = GalleryItemForm()
    return render(request, "core/admin_gallery_form.html", {"form": form, "editing": False})


@login_required
def admin_gallery_edit(request, pk):
    item = get_object_or_404(GalleryItem, pk=pk)
    if request.method == "POST":
        form = GalleryItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            if "image_file" in request.FILES:
                item.image = upload_image(
                    request.FILES["image_file"], folder="gallery"
                )
            item.save()
            return redirect("core:admin_gallery")
    else:
        form = GalleryItemForm(instance=item)
    return render(request, "core/admin_gallery_form.html", {"form": form, "editing": True, "item": item})


@login_required
def admin_gallery_delete(request, pk):
    item = get_object_or_404(GalleryItem, pk=pk)
    if request.method == "POST":
        item.delete()
    return redirect("core:admin_gallery")


@login_required
@require_POST
def admin_gallery_reorder(request):
    data = json.loads(request.body)
    order = data.get("order", [])
    for index, pk in enumerate(order):
        GalleryItem.objects.filter(pk=pk).update(sort_order=index)
    return JsonResponse({"status": "ok"})
```

**Step 5: Add admin gallery URL routes**

Add to `C:/Projects/treefel/core/urls.py`:

```python
path('admin-gallery/', views.admin_gallery, name='admin_gallery'),
path('admin-gallery/create/', views.admin_gallery_create, name='admin_gallery_create'),
path('admin-gallery/<int:pk>/edit/', views.admin_gallery_edit, name='admin_gallery_edit'),
path('admin-gallery/<int:pk>/delete/', views.admin_gallery_delete, name='admin_gallery_delete'),
path('admin-gallery/reorder/', views.admin_gallery_reorder, name='admin_gallery_reorder'),
```

**Step 6: Create admin gallery templates**

Create `C:/Projects/treefel/core/templates/core/admin_gallery.html`:
- Extends `base.html`
- 2D/3D tabs
- Draggable grid of items (using Sortable.js CDN)
- Each item shows thumbnail, title, edit/delete buttons
- "Add Item" button
- JS: Initialize Sortable.js, on sort end POST new order to reorder endpoint
- Delete confirmation modals

Create `C:/Projects/treefel/core/templates/core/admin_gallery_form.html`:
- Extends `base.html`
- Form with all fields
- Toggle: show image fields or YouTube field based on media_type selection
- File upload field
- Save/Cancel buttons

Use @frontend-design:frontend-design for visual quality.

**Step 7: Run tests to verify they pass**

Run: `C:/Projects/treefel/venv/Scripts/python.exe C:/Projects/treefel/manage.py test core.tests.test_views_admin_gallery -v 2`
Expected: All pass.

**Step 8: Commit**

```bash
git add core/
git commit -m "feat: add gallery admin with CRUD, image upload, and drag-and-drop reorder"
```

---

## Task 11: Admin Feedback Management

**Files:**
- Modify: `C:/Projects/treefel/core/urls.py`
- Modify: `C:/Projects/treefel/core/views.py`
- Create: `C:/Projects/treefel/core/templates/core/admin_feedback.html`
- Create: `C:/Projects/treefel/core/tests/test_views_admin_feedback.py`

**Step 1: Write admin feedback tests**

Create `C:/Projects/treefel/core/tests/test_views_admin_feedback.py`:

```python
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import FeedbackMessage, SiteSetting


class AdminFeedbackViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="treefel", password="testpass123")

    def test_admin_feedback_requires_login(self):
        response = self.client.get(reverse("core:admin_feedback"))
        self.assertEqual(response.status_code, 302)

    def test_admin_feedback_returns_200(self):
        self.client.login(username="treefel", password="testpass123")
        response = self.client.get(reverse("core:admin_feedback"))
        self.assertEqual(response.status_code, 200)

    def test_admin_feedback_shows_messages(self):
        self.client.login(username="treefel", password="testpass123")
        FeedbackMessage.objects.create(subject="Test Msg", body="Hello")
        response = self.client.get(reverse("core:admin_feedback"))
        self.assertContains(response, "Test Msg")

    def test_toggle_feedback_completed(self):
        self.client.login(username="treefel", password="testpass123")
        msg = FeedbackMessage.objects.create(subject="Toggle", body="body")
        self.assertFalse(msg.is_completed)
        self.client.post(reverse("core:admin_feedback_toggle", kwargs={"pk": msg.pk}))
        msg.refresh_from_db()
        self.assertTrue(msg.is_completed)
        # Toggle back
        self.client.post(reverse("core:admin_feedback_toggle", kwargs={"pk": msg.pk}))
        msg.refresh_from_db()
        self.assertFalse(msg.is_completed)

    def test_filter_completed(self):
        self.client.login(username="treefel", password="testpass123")
        FeedbackMessage.objects.create(subject="Done", body="b", is_completed=True)
        FeedbackMessage.objects.create(subject="New", body="b", is_completed=False)
        response = self.client.get(reverse("core:admin_feedback") + "?filter=completed")
        self.assertContains(response, "Done")
        self.assertNotContains(response, "New")

    def test_filter_new(self):
        self.client.login(username="treefel", password="testpass123")
        FeedbackMessage.objects.create(subject="Done", body="b", is_completed=True)
        FeedbackMessage.objects.create(subject="New", body="b", is_completed=False)
        response = self.client.get(reverse("core:admin_feedback") + "?filter=new")
        self.assertNotContains(response, "Done")
        self.assertContains(response, "New")

    def test_update_welcome_message(self):
        self.client.login(username="treefel", password="testpass123")
        SiteSetting.objects.create(key="feedback_welcome", value="Old message")
        self.client.post(reverse("core:admin_feedback_welcome"), {
            "welcome_message": "New welcome message!",
        })
        setting = SiteSetting.objects.get(key="feedback_welcome")
        self.assertEqual(setting.value, "New welcome message!")
```

**Step 2: Run tests to verify they fail**

Run: `C:/Projects/treefel/venv/Scripts/python.exe C:/Projects/treefel/manage.py test core.tests.test_views_admin_feedback -v 2`

**Step 3: Implement admin feedback views**

Add to `C:/Projects/treefel/core/views.py`:

```python
@login_required
def admin_feedback(request):
    messages = FeedbackMessage.objects.all()

    filter_param = request.GET.get("filter")
    if filter_param == "completed":
        messages = messages.filter(is_completed=True)
    elif filter_param == "new":
        messages = messages.filter(is_completed=False)

    welcome = SiteSetting.objects.filter(key="feedback_welcome").first()
    welcome_message = welcome.value if welcome else ""

    template = "core/partials/admin_feedback_list.html" if request.htmx else "core/admin_feedback.html"
    return render(request, template, {
        "messages": messages,
        "welcome_message": welcome_message,
        "current_filter": filter_param,
    })


@login_required
@require_POST
def admin_feedback_toggle(request, pk):
    msg = get_object_or_404(FeedbackMessage, pk=pk)
    msg.is_completed = not msg.is_completed
    msg.save()
    if request.htmx:
        return render(request, "core/partials/admin_feedback_row.html", {"msg": msg})
    return redirect("core:admin_feedback")


@login_required
@require_POST
def admin_feedback_welcome(request):
    text = request.POST.get("welcome_message", "")
    setting, _ = SiteSetting.objects.get_or_create(key="feedback_welcome")
    setting.value = text
    setting.save()
    return redirect("core:admin_feedback")
```

**Step 4: Add admin feedback URL routes**

Add to `C:/Projects/treefel/core/urls.py`:

```python
path('admin-feedback/', views.admin_feedback, name='admin_feedback'),
path('admin-feedback/<int:pk>/toggle/', views.admin_feedback_toggle, name='admin_feedback_toggle'),
path('admin-feedback/welcome/', views.admin_feedback_welcome, name='admin_feedback_welcome'),
```

**Step 5: Create admin feedback templates**

Create `C:/Projects/treefel/core/templates/core/admin_feedback.html`:
- Extends `base.html`
- Editable welcome message at top with save button
- Filter tabs: All | New | Completed (HTMX filtering)
- Message list with expandable rows (click to show body)
- Each row: subject, email (if provided), date, completed badge, toggle button
- Toggle uses HTMX `hx-post` to swap the row

Create `C:/Projects/treefel/core/templates/core/partials/admin_feedback_list.html`:
- Just the message list (HTMX swappable for filtering)

Create `C:/Projects/treefel/core/templates/core/partials/admin_feedback_row.html`:
- Single message row (HTMX swappable for toggle)

Use @frontend-design:frontend-design for visual quality.

**Step 6: Run tests to verify they pass**

Run: `C:/Projects/treefel/venv/Scripts/python.exe C:/Projects/treefel/manage.py test core.tests.test_views_admin_feedback -v 2`
Expected: All pass.

**Step 7: Commit**

```bash
git add core/
git commit -m "feat: add feedback admin with filtering, toggle, and welcome message editing"
```

---

## Task 12: TinyMCE Image Upload Endpoint

**Files:**
- Modify: `C:/Projects/treefel/core/urls.py`
- Modify: `C:/Projects/treefel/core/views.py`
- Modify: `C:/Projects/treefel/treefel/settings.py`
- Create: `C:/Projects/treefel/core/tests/test_views_upload.py`

**Step 1: Write upload endpoint tests**

Create `C:/Projects/treefel/core/tests/test_views_upload.py`:

```python
from unittest.mock import patch
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO


class TinyMCEUploadTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="treefel", password="testpass123")

    def _create_test_image(self):
        img = Image.new("RGB", (100, 100), color="red")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        return SimpleUploadedFile("test.png", buffer.read(), content_type="image/png")

    def test_upload_requires_login(self):
        response = self.client.post(reverse("core:tinymce_upload"))
        self.assertEqual(response.status_code, 302)

    @patch("core.views.upload_image")
    def test_upload_returns_url(self, mock_upload):
        mock_upload.return_value = "https://r2.example.com/blog/abc123.jpg"
        self.client.login(username="treefel", password="testpass123")
        image = self._create_test_image()
        response = self.client.post(
            reverse("core:tinymce_upload"),
            {"file": image},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("location", data)
```

**Step 2: Run tests to verify they fail**

Run: `C:/Projects/treefel/venv/Scripts/python.exe C:/Projects/treefel/manage.py test core.tests.test_views_upload -v 2`

**Step 3: Implement upload endpoint**

Add to `C:/Projects/treefel/core/views.py`:

```python
@login_required
@require_POST
def tinymce_upload(request):
    file = request.FILES.get("file")
    if not file:
        return JsonResponse({"error": "No file provided"}, status=400)
    url = upload_image(file, folder="blog")
    return JsonResponse({"location": url})
```

**Step 4: Add URL route**

Add to `C:/Projects/treefel/core/urls.py`:

```python
path('api/upload/', views.tinymce_upload, name='tinymce_upload'),
```

**Step 5: Update TinyMCE config in settings**

Update `TINYMCE_DEFAULT_CONFIG` in `C:/Projects/treefel/treefel/settings.py` to add image upload:

```python
TINYMCE_DEFAULT_CONFIG = {
    'height': 400,
    'width': '100%',
    'menubar': False,
    'plugins': 'lists link image code',
    'toolbar': 'undo redo | bold italic underline | bullist numlist | link image | code',
    'content_css': '/static/css/tinymce-content.css',
    'images_upload_url': '/api/upload/',
    'images_upload_credentials': True,
    'automatic_uploads': True,
}
```

**Step 6: Run tests to verify they pass**

Run: `C:/Projects/treefel/venv/Scripts/python.exe C:/Projects/treefel/manage.py test core.tests.test_views_upload -v 2`
Expected: All pass.

**Step 7: Commit**

```bash
git add core/ treefel/settings.py
git commit -m "feat: add TinyMCE image upload endpoint with R2 storage"
```

---

## Task 13: Run Full Test Suite & Polish

**Step 1: Run all tests**

Run: `C:/Projects/treefel/venv/Scripts/python.exe C:/Projects/treefel/manage.py test core -v 2`
Expected: All tests pass.

**Step 2: Create superuser for local testing**

Run: `C:/Projects/treefel/venv/Scripts/python.exe C:/Projects/treefel/manage.py createsuperuser`
(Use username: treefel, set a password)

**Step 3: Run seed data**

Run: `C:/Projects/treefel/venv/Scripts/python.exe C:/Projects/treefel/manage.py seed_data`

**Step 4: Manual smoke test**

Run: `C:/Projects/treefel/venv/Scripts/python.exe C:/Projects/treefel/manage.py runserver`

Test each page:
- http://127.0.0.1:8000/ (home)
- http://127.0.0.1:8000/blog/ (blog list)
- http://127.0.0.1:8000/gallery/ (gallery)
- http://127.0.0.1:8000/about/ (about)
- http://127.0.0.1:8000/feedback/ (feedback form)
- http://127.0.0.1:8000/admin-blog/ (redirects to login, then shows admin)
- http://127.0.0.1:8000/admin-gallery/ (gallery admin)
- http://127.0.0.1:8000/admin-feedback/ (feedback admin)

**Step 5: Rebuild Tailwind CSS**

Run: `C:/Projects/treefel/venv/Scripts/tailwindcss.exe -i C:/Projects/treefel/static/css/input.css -o C:/Projects/treefel/static/css/output.css --content "C:/Projects/treefel/core/templates/**/*.html" --minify`

**Step 6: Commit**

```bash
git add .
git commit -m "chore: polish and verify full test suite passes"
```

---

## Task 14: Deployment Configuration

**Files:**
- Create: `C:/Projects/treefel/Procfile`
- Create: `C:/Projects/treefel/runtime.txt`
- Modify: `C:/Projects/treefel/treefel/settings.py`

**Step 1: Create Procfile for Railway**

Create `C:/Projects/treefel/Procfile`:

```
web: gunicorn treefel.wsgi --bind 0.0.0.0:$PORT
release: python manage.py migrate && python manage.py seed_data && python manage.py collectstatic --noinput
```

**Step 2: Create runtime.txt**

Create `C:/Projects/treefel/runtime.txt`:

```
python-3.14.2
```

**Step 3: Update settings for production**

Ensure `C:/Projects/treefel/treefel/settings.py` has:

```python
# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# WhiteNoise for static file serving
STORAGES = STORAGES if 'STORAGES' in dir() else {}
STORAGES.setdefault("staticfiles", {
    "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
})

# Security settings for production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
```

**Step 4: Collect static files locally to verify**

Run: `C:/Projects/treefel/venv/Scripts/python.exe C:/Projects/treefel/manage.py collectstatic --noinput`

**Step 5: Commit**

```bash
git add Procfile runtime.txt treefel/settings.py staticfiles/
git commit -m "feat: add Railway deployment configuration"
```

**Step 6: Push to GitHub**

```bash
git push -u origin main
```

---

## Summary

| Task | Description | Estimated Steps |
|------|-------------|-----------------|
| 1 | Project scaffolding & dependencies | 11 |
| 2 | Data models & tests | 8 |
| 3 | Tailwind setup & base template | 8 |
| 4 | Public blog pages | 7 |
| 5 | Public gallery page | 7 |
| 6 | About & feedback pages | 8 |
| 7 | Home page | 7 |
| 8 | R2 storage & image optimization | 8 |
| 9 | Admin blog management | 8 |
| 10 | Admin gallery management | 8 |
| 11 | Admin feedback management | 7 |
| 12 | TinyMCE image upload endpoint | 7 |
| 13 | Full test suite & polish | 6 |
| 14 | Deployment configuration | 6 |
| **Total** | | **106 steps** |

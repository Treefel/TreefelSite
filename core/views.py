import json

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django_ratelimit.decorators import ratelimit
from core.forms import FeedbackForm, BlogPostForm, BlogCategoryForm, GalleryItemForm
from core.models import BlogCategory, BlogPost, FeedbackMessage, GalleryItem, SiteSetting
from core.storage import upload_image


def home(request):
    latest_post = BlogPost.objects.filter(published=True).first()
    featured_item = GalleryItem.objects.first()
    return render(request, "core/home.html", {
        "latest_post": latest_post,
        "featured_item": featured_item,
    })


def blog_list(request):
    posts = BlogPost.objects.filter(published=True).select_related("category")
    categories = BlogCategory.objects.all()

    category_slug = request.GET.get("category")
    if category_slug:
        posts = posts.filter(category__slug=category_slug)

    paginator = Paginator(posts, 9)
    page = request.GET.get("page")
    posts = paginator.get_page(page)

    template = (
        "core/partials/blog_list_items.html"
        if request.htmx
        else "core/blog_list.html"
    )
    return render(
        request,
        template,
        {
            "posts": posts,
            "categories": categories,
            "current_category": category_slug,
        },
    )


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, published=True)
    tags = [tag.strip() for tag in post.tags.split(",") if tag.strip()] if post.tags else []
    return render(request, "core/blog_detail.html", {"post": post, "tags": tags})


def gallery(request):
    items = GalleryItem.objects.all()

    category = request.GET.get("category")
    if category in ("2D", "3D"):
        items = items.filter(category=category)

    template = (
        "core/partials/gallery_items.html"
        if request.htmx
        else "core/gallery.html"
    )
    return render(request, template, {
        "items": items,
        "current_category": category,
    })


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


# ---------------------------------------------------------------------------
# Admin Blog Views
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# Admin Gallery Views
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# Admin Feedback Views
# ---------------------------------------------------------------------------


@login_required
def admin_feedback(request):
    messages_qs = FeedbackMessage.objects.all()

    filter_param = request.GET.get("filter")
    if filter_param == "completed":
        messages_qs = messages_qs.filter(is_completed=True)
    elif filter_param == "new":
        messages_qs = messages_qs.filter(is_completed=False)

    welcome = SiteSetting.objects.filter(key="feedback_welcome").first()
    welcome_message = welcome.value if welcome else ""

    template = "core/partials/admin_feedback_list.html" if request.htmx else "core/admin_feedback.html"
    return render(request, template, {
        "messages": messages_qs,
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


# ---------------------------------------------------------------------------
# TinyMCE Image Upload
# ---------------------------------------------------------------------------


@login_required
@require_POST
def tinymce_upload(request):
    file = request.FILES.get("file")
    if not file:
        return JsonResponse({"error": "No file provided"}, status=400)
    url = upload_image(file, folder="blog")
    return JsonResponse({"location": url})

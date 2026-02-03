from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django_ratelimit.decorators import ratelimit
from core.forms import FeedbackForm
from core.models import BlogCategory, BlogPost, GalleryItem, SiteSetting


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

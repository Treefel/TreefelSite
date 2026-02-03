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

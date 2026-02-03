# Treefel.com -- Website Design Document

## Overview

Personal website for Treefel, a digital artist. Three goals:
1. Online presence
2. Portfolio to showcase 2D and 3D art
3. Blog for personal updates, dev logs, and interesting finds

## Tech Stack

| Component        | Choice                          | Rationale                                                  |
|------------------|---------------------------------|------------------------------------------------------------|
| Framework        | Django 5.x                      | Auth, ORM, file handling, admin -- batteries included      |
| Frontend         | Django templates + Tailwind v4  | Modern styling, utility-first                              |
| Interactivity    | HTMX                            | Snappy UX without heavy JS framework                       |
| Rich Text Editor | Django-TinyMCE                  | Blog body editing with formatting, images, links           |
| Database         | SQLite (PostgreSQL later)       | Django ORM makes migration a one-line config change        |
| Media Storage    | Cloudflare R2 via django-storages | S3-compatible, CDN-served, already on Cloudflare          |
| Hosting          | Railway                         | Supports Django, easy deploys                              |
| DNS/Domain       | Cloudflare (Treefel.com)        | Already configured                                         |
| Repo             | github.com/Treefel/TreefelSite  | Shared with ShafferButtars                                 |

## Project Structure

```
treefel/                    # Django project root
  treefel/                  # Project settings package
    settings.py
    urls.py
    wsgi.py
  core/                     # Single app (split later if needed)
    models.py
    views.py
    urls.py
    forms.py
    admin.py
    templates/
      core/
        base.html
        home.html
        blog_list.html
        blog_detail.html
        gallery.html
        about.html
        feedback.html
        admin_blog.html
        admin_blog_form.html
        admin_gallery.html
        admin_gallery_form.html
        admin_feedback.html
    static/
      css/
      js/
  manage.py
  requirements.txt
  Procfile                  # Railway deployment
  .gitignore
```

## Data Models

### BlogCategory
| Field          | Type           | Notes                                      |
|----------------|----------------|---------------------------------------------|
| name           | CharField      | Max 100 chars, unique                       |
| slug           | SlugField      | Auto-generated from name, unique            |

Editable through admin. Seeded with: "Dev Log", "Personal", "Interesting Finds".

### BlogPost
| Field          | Type           | Notes                                      |
|----------------|----------------|---------------------------------------------|
| title          | CharField      | Max 200 chars                               |
| slug           | SlugField      | Auto-generated from title, unique, URL key  |
| body           | TextField      | TinyMCE HTML content                        |
| category       | ForeignKey     | Links to BlogCategory                       |
| tags           | CharField      | Comma-separated tags                        |
| header_image   | URLField       | Optional, R2 URL                            |
| published      | BooleanField   | Draft/publish toggle                        |
| created_at     | DateTimeField  | Auto-set on creation                        |
| updated_at     | DateTimeField  | Auto-set on save                            |

### GalleryItem
| Field          | Type           | Notes                                      |
|----------------|----------------|---------------------------------------------|
| title          | CharField      | Max 200 chars                               |
| description    | TextField      | Artist commentary/context                   |
| category       | CharField      | Choices: "2D", "3D"                         |
| media_type     | CharField      | Choices: "image", "youtube"                 |
| image          | URLField       | Optional, R2 URL                            |
| youtube_url    | URLField       | Optional                                    |
| sort_order     | IntegerField   | Manual ordering                             |
| created_at     | DateTimeField  | Auto-set on creation                        |

### FeedbackMessage
| Field          | Type           | Notes                                      |
|----------------|----------------|---------------------------------------------|
| email          | EmailField     | Optional (blank=True)                       |
| subject        | CharField      | Max 200 chars                               |
| body           | TextField      |                                              |
| is_completed   | BooleanField   | Default False                               |
| created_at     | DateTimeField  | Auto-set on creation                        |

### SiteSetting
| Field          | Type           | Notes                                      |
|----------------|----------------|---------------------------------------------|
| key            | CharField      | Unique setting key (e.g. "feedback_welcome")|
| value          | TextField      | Setting value                               |

## URL Structure

### Public Pages
| URL                | Page                                         |
|--------------------|----------------------------------------------|
| `/`                | Landing -- intro, featured art, latest post   |
| `/blog/`           | Blog listing, filterable by category, paginated |
| `/blog/<slug>/`    | Individual blog post                          |
| `/gallery/`        | Gallery with 2D/3D filter tabs                |
| `/about/`          | About page (boilerplate)                      |
| `/feedback/`       | Feedback contact form                         |

### Admin Pages (auth required, no public links)
| URL                | Page                                         |
|--------------------|----------------------------------------------|
| `/admin-blog/`     | Blog post management                         |
| `/admin-gallery/`  | Gallery item management                       |
| `/admin-feedback/` | Feedback message management                   |
| `/accounts/login/` | Django login (redirect target only)           |

## Public Pages Detail

### Header
- Left: Blog | Gallery links
- Right: About | Feedback links
- Treefel branding (name/logo) far-left or centered, links to home
- Sticky nav, full-width

### Home (`/`)
- Brief intro to Treefel
- Featured artwork piece
- Latest blog post preview
- Call to action to explore gallery/blog

### Blog Listing (`/blog/`)
- Category filter buttons dynamically generated from BlogCategory model (HTMX filtering)
- Cards: title, date, category tag, text snippet
- Paginated

### Blog Detail (`/blog/<slug>/`)
- Title, date, category, tags
- Full rendered HTML body
- Header image if present

### Gallery (`/gallery/`)
- 2D / 3D toggle tabs (HTMX filtering)
- Grid of thumbnails
- Click opens lightbox/detail view with artist description
- YouTube items embed the video
- Right-click protection: CSS overlay on images + disabled context menu (deters casual download, not bulletproof)

### About (`/about/`)
- Boilerplate for now, Treefel fills in later

### Feedback (`/feedback/`)
- Welcome message (from SiteSetting)
- Form: email (optional), subject, body
- HTMX inline submission with success message

## Admin Pages Detail

All behind `@login_required`. No login links on public site.

### Blog Admin (`/admin-blog/`)
- List: title, date, category, published status
- "New Post" button opens form
- Form: title, category dropdown (from BlogCategory), tags, header image upload, published toggle
- Category management: add/rename/delete categories inline
- TinyMCE body editor: bold, italic, underline, bullets, numbered lists, links, image insert (upload to R2 or external URL)
- Edit/Delete on each post, delete with confirmation modal

### Gallery Admin (`/admin-gallery/`)
- Grid view, 2D/3D tabs
- "Add Item" form: title, description, category, image upload or YouTube URL, sort order
- Drag-and-drop reordering via Sortable.js + HTMX (updates sort_order)
- Edit inline, delete with confirmation

### Feedback Admin (`/admin-feedback/`)
- Editable welcome message at top
- Message list: subject, email, date, status
- Filter: All | New | Completed
- Toggle completed/uncompleted per message
- Click to expand full message body

## Visual Design

### Fonts
- **Headings:** Stick (Google Fonts) -- blocky, artistic personality
- **Body:** Poor Story (Google Fonts) -- handwritten, casual, approachable
- Loaded via Google Fonts CDN

### Color Palette
| Role      | Hex       | Usage                                          |
|-----------|-----------|-------------------------------------------------|
| Primary   | `#87aa6c` | Nav background, buttons, accents                |
| Secondary | `#567e54` | Hover states, active elements, footer           |
| Tertiary  | `#cfdc7b` | Highlights, tags, callouts                      |
| Dark      | `#1a1a1a` | Text, dark sections                             |
| Light     | `#f5f5f0` | Backgrounds (warm off-white)                    |

### Tailwind Config
Custom theme extending defaults:
- `colors.primary`, `colors.secondary`, `colors.tertiary`
- `fontFamily.heading` (Stick), `fontFamily.body` (Poor Story)

### Layout
- Full-width header, sticky nav
- Content max-width ~1200px, centered
- Generous spacing, rounded corners on cards, subtle shadows
- Mobile-first responsive via Tailwind breakpoints
- Art is the star -- UI stays out of the way

## Deployment

- Railway for Django app
- Cloudflare R2 for media (via django-storages S3 backend)
- Cloudflare DNS pointing Treefel.com to Railway
- Git repo: github.com/Treefel/TreefelSite

## Security & Protection

- **CSRF:** Django's built-in CSRF middleware enabled on all forms.
- **Feedback rate limiting:** `django-ratelimit` on the feedback submission endpoint to prevent spam. Honeypot field as an additional layer.
- **Image optimization:** Pillow resizes and compresses uploads before storing to R2. Keeps gallery load times fast and storage costs low.
- **Right-click protection:** CSS overlay + disabled context menu on gallery images. Deters casual downloads (not bulletproof, but sufficient).
- **Admin auth:** `@login_required` on all admin views. No public login links.

## Future Considerations
- SQLite to PostgreSQL migration (one-line Django config change)
- Social media links in footer
- Color/style tweaks by the artist

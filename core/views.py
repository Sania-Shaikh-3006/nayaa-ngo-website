from decimal import Decimal

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    RegisterForm,
    VolunteerForm,
    PartnershipForm,
    FundraisingForm,
    NewsletterForm,
    ContactForm,
    DonationForm,
)

from .models import *


# ============================================================
# HOME PAGE
# ============================================================

def home(request):
    homepage_content = HomePageContent.objects.first()

    # Active homepage banners
    banner_slides = BannerSlide.objects.filter(
        active=True
    ).order_by("order")

    # Real impact statistics only
    stats = ImpactStat.objects.filter(
        active=True
    ).order_by("order")

    # Active programs
    programs = Program.objects.filter(
        active=True
    )[:3]

    # Verified success stories
    stories = Story.objects.filter(
        verified=True
    ).order_by("-created_at")[:3]

    # Active campaigns
    campaigns = Campaign.objects.filter(
        active=True
    )[:3]

    # Verified projects
    projects = Project.objects.filter(
        verified=True
    ).order_by("-id")[:3]

    # Upcoming events
    events = Event.objects.filter(
        date__gte=__import__(
            "django.utils.timezone",
            fromlist=["localdate"]
        ).localdate()
    ).order_by("date")[:3]

    # Latest published blog posts
    latest_news = BlogPost.objects.filter(
        published=True
    ).order_by("-published_at")[:3]

    # Latest press releases
    press_releases = PressRelease.objects.order_by(
        "-date"
    )[:3]

    # Active partners and supporters
    partners = Partner.objects.filter(
        active=True
    ).order_by("order", "name")

    context = {
        "homepage_content": homepage_content,
        "banner_slides": banner_slides,
        "stats": stats,
        "programs": programs,
        "stories": stories,
        "campaigns": campaigns,
        "projects": projects,
        "events": events,
        "latest_news": latest_news,
        "press_releases": press_releases,
        "partners": partners,
    }

    return render(
        request,
        "core/home.html",
        context
    )
# ============================================================
# ABOUT
# ============================================================

def about(request):
    our_story = OurStory.objects.order_by("-updated_at").first()
    core_values = CoreValue.objects.all().order_by("id")
    programs = AboutProgram.objects.all().order_by("id")
    team_members = TeamMember.objects.all().order_by("id")
    impact_stats = ImpactStat.objects.filter(active=True).order_by("order")

    context = {
        "our_story": our_story,
        "core_values": core_values,
        "about_programs": programs,
        "team_members": team_members,
        "impact_stats": impact_stats,
    }
    return render(request, "core/about.html", context)

# ============================================================
# OUR WORK
# ============================================================

def work(request):
    return projects(request)


# ============================================================
# NAYAA — INDIVIDUAL AREAS OF WORK
# ============================================================

def education(request):
    return render(request, "core/education.html")


def healthcare(request):
    return render(request, "core/healthcare.html")


def women_empowerment(request):
    return render(request, "core/women_empowerment.html")


def skills_livelihoods(request):
    return render(request, "core/skills_livelihoods.html")


def community_development(request):
    return render(request, "core/community_development.html")


# ============================================================
# PROJECTS
# ============================================================

# ✅ REPLACE WITH THIS:
def projects(request):
    status_filter = request.GET.get("status")
    projects_list = Project.objects.filter(verified=True).order_by("-id")
    
    if status_filter in ["Ongoing", "Completed", "Upcoming"]:
        projects_list = projects_list.filter(status=status_filter)

    stats = ImpactStat.objects.filter(active=True).order_by("order")

    return render(
        request,
        "core/projects.html",
        {
            "projects": projects_list,
            "current_status": status_filter or "All",
            "stats": stats,
        }
    )

def stories(request):
    all_stories = Story.objects.filter(
        verified=True
    ).order_by("-created_at")

    return render(
        request,
        "core/stories.html",
        {"stories": all_stories}
    )


def project_detail(request, slug):
    return render(
        request,
        "core/project_detail.html",
        {
            "project": get_object_or_404(
                Project,
                slug=slug,
                verified=True
            )
        }
    )


# ============================================================
# MEDIA
# ============================================================

def media(request):
    press_releases = PressReleaseItem.objects.all().order_by("-release_date")
    media_coverages = MediaCoverage.objects.all().order_by("-created_at")
    gallery_images = ImageGallery.objects.all().order_by("-uploaded_at")
    videos = Video.objects.all().order_by("-uploaded_at")

    context = {
        "press_releases": press_releases,
        "media_coverages": media_coverages,
        "gallery_images": gallery_images,
        "videos": videos,
    }
    return render(request, "core/media.html", context)


# ============================================================
# VOLUNTEER
# ============================================================

def volunteer(request):
    form = VolunteerForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()

        messages.success(
            request,
            "Thank you. Your volunteer interest has been received."
        )

        return redirect("volunteer")

    return render(
        request,
        "core/volunteer.html",
        {
            "form": form
        }
    )


# ============================================================
# PARTNER
# ============================================================

def partner(request):
    form = PartnershipForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()

        messages.success(
            request,
            "Your partnership proposal has been received."
        )

        return redirect("partner")

    return render(
        request,
        "core/partner.html",
        {
            "form": form
        }
    )


# ============================================================
# FUNDRAISE
# ============================================================

def fundraise(request):
    form = FundraisingForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()

        messages.success(
            request,
            "Your fundraising request has been submitted for review."
        )

        return redirect("fundraise")

    return render(
        request,
        "core/fundraise.html",
        {
            "form": form
        }
    )


# ============================================================
# CAMPAIGNS
# ============================================================

def campaigns(request):
    return render(
        request,
        "core/campaigns.html",
        {
            "campaigns": Campaign.objects.filter(active=True)
        }
    )


# ============================================================
# COMMUNITY
# ============================================================

def community(request):
    form = NewsletterForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()

        messages.success(
            request,
            "You have joined the community newsletter."
        )

        return redirect("community")

    return render(
        request,
        "core/community.html",
        {
            "form": form,
            "events": Event.objects.order_by("date")
        }
    )


# ============================================================
# CONTACT
# ============================================================

def contact(request):
    form = ContactForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        obj = form.save()

        send_mail(
            "NGO website inquiry",
            obj.message,
            obj.email,
            ["admin@example.org"],
            fail_silently=True
        )

        messages.success(
            request,
            "Your message has been submitted."
        )

        return redirect("contact")

    return render(
        request,
        "core/contact.html",
        {
            "form": form
        }
    )


# ============================================================
# BLOG
# ============================================================

def blog(request):
    return render(
        request,
        "core/blog.html",
        {
            "posts": BlogPost.objects
                .filter(published=True)
                .order_by("-published_at")
        }
    )


def blog_detail(request, slug):
    return render(
        request,
        "core/blog_detail.html",
        {
            "post": get_object_or_404(
                BlogPost,
                slug=slug,
                published=True
            )
        }
    )


# ============================================================
# DONATE
# ============================================================

def donate(request):
    form = DonationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        donation = form.save()

        messages.info(
            request,
            "Donation record created. Configure Razorpay, "
            "Stripe, or PayPal credentials to start checkout."
        )

        return redirect(
            "donation_thanks",
            pk=donation.pk
        )

    return render(
        request,
        "core/donate.html",
        {
            "form": form
        }
    )


def donation_thanks(request, pk):
    donation = get_object_or_404(
        Donation,
        pk=pk
    )

    return render(
        request,
        "core/donation_thanks.html",
        {
            "donation": donation
        }
    )


# ============================================================
# REGISTER
# ============================================================

def register(request):
    form = RegisterForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()

        login(
            request,
            user
        )

        return redirect("dashboard")

    return render(
        request,
        "registration/register.html",
        {
            "form": form
        }
    )


# ============================================================
# DASHBOARD SECURITY
# ============================================================

def is_superuser(user):
    return user.is_authenticated and user.is_superuser


## ============================================================
# DASHBOARD
# Only superusers can access this page.
# ============================================================

@user_passes_test(is_superuser, login_url="/admin/login/")
def dashboard(request):
    context = {
        "project_count": Project.objects.count(),
        "volunteer_count": VolunteerApplication.objects.count(),
        "donation_total": (
            Donation.objects
            .filter(status="paid")
            .aggregate(total=Sum("amount"))["total"]
            or Decimal("0")
        ),
        "recent_donations": (
            Donation.objects
            .order_by("-created_at")[:5]
        ),
    }
    return render(request, "core/dashboard.html", context)


# ============================================================
# NAYAA REST API
# ============================================================

@api_view(["GET"])
def api_home(request):
    return Response({
        "organization": "Nayaa",
        "tagline": "For Futures Still Unwritten",
        "message": "Welcome to the Nayaa REST API",
        "available_endpoints": [
            "/api/",
            "/api/programs/",
            "/api/donations/",
            "/api/volunteers/",
        ],
    })


# ============================================================
# ABOUT US ADMIN DASHBOARD (PDF 2)
# ============================================================

@user_passes_test(is_superuser, login_url="/login/")
def about_dashboard(request):
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "save_story":
            content = request.POST.get("content", "").strip()
            story_id = request.POST.get("story_id")
            if content:
                if story_id:
                    story = get_object_or_404(OurStory, id=story_id)
                    story.content = content
                    story.save()
                    messages.success(request, "Story updated.")
                else:
                    OurStory.objects.create(content=content)
                    messages.success(request, "Story added.")
            return redirect("about_dashboard")

        elif action == "add_value":
            value = request.POST.get("value", "").strip()
            value_id = request.POST.get("value_id")
            if value:
                if value_id:
                    cv = get_object_or_404(CoreValue, id=value_id)
                    cv.value = value
                    cv.save()
                    messages.success(request, "Core value updated.")
                else:
                    CoreValue.objects.create(value=value)
                    messages.success(request, "Core value added.")
            return redirect("about_dashboard")

        elif action == "add_program":
            name = request.POST.get("name", "").strip()
            description = request.POST.get("description", "").strip()
            program_id = request.POST.get("program_id")
            if name:
                if program_id:
                    p = get_object_or_404(AboutProgram, id=program_id)
                    p.name = name
                    p.description = description
                    p.save()
                    messages.success(request, "Program updated.")
                else:
                    AboutProgram.objects.create(name=name, description=description)
                    messages.success(request, "Program added.")
            return redirect("about_dashboard")

        elif action == "add_team_member":
            name = request.POST.get("name", "").strip()
            role = request.POST.get("role", "").strip()
            image = request.FILES.get("image")
            member_id = request.POST.get("member_id")
            if name and role:
                if member_id:
                    m = get_object_or_404(TeamMember, id=member_id)
                    m.name = name
                    m.role = role
                    if image:
                        m.image = image
                    m.save()
                    messages.success(request, "Team member updated.")
                else:
                    TeamMember.objects.create(name=name, role=role, image=image)
                    messages.success(request, "Team member added.")
            return redirect("about_dashboard")

    context = {
        "our_stories": OurStory.objects.all().order_by("-updated_at"),
        "core_values": CoreValue.objects.all().order_by("id"),
        "about_programs": AboutProgram.objects.all().order_by("id"),
        "team_members": TeamMember.objects.all().order_by("id"),
    }
    return render(request, "core/about_dashboard.html", context)


@user_passes_test(is_superuser, login_url="/login/")
def about_delete_item(request, section, item_id):
    if section == "story":
        get_object_or_404(OurStory, id=item_id).delete()
        messages.success(request, "Story deleted.")
    elif section == "value":
        get_object_or_404(CoreValue, id=item_id).delete()
        messages.success(request, "Core value deleted.")
    elif section == "program":
        get_object_or_404(AboutProgram, id=item_id).delete()
        messages.success(request, "Program deleted.")
    elif section == "member":
        get_object_or_404(TeamMember, id=item_id).delete()
        messages.success(request, "Team member deleted.")
    return redirect("about_dashboard")

    # ============================================================
# PROJECT MANAGEMENT DASHBOARD (From PDF 1)
# ============================================================

@user_passes_test(is_superuser, login_url="/login/")
def projects_dashboard(request):
    edit_project = None
    edit_id = request.GET.get("edit")
    if edit_id:
        edit_project = get_object_or_404(Project, id=edit_id)

    if request.method == "POST":
        project_id = request.POST.get("project_id")
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        status = request.POST.get("status", "Ongoing")
        start_date = request.POST.get("start_date") or None
        end_date = request.POST.get("end_date") or None
        location = request.POST.get("location", "").strip()
        files = request.FILES.getlist("images")

        if title and description:
            if project_id:
                p = get_object_or_404(Project, id=project_id)
                p.title = title
                p.description = description
                p.status = status
                p.start_date = start_date
                p.end_date = end_date
                p.location = location
                p.save()
                messages.success(request, f"Project '{p.title}' updated successfully.")
            else:
                p = Project.objects.create(
                    title=title,
                    description=description,
                    status=status,
                    start_date=start_date,
                    end_date=end_date,
                    location=location,
                    verified=True
                )
                messages.success(request, f"Project '{p.title}' saved successfully.")

            # Save uploaded project images
            for f in files:
                ProjectImage.objects.create(project=p, image=f)

            return redirect("projects_dashboard")

    all_projects = Project.objects.all().order_by("-id")
    return render(
        request,
        "core/projects_dashboard.html",
        {
            "projects": all_projects,
            "edit_project": edit_project,
        }
    )


@user_passes_test(is_superuser, login_url="/login/")
def project_delete(request, project_id):
    p = get_object_or_404(Project, id=project_id)
    title = p.title
    p.delete()
    messages.success(request, f"Project '{title}' deleted successfully.")
    return redirect("projects_dashboard")

    # ============================================================
# MEDIA MANAGEMENT DASHBOARD (PDF 2)
# ============================================================

@user_passes_test(is_superuser, login_url="/login/")
def media_dashboard(request):
    if request.method == "POST":
        action = request.POST.get("action")

        # 1. PRESS RELEASE
        if action == "add_press":
            press_id = request.POST.get("press_id")
            title = request.POST.get("title", "").strip()
            date = request.POST.get("date")
            desc = request.POST.get("description", "").strip()
            if title and desc and date:
                if press_id:
                    p = get_object_or_404(PressReleaseItem, id=press_id)
                    p.title = title
                    p.release_date = date
                    p.description = desc
                    p.save()
                    messages.success(request, "Press release updated.")
                else:
                    PressReleaseItem.objects.create(title=title, release_date=date, description=desc)
                    messages.success(request, "Press release added.")
            return redirect("media_dashboard")

        # 2. MEDIA COVERAGE
        elif action == "add_coverage":
            cov_id = request.POST.get("coverage_id")
            title = request.POST.get("title", "").strip()
            url = request.POST.get("url", "").strip()
            if title and url:
                if cov_id:
                    c = get_object_or_404(MediaCoverage, id=cov_id)
                    c.title = title
                    c.url = url
                    c.save()
                    messages.success(request, "Media coverage updated.")
                else:
                    MediaCoverage.objects.create(title=title, url=url)
                    messages.success(request, "Media coverage added.")
            return redirect("media_dashboard")

        # 3. IMAGE GALLERY
        elif action == "add_image":
            image_file = request.FILES.get("image")
            desc = request.POST.get("description", "").strip()
            if image_file:
                ImageGallery.objects.create(image=image_file, description=desc)
                messages.success(request, "Gallery image added.")
            return redirect("media_dashboard")

        # 4. VIDEOS
        elif action == "add_video":
            video_id = request.POST.get("video_id")
            video_url = request.POST.get("video_url", "").strip()
            desc = request.POST.get("description", "").strip()
            if video_url:
                if video_id:
                    v = get_object_or_404(Video, id=video_id)
                    v.video_url = video_url
                    v.description = desc
                    v.save()
                    messages.success(request, "Video updated.")
                else:
                    Video.objects.create(video_url=video_url, description=desc)
                    messages.success(request, "Video added.")
            return redirect("media_dashboard")

    context = {
        "press_releases": PressReleaseItem.objects.all().order_by("-release_date"),
        "media_coverages": MediaCoverage.objects.all().order_by("-created_at"),
        "gallery_images": ImageGallery.objects.all().order_by("-uploaded_at"),
        "videos": Video.objects.all().order_by("-uploaded_at"),
    }
    return render(request, "core/media_dashboard.html", context)


@user_passes_test(is_superuser, login_url="/login/")
def media_delete_item(request, section, item_id):
    if section == "press":
        get_object_or_404(PressReleaseItem, id=item_id).delete()
        messages.success(request, "Press release deleted.")
    elif section == "coverage":
        get_object_or_404(MediaCoverage, id=item_id).delete()
        messages.success(request, "Media coverage deleted.")
    elif section == "image":
        get_object_or_404(ImageGallery, id=item_id).delete()
        messages.success(request, "Gallery image deleted.")
    elif section == "video":
        get_object_or_404(Video, id=item_id).delete()
        messages.success(request, "Video deleted.")
    return redirect("media_dashboard")